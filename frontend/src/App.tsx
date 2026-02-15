/**
 * AUDREY EVANS OFFICIAL — Main Application
 * All 8 mandatory standards enforced at the root level.
 */
import { Routes, Route } from 'react-router-dom'
import { Suspense, lazy } from 'react'
import { NotificationProvider } from './components/notifications/VisualNotification'
import { BreakReminder } from './components/neurodivergent/FocusMode'
import Layout from './components/layout/Layout'

// Lazy-load pages for eco-efficiency (Standard 2: minimize initial bundle)
const LandingPage = lazy(() => import('./pages/LandingPage'))
const LoginPage = lazy(() => import('./pages/LoginPage'))
const RegisterPage = lazy(() => import('./pages/RegisterPage'))
const DashboardPage = lazy(() => import('./pages/DashboardPage'))
const SkinAnalysisPage = lazy(() => import('./pages/SkinAnalysisPage'))
const ClinicalTrialsPage = lazy(() => import('./pages/ClinicalTrialsPage'))
const ProceduresPage = lazy(() => import('./pages/ProceduresPage'))
const MedicalTourismPage = lazy(() => import('./pages/MedicalTourismPage'))
const DataRouterPage = lazy(() => import('./pages/DataRouterPage'))
const BenchmarkPage = lazy(() => import('./pages/BenchmarkPage'))
const SellingSpacePage = lazy(() => import('./pages/SellingSpacePage'))
const AdminPage = lazy(() => import('./pages/AdminPage'))
const SettingsPage = lazy(() => import('./pages/SettingsPage'))
const PricingPage = lazy(() => import('./pages/PricingPage'))
const NotFoundPage = lazy(() => import('./pages/NotFoundPage'))

function LoadingFallback() {
  return (
    <div className="flex items-center justify-center min-h-[60vh]" role="status" aria-label="Loading page">
      <div className="glass-card text-center p-8">
        <div className="w-12 h-12 mx-auto mb-4 rounded-full border-2 border-amber-500/30 border-t-amber-500 animate-spin" aria-hidden="true" />
        <p className="text-secondary-brand text-sm">Loading...</p>
      </div>
    </div>
  )
}

export default function App() {
  return (
    <NotificationProvider>
      {/* Standard 7: Skip to content for keyboard navigation */}
      <a href="#main-content" className="skip-to-content">
        Skip to main content
      </a>

      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={
            <Suspense fallback={<LoadingFallback />}><LandingPage /></Suspense>
          } />
          <Route path="login" element={
            <Suspense fallback={<LoadingFallback />}><LoginPage /></Suspense>
          } />
          <Route path="register" element={
            <Suspense fallback={<LoadingFallback />}><RegisterPage /></Suspense>
          } />
          <Route path="dashboard" element={
            <Suspense fallback={<LoadingFallback />}><DashboardPage /></Suspense>
          } />
          <Route path="analyze" element={
            <Suspense fallback={<LoadingFallback />}><SkinAnalysisPage /></Suspense>
          } />
          <Route path="clinical-trials" element={
            <Suspense fallback={<LoadingFallback />}><ClinicalTrialsPage /></Suspense>
          } />
          <Route path="procedures" element={
            <Suspense fallback={<LoadingFallback />}><ProceduresPage /></Suspense>
          } />
          <Route path="medical-tourism" element={
            <Suspense fallback={<LoadingFallback />}><MedicalTourismPage /></Suspense>
          } />
          <Route path="pricing" element={
            <Suspense fallback={<LoadingFallback />}><PricingPage /></Suspense>
          } />
          <Route path="data-router" element={
            <Suspense fallback={<LoadingFallback />}><DataRouterPage /></Suspense>
          } />
          <Route path="benchmark" element={
            <Suspense fallback={<LoadingFallback />}><BenchmarkPage /></Suspense>
          } />
          <Route path="selling-space" element={
            <Suspense fallback={<LoadingFallback />}><SellingSpacePage /></Suspense>
          } />
          <Route path="admin" element={
            <Suspense fallback={<LoadingFallback />}><AdminPage /></Suspense>
          } />
          <Route path="settings" element={
            <Suspense fallback={<LoadingFallback />}><SettingsPage /></Suspense>
          } />
          <Route path="*" element={
            <Suspense fallback={<LoadingFallback />}><NotFoundPage /></Suspense>
          } />
        </Route>
      </Routes>

      {/* Standard 3: Neurodivergent break reminder (visual only, no audio) */}
      <BreakReminder intervalMinutes={25} />

      {/* Standard 3: Focus mode overlay */}
      <div className="focus-overlay" aria-hidden="true" />
    </NotificationProvider>
  )
}
