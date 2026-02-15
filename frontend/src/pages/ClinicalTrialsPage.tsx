import { useState } from 'react'
import { Search, MapPin, ExternalLink, Loader2, FlaskConical } from 'lucide-react'

interface Trial {
  nct_id: string
  title: string
  status: string
  phase: string
  conditions: string[]
  locations: string[]
  start_date: string
  url: string
}

export default function ClinicalTrialsPage() {
  const [condition, setCondition] = useState('')
  const [location, setLocation] = useState('')
  const [loading, setLoading] = useState(false)
  const [trials, setTrials] = useState<Trial[]>([])
  const [searched, setSearched] = useState(false)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setSearched(true)
    try {
      const params = new URLSearchParams({ condition: condition || 'dermatology', location, max_results: '20' })
      const resp = await fetch(`/api/skin/clinical-trials?${params}`)
      const data = await resp.json()
      setTrials(data.trials || [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const loadSkinTrials = async () => {
    setLoading(true)
    setSearched(true)
    try {
      const params = new URLSearchParams({ location })
      const resp = await fetch(`/api/skin/clinical-trials/skin?${params}`)
      const data = await resp.json()
      setTrials(data.trials || [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold mb-2">Clinical Trials Finder</h1>
        <p className="text-secondary-brand">Search ClinicalTrials.gov for dermatology trials near you</p>
      </div>

      <div className="medical-disclaimer mb-8" role="alert">
        <strong>Medical Disclaimer:</strong> Clinical trial information is sourced from ClinicalTrials.gov.
        Always consult your physician before enrolling in any clinical trial.
      </div>

      {/* Search Form */}
      <div className="glass-card mb-8">
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="condition" className="block text-sm font-medium mb-1">Condition</label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-secondary-brand" aria-hidden="true" />
                <input
                  id="condition"
                  type="text"
                  value={condition}
                  onChange={e => setCondition(e.target.value)}
                  className="glass-input pl-10"
                  placeholder="e.g., acne, eczema, psoriasis"
                />
              </div>
            </div>
            <div>
              <label htmlFor="location" className="block text-sm font-medium mb-1">Location</label>
              <div className="relative">
                <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-secondary-brand" aria-hidden="true" />
                <input
                  id="location"
                  type="text"
                  value={location}
                  onChange={e => setLocation(e.target.value)}
                  className="glass-input pl-10"
                  placeholder="e.g., Denver, Colorado"
                />
              </div>
            </div>
          </div>
          <div className="flex gap-3">
            <button type="submit" disabled={loading} className="glass-btn-primary flex-1">
              {loading ? <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" /> : <Search className="w-4 h-4" aria-hidden="true" />}
              Search Trials
            </button>
            <button type="button" onClick={loadSkinTrials} disabled={loading} className="glass-btn flex-1">
              <FlaskConical className="w-4 h-4" aria-hidden="true" />
              All Skin Trials
            </button>
          </div>
        </form>
      </div>

      {/* Results */}
      {loading ? (
        <div className="text-center py-16">
          <Loader2 className="w-12 h-12 animate-spin text-primary-brand mx-auto mb-4" aria-hidden="true" />
          <p className="text-secondary-brand">Searching ClinicalTrials.gov...</p>
        </div>
      ) : searched && trials.length === 0 ? (
        <div className="glass-card text-center py-16">
          <FlaskConical className="w-12 h-12 text-secondary-brand mx-auto mb-4" aria-hidden="true" />
          <h3 className="text-lg font-semibold mb-2">No trials found</h3>
          <p className="text-secondary-brand">Try broadening your search criteria.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {trials.map(trial => (
            <div key={trial.nct_id} className="glass-card">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                      trial.status === 'Recruiting' ? 'bg-green-500/20 text-green-400' :
                      trial.status === 'Active' ? 'bg-blue-500/20 text-blue-400' :
                      'bg-gray-500/20 text-gray-400'
                    }`}>
                      {trial.status}
                    </span>
                    {trial.phase && <span className="text-xs text-secondary-brand">{trial.phase}</span>}
                    <span className="text-xs text-secondary-brand">{trial.nct_id}</span>
                  </div>
                  <h3 className="font-semibold mb-2">{trial.title}</h3>
                  {trial.conditions?.length > 0 && (
                    <div className="flex flex-wrap gap-1 mb-2">
                      {trial.conditions.map(c => (
                        <span key={c} className="px-2 py-0.5 rounded bg-primary/10 text-primary-brand text-xs">{c}</span>
                      ))}
                    </div>
                  )}
                  {trial.locations?.length > 0 && (
                    <p className="text-sm text-secondary-brand flex items-center gap-1">
                      <MapPin className="w-3 h-3" aria-hidden="true" />
                      {trial.locations.slice(0, 3).join(' | ')}
                    </p>
                  )}
                </div>
                <a
                  href={trial.url || `https://clinicaltrials.gov/study/${trial.nct_id}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="glass-btn flex-shrink-0"
                  aria-label={`View trial ${trial.nct_id} on ClinicalTrials.gov`}
                >
                  <ExternalLink className="w-4 h-4" aria-hidden="true" />
                  View
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
