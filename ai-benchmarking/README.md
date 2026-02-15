# AI Model Benchmarking & Thought-Chain Reuse System

**Author:** Audrey Evans

This project provides a robust system for benchmarking the performance of various AI models and a caching engine to reuse thought-chain reasoning, optimizing for cost, speed, and quality.

### Features
- **Benchmark Tracker:** Logs model name, latency, token usage, cost, and success/failure for every API call.
- **Report Generator:** Creates Markdown and JSON reports detailing model performance, latency percentiles, and cost analysis.
- **Kimi Thought-Chain Cache:** Captures and stores the reasoning process from the `moonshotai/kimi-k2` model, allowing for the reuse of thought-chains on similar tasks to save tokens and time.

### Usage
1.  Wrap your AI model calls with the `BenchmarkTracker`.
2.  Before calling Kimi, check the `ThoughtChainCache` for existing reasoning.
3.  After a processing run, call the `ReportGenerator` to get performance insights.
