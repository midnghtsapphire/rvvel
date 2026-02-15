import { Check, Star, Zap, Crown, Rocket } from 'lucide-react'

const tiers = [
  {
    name: 'Free',
    price: 0,
    tokens: 10,
    icon: Star,
    features: ['10 AI tokens/month', 'Basic skin analysis', 'Weather-based tips', 'Community access'],
    cta: 'Get Started',
    popular: false,
  },
  {
    name: 'Starter',
    price: 9,
    tokens: 100,
    icon: Zap,
    features: ['100 AI tokens/month', 'Full skin analysis', 'Product recommendations', 'Clinical trials search', 'Email support'],
    cta: 'Start Free Trial',
    popular: false,
  },
  {
    name: 'Pro',
    price: 29,
    tokens: 500,
    icon: Crown,
    features: ['500 AI tokens/month', 'Advanced analysis + history', 'GPS personalization', 'Procedure education', 'Medical tourism info', 'Priority support'],
    cta: 'Go Pro',
    popular: true,
  },
  {
    name: 'Business',
    price: 99,
    tokens: 2000,
    icon: Rocket,
    features: ['2,000 AI tokens/month', 'Everything in Pro', 'Data router access', 'AI benchmarking', 'Affiliate dashboard', 'API access'],
    cta: 'Start Business',
    popular: false,
  },
  {
    name: 'Enterprise',
    price: 299,
    tokens: 10000,
    icon: Crown,
    features: ['10,000 AI tokens/month', 'Everything in Business', 'White-label options', 'Custom integrations', 'Dedicated support', 'SLA guarantee'],
    cta: 'Contact Sales',
    popular: false,
  },
]

export default function PricingPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="text-center mb-12">
        <h1 className="text-3xl font-bold gradient-text mb-3">Simple, Transparent Pricing</h1>
        <p className="text-secondary-brand max-w-xl mx-auto">
          Choose the plan that fits your needs. All plans include our 8 mandatory standards:
          no blue light, eco code, neurodivergent-friendly design, and full WCAG AAA accessibility.
        </p>
      </div>

      <div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4"
        role="list"
        aria-label="Subscription plans"
      >
        {tiers.map((tier) => {
          const Icon = tier.icon
          return (
            <div
              key={tier.name}
              role="listitem"
              className={`glass-card relative flex flex-col ${
                tier.popular ? 'ring-2 ring-primary' : ''
              }`}
            >
              {tier.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary text-dark-brand text-xs font-bold px-3 py-1 rounded-full">
                  Most Popular
                </div>
              )}

              <div className="flex items-center gap-2 mb-3">
                <Icon className="w-5 h-5 text-primary" aria-hidden="true" />
                <h2 className="text-lg font-semibold">{tier.name}</h2>
              </div>

              <div className="mb-4">
                <span className="text-3xl font-bold gradient-text">
                  ${tier.price}
                </span>
                <span className="text-secondary-brand text-sm">/month</span>
              </div>

              <p className="text-xs text-secondary-brand mb-4">
                {tier.tokens.toLocaleString()} AI tokens included
              </p>

              <ul className="space-y-2 mb-6 flex-1" aria-label={`${tier.name} plan features`}>
                {tier.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-2 text-sm">
                    <Check className="w-4 h-4 text-primary shrink-0 mt-0.5" aria-hidden="true" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>

              <button
                className={tier.popular ? 'glass-btn-primary w-full' : 'glass-btn w-full'}
                aria-label={`${tier.cta} — ${tier.name} plan at $${tier.price} per month`}
              >
                {tier.cta}
              </button>
            </div>
          )
        })}
      </div>

      {/* Carbon savings note */}
      <div className="glass-card mt-8 text-center" role="complementary" aria-label="Carbon savings information">
        <p className="text-sm text-secondary-brand">
          <span className="text-primary font-semibold" aria-hidden="true">🌱</span>{' '}
          Every plan includes carbon tracking. Your usage is optimized for minimal environmental impact.
          We cache aggressively and use lightweight models first — saving an average of{' '}
          <span className="text-primary font-semibold">3.2 Starbucks cups of carbon</span> per user per month.
        </p>
      </div>

      {/* Medical disclaimer */}
      <div className="mt-6 text-center text-xs text-secondary-brand opacity-60" role="note">
        <p>
          Project Face provides informational skin analysis only. This is not medical advice.
          Always consult a board-certified dermatologist for medical skin concerns.
        </p>
      </div>
    </div>
  )
}
