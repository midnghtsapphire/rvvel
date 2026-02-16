/*
 * Design: Earth & Canopy — Grounded Glassmorphism
 * Hero section with Audrey's primary tree photo, name, tagline, and brief intro.
 * Earthy warm tones: deep reds, forest greens, gold accents.
 * NO blue light anywhere. WCAG AAA accessible.
 */
import { ChevronDown } from "lucide-react";

const PRIMARY_PHOTO = "https://files.manuscdn.com/user_upload_by_module/session_file/310419663032705003/GrSpBEVXdxZidAEe.png";

export default function Hero() {
  return (
    <section
      id="hero"
      aria-label="Introduction"
      className="relative min-h-screen flex items-center overflow-hidden"
    >
      {/* Background — warm dark earth with subtle texture */}
      <div className="absolute inset-0 z-0">
        <div
          className="w-full h-full"
          style={{
            background: "linear-gradient(135deg, #1a1510 0%, #231e18 30%, #1a1510 60%, #171310 100%)",
          }}
        />
        {/* Subtle leaf-pattern overlay via radial gradients */}
        <div
          className="absolute inset-0 opacity-[0.04]"
          style={{
            background:
              "radial-gradient(ellipse at 20% 50%, rgba(22, 101, 52, 0.5) 0%, transparent 50%), radial-gradient(ellipse at 80% 30%, rgba(185, 28, 28, 0.3) 0%, transparent 50%), radial-gradient(ellipse at 50% 80%, rgba(217, 119, 6, 0.3) 0%, transparent 50%)",
          }}
          aria-hidden="true"
        />
      </div>

      {/* Ambient warm glow — crimson + gold */}
      <div
        className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[700px] h-[700px] rounded-full opacity-15 pointer-events-none z-0"
        style={{
          background:
            "radial-gradient(circle, rgba(185, 28, 28, 0.25) 0%, rgba(217, 119, 6, 0.12) 40%, rgba(22, 101, 52, 0.06) 65%, transparent 80%)",
        }}
        aria-hidden="true"
      />

      <div className="container relative z-10 pt-24 pb-16 md:pt-32 md:pb-24">
        <div className="flex flex-col lg:flex-row items-center gap-10 lg:gap-16">
          {/* Photo — Audrey in tree */}
          <div className="relative flex-shrink-0">
            <div className="relative w-64 h-80 md:w-80 md:h-[26rem] lg:w-96 lg:h-[30rem] rounded-2xl overflow-hidden glass-panel-strong shadow-2xl shadow-crimson-900/30">
              <img
                src={PRIMARY_PHOTO}
                alt="Audrey Evans in a red top and jeans, sitting in a tree surrounded by green leaves — grounded, natural, and warm"
                className="w-full h-full object-cover object-top"
                loading="eager"
              />
              {/* Warm overlay at bottom for depth */}
              <div className="absolute bottom-0 left-0 right-0 h-28 bg-gradient-to-t from-black/50 via-black/20 to-transparent" />
            </div>
            {/* Decorative ring — crimson/gold gradient border */}
            <div
              className="absolute -inset-3 rounded-2xl pointer-events-none"
              style={{
                border: "1px solid rgba(185, 28, 28, 0.25)",
                boxShadow: "0 0 40px rgba(185, 28, 28, 0.08), 0 0 80px rgba(22, 101, 52, 0.04)",
              }}
              aria-hidden="true"
            />
          </div>

          {/* Text Content */}
          <div className="text-center lg:text-left max-w-2xl">
            <p
              className="font-medium text-sm md:text-base tracking-widest uppercase mb-3"
              style={{ color: "#d97706" }}
            >
              Welcome
            </p>
            <h1 className="font-serif text-4xl md:text-5xl lg:text-6xl xl:text-7xl text-warm-50 leading-tight mb-4">
              Audrey Evans
            </h1>
            <p
              className="text-lg md:text-xl lg:text-2xl font-medium mb-6"
              style={{ color: "#dc2626" }}
            >
              Inventor. Engineer. Advocate. Musician.
            </p>
            <p className="text-warm-300 text-base md:text-lg leading-relaxed mb-8 max-w-xl mx-auto lg:mx-0">
              Proud Native Hawaiian with 30+ years in information technology — from software engineering
              and database architecture to project management and invention. Published author, published
              musician, paralegal, CLE instructor, and founder of Freedom Angel Corps.
            </p>
            <div className="flex flex-wrap gap-3 justify-center lg:justify-start">
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
                className="inline-flex items-center px-6 py-3 rounded-lg glass-panel text-warm-200 font-semibold text-sm hover:bg-white/10 transition-colors duration-200"
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
