import { Link } from 'react-router-dom'
import { Sparkles, Upload, Search, Shield, BarChart3, FileText, Zap, Settings } from 'lucide-react'

const quickActions = [
  { icon: Upload, title: 'New Skin Analysis', description: 'Upload a photo for AI analysis', to: '/analyze', color: 'bg-amber-500/10 text-amber-500' },
  { icon: Search, title: 'Clinical Trials', description: 'Find trials near you', to: '/clinical-trials', color: 'bg-blue-500/10 text-blue-500' },
  { icon: Shield, title: 'Procedures', description: 'Research procedures', to: '/procedures', color: 'bg-green-500/10 text-green-500' },
  { icon: BarChart3, title: 'AI Benchmark', description: 'Compare AI models', to: '/benchmark', color: 'bg-purple-500/10 text-purple-500' },
  { icon: FileText, title: 'Data Router', description: 'Manage file routing', to: '/data-router', color: 'bg-cyan-500/10 text-cyan-500' },
  { icon: Zap, title: 'Quick Analysis', description: 'Weather-based tips', to: '/analyze', color: 'bg-orange-500/10 text-orange-500' },
]

export default function DashboardPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-secondary-brand mt-1">Welcome back. Here's your overview.</p>
        </div>
        <Link to="/analyze" className="glass-btn-primary">
          <Upload className="w-4 h-4" aria-hidden="true" />
          New Analysis
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {[
          { label: 'AI Tokens Left', value: '10', sublabel: 'of 10 this month' },
          { label: 'Analyses Done', value: '0', sublabel: 'lifetime' },
          { label: 'Subscription', value: 'Free', sublabel: 'Upgrade for more' },
          { label: 'Saved Products', value: '0', sublabel: 'recommendations' },
        ].map(stat => (
          <div key={stat.label} className="glass-card">
            <p className="text-sm text-secondary-brand">{stat.label}</p>
            <p className="text-3xl font-bold mt-1">{stat.value}</p>
            <p className="text-xs text-secondary-brand mt-1">{stat.sublabel}</p>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {quickActions.map(action => (
          <Link key={action.title} to={action.to} className="glass-card flex items-start gap-4 group">
            <div className={`w-12 h-12 rounded-xl ${action.color} flex items-center justify-center flex-shrink-0`}>
              <action.icon className="w-6 h-6" aria-hidden="true" />
            </div>
            <div>
              <h3 className="font-semibold group-hover:text-primary-brand transition-colors">{action.title}</h3>
              <p className="text-sm text-secondary-brand">{action.description}</p>
            </div>
          </Link>
        ))}
      </div>

      {/* Recent Activity */}
      <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
      <div className="glass-card">
        <div className="text-center py-12">
          <Sparkles className="w-12 h-12 text-secondary-brand mx-auto mb-4" aria-hidden="true" />
          <h3 className="text-lg font-semibold mb-2">No activity yet</h3>
          <p className="text-secondary-brand mb-4">Start by uploading a photo for your first skin analysis.</p>
          <Link to="/analyze" className="glass-btn-primary">
            Get Started
          </Link>
        </div>
      </div>
    </div>
  )
}
