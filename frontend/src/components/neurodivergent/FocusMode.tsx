/**
 * STANDARD 3: NEURODIVERGENT-FRIENDLY — AuDHD-Optimized UX
 *
 * Focus Mode: Reduces stimulation, disables animations, narrows viewport focus.
 * Break Reminder: Gentle visual nudge to take breaks (no audio).
 * Progress Tracker: Dopamine-friendly progress with achievement badges.
 * Executive Function Support: Clear next steps, no decision paralysis.
 */
import { useState, useEffect, useCallback } from 'react'
import { Eye, EyeOff, Coffee, Trophy, ChevronRight, Timer, Sun, Moon, Type, Maximize2, Minimize2 } from 'lucide-react'

// ============================================================
// Focus Mode Toggle
// ============================================================
export function FocusModeToggle() {
  const [focusMode, setFocusMode] = useState(() =>
    document.documentElement.getAttribute('data-mode') === 'focus'
  )

  const toggle = useCallback(() => {
    const next = !focusMode
    setFocusMode(next)
    document.documentElement.setAttribute('data-mode', next ? 'focus' : 'default')
    localStorage.setItem('ae-focus-mode', next ? 'on' : 'off')
  }, [focusMode])

  useEffect(() => {
    const saved = localStorage.getItem('ae-focus-mode')
    if (saved === 'on') {
      setFocusMode(true)
      document.documentElement.setAttribute('data-mode', 'focus')
    }
  }, [])

  return (
    <button
      onClick={toggle}
      className="glass-btn text-sm"
      aria-label={focusMode ? 'Disable focus mode' : 'Enable focus mode — reduces animations and visual noise'}
      aria-pressed={focusMode}
    >
      {focusMode ? <EyeOff className="w-4 h-4" aria-hidden="true" /> : <Eye className="w-4 h-4" aria-hidden="true" />}
      {focusMode ? 'Focus: ON' : 'Focus Mode'}
    </button>
  )
}

// ============================================================
// Break Reminder (visual only, no audio)
// ============================================================
export function BreakReminder({ intervalMinutes = 25 }: { intervalMinutes?: number }) {
  const [showReminder, setShowReminder] = useState(false)
  const [minutesWorked, setMinutesWorked] = useState(0)

  useEffect(() => {
    const timer = setInterval(() => {
      setMinutesWorked(prev => {
        const next = prev + 1
        if (next >= intervalMinutes) {
          setShowReminder(true)
          return 0
        }
        return next
      })
    }, 60000) // Every minute
    return () => clearInterval(timer)
  }, [intervalMinutes])

  if (!showReminder) return null

  return (
    <div
      className="break-reminder"
      role="alert"
      aria-live="polite"
      aria-label="Break reminder"
    >
      <div className="flex items-start gap-3">
        <Coffee className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" aria-hidden="true" />
        <div>
          <p className="font-semibold text-sm">Time for a break</p>
          <p className="text-xs text-secondary-brand mt-1">
            You've been focused for {intervalMinutes} minutes. Stretch, hydrate, or look away from the screen.
          </p>
          <button
            onClick={() => setShowReminder(false)}
            className="mt-2 text-xs text-primary-brand hover:underline"
          >
            Dismiss
          </button>
        </div>
      </div>
    </div>
  )
}

// ============================================================
// Progress Tracker with Achievement Badges (dopamine-friendly)
// ============================================================
interface ProgressStep {
  id: string
  label: string
  completed: boolean
  current?: boolean
}

export function ProgressTracker({ steps, title }: { steps: ProgressStep[]; title: string }) {
  const completed = steps.filter(s => s.completed).length
  const percent = Math.round((completed / steps.length) * 100)

  return (
    <div className="glass-card space-y-4" role="region" aria-label={`Progress: ${title}`}>
      <div className="flex items-center justify-between">
        <h3 className="font-semibold">{title}</h3>
        {percent === 100 && (
          <span className="achievement-badge">
            <Trophy className="w-3 h-3" aria-hidden="true" />
            Complete
          </span>
        )}
      </div>

      {/* Progress Bar */}
      <div>
        <div className="flex justify-between text-xs mb-1">
          <span className="text-secondary-brand">{completed} of {steps.length} steps</span>
          <span className="text-primary-brand font-medium">{percent}%</span>
        </div>
        <div className="progress-bar">
          <div className="progress-bar-fill" style={{ width: `${percent}%` }} />
        </div>
      </div>

      {/* Steps */}
      <ol className="space-y-2" aria-label="Steps">
        {steps.map((step, i) => (
          <li
            key={step.id}
            className={`flex items-center gap-3 text-sm p-2 rounded-lg transition-colors ${
              step.current ? 'bg-amber-500/10 border border-amber-500/20' :
              step.completed ? 'opacity-60' : ''
            }`}
          >
            <span
              className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 ${
                step.completed ? 'bg-green-500/20 text-green-400' :
                step.current ? 'bg-amber-500/20 text-amber-400' :
                'bg-surface-700 text-secondary-brand'
              }`}
              aria-hidden="true"
            >
              {step.completed ? '✓' : i + 1}
            </span>
            <span className={step.completed ? 'line-through' : ''}>{step.label}</span>
            {step.current && (
              <ChevronRight className="w-4 h-4 text-amber-400 ml-auto" aria-hidden="true" />
            )}
          </li>
        ))}
      </ol>
    </div>
  )
}

// ============================================================
// Accessibility Settings Panel
// ============================================================
export function AccessibilityPanel() {
  const [nightMode, setNightMode] = useState(false)
  const [highContrast, setHighContrast] = useState(false)
  const [fontScale, setFontScale] = useState('normal')
  const [density, setDensity] = useState('normal')

  useEffect(() => {
    // Load saved preferences
    const saved = localStorage.getItem('ae-a11y')
    if (saved) {
      try {
        const prefs = JSON.parse(saved)
        if (prefs.nightMode) { setNightMode(true); document.documentElement.setAttribute('data-theme', 'night') }
        if (prefs.highContrast) { setHighContrast(true); document.documentElement.setAttribute('data-mode', 'high-contrast') }
        if (prefs.fontScale) { setFontScale(prefs.fontScale); document.documentElement.setAttribute('data-font-scale', prefs.fontScale) }
      } catch { /* ignore */ }
    }
  }, [])

  const save = (prefs: Record<string, any>) => {
    localStorage.setItem('ae-a11y', JSON.stringify(prefs))
  }

  const toggleNight = () => {
    const next = !nightMode
    setNightMode(next)
    document.documentElement.setAttribute('data-theme', next ? 'night' : 'default')
    save({ nightMode: next, highContrast, fontScale })
  }

  const toggleContrast = () => {
    const next = !highContrast
    setHighContrast(next)
    document.documentElement.setAttribute('data-mode', next ? 'high-contrast' : 'default')
    save({ nightMode, highContrast: next, fontScale })
  }

  const changeFontScale = (scale: string) => {
    setFontScale(scale)
    document.documentElement.setAttribute('data-font-scale', scale)
    save({ nightMode, highContrast, fontScale: scale })
  }

  return (
    <div className="glass-card space-y-4" role="region" aria-label="Accessibility settings">
      <h3 className="font-semibold">Accessibility</h3>

      <div className="space-y-3">
        {/* Night Mode */}
        <button
          onClick={toggleNight}
          className="w-full flex items-center justify-between p-3 rounded-xl hover:bg-white/5 transition-colors"
          aria-pressed={nightMode}
        >
          <div className="flex items-center gap-3">
            {nightMode ? <Moon className="w-5 h-5 text-amber-400" aria-hidden="true" /> : <Sun className="w-5 h-5 text-amber-400" aria-hidden="true" />}
            <div className="text-left">
              <p className="text-sm font-medium">Night Mode</p>
              <p className="text-xs text-secondary-brand">Extra warm, reduced brightness</p>
            </div>
          </div>
          <div className={`w-10 h-6 rounded-full transition-colors ${nightMode ? 'bg-amber-500' : 'bg-surface-600'}`}>
            <div className={`w-4 h-4 rounded-full bg-white mt-1 transition-transform ${nightMode ? 'translate-x-5' : 'translate-x-1'}`} />
          </div>
        </button>

        {/* High Contrast */}
        <button
          onClick={toggleContrast}
          className="w-full flex items-center justify-between p-3 rounded-xl hover:bg-white/5 transition-colors"
          aria-pressed={highContrast}
        >
          <div className="flex items-center gap-3">
            <Maximize2 className="w-5 h-5 text-amber-400" aria-hidden="true" />
            <div className="text-left">
              <p className="text-sm font-medium">High Contrast</p>
              <p className="text-xs text-secondary-brand">Maximum readability</p>
            </div>
          </div>
          <div className={`w-10 h-6 rounded-full transition-colors ${highContrast ? 'bg-amber-500' : 'bg-surface-600'}`}>
            <div className={`w-4 h-4 rounded-full bg-white mt-1 transition-transform ${highContrast ? 'translate-x-5' : 'translate-x-1'}`} />
          </div>
        </button>

        {/* Font Size */}
        <div className="p-3">
          <div className="flex items-center gap-3 mb-3">
            <Type className="w-5 h-5 text-amber-400" aria-hidden="true" />
            <p className="text-sm font-medium">Font Size</p>
          </div>
          <div className="flex gap-2" role="radiogroup" aria-label="Font size">
            {[
              { value: 'small', label: 'S' },
              { value: 'normal', label: 'M' },
              { value: 'large', label: 'L' },
              { value: 'xl', label: 'XL' },
            ].map(opt => (
              <button
                key={opt.value}
                onClick={() => changeFontScale(opt.value)}
                className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors ${
                  fontScale === opt.value ? 'bg-amber-500 text-black' : 'glass-btn'
                }`}
                role="radio"
                aria-checked={fontScale === opt.value}
                aria-label={`Font size ${opt.label}`}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

// ============================================================
// Next Step Prompt (Executive Function Support)
// ============================================================
export function NextStepPrompt({ step, onAction }: { step: string; onAction: () => void }) {
  return (
    <div className="glass-card-glow flex items-center gap-4" role="status" aria-label="Next step">
      <div className="w-10 h-10 rounded-xl bg-amber-500/10 flex items-center justify-center flex-shrink-0">
        <ChevronRight className="w-5 h-5 text-amber-400" aria-hidden="true" />
      </div>
      <div className="flex-1">
        <p className="text-xs text-secondary-brand">Your next step:</p>
        <p className="font-medium">{step}</p>
      </div>
      <button onClick={onAction} className="glass-btn-primary text-sm">
        Do It
      </button>
    </div>
  )
}
