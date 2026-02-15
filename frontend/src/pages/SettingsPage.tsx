/**
 * Settings Page — Central hub for all accessibility and preference controls.
 * Standards 1, 3, 7 all converge here.
 */
import { AccessibilityPanel } from '../components/neurodivergent/FocusMode'
import { CarbonDashboard } from '../components/eco/CarbonBadge'
import { Shield, Palette, Brain, Leaf } from 'lucide-react'

export default function SettingsPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold mb-2">Settings</h1>
        <p className="text-secondary-brand">Customize your experience</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Accessibility Panel */}
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Shield className="w-5 h-5 text-amber-400" aria-hidden="true" />
            <h2 className="text-lg font-semibold">Accessibility</h2>
          </div>
          <AccessibilityPanel />
        </div>

        {/* Carbon Dashboard */}
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Leaf className="w-5 h-5 text-green-400" aria-hidden="true" />
            <h2 className="text-lg font-semibold">Eco Impact</h2>
          </div>
          <CarbonDashboard />
        </div>

        {/* Display Preferences */}
        <div className="glass-card space-y-4">
          <div className="flex items-center gap-2">
            <Palette className="w-5 h-5 text-amber-400" aria-hidden="true" />
            <h3 className="font-semibold">Display</h3>
          </div>
          <div className="space-y-3 text-sm">
            <div className="flex items-center justify-between p-3 rounded-xl hover:bg-white/5 transition-colors">
              <div>
                <p className="font-medium">Blue Light Filter</p>
                <p className="text-xs text-secondary-brand">Always on — protects your eyes</p>
              </div>
              <span className="text-xs text-green-400 font-medium">Active</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-xl hover:bg-white/5 transition-colors">
              <div>
                <p className="font-medium">Dark Mode</p>
                <p className="text-xs text-secondary-brand">Default — warm dark theme</p>
              </div>
              <span className="text-xs text-green-400 font-medium">Active</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-xl hover:bg-white/5 transition-colors">
              <div>
                <p className="font-medium">Animations</p>
                <p className="text-xs text-secondary-brand">Respects system reduced-motion preference</p>
              </div>
              <span className="text-xs text-amber-400 font-medium">System</span>
            </div>
          </div>
        </div>

        {/* Neurodivergent Features */}
        <div className="glass-card space-y-4">
          <div className="flex items-center gap-2">
            <Brain className="w-5 h-5 text-purple-400" aria-hidden="true" />
            <h3 className="font-semibold">Neurodivergent Support</h3>
          </div>
          <div className="space-y-3 text-sm">
            <div className="flex items-center justify-between p-3 rounded-xl hover:bg-white/5 transition-colors">
              <div>
                <p className="font-medium">Break Reminders</p>
                <p className="text-xs text-secondary-brand">Gentle visual nudge every 25 minutes</p>
              </div>
              <span className="text-xs text-green-400 font-medium">On</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-xl hover:bg-white/5 transition-colors">
              <div>
                <p className="font-medium">Progress Indicators</p>
                <p className="text-xs text-secondary-brand">Dopamine-friendly achievement tracking</p>
              </div>
              <span className="text-xs text-green-400 font-medium">On</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-xl hover:bg-white/5 transition-colors">
              <div>
                <p className="font-medium">Audio Notifications</p>
                <p className="text-xs text-secondary-brand">Disabled — all notifications are visual only</p>
              </div>
              <span className="text-xs text-red-400 font-medium">Disabled</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-xl hover:bg-white/5 transition-colors">
              <div>
                <p className="font-medium">Auto-play Media</p>
                <p className="text-xs text-secondary-brand">Disabled — no sudden sounds or motion</p>
              </div>
              <span className="text-xs text-red-400 font-medium">Disabled</span>
            </div>
          </div>
        </div>
      </div>

      {/* Attribution Footer */}
      <div className="mt-12 text-center text-xs text-secondary-brand" role="contentinfo">
        <p>Authentication provided by free sources and API (Google OAuth, Apple Sign-In)</p>
        <p>Payment processing provided by Stripe API</p>
        <p>AI models provided by OpenRouter API</p>
        <p className="mt-2">Audrey Evans Official / GlowStarLabs — Built with care for every user.</p>
      </div>
    </div>
  )
}
