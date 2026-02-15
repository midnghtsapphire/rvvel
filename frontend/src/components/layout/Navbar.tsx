import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X, Sparkles, Settings, User } from 'lucide-react'
import { FocusModeToggle } from '../neurodivergent/FocusMode'

const navLinks = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/analyze', label: 'Skin Analysis' },
  { to: '/clinical-trials', label: 'Clinical Trials' },
  { to: '/procedures', label: 'Procedures' },
  { to: '/data-router', label: 'Data Router' },
  { to: '/benchmark', label: 'AI Benchmark' },
  { to: '/pricing', label: 'Pricing' },
]

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false)
  const location = useLocation()

  return (
    <nav
      className="fixed top-0 left-0 right-0 z-50"
      style={{
        background: 'rgba(13, 11, 8, 0.85)',
        backdropFilter: 'blur(20px)',
        WebkitBackdropFilter: 'blur(20px)',
        borderBottom: '1px solid rgba(251, 191, 36, 0.08)',
      }}
      role="navigation"
      aria-label="Main navigation"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link
            to="/"
            className="flex items-center gap-2"
            aria-label="Project Face by GlowStarLabs — Home"
          >
            <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{
              background: 'linear-gradient(135deg, #F59E0B, #D97706)',
            }} aria-hidden="true">
              <Sparkles className="w-4 h-4 text-black" />
            </div>
            <div>
              <span className="font-bold text-sm gradient-text">Project Face</span>
              <span className="text-xs block" style={{ color: 'var(--text-muted)' }}>by GlowStarLabs</span>
            </div>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden lg:flex items-center gap-1" role="menubar">
            {navLinks.map(link => (
              <Link
                key={link.to}
                to={link.to}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  location.pathname === link.to
                    ? 'text-primary-brand bg-amber-500/10'
                    : 'text-secondary-brand hover:text-primary-brand hover:bg-white/5'
                }`}
                role="menuitem"
                aria-current={location.pathname === link.to ? 'page' : undefined}
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* Right side controls */}
          <div className="flex items-center gap-2">
            {/* Standard 3: Focus mode toggle */}
            <div className="hidden sm:block">
              <FocusModeToggle />
            </div>

            <Link to="/settings" className="glass-btn p-2" aria-label="Settings and accessibility">
              <Settings className="w-4 h-4" aria-hidden="true" />
            </Link>

            <div className="hidden md:flex items-center gap-2">
              <Link to="/login" className="glass-btn text-sm">Sign In</Link>
              <Link to="/register" className="glass-btn-primary text-sm">
                <User className="w-4 h-4" aria-hidden="true" />
                Get Started
              </Link>
            </div>

            {/* Mobile Menu Button */}
            <button
              className="lg:hidden glass-btn p-2"
              onClick={() => setIsOpen(!isOpen)}
              aria-expanded={isOpen}
              aria-controls="mobile-menu"
              aria-label={isOpen ? 'Close menu' : 'Open menu'}
            >
              {isOpen ? <X className="w-5 h-5" aria-hidden="true" /> : <Menu className="w-5 h-5" aria-hidden="true" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div
          id="mobile-menu"
          className="lg:hidden"
          style={{
            background: 'rgba(13, 11, 8, 0.95)',
            backdropFilter: 'blur(20px)',
            borderTop: '1px solid rgba(251, 191, 36, 0.08)',
          }}
          role="menu"
        >
          <div className="px-4 py-4 space-y-1">
            {navLinks.map(link => (
              <Link
                key={link.to}
                to={link.to}
                className={`block px-4 py-3 rounded-xl text-sm font-medium transition-colors ${
                  location.pathname === link.to
                    ? 'text-amber-400 bg-amber-500/10'
                    : 'text-secondary-brand hover:text-primary-brand hover:bg-white/5'
                }`}
                onClick={() => setIsOpen(false)}
                role="menuitem"
                aria-current={location.pathname === link.to ? 'page' : undefined}
              >
                {link.label}
              </Link>
            ))}
            <div className="pt-4 space-y-2 border-t" style={{ borderColor: 'rgba(251, 191, 36, 0.08)' }}>
              <FocusModeToggle />
              <Link to="/login" className="block glass-btn text-sm text-center w-full" onClick={() => setIsOpen(false)}>
                Sign In
              </Link>
              <Link to="/register" className="block glass-btn-primary text-sm text-center w-full" onClick={() => setIsOpen(false)}>
                Get Started
              </Link>
            </div>
          </div>
        </div>
      )}
    </nav>
  )
}
