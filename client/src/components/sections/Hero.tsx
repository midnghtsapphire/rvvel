/*
 * Design: Earth & Canopy — Grounded Glassmorphism
 * Hero section with Audrey's smoky stage photo, name, tagline, and brief intro.
 * Earthy warm tones: deep reds, forest greens, gold accents.
 * NO blue light anywhere. WCAG AAA accessible.
 */
import { ChevronDown } from "lucide-react";

const PRIMARY_PHOTO = "/hero-audrey.png";

export default function Hero() {
  return (
    <section
      id="hero"
      aria-label="Introduction"
      className="relative min-h-screen flex items-center overflow-hidden"
    >
      {/* Full-bleed background image with warm overlay */}
      <div className="absolute inset-0 z-0">
        <img
          src={PRIMARY_PHOTO}
          alt="Audrey Evans — blonde curly hair, red shirt, jeans, sitting in a tree outdoors with natural lighting"
          className="w-full h-full object-cover object-top"
          loading="eager"
        />
        {/* Warm dark overlay — eliminates blue light from the stage photo */}
        <div
          className="absolute inset-0"
          style={{
            background: "linear-gradient(180deg, rgba(26,21,16,0.45) 0%, rgba(26,21,16,0.25) 35%, rgba(26,21,16,0.55) 70%, rgba(26,21,16,0.92) 100%)",
          }}
        />
        {/* Warm color-correction overlay to shift any cool tones to earthy warmth */}
        <div
          className="absolute inset-0"
          style={{
            background: "linear-gradient(135deg, rgba(185,28,28,0.08) 0%, rgba(217,119,6,0.06) 50%, rgba(22,101,52,0.04) 100%)",
            mixBlendMode: "overlay",
          }}
          aria-hidden="true"
        />
      </div>

      {/* Ambient warm glow — crimson + gold */}
      <div
        className="absolute top-1/3 left-1/2 -translate-x-1/2 w-[800px] h-[800px] rounded-full opacity-20 pointer-events-none z-[1]"
        style={{
          background:
            "radial-gradient(circle, rgba(185, 28, 28, 0.2) 0%, rgba(217, 119, 6, 0.1) 40%, transparent 70%)",
        }}
        aria-hidden="true"
      />

      <div className="container relative z-10 pt-24 pb-16 md:pt-32 md:pb-24">
        <div className="flex flex-col items-center text-center">
          {/* Text Content — centered over the hero image */}
          <div className="max-w-3xl">
            <p
              className="font-medium text-sm md:text-base tracking-widest uppercase mb-3"
              style={{ color: "#d97706" }}
            >
              Welcome
            </p>
            <h1 className="font-serif text-5xl md:text-6xl lg:text-7xl xl:text-8xl text-warm-50 leading-tight mb-4 drop-shadow-lg">
              Audrey Evans
            </h1>
            <p
              className="text-xl md:text-2xl lg:text-3xl font-medium mb-6 drop-shadow-md"
              style={{ color: "#dc2626" }}
            >
              Inventor. Engineer. Advocate. Musician.
            </p>
            <p className="text-warm-200 text-base md:text-lg leading-relaxed mb-8 max-w-xl mx-auto drop-shadow-sm">
              Proud Native Hawaiian with 30+ years in information technology — from software engineering
              and database architecture to project management and invention. Published author, published
              musician, paralegal, CLE instructor, and founder of Freedom Angel Corps.
            </p>
            <div className="flex flex-wrap gap-3 justify-center">
              <a
                href="#about"
                onClick={(e) => {
                  e.preventDefault();
                  document.querySelector("#about")?.scrollIntoView({ behavior: "smooth" });
                }}
                className="inline-flex items-center px-6 py-3 rounded-lg font-semibold text-sm transition-colors duration-200 shadow-lg"
                style={{
                  backgroundColor: "#b91c1c",
                  color: "#fef2f2",
                  boxShadow: "0 4px 14px rgba(185, 28, 28, 0.3)",
                }}
                onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#dc2626")}
                onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "#b91c1c")}
              >
                Learn More
              </a>
              <a
                href="#contact"
                onClick={(e) => {
                  e.preventDefault();
                  document.querySelector("#contact")?.scrollIntoView({ behavior: "smooth" });
                }}
                className="inline-flex items-center px-6 py-3 rounded-lg font-semibold text-sm transition-colors duration-200"
                style={{
                  backgroundColor: "rgba(255,255,255,0.1)",
                  backdropFilter: "blur(12px)",
                  border: "1px solid rgba(255,255,255,0.15)",
                  color: "#f5ede4",
                }}
                onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "rgba(255,255,255,0.18)")}
                onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "rgba(255,255,255,0.1)")}
              >
                Get in Touch
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 z-10" aria-hidden="true">
        <ChevronDown className="w-6 h-6 animate-bounce" style={{ color: "rgba(217, 119, 6, 0.5)" }} />
      </div>
    </section>
  );
}
