/**
 * Layout — wraps all pages with Navbar, Footer, and mandatory standards.
 * Includes: Carbon badge (Standard 8), Focus mode (Standard 3), Attribution footer.
 */
import { Outlet } from 'react-router-dom'
import Navbar from './Navbar'
import Footer from './Footer'
import CarbonBadge from '../eco/CarbonBadge'

export default function Layout() {
  return (
    <div className="min-h-screen flex flex-col relative">
      {/* Ambient glow effects (GPU-composited, eco-efficient) */}
      <div className="ambient-glow fixed top-[-20%] right-[-10%] w-[600px] h-[600px] opacity-30" aria-hidden="true" />
      <div className="ambient-glow fixed bottom-[-20%] left-[-10%] w-[500px] h-[500px] opacity-20" aria-hidden="true" />

      <Navbar />

      <main id="main-content" className="flex-1 relative z-10 pt-16" role="main" tabIndex={-1}>
        <Outlet />
      </main>

      {/* Standard 8: Carbon savings badge — always visible */}
      <div className="fixed bottom-4 left-4 z-40">
        <CarbonBadge apiCallsSaved={42} cachedResponses={28} />
      </div>

      <Footer />
    </div>
  )
}
