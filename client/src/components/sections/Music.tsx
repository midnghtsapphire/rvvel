/*
 * Design: Earth & Canopy
 * Music section — Revvel / Hailstorm brand showcase.
 * Crimson/gold accents for the creative/music vibe. NO blue light.
 */
import { useInView } from "@/hooks/useInView";
import { Music2, Headphones, ExternalLink } from "lucide-react";

const MUSIC_PHOTO = "https://files.manuscdn.com/user_upload_by_module/session_file/310419663032705003/UkBAvqxgFYMhSRBc.jpeg";

export default function MusicSection() {
  const { ref, isVisible } = useInView();

  return (
    <section
      id="music"
      aria-label="Music — Revvel and Hailstorm"
      className="relative py-20 md:py-28 overflow-hidden"
    >
      {/* Background — subtle warm crimson glow */}
      <div className="absolute inset-0 z-0">
        <div
          className="w-full h-full opacity-[0.04]"
          style={{
            background:
              "radial-gradient(ellipse at 40% 50%, rgba(185, 28, 28, 0.5) 0%, transparent 60%), radial-gradient(ellipse at 70% 70%, rgba(217, 119, 6, 0.3) 0%, transparent 50%)",
          }}
          aria-hidden="true"
        />
      </div>

      <div className="container relative z-10">
        <div ref={ref} className={`fade-in-section ${isVisible ? "visible" : ""}`}>
          {/* Section Header */}
          <div className="mb-12 md:mb-16">
            <p
              className="font-medium text-sm tracking-widest uppercase mb-2"
              style={{ color: "#dc2626" }}
            >
              Music
            </p>
            <h2 className="font-serif text-3xl md:text-4xl lg:text-5xl text-warm-50 mb-4">
              Revvel &amp; Hailstorm
            </h2>
            <div className="gold-line w-24" />
          </div>

          <div className="flex flex-col lg:flex-row gap-10 lg:gap-16 items-center">
            {/* Music Photo — purple dress */}
            <div className="flex-shrink-0">
              <div
                className="relative w-56 h-72 md:w-64 md:h-80 rounded-xl overflow-hidden glass-panel-strong shadow-xl"
                style={{ boxShadow: "0 10px 40px rgba(185, 28, 28, 0.15)" }}
              >
                <img
                  src={MUSIC_PHOTO}
                  alt="Audrey Evans in a purple sequin and satin gown against a mountain sunset — artist portrait for Revvel music brand"
                  className="w-full h-full object-cover object-top"
                  loading="lazy"
                />
              </div>
            </div>

            {/* Music Content */}
            <div className="flex-1 space-y-6">
              <p className="text-warm-200 text-base md:text-lg leading-relaxed">
                As a published musician, Audrey performs and produces under two artist names —
                <strong style={{ color: "#dc2626" }}> Revvel</strong> and
                <strong style={{ color: "#d97706" }}> Hailstorm</strong>. Her music blends
                personal storytelling with powerful production, drawing from her life experiences
                as an inventor, advocate, and survivor.
              </p>
              <p className="text-warm-300 text-base md:text-lg leading-relaxed">
                Music is both a creative outlet and a healing practice. Through her art, Audrey
                channels the resilience and determination that define her professional and personal
                journey into sound.
              </p>

              {/* Music Links */}
              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                <a
                  href="https://soundcloud.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-6 py-3 rounded-lg font-medium text-sm transition-all duration-200"
                  style={{
                    backgroundColor: "rgba(185, 28, 28, 0.15)",
                    border: "1px solid rgba(185, 28, 28, 0.25)",
                    color: "#dc2626",
                  }}
                >
                  <Headphones size={18} aria-hidden="true" />
                  Listen on SoundCloud
                  <ExternalLink size={14} aria-hidden="true" />
                </a>
                <div className="glass-panel px-6 py-3 flex items-center gap-2">
                  <Music2 size={18} style={{ color: "#d97706" }} aria-hidden="true" />
                  <span className="text-warm-300 text-sm">
                    More platforms coming soon
                  </span>
                </div>
              </div>

              {/* Brand badges */}
              <div className="flex gap-4 pt-2">
                <div
                  className="glass-panel px-4 py-2"
                  style={{ borderColor: "rgba(185, 28, 28, 0.2)" }}
                >
                  <span className="font-serif text-lg" style={{ color: "#dc2626" }}>Revvel</span>
                </div>
                <div
                  className="glass-panel px-4 py-2"
                  style={{ borderColor: "rgba(217, 119, 6, 0.2)" }}
                >
                  <span className="font-serif text-lg" style={{ color: "#d97706" }}>Hailstorm</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
