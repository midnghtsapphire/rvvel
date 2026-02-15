import { useState, useRef } from 'react'
import { Upload, Camera, MapPin, Loader2, Sparkles, AlertTriangle } from 'lucide-react'

const skinConcerns = [
  'Acne', 'Aging', 'Dark spots', 'Dryness', 'Oiliness', 'Redness',
  'Wrinkles', 'Sun damage', 'Texture', 'Pores', 'Sensitivity', 'General',
]

export default function SkinAnalysisPage() {
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string>('')
  const [concerns, setConcerns] = useState<string[]>(['General'])
  const [location, setLocation] = useState<{ lat: number; lon: number } | null>(null)
  const [city, setCity] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const fileRef = useRef<HTMLInputElement>(null)

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (f) {
      setFile(f)
      setPreview(URL.createObjectURL(f))
    }
  }

  const toggleConcern = (c: string) => {
    setConcerns(prev =>
      prev.includes(c) ? prev.filter(x => x !== c) : [...prev, c]
    )
  }

  const getLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        pos => setLocation({ lat: pos.coords.latitude, lon: pos.coords.longitude }),
        () => alert('Location access denied. Enter your city instead.')
      )
    }
  }

  const handleAnalyze = async () => {
    if (!file) return
    setLoading(true)
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('concerns', concerns.join(','))
    if (location) {
      formData.append('latitude', String(location.lat))
      formData.append('longitude', String(location.lon))
    } else if (city) {
      formData.append('city', city)
    }

    try {
      const resp = await fetch('/api/skin/analyze', { method: 'POST', body: formData })
      const data = await resp.json()
      setResult(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold mb-2">AI Skin Analysis</h1>
        <p className="text-secondary-brand">Upload a photo for personalized skincare recommendations</p>
      </div>

      {/* Medical Disclaimer */}
      <div className="medical-disclaimer mb-8" role="alert">
        <strong>Medical Disclaimer:</strong> This tool provides informational analysis only.
        It is not a substitute for professional medical advice. Always consult a dermatologist
        for medical concerns.
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Upload Section */}
        <div className="space-y-6">
          {/* Photo Upload */}
          <div className="glass-card">
            <h2 className="text-lg font-semibold mb-4">Step 1: Upload Photo</h2>
            <div
              className="border-2 border-dashed border-glass rounded-xl p-8 text-center cursor-pointer hover:border-primary transition-colors"
              onClick={() => fileRef.current?.click()}
              role="button"
              tabIndex={0}
              aria-label="Click to upload a photo"
              onKeyDown={e => e.key === 'Enter' && fileRef.current?.click()}
            >
              {preview ? (
                <img src={preview} alt="Uploaded skin photo preview" className="max-h-64 mx-auto rounded-lg" />
              ) : (
                <>
                  <Camera className="w-12 h-12 text-secondary-brand mx-auto mb-4" aria-hidden="true" />
                  <p className="font-medium">Click to upload or drag and drop</p>
                  <p className="text-sm text-secondary-brand mt-1">PNG, JPG up to 10MB</p>
                </>
              )}
              <input
                ref={fileRef}
                type="file"
                accept="image/*"
                onChange={handleFile}
                className="hidden"
                aria-label="Upload skin photo"
              />
            </div>
          </div>

          {/* Concerns */}
          <div className="glass-card">
            <h2 className="text-lg font-semibold mb-4">Step 2: Select Concerns</h2>
            <div className="flex flex-wrap gap-2" role="group" aria-label="Skin concerns">
              {skinConcerns.map(c => (
                <button
                  key={c}
                  onClick={() => toggleConcern(c)}
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    concerns.includes(c)
                      ? 'bg-primary text-dark'
                      : 'glass-btn'
                  }`}
                  aria-pressed={concerns.includes(c)}
                >
                  {c}
                </button>
              ))}
            </div>
          </div>

          {/* Location */}
          <div className="glass-card">
            <h2 className="text-lg font-semibold mb-4">Step 3: Location (Optional)</h2>
            <p className="text-sm text-secondary-brand mb-4">
              GPS data personalizes recommendations for your climate (dry Colorado vs. humid California).
            </p>
            <div className="flex gap-3">
              <button onClick={getLocation} className="glass-btn flex-1">
                <MapPin className="w-4 h-4" aria-hidden="true" />
                {location ? 'Location Set' : 'Use GPS'}
              </button>
              <input
                type="text"
                value={city}
                onChange={e => setCity(e.target.value)}
                className="glass-input flex-1"
                placeholder="Or enter city name"
                aria-label="City name for weather data"
              />
            </div>
          </div>

          {/* Analyze Button */}
          <button
            onClick={handleAnalyze}
            disabled={!file || loading}
            className="glass-btn-primary w-full py-4 rounded-xl text-lg disabled:opacity-50"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" aria-hidden="true" />
                Analyzing...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" aria-hidden="true" />
                Analyze My Skin
              </>
            )}
          </button>
        </div>

        {/* Results Section */}
        <div>
          {result ? (
            <div className="glass-card space-y-6" role="region" aria-label="Analysis results">
              <div className="flex items-center gap-2">
                <Sparkles className="w-6 h-6 text-primary-brand" aria-hidden="true" />
                <h2 className="text-xl font-bold">Your Analysis</h2>
              </div>

              {/* AI Analysis */}
              <div className="prose prose-invert max-w-none">
                <div className="whitespace-pre-wrap text-sm leading-relaxed">
                  {result.skin_analysis}
                </div>
              </div>

              {/* Weather Data */}
              {result.weather_personalization && (
                <div className="bg-blue-500/10 border border-blue-500/20 rounded-xl p-4">
                  <h3 className="font-semibold text-blue-400 mb-2">Weather Personalization</h3>
                  <pre className="text-xs text-secondary-brand overflow-auto">
                    {JSON.stringify(result.weather_personalization, null, 2)}
                  </pre>
                </div>
              )}

              {/* Tokens Used */}
              <div className="flex items-center justify-between text-sm text-secondary-brand pt-4 border-t border-glass">
                <span>Model: {result.model_used}</span>
                <span>Tokens used: {result.tokens_used}</span>
              </div>

              {/* Disclaimer */}
              <div className="medical-disclaimer">
                <strong>Reminder:</strong> {result.medical_disclaimer}
              </div>
            </div>
          ) : (
            <div className="glass-card text-center py-16">
              <Upload className="w-16 h-16 text-secondary-brand mx-auto mb-4" aria-hidden="true" />
              <h3 className="text-lg font-semibold mb-2">Upload a Photo to Begin</h3>
              <p className="text-secondary-brand text-sm">
                Your AI-powered skin analysis will appear here.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
