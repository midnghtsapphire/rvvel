import { Link } from 'react-router-dom'
import { Sparkles, MapPin, CloudSun, Search, Shield, Globe, Upload, ArrowRight, Check } from 'lucide-react'

const features = [
  { icon: Sparkles, title: 'AI Skin Analysis', description: 'Upload a photo and get instant AI-powered skin analysis with personalized recommendations.' },
  { icon: MapPin, title: 'GPS Personalization', description: 'Recommendations adapt to your location — dry Colorado air vs. humid California coast.' },
  { icon: CloudSun, title: 'Weather Skincare', description: 'Daily skincare adjustments based on real-time weather conditions in your area.' },
  { icon: Search, title: 'Clinical Trials Finder', description: 'Search ClinicalTrials.gov for relevant dermatology trials near you.' },
  { icon: Shield, title: 'Procedure Education', description: 'Learn about hidden procedures like PDO threads, with BBB ratings and reviews.' },
  { icon: Globe, title: 'Medical Tourism', description: 'Explore safe, affordable skincare procedures worldwide with verified providers.' },
]

const pricingTiers = [
  { name: 'Free', price: 0, tokens: 10, features: ['10 AI tokens/month', 'Basic skin analysis', 'Weather tips'], cta: 'Get Started', popular: false },
  { name: 'Starter', price: 9, tokens: 100, features: ['100 AI tokens/month', 'Full skin analysis', 'Makeup advisor', 'DIY recipes'], cta: 'Start Free Trial', popular: false },
  { name: 'Pro', price: 29, tokens: 500, features: ['500 AI tokens/month', 'All features', 'Clinical trials', 'Priority support'], cta: 'Go Pro', popular: true },
  { name: 'Business', price: 99, tokens: 2000, features: ['2,000 AI tokens/month', 'API access', 'White label', 'Analytics dashboard'], cta: 'Contact Sales', popular: false },
  { name: 'Enterprise', price: 299, tokens: 10000, features: ['10,000 AI tokens/month', 'Dedicated support', 'Custom integration', 'SLA guarantee'], cta: 'Contact Sales', popular: false },
]

export default function LandingPage() {
  return (
    <div>
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 sm:py-32" aria-labelledby="hero-title">
        {/* Ambient glow */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl" aria-hidden="true" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl" aria-hidden="true" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 glass-card px-4 py-2 mb-8 text-sm">
            <Sparkles className="w-4 h-4 text-primary-brand" aria-hidden="true" />
            <span>Powered by AI + GPS + Real-Time Weather</span>
          </div>

          <h1 id="hero-title" className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight mb-6">
            Your Skin,{' '}
            <span className="gradient-text">Decoded by AI</span>
          </h1>

          <p className="max-w-2xl mx-auto text-lg sm:text-xl text-secondary-brand mb-10">
            Upload a photo. Get personalized skincare recommendations powered by artificial intelligence,
            GPS-based climate data, and real-time weather conditions.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/analyze" className="glass-btn-primary text-lg px-8 py-4 rounded-xl">
              <Upload className="w-5 h-5" aria-hidden="true" />
              Start Free Analysis
            </Link>
            <Link to="/pricing" className="glass-btn text-lg px-8 py-4 rounded-xl">
              View Pricing
              <ArrowRight className="w-5 h-5" aria-hidden="true" />
            </Link>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20" aria-labelledby="features-title">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 id="features-title" className="text-3xl sm:text-4xl font-bold mb-4">
              Everything Your Skin Needs
            </h2>
            <p className="text-lg text-secondary-brand max-w-2xl mx-auto">
              From AI analysis to clinical trials, we cover every aspect of your skincare journey.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, i) => (
              <div
                key={feature.title}
                className="glass-card group"
                style={{ animationDelay: `${i * 100}ms` }}
              >
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
                  <feature.icon className="w-6 h-6 text-primary-brand" aria-hidden="true" />
                </div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-secondary-brand text-sm">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-glass" aria-labelledby="how-title">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 id="how-title" className="text-3xl sm:text-4xl font-bold mb-4">
              How It Works
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { step: '01', title: 'Upload Your Photo', description: 'Take a clear photo of your skin in natural lighting. Our AI works best with well-lit, close-up images.' },
              { step: '02', title: 'AI Analyzes Your Skin', description: 'Our AI identifies skin type, conditions, texture, hydration levels, and sun damage using advanced vision models.' },
              { step: '03', title: 'Get Personalized Plan', description: 'Receive a customized skincare routine adjusted for your location, weather, and specific concerns.' },
            ].map((item) => (
              <div key={item.step} className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 text-primary-brand text-2xl font-bold mb-4">
                  {item.step}
                </div>
                <h3 className="text-lg font-semibold mb-2">{item.title}</h3>
                <p className="text-secondary-brand text-sm">{item.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20" aria-labelledby="pricing-title">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 id="pricing-title" className="text-3xl sm:text-4xl font-bold mb-4">
              Simple, Transparent Pricing
            </h2>
            <p className="text-lg text-secondary-brand">
              Start free. Upgrade when you need more.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6">
            {pricingTiers.map((tier) => (
              <div
                key={tier.name}
                className={`glass-card relative ${tier.popular ? 'ring-2 ring-primary' : ''}`}
              >
                {tier.popular && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary text-dark px-3 py-1 rounded-full text-xs font-bold">
                    Most Popular
                  </div>
                )}
                <h3 className="text-lg font-semibold mb-2">{tier.name}</h3>
                <div className="mb-4">
                  <span className="text-3xl font-bold">${tier.price}</span>
                  {tier.price > 0 && <span className="text-secondary-brand">/mo</span>}
                </div>
                <ul className="space-y-2 mb-6" role="list">
                  {tier.features.map((f) => (
                    <li key={f} className="flex items-start gap-2 text-sm">
                      <Check className="w-4 h-4 text-primary-brand mt-0.5 flex-shrink-0" aria-hidden="true" />
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>
                <Link
                  to={tier.price === 0 ? '/register' : '/pricing'}
                  className={`block text-center rounded-lg py-3 text-sm font-semibold transition-colors ${
                    tier.popular
                      ? 'bg-primary text-dark hover:bg-secondary'
                      : 'glass-btn w-full'
                  }`}
                >
                  {tier.cta}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-glass" aria-labelledby="cta-title">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 id="cta-title" className="text-3xl sm:text-4xl font-bold mb-4">
            Ready to Decode Your Skin?
          </h2>
          <p className="text-lg text-secondary-brand mb-8">
            Join thousands who trust AI-powered skincare recommendations.
            Start with 10 free tokens — no credit card required.
          </p>
          <Link to="/register" className="glass-btn-primary text-lg px-8 py-4 rounded-xl inline-flex items-center gap-2">
            <Sparkles className="w-5 h-5" aria-hidden="true" />
            Start Free Analysis
          </Link>
        </div>
      </section>
    </div>
  )
}
