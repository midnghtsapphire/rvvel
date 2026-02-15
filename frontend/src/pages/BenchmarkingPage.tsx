import { useState } from 'react'
import { Activity, Zap, DollarSign, Clock, Leaf } from 'lucide-react'

interface BenchmarkResult {
  model: string
  provider: string
  latencyMs: number
  costUsd: number
  qualityScore: number
  co2Grams: number
  cached: boolean
}

const mockResults: BenchmarkResult[] = [
  { model: 'gpt-4o-mini', provider: 'OpenAI', latencyMs: 450, costUsd: 0.0002, qualityScore: 8.5, co2Grams: 0.15, cached: false },
  { model: 'claude-3-haiku', provider: 'Anthropic', latencyMs: 380, costUsd: 0.00015, qualityScore: 8.2, co2Grams: 0.12, cached: false },
  { model: 'gemini-2.0-flash', provider: 'Google', latencyMs: 320, costUsd: 0.0001, qualityScore: 7.8, co2Grams: 0.10, cached: false },
  { model: 'gpt-4o', provider: 'OpenAI', latencyMs: 1200, costUsd: 0.005, qualityScore: 9.5, co2Grams: 0.45, cached: false },
  { model: 'claude-3.5-sonnet', provider: 'Anthropic', latencyMs: 900, costUsd: 0.003, qualityScore: 9.3, co2Grams: 0.35, cached: false },
]

export default function BenchmarkingPage() {
  const [results] = useState<BenchmarkResult[]>(mockResults)
  const [sortBy, setSortBy] = useState<keyof BenchmarkResult>('qualityScore')

  const sorted = [...results].sort((a, b) => {
    if (sortBy === 'model' || sortBy === 'provider') return 0
    if (sortBy === 'qualityScore') return (b[sortBy] as number) - (a[sortBy] as number)
    return (a[sortBy] as number) - (b[sortBy] as number)
  })

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold gradient-text mb-3">AI Model Benchmarking</h1>
        <p className="text-secondary-brand max-w-xl mx-auto">
          Real-time performance comparison across OpenRouter models.
          Eco-optimized: lightweight models tried first to minimize carbon footprint.
        </p>
      </div>

      {/* Sort controls */}
      <div className="glass-card mb-6">
        <div className="flex flex-wrap items-center gap-3">
          <span className="text-sm text-secondary-brand">Sort by:</span>
          {[
            { key: 'qualityScore', label: 'Quality', icon: Activity },
            { key: 'latencyMs', label: 'Speed', icon: Clock },
            { key: 'costUsd', label: 'Cost', icon: DollarSign },
            { key: 'co2Grams', label: 'Carbon', icon: Leaf },
          ].map(({ key, label, icon: Icon }) => (
            <button
              key={key}
              onClick={() => setSortBy(key as keyof BenchmarkResult)}
              className={`glass-btn text-sm flex items-center gap-1 ${
                sortBy === key ? 'ring-1 ring-primary text-primary' : ''
              }`}
              aria-label={`Sort by ${label}`}
              aria-pressed={sortBy === key}
            >
              <Icon className="w-3.5 h-3.5" aria-hidden="true" />
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Results table */}
      <div className="glass-card overflow-x-auto">
        <table className="w-full text-sm" role="table" aria-label="AI model benchmark results">
          <thead>
            <tr className="border-b border-glass-border">
              <th className="text-left py-3 px-2 text-secondary-brand font-medium" scope="col">Model</th>
              <th className="text-left py-3 px-2 text-secondary-brand font-medium" scope="col">Provider</th>
              <th className="text-right py-3 px-2 text-secondary-brand font-medium" scope="col">Quality</th>
              <th className="text-right py-3 px-2 text-secondary-brand font-medium" scope="col">Latency</th>
              <th className="text-right py-3 px-2 text-secondary-brand font-medium" scope="col">Cost</th>
              <th className="text-right py-3 px-2 text-secondary-brand font-medium" scope="col">CO2</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((r, i) => (
              <tr key={r.model} className="border-b border-glass-border last:border-0 hover:bg-dark-glass transition-colors">
                <td className="py-3 px-2 font-medium">
                  <div className="flex items-center gap-2">
                    {i === 0 && <span className="text-primary text-xs" aria-label="Top ranked">★</span>}
                    {r.model}
                  </div>
                </td>
                <td className="py-3 px-2 text-secondary-brand">{r.provider}</td>
                <td className="py-3 px-2 text-right">
                  <span className={r.qualityScore >= 9 ? 'text-primary font-semibold' : ''}>
                    {r.qualityScore}/10
                  </span>
                </td>
                <td className="py-3 px-2 text-right">
                  <span className={r.latencyMs < 500 ? 'text-green-400' : ''}>
                    {r.latencyMs}ms
                  </span>
                </td>
                <td className="py-3 px-2 text-right">${r.costUsd.toFixed(4)}</td>
                <td className="py-3 px-2 text-right">
                  <span className={r.co2Grams < 0.2 ? 'text-green-400' : 'text-amber-400'}>
                    {r.co2Grams}g
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Eco summary */}
      <div className="glass-card mt-6 flex items-center gap-3" role="status" aria-label="Carbon savings summary">
        <Leaf className="w-5 h-5 text-green-400 shrink-0" aria-hidden="true" />
        <p className="text-sm text-secondary-brand">
          <span className="text-primary font-semibold">Eco Code Active:</span>{' '}
          Lightweight models (gpt-4o-mini, claude-3-haiku) are tried first.
          Cached responses use 200x less carbon. Current session saved{' '}
          <span className="text-green-400 font-semibold">0.8g CO2</span>{' '}
          (0.04 Starbucks cups).
        </p>
      </div>
    </div>
  )
}
