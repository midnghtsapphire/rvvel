/*
 * Design: Earth & Canopy — Grounded Glassmorphism
 * Home page — single-page hub assembling all sections.
 * Warm earthy dark theme: deep reds, forest greens, gold accents. No blue anywhere.
 * WCAG AAA accessible, neurodivergent-friendly, carbon-efficient.
 */
import Navbar from "@/components/Navbar";
import Hero from "@/components/sections/Hero";
import About from "@/components/sections/About";
import Resume from "@/components/sections/Resume";
import Portfolio from "@/components/sections/Portfolio";
import MusicSection from "@/components/sections/Music";
import Advocacy from "@/components/sections/Advocacy";
import Contact from "@/components/sections/Contact";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Skip to main content link for screen readers */}
      <a
        href="#main-content"
        className="skip-link font-semibold text-sm rounded-b-md"
        style={{ backgroundColor: "#b91c1c", color: "#fef2f2" }}
      >
        Skip to main content
      </a>

      <Navbar />

      <main id="main-content" role="main">
        <Hero />

        {/* Earth divider — red to green gradient */}
        <div className="earth-line" aria-hidden="true" />

        <About />

        <div className="earth-line" aria-hidden="true" />

        <Resume />

        <div className="earth-line" aria-hidden="true" />

        <Portfolio />

        <div className="earth-line" aria-hidden="true" />

        <MusicSection />

        <div className="earth-line" aria-hidden="true" />

        <Advocacy />

        <div className="earth-line" aria-hidden="true" />

        <Contact />
      </main>

      <Footer />
    </div>
  );
}
