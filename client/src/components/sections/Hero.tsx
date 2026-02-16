/*
 * Design: Amber Glass Atelier
 * Hero section with Audrey's primary photo, name, tagline, and brief intro.
 * Asymmetric layout on desktop, stacked on mobile. Warm amber radial glow behind photo.
 */
import { ChevronDown } from "lucide-react";

const HERO_BG = "https://private-us-east-1.manuscdn.com/sessionFile/x4BxLyx19pDLdlci38lXjR/sandbox/jdvSFsOCL7DD4VSFYX6xJK-img-1_1771202617000_na1fn_aGVyby1iZw.jpg?x-oss-process=image/resize,w_1920,h_1920/format,webp/quality,q_80&Expires=1798761600&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUveDRCeEx5eDE5cERMZGxjaTM4bFhqUi9zYW5kYm94L2pkdlNGc09DTDdERDRWU0ZZWDZ4SkstaW1nLTFfMTc3MTIwMjYxNzAwMF9uYTFmbl9hR1Z5YnkxaVp3LmpwZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSx3XzE5MjAsaF8xOTIwL2Zvcm1hdCx3ZWJwL3F1YWxpdHkscV84MCIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=GN8qwxENJGJUoYkMj9t~agJstllTcJdwLNYpcPPDj~1kYD~9tN4JWp7ZQ4FlMNMVGdAm~Wr5IAz3k1e24x9TbZkqccctIiYeQp2VdQJZ5jl-jCSPcINOf18zatqrkCLbxx7f2EQfk3-8nLobGi~PVazLCXwwRnrWeiIoZvmGinyQ2aKNxTSvzChmuZMzNc-U6XeJKlgEWrfCyRcf6ZCQ-ULj0WpEV1UjazDTq9LcCAJ4ipSbzkK4Y9qM~xpWyfSjVG8iW6KznapOla34o4AfSwHy5GD8O3CERulxU-73IF3Glg5HEyEnCrSl-qJBvJ7FmfHhlQVGR74LM~kKnbMbNw__";
const PRIMARY_PHOTO = "https://files.manuscdn.com/user_upload_by_module/session_file/310419663032705003/ZvzsEkOOmVsTRUpa.jpeg";

export default function Hero() {
  return (
    <section
      id="hero"
      aria-label="Introduction"
      className="relative min-h-screen flex items-center overflow-hidden"
    >
      {/* Background image with overlay */}
      <div className="absolute inset-0 z-0">
        <img
          src={HERO_BG}
          alt=""
          role="presentation"
          className="w-full h-full object-cover opacity-30"
          loading="eager"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-background/80 via-background/60 to-background" />
      </div>

      {/* Ambient warm glow */}
      <div
        className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full opacity-20 pointer-events-none z-0"
        style={{
          background:
            "radial-gradient(circle, rgba(245, 158, 11, 0.3) 0%, rgba(234, 88, 12, 0.1) 50%, transparent 70%)",
        }}
        aria-hidden="true"
      />

      <div className="container relative z-10 pt-24 pb-16 md:pt-32 md:pb-24">
        <div className="flex flex-col lg:flex-row items-center gap-10 lg:gap-16">
          {/* Photo */}
          <div className="relative flex-shrink-0">
            <div className="relative w-64 h-80 md:w-80 md:h-[26rem] lg:w-96 lg:h-[30rem] rounded-2xl overflow-hidden glass-panel-strong shadow-2xl shadow-amber-900/20">
              <img
                src={PRIMARY_PHOTO}
                alt="Audrey Evans — professional portrait in a blue dress against a mountain sunset backdrop"
                className="w-full h-full object-cover object-top"
                loading="eager"
              />
              {/* Warm overlay at bottom for text readability */}
              <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-black/40 to-transparent" />
            </div>
            {/* Decorative amber ring */}
            <div
              className="absolute -inset-3 rounded-2xl border border-amber-500/20 pointer-events-none"
              aria-hidden="true"
            />
          </div>

          {/* Text Content */}
          <div className="text-center lg:text-left max-w-2xl">
            <p className="text-amber-400 font-medium text-sm md:text-base tracking-widest uppercase mb-3">
              Welcome
            </p>
            <h1 className="font-serif text-4xl md:text-5xl lg:text-6xl xl:text-7xl text-warm-50 leading-tight mb-4">
              Audrey Evans
            </h1>
            <p className="text-lg md:text-xl lg:text-2xl text-amber-400/90 font-medium mb-6">
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
                className="inline-flex items-center px-6 py-3 rounded-lg bg-amber-500 text-warm-950 font-semibold text-sm hover:bg-amber-400 transition-colors duration-200 shadow-lg shadow-amber-500/20"
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
        <ChevronDown className="w-6 h-6 text-amber-500/50 animate-bounce" />
      </div>
    </section>
  );
}
