import { useState } from 'react'
import { DollarSign, BarChart3, Target, Eye, MousePointer, TrendingUp } from 'lucide-react'

interface AdSlot {
  id: string
  name: string
  location: string
  size: string
  price_monthly: number
  impressions_est: string
  status: 'available' | 'sold' | 'pending'
}

const adSlots: AdSlot[] = [
  { id: '1', name: 'Hero Banner', location: 'Landing Page Top', size: '1200x300', price_monthly: 299, impressions_est: '50K-100K', status: 'available' },
  { id: '2', name: 'Sidebar Premium', location: 'Dashboard Right', size: '300x600', price_monthly: 149, impressions_est: '30K-60K', status: 'available' },
  { id: '3', name: 'In-Feed Native', location: 'Analysis Results', size: '600x200', price_monthly: 199, impressions_est: '20K-40K', status: 'sold' },
  { id: '4', name: 'Footer Sponsor', location: 'All Pages Footer', size: '728x90', price_monthly: 99, impressions_est: '80K-150K', status: 'available' },
  { id: '5', name: 'Product Spotlight', location: 'Recommendations', size: '400x400', price_monthly: 249, impressions_est: '15K-30K', status: 'pending' },
  { id: '6', name: 'Email Digest', location: 'Weekly Newsletter', size: '600x200', price_monthly: 179, impressions_est: '10K-25K', status: 'available' },
]

export default function SellingSpacePage() {
  const [filter, setFilter] = useState<'all' | 'available' | 'sold' | 'pending'>('all')

  const filtered = filter === 'all' ? adSlots : adSlots.filter(s => s.status === filter)

  const totalRevenue = adSlots.filter(s => s.status === 'sold').reduce((sum, s) => sum + s.price_monthly, 0)
  const availableSlots = adSlots.filter(s => s.status === 'available').length
  const potentialRevenue = adSlots.reduce((sum, s) => sum + s.price_monthly, 0)

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold mb-2">Selling Space</h1>
        <p className="text-secondary-brand">Premium ad placements for skincare and wellness brands</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <div className="glass-card text-center">
          <DollarSign className="w-8 h-8 text-green-400 mx-auto mb-2" aria-hidden="true" />
          <p className="text-2xl font-bold">${totalRevenue}</p>
          <p className="text-xs text-secondary-brand">Monthly Revenue</p>
        </div>
        <div className="glass-card text-center">
          <Target className="w-8 h-8 text-amber-400 mx-auto mb-2" aria-hidden="true" />
          <p className="text-2xl font-bold">{availableSlots}</p>
          <p className="text-xs text-secondary-brand">Available Slots</p>
        </div>
        <div className="glass-card text-center">
          <TrendingUp className="w-8 h-8 text-purple-400 mx-auto mb-2" aria-hidden="true" />
          <p className="text-2xl font-bold">${potentialRevenue}</p>
          <p className="text-xs text-secondary-brand">Potential Monthly</p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-2 mb-6" role="group" aria-label="Filter ad slots">
        {(['all', 'available', 'sold', 'pending'] as const).map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`glass-btn text-sm capitalize ${filter === f ? 'bg-amber-500/20 border-amber-500/30 text-amber-400' : ''}`}
            aria-pressed={filter === f}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Ad Slots Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map(slot => (
          <div key={slot.id} className="glass-card space-y-3">
            <div className="flex items-start justify-between">
              <h3 className="font-semibold">{slot.name}</h3>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                slot.status === 'available' ? 'bg-green-500/10 text-green-400' :
                slot.status === 'sold' ? 'bg-red-500/10 text-red-400' :
                'bg-amber-500/10 text-amber-400'
              }`}>
                {slot.status}
              </span>
            </div>

            <p className="text-sm text-secondary-brand">{slot.location}</p>

            <div className="grid grid-cols-2 gap-3 text-sm">
              <div className="flex items-center gap-2">
                <Eye className="w-4 h-4 text-secondary-brand" aria-hidden="true" />
                <span>{slot.impressions_est}/mo</span>
              </div>
              <div className="flex items-center gap-2">
                <MousePointer className="w-4 h-4 text-secondary-brand" aria-hidden="true" />
                <span>{slot.size}px</span>
              </div>
            </div>

            <div className="flex items-center justify-between pt-3 border-t" style={{ borderColor: 'rgba(251, 191, 36, 0.08)' }}>
              <span className="text-lg font-bold text-green-400">${slot.price_monthly}<span className="text-xs text-secondary-brand font-normal">/mo</span></span>
              {slot.status === 'available' && (
                <button className="glass-btn-primary text-sm">Purchase</button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
