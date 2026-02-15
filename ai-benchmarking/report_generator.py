"""
AI Benchmarking Report Generator
=================================
Generates markdown and JSON reports from benchmarking data.
Provides dashboard-ready visualizations and actionable recommendations.

Author: Audrey Evans
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from benchmark_tracker import BenchmarkTracker, RunSummary, ModelCallRecord
from thought_chain_cache import ThoughtChainCache

# ---------------------------------------------------------------------------
# Report Generator
# ---------------------------------------------------------------------------

class ReportGenerator:
    """Generate comprehensive benchmarking reports in multiple formats."""

    def __init__(self, tracker: BenchmarkTracker, cache: Optional[ThoughtChainCache] = None):
        self.tracker = tracker
        self.cache = cache or ThoughtChainCache()

    # ---- Markdown Reports ----

    def generate_run_report(self, summary: RunSummary, output_path: str):
        """Generate a markdown report for a single run."""
        lines = []
        lines.append(f"# AI Benchmarking Report: {summary.run_id}")
        lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        lines.append(f"\n**Run Period:** {summary.started_at} to {summary.ended_at}")
        lines.append(f"\n---\n")

        # Executive Summary
        lines.append("## Executive Summary\n")
        lines.append(f"- **Total API Calls:** {summary.total_calls}")
        lines.append(f"- **Successful:** {summary.successful} ({round(summary.successful/summary.total_calls*100, 1)}%)")
        lines.append(f"- **Failed:** {summary.failed}")
        lines.append(f"- **Timed Out:** {summary.timed_out}")
        lines.append(f"- **Total Cost:** ${summary.total_cost_usd:.6f}")
        lines.append(f"- **Total Tokens:** {summary.total_tokens_in:,} in / {summary.total_tokens_out:,} out")
        lines.append(f"- **Average Response Time:** {summary.avg_response_time_ms:.2f}ms")
        lines.append("\n---\n")

        # Per-Model Performance
        lines.append("## Model Performance Breakdown\n")
        
        for model, data in sorted(summary.model_summaries.items(), key=lambda x: x[1]['avg_response_time_ms']):
            lines.append(f"### {model}\n")
            lines.append(f"- **Calls:** {data['total_calls']}")
            lines.append(f"- **Success Rate:** {round((data['successful']/data['total_calls'])*100, 1)}%")
            lines.append(f"- **Cost:** ${data['total_cost_usd']:.6f}")
            lines.append(f"- **Tokens:** {data['total_tokens_in']:,} in / {data['total_tokens_out']:,} out")
            lines.append(f"- **Avg Response Time:** {data['avg_response_time_ms']:.2f}ms")
            lines.append(f"- **Latency Percentiles:**")
            lines.append(f"  - p50: {data['p50_response_time_ms']:.2f}ms")
            lines.append(f"  - p95: {data['p95_response_time_ms']:.2f}ms")
            lines.append(f"  - p99: {data['p99_response_time_ms']:.2f}ms")
            lines.append(f"- **Error Rate:** {round(data['error_rate']*100, 2)}%")
            
            if data['avg_quality_score'] is not None:
                lines.append(f"- **Avg Quality Score:** {data['avg_quality_score']:.4f}")
            
            lines.append(f"- **Task Types:** {', '.join(data['task_types'])}")
            lines.append("")

        lines.append("\n---\n")

        # Comparison Table
        lines.append("## Model Comparison Table\n")
        lines.append("| Model | Calls | Success % | Avg Time (ms) | p95 (ms) | Cost ($) | Error % |")
        lines.append("|-------|-------|-----------|---------------|----------|----------|---------|")
        
        for model, data in sorted(summary.model_summaries.items(), key=lambda x: x[1]['avg_response_time_ms']):
            success_pct = round((data['successful']/data['total_calls'])*100, 1)
            error_pct = round(data['error_rate']*100, 2)
            lines.append(
                f"| {model} | {data['total_calls']} | {success_pct}% | "
                f"{data['avg_response_time_ms']:.2f} | {data['p95_response_time_ms']:.2f} | "
                f"${data['total_cost_usd']:.6f} | {error_pct}% |"
            )
        
        lines.append("\n---\n")

        # Recommendations
        lines.append("## Recommendations\n")
        recommendations = self.tracker.generate_recommendations()
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"{i}. {rec}")
        
        lines.append("\n---\n")

        # Thought-Chain Cache Stats
        cache_stats = self.cache.get_stats()
        lines.append("## Thought-Chain Cache Status\n")
        lines.append(f"- **Total Chains:** {cache_stats['total_chains']}")
        lines.append(f"- **Golden Chains:** {cache_stats['golden_chains']}")
        lines.append(f"- **Validated Chains:** {cache_stats['validated_chains']}")
        lines.append(f"- **Total Reuses:** {cache_stats['total_reuses']}")
        lines.append(f"- **Avg Success Rate:** {cache_stats['avg_success_rate']:.2%}")
        
        if cache_stats['task_types']:
            lines.append(f"\n**Chains by Task Type:**")
            for task_type, count in cache_stats['task_types'].items():
                lines.append(f"- {task_type}: {count}")

        # Write to file
        with open(output_path, "w") as f:
            f.write("\n".join(lines))

    def generate_historical_report(self, output_path: str, task_type: Optional[str] = None):
        """Generate a historical comparison report across all runs."""
        history = self.tracker.load_history()
        
        if not history:
            with open(output_path, "w") as f:
                f.write("# Historical Benchmarking Report\n\nNo historical data available.\n")
            return

        lines = []
        lines.append("# Historical Benchmarking Report")
        lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        if task_type:
            lines.append(f"\n**Filtered by Task Type:** {task_type}")
        
        lines.append(f"\n**Total Runs:** {len(history)}")
        lines.append("\n---\n")

        # Aggregate stats
        total_calls = sum(r.total_calls for r in history)
        total_cost = sum(r.total_cost_usd for r in history)
        total_tokens_in = sum(r.total_tokens_in for r in history)
        total_tokens_out = sum(r.total_tokens_out for r in history)

        lines.append("## Aggregate Statistics\n")
        lines.append(f"- **Total API Calls:** {total_calls:,}")
        lines.append(f"- **Total Cost:** ${total_cost:.6f}")
        lines.append(f"- **Total Tokens:** {total_tokens_in:,} in / {total_tokens_out:,} out")
        lines.append("\n---\n")

        # Model comparison
        comparison = self.tracker.get_model_comparison(task_type)
        
        lines.append("## Historical Model Comparison\n")
        lines.append("| Model | Total Calls | Success % | Avg Time (ms) | p95 (ms) | Total Cost ($) | Avg Cost/Call ($) | Avg Quality |")
        lines.append("|-------|-------------|-----------|---------------|----------|----------------|-------------------|-------------|")
        
        for model, data in sorted(comparison.items(), key=lambda x: x[1]['avg_response_ms']):
            quality_str = f"{data['avg_quality']:.4f}" if data['avg_quality'] is not None else "N/A"
            lines.append(
                f"| {model} | {data['total_calls']} | {data['success_rate']*100:.1f}% | "
                f"{data['avg_response_ms']:.2f} | {data['p95_ms']:.2f} | "
                f"${data['total_cost_usd']:.6f} | ${data['avg_cost_per_call']:.8f} | {quality_str} |"
            )
        
        lines.append("\n---\n")

        # Recommendations
        lines.append("## Historical Recommendations\n")
        recommendations = self.tracker.generate_recommendations(task_type)
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"{i}. {rec}")
        
        lines.append("\n---\n")

        # Run history table
        lines.append("## Run History\n")
        lines.append("| Run ID | Started | Calls | Success % | Cost ($) | Avg Time (ms) |")
        lines.append("|--------|---------|-------|-----------|----------|---------------|")
        
        for run in sorted(history, key=lambda r: r.started_at, reverse=True):
            success_pct = round((run.successful/run.total_calls)*100, 1) if run.total_calls > 0 else 0
            lines.append(
                f"| {run.run_id} | {run.started_at[:19]} | {run.total_calls} | "
                f"{success_pct}% | ${run.total_cost_usd:.6f} | {run.avg_response_time_ms:.2f} |"
            )

        # Write to file
        with open(output_path, "w") as f:
            f.write("\n".join(lines))

    # ---- JSON Reports (Dashboard-Ready) ----

    def generate_json_report(self, summary: RunSummary, output_path: str):
        """Generate a JSON report for dashboard consumption."""
        report = {
            "run_id": summary.run_id,
            "generated_at": datetime.now().isoformat(),
            "run_period": {
                "started_at": summary.started_at,
                "ended_at": summary.ended_at,
            },
            "summary": {
                "total_calls": summary.total_calls,
                "successful": summary.successful,
                "failed": summary.failed,
                "timed_out": summary.timed_out,
                "success_rate": round(summary.successful / summary.total_calls, 4) if summary.total_calls > 0 else 0,
                "total_cost_usd": summary.total_cost_usd,
                "total_tokens_in": summary.total_tokens_in,
                "total_tokens_out": summary.total_tokens_out,
                "avg_response_time_ms": summary.avg_response_time_ms,
            },
            "models": summary.model_summaries,
            "recommendations": self.tracker.generate_recommendations(),
            "thought_chain_cache": self.cache.get_stats(),
        }

        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)

    def generate_historical_json(self, output_path: str, task_type: Optional[str] = None):
        """Generate historical JSON report for dashboard."""
        history = self.tracker.load_history()
        comparison = self.tracker.get_model_comparison(task_type)
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "task_type_filter": task_type,
            "total_runs": len(history),
            "aggregate": {
                "total_calls": sum(r.total_calls for r in history),
                "total_cost_usd": round(sum(r.total_cost_usd for r in history), 6),
                "total_tokens_in": sum(r.total_tokens_in for r in history),
                "total_tokens_out": sum(r.total_tokens_out for r in history),
            },
            "model_comparison": comparison,
            "recommendations": self.tracker.generate_recommendations(task_type),
            "runs": [
                {
                    "run_id": r.run_id,
                    "started_at": r.started_at,
                    "ended_at": r.ended_at,
                    "total_calls": r.total_calls,
                    "successful": r.successful,
                    "total_cost_usd": r.total_cost_usd,
                    "avg_response_time_ms": r.avg_response_time_ms,
                }
                for r in sorted(history, key=lambda x: x.started_at, reverse=True)
            ],
        }

        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)

    # ---- Thought-Chain Reports ----

    def generate_chain_report(self, output_path: str):
        """Generate a report on thought-chain cache performance."""
        stats = self.cache.get_stats()
        chains = self.cache.list_chains()

        lines = []
        lines.append("# Thought-Chain Cache Report")
        lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        lines.append("\n---\n")

        lines.append("## Cache Statistics\n")
        lines.append(f"- **Total Chains:** {stats['total_chains']}")
        lines.append(f"- **Golden Chains:** {stats['golden_chains']}")
        lines.append(f"- **Validated Chains:** {stats['validated_chains']}")
        lines.append(f"- **Experimental Chains:** {stats['experimental_chains']}")
        lines.append(f"- **Total Reuses:** {stats['total_reuses']}")
        lines.append(f"- **Average Success Rate:** {stats['avg_success_rate']:.2%}")
        lines.append("\n---\n")

        lines.append("## Chains by Task Type\n")
        for task_type, count in stats['task_types'].items():
            lines.append(f"- **{task_type}:** {count} chains")
        lines.append("\n---\n")

        lines.append("## Chains by Domain\n")
        for domain, count in stats['domains'].items():
            lines.append(f"- **{domain}:** {count} chains")
        lines.append("\n---\n")

        # Golden chains detail
        golden_chains = [c for c in chains if c.status == "golden"]
        if golden_chains:
            lines.append("## Golden Chains (Always Reuse)\n")
            for chain in golden_chains:
                lines.append(f"### {chain.chain_id}")
                lines.append(f"- **Task Type:** {chain.task_type}")
                lines.append(f"- **Domain:** {chain.domain}")
                lines.append(f"- **Complexity:** {chain.complexity}")
                lines.append(f"- **Keywords:** {', '.join(chain.keywords)}")
                lines.append(f"- **Reuse Count:** {chain.reuse_count}")
                lines.append(f"- **Success Rate:** {chain.success_rate:.2%}")
                lines.append(f"- **Captured:** {chain.captured_at[:19]}")
                lines.append("")

        # Most reused chains
        most_reused = sorted(chains, key=lambda c: c.reuse_count, reverse=True)[:10]
        if most_reused:
            lines.append("\n---\n")
            lines.append("## Top 10 Most Reused Chains\n")
            lines.append("| Chain ID | Task Type | Domain | Reuses | Success Rate | Status |")
            lines.append("|----------|-----------|--------|--------|--------------|--------|")
            for chain in most_reused:
                lines.append(
                    f"| {chain.chain_id} | {chain.task_type} | {chain.domain} | "
                    f"{chain.reuse_count} | {chain.success_rate:.2%} | {chain.status} |"
                )

        with open(output_path, "w") as f:
            f.write("\n".join(lines))


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("AI Benchmarking Report Generator — Demo")
    print("=" * 50)

    tracker = BenchmarkTracker()
    cache = ThoughtChainCache()
    generator = ReportGenerator(tracker, cache)

    # Check if there's any historical data
    history = tracker.load_history()
    
    if history:
        print(f"Found {len(history)} historical runs")
        
        # Generate historical report
        generator.generate_historical_report("historical_report.md")
        print("Generated: historical_report.md")
        
        generator.generate_historical_json("historical_report.json")
        print("Generated: historical_report.json")
        
        # Generate chain report
        generator.generate_chain_report("thought_chain_report.md")
        print("Generated: thought_chain_report.md")
    else:
        print("No historical data found. Run benchmark_tracker.py first to generate data.")
