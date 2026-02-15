import { Link } from 'react-router-dom'
import { Sparkles, Leaf, Heart } from 'lucide-react'

export default function Footer() {
  return (
    <footer
      className="relative z-10 mt-auto"
      style={{
        background: 'rgba(13, 11, 8, 0.9)',
        backdropFilter: 'blur(20px)',
        borderTop: '1px solid rgba(251, 191, 36, 0.08)',
      }}
      role="contentinfo"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="md:col-span-1">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles className="w-5 h-5 text-primary-brand" aria-hidden="true" />
              <span className="font-bold gradient-text">Project Face</span>
            </div>
            <p className="text-sm text-secondary-brand">
              AI-powered skin analysis by GlowStarLabs. Your skin, decoded.
            </p>
            <p className="text-xs text-secondary-brand mt-2">
              A product of Audrey Evans Official
            </p>
            <div className="flex items-center gap-2 text-xs text-green-400 mt-3">
              <Leaf className="w-3 h-3" aria-hidden="true" />
              <span>Eco-coded with carbon tracking</span>
            </div>
          </div>

          {/* Product */}
          <div>
            <h3 className="font-semibold mb-4 text-sm uppercase tracking-wider">Product</h3>
            <ul className="space-y-2" aria-label="Product links">
              <li><Link to="/analyze" className="text-sm text-secondary-brand hover:text-primary-brand transition-colors">Skin Analysis</Link></li>
              <li><Link to="/clinical-trials" className="text-sm text-secondary-brand hover:text-primary-brand transition-colors">Clinical Trials</Link></li>
              <li><Link to="/procedures" className="text-sm text-secondary-brand hover:text-primary-brand transition-colors">Procedures</Link></li>
              <li><Link to="/medical-tourism" className="text-sm text-secondary-brand hover:text-primary-brand transition-colors">Medical Tourism</Link></li>
              <li><Link to="/pricing" className="text-sm text-secondary-brand hover:text-primary-brand transition-colors">Pricing</Link></li>
            </ul>
          </div>

          {/* Tools */}
          <div>
            <h3 className="font-semibold mb-4 text-sm uppercase tracking-wider">Tools</h3>
            <ul className="space-y-2" aria-label="Tools links">
              <li><Link to="/benchmark" className="text-sm text-secondary-brand hover:text-primary-brand transition-colors">AI Benchmark</Link></li>
              <li><Link to="/data-router" className="text-sm text-secondary-brand hover:text-primary-brand transition-colors">Data Router</Link></li>
              <li><Link to="/selling-space" className="text-sm text-secondary-brand hover:text-primary-brand transition-colors">Selling Space</Link></li>
              <li><Link to="/dashboard" className="text-sm text-secondary-brand hover:text-primary-brand transition-colors">Dashboard</Link></li>
              <li><Link to="/settings" className="text-sm text-secondary-brand hover:text-primary-brand transition-colors">Accessibility</Link></li>
            </ul>
          </div>

          {/* Domains */}
          <div>
            <h3 className="font-semibold mb-4 text-sm uppercase tracking-wider">Our Sites</h3>
            <ul className="space-y-2" aria-label="Company websites">
              <li><a href="https://meetaudreyevans.com" className="text-sm text-secondary-brand hover:text-primary-brand transition-colors" target="_blank" rel="noopener noreferrer">meetaudreyevans.com</a></li>
              <li><a href="https://glowstarlabs.com" className="text-sm text-secondary-brand hover:text-primary-brand transition-colors" target="_blank" rel="noopener noreferrer">glowstarlabs.com</a></li>
              <li><a href="https://truthslayer.com" className="text-sm text-secondary-brand hover:text-primary-brand transition-colors" target="_blank" rel="noopener noreferrer">truthslayer.com</a></li>
              <li><a href="https://reesereviews.com" className="text-sm text-secondary-brand hover:text-primary-brand transition-colors" target="_blank" rel="noopener noreferrer">reesereviews.com</a></li>
              <li><a href="https://growlingeyes.com" className="text-sm text-secondary-brand hover:text-primary-brand transition-colors" target="_blank" rel="noopener noreferrer">growlingeyes.com</a></li>
              <li><a href="https://yumyumcode.com" className="text-sm text-secondary-brand hover:text-primary-brand transition-colors" target="_blank" rel="noopener noreferrer">yumyumcode.com</a></li>
            </ul>
          </div>
        </div>

        {/* Medical Disclaimer */}
        <div className="medical-disclaimer mt-8">
          <strong>Medical Disclaimer:</strong> This application is for informational purposes only
          and is not a substitute for professional medical advice, diagnosis, or treatment.
          Always seek the advice of your physician or other qualified health care provider.
        </div>

        {/* Bottom Bar */}
        <div className="mt-8 pt-8 border-t" style={{ borderColor: 'rgba(251, 191, 36, 0.08)' }}>
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-xs text-secondary-brand">
              &copy; {new Date().getFullYear()} Audrey Evans Official / GlowStarLabs. All rights reserved.
            </p>
            <div className="flex items-center gap-1 text-xs text-secondary-brand">
              <span>Made with</span>
              <Heart className="w-3 h-3 text-red-400" aria-hidden="true" />
              <span>for every body, every skin, every ability.</span>
            </div>
            <div className="flex items-center gap-4">
              <Link to="/privacy" className="text-xs text-secondary-brand hover:text-primary-brand transition-colors">Privacy</Link>
              <Link to="/terms" className="text-xs text-secondary-brand hover:text-primary-brand transition-colors">Terms</Link>
              <Link to="/settings" className="text-xs text-secondary-brand hover:text-primary-brand transition-colors">Accessibility</Link>
            </div>
          </div>

          {/* Standard: Mandatory attribution for integrated components */}
          <div className="mt-4 text-center text-xs text-secondary-brand opacity-60">
            <p>Authentication provided by free sources and API (Google OAuth, Apple Sign-In) |
              Payment processing provided by Stripe |
              AI models provided by OpenRouter API |
              Clinical data provided by ClinicalTrials.gov API</p>
          </div>
        </div>
      </div>
    </footer>
  )
}
