import { Users, DollarSign, Activity, Leaf, Shield, Settings, BarChart3, AlertTriangle } from 'lucide-react'

const adminStats = [
  { label: 'Total Users', value: '1,247', change: '+23 today', icon: Users, color: 'text-primary' },
  { label: 'MRR', value: '$8,450', change: '+$340', icon: DollarSign, color: 'text-green-400' },
  { label: 'API Calls Today', value: '12,847', change: '78% cached', icon: Activity, color: 'text-blue-400' },
  { label: 'CO2 Saved', value: '2.4kg', change: '114 cups', icon: Leaf, color: 'text-emerald-400' },
]

const recentActivity = [
  { time: '2 min ago', event: 'New user registration', detail: 'user@example.com', type: 'info' },
  { time: '5 min ago', event: 'Subscription upgrade', detail: 'Free → Pro', type: 'success' },
  { time: '12 min ago', event: 'Skin analysis completed', detail: 'Score: 8.2/10', type: 'info' },
  { time: '18 min ago', event: 'Affiliate conversion', detail: '$12.50 commission', type: 'success' },
  { time: '25 min ago', event: 'Break reminder sent', detail: '47 users notified (visual)', type: 'info' },
  { time: '1 hr ago', event: 'Cache hit rate optimal', detail: '92% efficiency', type: 'success' },
]

export default function AdminPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold gradient-text mb-2">Admin Dashboard</h1>
          <p className="text-secondary-brand text-sm">
            GlowStarLabs platform management. All 8 mandatory standards active.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="flex items-center gap-1 text-xs text-green-400 bg-green-400/10 px-2 py-1 rounded-full">
            <span className="w-2 h-2 bg-green-400 rounded-full" aria-hidden="true"></span>
            All Systems Operational
          </span>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-8" role="list" aria-label="Platform statistics">
        {adminStats.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.label} className="glass-card" role="listitem">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs text-secondary-brand">{stat.label}</span>
                <Icon className={`w-4 h-4 ${stat.color}`} aria-hidden="true" />
              </div>
              <div className="text-2xl font-bold">{stat.value}</div>
              <div className="text-xs text-secondary-brand mt-1">{stat.change}</div>
            </div>
          )
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Recent activity */}
        <div className="glass-card">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Activity className="w-4 h-4 text-primary" aria-hidden="true" />
            Recent Activity
          </h2>
          <div className="space-y-3" role="log" aria-label="Recent platform activity">
            {recentActivity.map((item, i) => (
              <div key={i} className="flex items-start gap-3 text-sm">
                <span className={`w-2 h-2 rounded-full mt-1.5 shrink-0 ${
                  item.type === 'success' ? 'bg-green-400' : 'bg-primary'
                }`} aria-hidden="true" />
                <div className="flex-1 min-w-0">
                  <div className="font-medium">{item.event}</div>
                  <div className="text-xs text-secondary-brand">{item.detail}</div>
                </div>
                <span className="text-xs text-secondary-brand whitespace-nowrap">{item.time}</span>
              </div>
            ))}
          </div>
        </div>

        {/* 8 Standards compliance */}
        <div className="glass-card">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Shield className="w-4 h-4 text-primary" aria-hidden="true" />
            8 Standards Compliance
          </h2>
          <div className="space-y-2" role="list" aria-label="Mandatory standards compliance status">
            {[
              { name: 'No Blue Light', status: 'Active', score: 100 },
              { name: 'Eco Code', status: 'Active', score: 96 },
              { name: 'Neurodivergent-Friendly', status: 'Active', score: 100 },
              { name: 'Glassmorphism UI', status: 'Active', score: 100 },
              { name: 'Best in Class', status: 'Active', score: 94 },
              { name: 'Blue Ocean Gangster', status: 'Active', score: 98 },
              { name: 'Alt Text Everywhere', status: 'Active', score: 100 },
              { name: 'Carbon Quantifier', status: 'Active', score: 97 },
            ].map((standard) => (
              <div key={standard.name} className="flex items-center justify-between text-sm" role="listitem">
                <span>{standard.name}</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 h-1.5 bg-dark-glass rounded-full overflow-hidden" role="progressbar" aria-valuenow={standard.score} aria-valuemin={0} aria-valuemax={100} aria-label={`${standard.name}: ${standard.score}%`}>
                    <div className="h-full bg-primary rounded-full" style={{ width: `${standard.score}%` }} />
                  </div>
                  <span className="text-xs text-green-400 font-mono w-8 text-right">{standard.score}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
