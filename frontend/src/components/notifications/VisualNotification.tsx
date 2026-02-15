/**
 * STANDARD 7: VISUAL-ONLY NOTIFICATIONS
 * Audrey's daughter is legally deaf — NO audio-dependent features.
 * All notifications are visual: color-coded, icon-based, with flash indicator.
 */
import { useState, useEffect, createContext, useContext, useCallback } from 'react'
import { CheckCircle, AlertTriangle, XCircle, Info, X } from 'lucide-react'

type NotificationType = 'success' | 'warning' | 'error' | 'info'

interface Notification {
  id: string
  type: NotificationType
  title: string
  message: string
  duration?: number
  persistent?: boolean
}

interface NotificationContextType {
  notify: (n: Omit<Notification, 'id'>) => void
  dismiss: (id: string) => void
}

const NotificationContext = createContext<NotificationContextType>({
  notify: () => {},
  dismiss: () => {},
})

export function useNotification() {
  return useContext(NotificationContext)
}

const icons: Record<NotificationType, typeof CheckCircle> = {
  success: CheckCircle,
  warning: AlertTriangle,
  error: XCircle,
  info: Info,
}

const colors: Record<NotificationType, string> = {
  success: 'text-green-400',
  warning: 'text-amber-400',
  error: 'text-red-400',
  info: 'text-amber-300',
}

export function NotificationProvider({ children }: { children: React.ReactNode }) {
  const [notifications, setNotifications] = useState<Notification[]>([])

  const notify = useCallback((n: Omit<Notification, 'id'>) => {
    const id = `notif-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`
    const notification: Notification = { ...n, id, duration: n.duration ?? 5000 }
    setNotifications(prev => [...prev, notification])

    // Auto-dismiss non-persistent notifications
    if (!n.persistent) {
      setTimeout(() => {
        setNotifications(prev => prev.filter(x => x.id !== id))
      }, notification.duration)
    }
  }, [])

  const dismiss = useCallback((id: string) => {
    setNotifications(prev => prev.filter(x => x.id !== id))
  }, [])

  return (
    <NotificationContext.Provider value={{ notify, dismiss }}>
      {children}
      {/* Notification Container */}
      <div
        className="fixed top-4 right-4 z-50 space-y-3 max-w-sm w-full pointer-events-none"
        role="region"
        aria-label="Notifications"
        aria-live="polite"
        aria-atomic="false"
      >
        {notifications.map(n => {
          const Icon = icons[n.type]
          return (
            <div
              key={n.id}
              className="notification-toast notification-flash pointer-events-auto"
              data-type={n.type}
              role="alert"
              aria-label={`${n.type}: ${n.title}`}
            >
              <div className="flex items-start gap-3">
                <Icon className={`w-5 h-5 flex-shrink-0 mt-0.5 ${colors[n.type]}`} aria-hidden="true" />
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-sm">{n.title}</p>
                  <p className="text-xs text-secondary-brand mt-0.5">{n.message}</p>
                </div>
                <button
                  onClick={() => dismiss(n.id)}
                  className="flex-shrink-0 p-1 rounded hover:bg-white/10 transition-colors"
                  aria-label={`Dismiss notification: ${n.title}`}
                >
                  <X className="w-4 h-4 text-secondary-brand" aria-hidden="true" />
                </button>
              </div>
            </div>
          )
        })}
      </div>
    </NotificationContext.Provider>
  )
}
