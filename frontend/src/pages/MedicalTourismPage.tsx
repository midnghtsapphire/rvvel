import { useState } from 'react'
import { MapPin, DollarSign, Shield, Star, ExternalLink, Plane, AlertTriangle } from 'lucide-react'

interface Destination {
  city: string
  country: string
  specialty: string
  savings: string
  rating: number
  accreditation: string
  popular_procedures: string[]
}

const destinations: Destination[] = [
  {
    city: 'Tijuana',
    country: 'Mexico',
    specialty: 'Dental, Cosmetic Surgery, Bariatric',
    savings: '40-80% less than US prices',
    rating: 4.2,
    accreditation: 'JCI Accredited facilities available',
    popular_procedures: ['Dental Veneers', 'Rhinoplasty', 'Gastric Sleeve', 'Breast Augmentation'],
  },
  {
    city: 'Mexico City',
    country: 'Mexico',
    specialty: 'Cosmetic Surgery, Orthopedics',
    savings: '50-70% less than US prices',
    rating: 4.5,
    accreditation: 'JCI Accredited',
    popular_procedures: ['Facelift', 'Knee Replacement', 'Liposuction', 'Tummy Tuck'],
  },
  {
    city: 'Bangkok',
    country: 'Thailand',
    specialty: 'Cosmetic Surgery, Gender Affirming Care',
    savings: '50-80% less than US prices',
    rating: 4.7,
    accreditation: 'JCI Accredited — Bumrungrad International',
    popular_procedures: ['Gender Affirming Surgery', 'Cosmetic Surgery', 'Dental', 'Eye Surgery'],
  },
  {
    city: 'Seoul',
    country: 'South Korea',
    specialty: 'Cosmetic Surgery, Dermatology, Skincare',
    savings: '30-60% less than US prices',
    rating: 4.8,
    accreditation: 'KHA Certified',
    popular_procedures: ['Double Eyelid', 'Rhinoplasty', 'Skin Treatments', 'Hair Transplant'],
  },
  {
    city: 'Istanbul',
    country: 'Turkey',
    specialty: 'Hair Transplant, Dental, Cosmetic',
    savings: '50-80% less than US prices',
    rating: 4.3,
    accreditation: 'JCI Accredited facilities',
    popular_procedures: ['Hair Transplant', 'Dental Implants', 'BBL', 'Rhinoplasty'],
  },
  {
    city: 'Medellín',
    country: 'Colombia',
    specialty: 'Cosmetic Surgery, Dental',
    savings: '40-70% less than US prices',
    rating: 4.4,
    accreditation: 'Ministry of Health certified',
    popular_procedures: ['BBL', 'Breast Augmentation', 'Liposuction', 'Dental Veneers'],
  },
]

export default function MedicalTourismPage() {
  const [selectedCountry, setSelectedCountry] = useState('all')

  const filtered = selectedCountry === 'all'
    ? destinations
    : destinations.filter(d => d.country === selectedCountry)

  const countries = [...new Set(destinations.map(d => d.country))]

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold mb-2">Medical Tourism</h1>
        <p className="text-secondary-brand">Quality care at a fraction of US prices — with safety first</p>
      </div>

      {/* Safety Warning */}
      <div className="medical-disclaimer mb-8" role="alert">
        <div className="flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" aria-hidden="true" />
          <div>
            <strong>Safety First:</strong> Always verify facility accreditation (JCI is the gold standard),
            check surgeon credentials, read verified patient reviews, and consult your primary care physician
            before traveling for medical procedures. Never choose solely based on price.
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2 mb-6">
        <button
          onClick={() => setSelectedCountry('all')}
          className={`glass-btn text-sm ${selectedCountry === 'all' ? 'bg-amber-500/20 border-amber-500/30 text-amber-400' : ''}`}
          aria-pressed={selectedCountry === 'all'}
        >
          All Destinations
        </button>
        {countries.map(c => (
          <button
            key={c}
            onClick={() => setSelectedCountry(c)}
            className={`glass-btn text-sm ${selectedCountry === c ? 'bg-amber-500/20 border-amber-500/30 text-amber-400' : ''}`}
            aria-pressed={selectedCountry === c}
          >
            {c}
          </button>
        ))}
      </div>

      {/* Destinations Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map(dest => (
          <div key={`${dest.city}-${dest.country}`} className="glass-card space-y-4">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-lg font-bold">{dest.city}</h3>
                <div className="flex items-center gap-1 text-sm text-secondary-brand">
                  <MapPin className="w-3 h-3" aria-hidden="true" />
                  {dest.country}
                </div>
              </div>
              <div className="flex items-center gap-1 text-amber-400">
                <Star className="w-4 h-4 fill-current" aria-hidden="true" />
                <span className="text-sm font-medium">{dest.rating}</span>
              </div>
            </div>

            <p className="text-sm text-secondary-brand">{dest.specialty}</p>

            <div className="flex items-center gap-2">
              <DollarSign className="w-4 h-4 text-green-400" aria-hidden="true" />
              <span className="text-sm text-green-400 font-medium">{dest.savings}</span>
            </div>

            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4 text-amber-400" aria-hidden="true" />
              <span className="text-xs text-secondary-brand">{dest.accreditation}</span>
            </div>

            <div>
              <p className="text-xs text-secondary-brand mb-2">Popular Procedures:</p>
              <div className="flex flex-wrap gap-1">
                {dest.popular_procedures.map(p => (
                  <span key={p} className="px-2 py-1 rounded-lg text-xs" style={{
                    background: 'rgba(245, 158, 11, 0.08)',
                    border: '1px solid rgba(245, 158, 11, 0.15)',
                    color: 'var(--amber-300)',
                  }}>
                    {p}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Tips Section */}
      <div className="mt-12 glass-card">
        <h2 className="text-xl font-bold mb-4">Medical Tourism Checklist</h2>
        <ol className="space-y-3 text-sm text-secondary-brand" aria-label="Medical tourism safety checklist">
          <li className="flex items-start gap-3">
            <span className="w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center flex-shrink-0 text-xs font-bold" aria-hidden="true">1</span>
            <span>Verify the facility has JCI or equivalent international accreditation</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center flex-shrink-0 text-xs font-bold" aria-hidden="true">2</span>
            <span>Check surgeon credentials — board certification in their country + international training</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center flex-shrink-0 text-xs font-bold" aria-hidden="true">3</span>
            <span>Read verified patient reviews (not just testimonials on the clinic's site)</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center flex-shrink-0 text-xs font-bold" aria-hidden="true">4</span>
            <span>Plan for recovery time — don't fly home too soon after surgery</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center flex-shrink-0 text-xs font-bold" aria-hidden="true">5</span>
            <span>Get medical tourism insurance (standard travel insurance usually doesn't cover procedures)</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center flex-shrink-0 text-xs font-bold" aria-hidden="true">6</span>
            <span>Have a follow-up plan with a local doctor when you return home</span>
          </li>
        </ol>
      </div>
    </div>
  )
}
