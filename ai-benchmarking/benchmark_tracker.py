"""
AI Model Benchmarking Tracker
=============================
Core module for tracking AI model performance metrics across multi-model team workflows.
Tracks response time, tokens, cost, success/failure/timeout, and quality scores.

Author: Audrey Evans
"""

import json
import time
import os
import hashlib
import statistics
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any, Literal
from dataclasses import dataclass, field, asdict
from pathlib import Path
from openai import OpenAI

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODEL_COST_TABLE: Dict[str, Dict[str, float]] = {
    # cost per 1K tokens (input / output)
    "deepseek/deepseek-chat": {"input": 0.00014, "output": 0.00028},
    "moonshotai/kimi-k2": {"input": 0.0006, "output": 0.0024},
    "openai/gpt-4.1-mini": {"input": 0.0004, "output": 0.0016},
    "openai/gpt-4.1-nano": {"input": 0.0001, "output": 0.0004},
    "google/gemini-2.5-flash": {"input": 0.00015, "output": 0.0006},
    "anthropic/claude-sonnet-4": {"input": 0.003, "output": 0.015},
    "anthropic/claude-3.5-sonnet": {"input": 0.003, "output": 0.015},
    "meta-llama/llama-4-maverick": {"input": 0.0002, "output": 0.0008},
}

DEFAULT_TIMEOUT_MS = 120_000  # 2 minutes
DATA_DIR = Path(__file__).parent / "data"
BENCHMARK_LOG = DATA_DIR / "benchmark_log.jsonl"
HISTORY_DIR = DATA_DIR / "history"


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class ModelCallRecord:
    """Single model invocation record."""
    call_id: str
    run_id: str
    model: str
    task_type: str
    timestamp: str
    response_time_ms: float
    tokens_in: int
    tokens_out: int
    cost_usd: float
    status: Literal["success", "failure", "timeout"]
    error_message: Optional[str] = None
    quality_score: Optional[float] = None  # 0.0 - 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "ModelCallRecord":
        return cls(**d)


@dataclass
class RunSummary:
    """Aggregate summary for a single processing run."""
    run_id: str
    started_at: str
    ended_at: str
    total_calls: int
    successful: int
    failed: int
    timed_out: int
    total_cost_usd: float
    total_tokens_in: int
    total_tokens_out: int
    avg_response_time_ms: float
    model_summaries: Dict[str, Dict[str, Any]] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Benchmark Tracker
# ---------------------------------------------------------------------------

class BenchmarkTracker:
    """
    Tracks and records every AI model call with full telemetry.
    Provides aggregation, historical comparison, and recommendations.
    """

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir) if data_dir else DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        (self.data_dir / "history").mkdir(exist_ok=True)
        self.log_path = self.data_dir / "benchmark_log.jsonl"
        self._current_run_id: Optional[str] = None
        self._current_records: List[ModelCallRecord] = []
        self._cost_table = MODEL_COST_TABLE.copy()

    # ---- Run lifecycle ----

    def start_run(self, run_id: Optional[str] = None) -> str:
        """Begin a new benchmarking run."""
        self._current_run_id = run_id or f"run_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"
        self._current_records = []
        return self._current_run_id

    def end_run(self) -> RunSummary:
        """Finalize current run, persist records, return summary."""
        if not self._current_run_id:
            raise RuntimeError("No active run. Call start_run() first.")

        summary = self._build_summary()

        # Persist individual records
        with open(self.log_path, "a") as f:
            for rec in self._current_records:
                f.write(json.dumps(rec.to_dict()) + "\n")

        # Persist run summary
        summary_path = self.data_dir / "history" / f"{self._current_run_id}.json"
        with open(summary_path, "w") as f:
            json.dump(asdict(summary), f, indent=2)

        run_id = self._current_run_id
        self._current_run_id = None
        self._current_records = []
        return summary

    # ---- Recording ----

    def record_call(
        self,
        model: str,
        task_type: str,
        response_time_ms: float,
        tokens_in: int,
        tokens_out: int,
        status: Literal["success", "failure", "timeout"],
        error_message: Optional[str] = None,
        quality_score: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ModelCallRecord:
        """Record a single model call."""
        if not self._current_run_id:
            raise RuntimeError("No active run. Call start_run() first.")

        cost = self._calculate_cost(model, tokens_in, tokens_out)
        call_id = hashlib.sha256(
            f"{self._current_run_id}:{model}:{time.time_ns()}".encode()
        ).hexdigest()[:16]

        record = ModelCallRecord(
            call_id=call_id,
            run_id=self._current_run_id,
            model=model,
            task_type=task_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            response_time_ms=response_time_ms,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost_usd=cost,
            status=status,
            error_message=error_message,
            quality_score=quality_score,
            metadata=metadata or {},
        )
        self._current_records.append(record)
        return record

    def tracked_call(
        self,
        client: OpenAI,
        model: str,
        messages: List[Dict[str, str]],
        task_type: str = "general",
        timeout_ms: int = DEFAULT_TIMEOUT_MS,
        quality_scorer: Optional[callable] = None,
        **kwargs,
    ) -> tuple:
        """
        Execute an OpenRouter API call with full benchmarking instrumentation.
        Returns (response_content, record).
        """
        start = time.perf_counter_ns()
        status = "success"
        error_msg = None
        tokens_in = 0
        tokens_out = 0
        content = ""

        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                timeout=timeout_ms / 1000,
                **kwargs,
            )
            elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000

            if response.usage:
                tokens_in = response.usage.prompt_tokens or 0
                tokens_out = response.usage.completion_tokens or 0

            content = response.choices[0].message.content if response.choices else ""

        except Exception as e:
            elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
            error_msg = str(e)
            if elapsed_ms >= timeout_ms:
                status = "timeout"
            else:
                status = "failure"

        quality = None
        if quality_scorer and status == "success":
            try:
                quality = quality_scorer(content)
            except Exception:
                quality = None

        record = self.record_call(
            model=model,
            task_type=task_type,
            response_time_ms=round(elapsed_ms, 2),
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            status=status,
            error_message=error_msg,
            quality_score=quality,
        )
        return content, record

    # ---- Cost calculation ----

    def _calculate_cost(self, model: str, tokens_in: int, tokens_out: int) -> float:
        rates = self._cost_table.get(model, {"input": 0.001, "output": 0.002})
        cost = (tokens_in / 1000) * rates["input"] + (tokens_out / 1000) * rates["output"]
        return round(cost, 8)

    def update_cost_table(self, model: str, input_cost: float, output_cost: float):
        """Update or add model pricing."""
        self._cost_table[model] = {"input": input_cost, "output": output_cost}

    # ---- Aggregation ----

    def _build_summary(self) -> RunSummary:
        records = self._current_records
        if not records:
            return RunSummary(
                run_id=self._current_run_id,
                started_at="",
                ended_at="",
                total_calls=0,
                successful=0,
                failed=0,
                timed_out=0,
                total_cost_usd=0.0,
                total_tokens_in=0,
                total_tokens_out=0,
                avg_response_time_ms=0.0,
            )

        timestamps = [r.timestamp for r in records]
        response_times = [r.response_time_ms for r in records]

        # Per-model aggregation
        model_groups: Dict[str, List[ModelCallRecord]] = {}
        for r in records:
            model_groups.setdefault(r.model, []).append(r)

        model_summaries = {}
        for model, recs in model_groups.items():
            times = [r.response_time_ms for r in recs]
            costs = [r.cost_usd for r in recs]
            qualities = [r.quality_score for r in recs if r.quality_score is not None]
            sorted_times = sorted(times)

            model_summaries[model] = {
                "total_calls": len(recs),
                "successful": sum(1 for r in recs if r.status == "success"),
                "failed": sum(1 for r in recs if r.status == "failure"),
                "timed_out": sum(1 for r in recs if r.status == "timeout"),
                "total_cost_usd": round(sum(costs), 8),
                "total_tokens_in": sum(r.tokens_in for r in recs),
                "total_tokens_out": sum(r.tokens_out for r in recs),
                "avg_response_time_ms": round(statistics.mean(times), 2),
                "p50_response_time_ms": round(self._percentile(sorted_times, 50), 2),
                "p95_response_time_ms": round(self._percentile(sorted_times, 95), 2),
                "p99_response_time_ms": round(self._percentile(sorted_times, 99), 2),
                "error_rate": round(
                    sum(1 for r in recs if r.status != "success") / len(recs), 4
                ),
                "avg_quality_score": round(statistics.mean(qualities), 4) if qualities else None,
                "task_types": list(set(r.task_type for r in recs)),
            }

        return RunSummary(
            run_id=self._current_run_id,
            started_at=min(timestamps),
            ended_at=max(timestamps),
            total_calls=len(records),
            successful=sum(1 for r in records if r.status == "success"),
            failed=sum(1 for r in records if r.status == "failure"),
            timed_out=sum(1 for r in records if r.status == "timeout"),
            total_cost_usd=round(sum(r.cost_usd for r in records), 8),
            total_tokens_in=sum(r.tokens_in for r in records),
            total_tokens_out=sum(r.tokens_out for r in records),
            avg_response_time_ms=round(statistics.mean(response_times), 2),
            model_summaries=model_summaries,
        )

    @staticmethod
    def _percentile(sorted_data: List[float], p: float) -> float:
        if not sorted_data:
            return 0.0
        k = (len(sorted_data) - 1) * (p / 100)
        f = int(k)
        c = f + 1
        if c >= len(sorted_data):
            return sorted_data[-1]
        return sorted_data[f] + (k - f) * (sorted_data[c] - sorted_data[f])

    # ---- Historical analysis ----

    def load_history(self) -> List[RunSummary]:
        """Load all historical run summaries."""
        history_dir = self.data_dir / "history"
        summaries = []
        for path in sorted(history_dir.glob("*.json")):
            with open(path) as f:
                data = json.load(f)
                summaries.append(RunSummary(**data))
        return summaries

    def load_all_records(self) -> List[ModelCallRecord]:
        """Load all individual call records from the log."""
        records = []
        if self.log_path.exists():
            with open(self.log_path) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        records.append(ModelCallRecord.from_dict(json.loads(line)))
        return records

    def get_model_comparison(self, task_type: Optional[str] = None) -> Dict[str, Dict]:
        """Compare models across all historical data, optionally filtered by task type."""
        records = self.load_all_records()
        if task_type:
            records = [r for r in records if r.task_type == task_type]

        model_groups: Dict[str, List[ModelCallRecord]] = {}
        for r in records:
            model_groups.setdefault(r.model, []).append(r)

        comparison = {}
        for model, recs in model_groups.items():
            times = sorted([r.response_time_ms for r in recs])
            qualities = [r.quality_score for r in recs if r.quality_score is not None]
            comparison[model] = {
                "total_calls": len(recs),
                "success_rate": round(sum(1 for r in recs if r.status == "success") / len(recs), 4),
                "avg_response_ms": round(statistics.mean(times), 2),
                "p50_ms": round(BenchmarkTracker._percentile(times, 50), 2),
                "p95_ms": round(BenchmarkTracker._percentile(times, 95), 2),
                "p99_ms": round(BenchmarkTracker._percentile(times, 99), 2),
                "total_cost_usd": round(sum(r.cost_usd for r in recs), 6),
                "avg_cost_per_call": round(sum(r.cost_usd for r in recs) / len(recs), 8),
                "avg_quality": round(statistics.mean(qualities), 4) if qualities else None,
            }
        return comparison

    def generate_recommendations(self, task_type: Optional[str] = None) -> List[str]:
        """Generate actionable recommendations based on historical data."""
        comparison = self.get_model_comparison(task_type)
        if len(comparison) < 2:
            return ["Not enough model data to generate recommendations."]

        recommendations = []
        models = list(comparison.items())

        # Find fastest and slowest
        fastest = min(models, key=lambda x: x[1]["avg_response_ms"])
        slowest = max(models, key=lambda x: x[1]["avg_response_ms"])
        if slowest[1]["avg_response_ms"] > fastest[1]["avg_response_ms"] * 2:
            speedup = round(slowest[1]["avg_response_ms"] / fastest[1]["avg_response_ms"], 1)
            recommendations.append(
                f"Switch from {slowest[0]} to {fastest[0]} for {task_type or 'general'} tasks "
                f"— {speedup}x faster"
            )

        # Find cheapest
        cheapest = min(models, key=lambda x: x[1]["avg_cost_per_call"])
        most_expensive = max(models, key=lambda x: x[1]["avg_cost_per_call"])
        if most_expensive[1]["avg_cost_per_call"] > cheapest[1]["avg_cost_per_call"] * 2:
            savings = round(
                (most_expensive[1]["avg_cost_per_call"] - cheapest[1]["avg_cost_per_call"])
                / most_expensive[1]["avg_cost_per_call"] * 100, 1
            )
            recommendations.append(
                f"Switch from {most_expensive[0]} to {cheapest[0]} — "
                f"saves {savings}% cost per call"
            )

        # Quality-based recommendations
        quality_models = [(m, d) for m, d in models if d["avg_quality"] is not None]
        if len(quality_models) >= 2:
            best_quality = max(quality_models, key=lambda x: x[1]["avg_quality"])
            worst_quality = min(quality_models, key=lambda x: x[1]["avg_quality"])
            if best_quality[1]["avg_quality"] > worst_quality[1]["avg_quality"] * 1.1:
                recommendations.append(
                    f"For quality-critical tasks, prefer {best_quality[0]} "
                    f"(quality score: {best_quality[1]['avg_quality']}) over "
                    f"{worst_quality[0]} (quality score: {worst_quality[1]['avg_quality']})"
                )

        # Error rate warnings
        for model, data in models:
            if data["success_rate"] < 0.95:
                recommendations.append(
                    f"WARNING: {model} has a {round((1 - data['success_rate']) * 100, 1)}% error rate. "
                    f"Consider adding fallback routing."
                )

        # Best value (quality / cost)
        value_models = [(m, d) for m, d in models if d["avg_quality"] is not None and d["avg_cost_per_call"] > 0]
        if len(value_models) >= 2:
            best_value = max(value_models, key=lambda x: x[1]["avg_quality"] / x[1]["avg_cost_per_call"])
            recommendations.append(
                f"Best value model: {best_value[0]} — highest quality-to-cost ratio"
            )

        return recommendations if recommendations else ["All models performing within acceptable ranges."]


# ---------------------------------------------------------------------------
# Convenience: create a pre-configured OpenRouter client
# ---------------------------------------------------------------------------

def create_openrouter_client() -> OpenAI:
    """Create an OpenAI client configured for OpenRouter."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set")
    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("AI Benchmarking Tracker — Demo Run")
    print("=" * 50)

    client = create_openrouter_client()
    tracker = BenchmarkTracker()

    run_id = tracker.start_run()
    print(f"Started run: {run_id}")

    # Demo: call deepseek/deepseek-chat
    content, record = tracker.tracked_call(
        client=client,
        model="deepseek/deepseek-chat",
        messages=[{"role": "user", "content": "Say hello in exactly 5 words."}],
        task_type="greeting",
    )
    print(f"\n[{record.model}] Status: {record.status}")
    print(f"  Response: {content[:100]}")
    print(f"  Time: {record.response_time_ms}ms | Tokens: {record.tokens_in}/{record.tokens_out}")
    print(f"  Cost: ${record.cost_usd}")

    summary = tracker.end_run()
    print(f"\nRun Summary:")
    print(f"  Total calls: {summary.total_calls}")
    print(f"  Successful: {summary.successful}")
    print(f"  Total cost: ${summary.total_cost_usd}")
    print(f"  Avg response: {summary.avg_response_time_ms}ms")
