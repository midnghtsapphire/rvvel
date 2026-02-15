import { useState, useEffect } from 'react'
import { Shield, AlertTriangle, DollarSign, Clock, Heart, ExternalLink, Loader2 } from 'lucide-react'

interface Procedure {
  name: string
  description: string
  avg_cost: string
  recovery: string
  duration: string
  risks: string[]
  what_they_dont_tell_you: string
  resources?: string[]
}

export default function ProceduresPage() {
  const [procedures, setProcedures] = useState<Procedure[]>([])
  const [loading, setLoading] = useState(true)
  const [expanded, setExpanded] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/skin/procedures/hidden')
      .then(r => r.json())
      .then(data => { setProcedures(data.procedures || []); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold mb-2">Procedure Education</h1>
        <p className="text-secondary-brand">What they don't tell you about cosmetic procedures</p>
      </div>

      <div className="medical-disclaimer mb-8" role="alert">
        <strong>Medical Disclaimer:</strong> This information is for educational purposes only.
        Always consult a board-certified provider before undergoing any procedure.
      </div>

      {/* Special Section: Mastectomy Survivors */}
      <div className="glass-card mb-8 border-pink-500/30" style={{ borderColor: 'rgba(236,72,153,0.3)' }}>
        <div className="flex items-start gap-4">
          <Heart className="w-8 h-8 text-pink-400 flex-shrink-0 mt-1" aria-hidden="true" />
          <div>
            <h2 className="text-xl font-bold text-pink-400 mb-2">For Mastectomy Survivors</h2>
            <p className="text-secondary-brand mb-3">
              3D areola tattooing can restore natural appearance after breast reconstruction.
              Many artists offer this service free or at reduced cost for survivors.
            </p>
            <div className="flex flex-wrap gap-2">
              <a href="https://personalink.org" target="_blank" rel="noopener noreferrer" className="glass-btn text-sm">
                P.ink (personalink.org) <ExternalLink className="w-3 h-3" aria-hidden="true" />
              </a>
              <a href="https://www.breastcancerrecovery.org" target="_blank" rel="noopener noreferrer" className="glass-btn text-sm">
                Breast Cancer Recovery Foundation <ExternalLink className="w-3 h-3" aria-hidden="true" />
              </a>
            </div>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-16">
          <Loader2 className="w-12 h-12 animate-spin text-primary-brand mx-auto" aria-hidden="true" />
        </div>
      ) : (
        <div className="space-y-4">
          {procedures.map(proc => (
            <div key={proc.name} className="glass-card">
              <button
                onClick={() => setExpanded(expanded === proc.name ? null : proc.name)}
                className="w-full text-left"
                aria-expanded={expanded === proc.name}
              >
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">{proc.name}</h3>
                  <span className="text-2xl text-secondary-brand" aria-hidden="true">
                    {expanded === proc.name ? '−' : '+'}
                  </span>
                </div>
                <p className="text-secondary-brand text-sm mt-1">{proc.description}</p>
              </button>

              {expanded === proc.name && (
                <div className="mt-4 pt-4 border-t border-glass space-y-4" role="region" aria-label={`Details for ${proc.name}`}>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div className="flex items-center gap-2">
                      <DollarSign className="w-5 h-5 text-green-400" aria-hidden="true" />
                      <div>
                        <p className="text-xs text-secondary-brand">Average Cost</p>
                        <p className="font-medium">{proc.avg_cost}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock className="w-5 h-5 text-blue-400" aria-hidden="true" />
                      <div>
                        <p className="text-xs text-secondary-brand">Recovery</p>
                        <p className="font-medium">{proc.recovery}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Shield className="w-5 h-5 text-purple-400" aria-hidden="true" />
                      <div>
                        <p className="text-xs text-secondary-brand">Duration</p>
                        <p className="font-medium">{proc.duration}</p>
                      </div>
                    </div>
                  </div>

                  {/* Risks */}
                  <div>
                    <h4 className="font-medium flex items-center gap-2 mb-2">
                      <AlertTriangle className="w-4 h-4 text-red-400" aria-hidden="true" />
                      Risks
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {proc.risks.map(r => (
                        <span key={r} className="px-2 py-1 rounded bg-red-500/10 text-red-400 text-xs">{r}</span>
                      ))}
                    </div>
                  </div>

                  {/* What They Don't Tell You */}
                  <div className="bg-amber-500/10 border border-amber-500/20 rounded-xl p-4">
                    <h4 className="font-medium text-amber-400 mb-2">What They Don't Tell You</h4>
                    <p className="text-sm text-secondary-brand">{proc.what_they_dont_tell_you}</p>
                  </div>

                  {/* Resources */}
                  {proc.resources && proc.resources.length > 0 && (
                    <div>
                      <h4 className="font-medium mb-2">Resources</h4>
                      <ul className="space-y-1">
                        {proc.resources.map(r => (
                          <li key={r} className="text-sm text-secondary-brand">• {r}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
