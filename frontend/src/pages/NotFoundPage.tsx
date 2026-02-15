import { Link } from 'react-router-dom'
import { Home, ArrowLeft } from 'lucide-react'

export default function NotFoundPage() {
  return (
    <div className="min-h-[60vh] flex items-center justify-center px-4">
      <div className="glass-card text-center max-w-md">
        <div className="text-6xl font-bold gradient-text mb-4" aria-hidden="true">404</div>
        <h1 className="text-xl font-semibold mb-2">Page Not Found</h1>
        <p className="text-secondary-brand text-sm mb-6">
          The page you are looking for does not exist or has been moved.
        </p>
        <div className="flex items-center justify-center gap-3">
          <button
            onClick={() => window.history.back()}
            className="glass-btn text-sm"
            aria-label="Go back to previous page"
          >
            <ArrowLeft className="w-4 h-4" aria-hidden="true" />
            Go Back
          </button>
          <Link to="/" className="glass-btn-primary text-sm" aria-label="Go to home page">
            <Home className="w-4 h-4" aria-hidden="true" />
            Home
          </Link>
        </div>
      </div>
    </div>
  )
}
