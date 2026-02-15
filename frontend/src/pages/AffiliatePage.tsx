import { DollarSign, MousePointer, ShoppingCart, TrendingUp, ExternalLink } from 'lucide-react'

const stats = [
  { label: 'Total Clicks', value: '2,847', change: '+12%', icon: MousePointer },
  { label: 'Conversions', value: '156', change: '+8%', icon: ShoppingCart },
  { label: 'Revenue', value: '$1,247.50', change: '+15%', icon: DollarSign },
  { label: 'Conversion Rate', value: '5.5%', change: '+0.3%', icon: TrendingUp },
]

const topProducts = [
  { name: 'CeraVe Moisturizing Cream', clicks: 342, conversions: 28, revenue: '$156.80', category: 'Moisturizer' },
  { name: 'La Roche-Posay SPF 50', clicks: 287, conversions: 22, revenue: '$132.00', category: 'Sunscreen' },
  { name: 'The Ordinary Niacinamide', clicks: 198, conversions: 19, revenue: '$95.00', category: 'Serum' },
  { name: 'Neutrogena Hydro Boost', clicks: 176, conversions: 15, revenue: '$82.50', category: 'Moisturizer' },
  { name: 'Paula\'s Choice BHA Exfoliant', clicks: 154, conversions: 12, revenue: '$72.00', category: 'Exfoliant' },
]

export default function AffiliatePage() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold gradient-text mb-2">Affiliate Dashboard</h1>
        <p className="text-secondary-brand text-sm">
          Track your affiliate link performance. Auto-generated Amazon Associates links on all product recommendations.
        </p>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-8" role="list" aria-label="Affiliate statistics">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.label} className="glass-card" role="listitem">
              <div className="flex items-center gap-2 mb-2">
                <Icon className="w-4 h-4 text-primary" aria-hidden="true" />
                <span className="text-xs text-secondary-brand">{stat.label}</span>
              </div>
              <div className="text-2xl font-bold">{stat.value}</div>
              <div className="text-xs text-green-400 mt-1" aria-label={`Change: ${stat.change}`}>
                {stat.change} this month
              </div>
            </div>
          )
        })}
      </div>

      {/* Top products table */}
      <div className="glass-card">
        <h2 className="text-lg font-semibold mb-4">Top Performing Products</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm" role="table" aria-label="Top affiliate products">
            <thead>
              <tr className="border-b border-glass-border">
                <th className="text-left py-3 px-2 text-secondary-brand font-medium" scope="col">Product</th>
                <th className="text-left py-3 px-2 text-secondary-brand font-medium" scope="col">Category</th>
                <th className="text-right py-3 px-2 text-secondary-brand font-medium" scope="col">Clicks</th>
                <th className="text-right py-3 px-2 text-secondary-brand font-medium" scope="col">Conversions</th>
                <th className="text-right py-3 px-2 text-secondary-brand font-medium" scope="col">Revenue</th>
                <th className="text-right py-3 px-2 text-secondary-brand font-medium" scope="col">Link</th>
              </tr>
            </thead>
            <tbody>
              {topProducts.map((product) => (
                <tr key={product.name} className="border-b border-glass-border last:border-0 hover:bg-dark-glass transition-colors">
                  <td className="py-3 px-2 font-medium">{product.name}</td>
                  <td className="py-3 px-2 text-secondary-brand">{product.category}</td>
                  <td className="py-3 px-2 text-right">{product.clicks}</td>
                  <td className="py-3 px-2 text-right text-primary">{product.conversions}</td>
                  <td className="py-3 px-2 text-right text-green-400 font-semibold">{product.revenue}</td>
                  <td className="py-3 px-2 text-right">
                    <button className="glass-btn p-1.5" aria-label={`Open affiliate link for ${product.name}`}>
                      <ExternalLink className="w-3.5 h-3.5" aria-hidden="true" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
