/*
 * Design: Earth & Canopy
 * Music section — Audrey Evans (solo) + Revvel Hail (band) artist showcase.
 * Crimson/gold accents for the creative/music vibe. NO blue light.
 * Real artist page feel — streams, platforms, embedded player.
 * Spotify embed for album 4LfS8u61VzNgmEOUBgDNn3.
 */
import { useInView } from "@/hooks/useInView";
import { Music2, Headphones, ExternalLink, Disc3, TrendingUp, Mic2 } from "lucide-react";

const MUSIC_PHOTO = "/audrey-stage.png";

export default function MusicSection() {
  const { ref, isVisible } = useInView();

  return (
    <section
      id="music"
      aria-label="Music — Audrey Evans, Revvel, and Hail"
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
            <h2 className="font-serif text-3xl md:text-4xl lg:text-5xl text-warm-50 mb-2">
              Audrey Evans
            </h2>
            <p className="text-warm-300 text-lg md:text-xl mb-4">
              <span style={{ color: "#d97706" }}>#MeetAudreyEvans</span>
              <span className="text-warm-500 mx-2">|</span>
              <span style={{ color: "#dc2626" }}>Revvel Hail</span>
            </p>
            <div className="gold-line w-24" />
          </div>

          <div className="flex flex-col lg:flex-row gap-10 lg:gap-16 items-start">
            {/* Left Column — Photo + Stats */}
            <div className="flex-shrink-0 flex flex-col items-center gap-6">
              {/* Music Photo — purple dress */}
              <div
                className="relative w-56 h-72 md:w-64 md:h-80 rounded-xl overflow-hidden glass-panel-strong shadow-xl"
                style={{ boxShadow: "0 10px 40px rgba(185, 28, 28, 0.15)" }}
              >
                <img
                  src={MUSIC_PHOTO}
                  alt="Audrey Evans on a dramatic smoky stage — blonde curly hair, floral dress, silver boots, bathed in stage lighting"
                  className="w-full h-full object-cover object-top"
                  loading="lazy"
                />
              </div>

              {/* Stream Stats Card */}
              <div
                className="glass-panel p-4 w-56 md:w-64 text-center"
                style={{
                  borderColor: "rgba(217, 119, 6, 0.25)",
                  background: "rgba(217, 119, 6, 0.06)",
                }}
              >
                <div className="flex items-center justify-center gap-2 mb-2">
                  <TrendingUp size={16} style={{ color: "#d97706" }} aria-hidden="true" />
                  <span className="text-warm-300 text-xs font-medium uppercase tracking-wider">
                    Streams
                  </span>
                </div>
                <div className="font-serif text-2xl md:text-3xl" style={{ color: "#d97706" }}>
                  476+
                </div>
                <p className="text-warm-400 text-xs mt-1">
                  with zero promotion
                </p>
              </div>

              {/* Artist Name Badges */}
              <div className="flex flex-col gap-3 w-56 md:w-64">
                <div
                  className="glass-panel px-4 py-3 text-center"
                  style={{ borderColor: "rgba(185, 28, 28, 0.2)" }}
                >
                  <div className="flex items-center justify-center gap-2">
                    <Mic2 size={14} style={{ color: "#dc2626" }} aria-hidden="true" />
                    <span className="text-warm-400 text-xs uppercase tracking-wider">Solo</span>
                  </div>
                  <span className="font-serif text-lg" style={{ color: "#dc2626" }}>
                    Audrey Evans
                  </span>
                </div>
                <div
                  className="glass-panel px-4 py-3 text-center"
                  style={{ borderColor: "rgba(217, 119, 6, 0.2)" }}
                >
                  <div className="flex items-center justify-center gap-2">
                    <Music2 size={14} style={{ color: "#d97706" }} aria-hidden="true" />
                    <span className="text-warm-400 text-xs uppercase tracking-wider">Band</span>
                  </div>
                  <span className="font-serif text-lg" style={{ color: "#d97706" }}>
                    Revvel Hail
                  </span>
                </div>
              </div>
            </div>

            {/* Right Column — Bio, Embed, Links */}
            <div className="flex-1 space-y-6">
              <p className="text-warm-200 text-base md:text-lg leading-relaxed">
                As a published musician, Audrey performs and produces under multiple artist names —
                solo as <strong style={{ color: "#dc2626" }}>Audrey Evans</strong>{" "}
                (<span style={{ color: "#d97706" }}>#MeetAudreyEvans</span>), and with her band project{" "}
                <strong style={{ color: "#d97706" }}>Revvel Hail</strong>. Her music blends
                personal storytelling with powerful production, drawing from her life experiences
                as an inventor, advocate, and survivor.
              </p>
              <p className="text-warm-300 text-base md:text-lg leading-relaxed">
                Music is both a creative outlet and a healing practice. Through her art, Audrey
                channels the resilience and determination that define her professional and personal
                journey into sound. With 476+ streams and zero promotion, the music speaks for itself.
              </p>

              {/* Spotify Embedded Player */}
              <div className="pt-2">
                <div className="flex items-center gap-2 mb-3">
                  <Disc3 size={18} style={{ color: "#22c55e" }} aria-hidden="true" />
                  <span className="text-warm-200 text-sm font-medium">Now Streaming</span>
                </div>
                <div
                  className="rounded-xl overflow-hidden glass-panel"
                  style={{
                    borderColor: "rgba(34, 197, 94, 0.15)",
                    padding: "2px",
                  }}
                >
                  <iframe
                    style={{ borderRadius: "12px" }}
                    src="https://open.spotify.com/embed/album/4LfS8u61VzNgmEOUBgDNn3?utm_source=generator&theme=0"
                    width="100%"
                    height="352"
                    frameBorder="0"
                    allowFullScreen
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                    loading="lazy"
                    title="Audrey Evans on Spotify"
                  />
                </div>
              </div>

              {/* Platform Links */}
              <div className="flex flex-col sm:flex-row flex-wrap gap-3 pt-4">
                <a
                  href="https://open.spotify.com/album/4LfS8u61VzNgmEOUBgDNn3"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-5 py-3 rounded-lg font-medium text-sm transition-all duration-200 hover:scale-[1.02]"
                  style={{
                    backgroundColor: "rgba(22, 101, 52, 0.15)",
                    border: "1px solid rgba(22, 101, 52, 0.25)",
                    color: "#22c55e",
                  }}
                >
                  <Disc3 size={18} aria-hidden="true" />
                  Spotify
                  <ExternalLink size={14} aria-hidden="true" />
                </a>
                <a
                  href="https://music.apple.com/us/artist/audrey-evans"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-5 py-3 rounded-lg font-medium text-sm transition-all duration-200 hover:scale-[1.02]"
                  style={{
                    backgroundColor: "rgba(185, 28, 28, 0.15)",
                    border: "1px solid rgba(185, 28, 28, 0.25)",
                    color: "#dc2626",
                  }}
                >
                  <Music2 size={18} aria-hidden="true" />
                  Apple Music
                  <ExternalLink size={14} aria-hidden="true" />
                </a>
                <a
                  href="https://artists.landr.com/057914347707"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-5 py-3 rounded-lg font-medium text-sm transition-all duration-200 hover:scale-[1.02]"
                  style={{
                    backgroundColor: "rgba(217, 119, 6, 0.15)",
                    border: "1px solid rgba(217, 119, 6, 0.25)",
                    color: "#d97706",
                  }}
                >
                  <Music2 size={18} aria-hidden="true" />
                  LANDR
                  <ExternalLink size={14} aria-hidden="true" />
                </a>
                <a
                  href="https://soundcloud.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-5 py-3 rounded-lg font-medium text-sm transition-all duration-200 hover:scale-[1.02]"
                  style={{
                    backgroundColor: "rgba(185, 28, 28, 0.15)",
                    border: "1px solid rgba(185, 28, 28, 0.25)",
                    color: "#dc2626",
                  }}
                >
                  <Headphones size={18} aria-hidden="true" />
                  SoundCloud
                  <ExternalLink size={14} aria-hidden="true" />
                </a>
              </div>

              {/* LANDR Release Note */}
              <div
                className="glass-panel px-5 py-3 inline-flex items-center gap-3"
                style={{
                  borderColor: "rgba(217, 119, 6, 0.2)",
                  background: "rgba(217, 119, 6, 0.05)",
                }}
              >
                <TrendingUp size={16} style={{ color: "#d97706" }} aria-hidden="true" />
                <span className="text-warm-300 text-sm">
                  <strong style={{ color: "#d97706" }}>476+ streams</strong> with zero promotion —
                  available on{" "}
                  <a
                    href="https://artists.landr.com/057914347707"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="underline underline-offset-2 transition-colors"
                    style={{ color: "#d97706" }}
                  >
                    LANDR
                  </a>
                  , Spotify, Apple Music, SoundCloud, and more.
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
