/*
 * Design: Earth & Canopy
 * Music section — Audrey Evans (solo) & Revvel Hail (band) showcase.
 * Crimson/gold accents for the creative/music vibe. NO blue light.
 * Real streaming links, Spotify embed, LANDR distribution info.
 */
import { useInView } from "@/hooks/useInView";
import { Music2, Headphones, ExternalLink, Disc3, Radio, Hash } from "lucide-react";

const MUSIC_PHOTO = "https://files.manuscdn.com/user_upload_by_module/session_file/310419663032705003/UkBAvqxgFYMhSRBc.jpeg";

const streamingPlatforms = [
  {
    name: "Spotify",
    url: "https://open.spotify.com/artist/6WA79rCaJmTjgjwDqwJN1P",
    color: "#22c55e",
    bgColor: "rgba(22, 101, 52, 0.15)",
    borderColor: "rgba(22, 101, 52, 0.25)",
  },
  {
    name: "Apple Music",
    url: "https://music.apple.com/us/artist/audrey-evans/1825732282",
    color: "#dc2626",
    bgColor: "rgba(185, 28, 28, 0.15)",
    borderColor: "rgba(185, 28, 28, 0.25)",
  },
  {
    name: "SoundCloud",
    url: "https://soundcloud.com/audrey-evans-389360721",
    color: "#d97706",
    bgColor: "rgba(217, 119, 6, 0.15)",
    borderColor: "rgba(217, 119, 6, 0.25)",
  },
  {
    name: "LANDR",
    url: "https://artists.landr.com/057914347707",
    color: "#f5ede4",
    bgColor: "rgba(169, 149, 128, 0.12)",
    borderColor: "rgba(169, 149, 128, 0.25)",
  },
];

export default function MusicSection() {
  const { ref, isVisible } = useInView();

  return (
    <section
      id="music"
      aria-label="Music — Audrey Evans and Revvel Hail"
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
              Audrey Evans &amp; Revvel Hail
            </h2>
            <div className="gold-line w-24" />
          </div>

          <div className="flex flex-col lg:flex-row gap-10 lg:gap-16 items-start">
            {/* Music Photo — purple dress */}
            <div className="flex-shrink-0 w-full lg:w-auto flex flex-col items-center lg:items-start gap-4">
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
              {/* Hashtag badge */}
              <div
                className="glass-panel px-4 py-2 flex items-center gap-2"
                style={{ borderColor: "rgba(185, 28, 28, 0.25)" }}
              >
                <Hash size={16} style={{ color: "#dc2626" }} aria-hidden="true" />
                <span className="font-medium text-sm" style={{ color: "#dc2626" }}>
                  MeetAudreyEvans
                </span>
              </div>
            </div>

            {/* Music Content */}
            <div className="flex-1 space-y-6">
              <p className="text-warm-200 text-base md:text-lg leading-relaxed">
                As a published musician, Audrey performs and produces under two artist identities —
                solo as <strong style={{ color: "#dc2626" }}>Audrey Evans</strong> and
                with her band <strong style={{ color: "#d97706" }}>Revvel Hail</strong>. Her music blends
                personal storytelling with powerful production, drawing from her life experiences
                as an inventor, advocate, and survivor.
              </p>
              <p className="text-warm-300 text-base md:text-lg leading-relaxed">
                Music is both a creative outlet and a healing practice. Through her art, Audrey
                channels the resilience and determination that define her professional and personal
                journey into sound. Distributed via{" "}
                <a
                  href="https://artists.landr.com/057914347707"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="underline underline-offset-2 transition-colors"
                  style={{ color: "#d97706" }}
                >
                  LANDR
                </a>{" "}
                to all major platforms, her releases have earned{" "}
                <strong style={{ color: "#22c55e" }}>476+ streams with zero promotion</strong> — pure organic reach.
              </p>

              {/* Artist Identity Badges */}
              <div className="flex flex-wrap gap-4">
                <div
                  className="glass-panel-strong px-5 py-3 flex items-center gap-3"
                  style={{ borderColor: "rgba(185, 28, 28, 0.25)" }}
                >
                  <Disc3 size={20} style={{ color: "#dc2626" }} aria-hidden="true" />
                  <div>
                    <span className="font-serif text-lg block" style={{ color: "#dc2626" }}>Audrey Evans</span>
                    <span className="text-warm-400 text-xs">Solo Artist</span>
                  </div>
                </div>
                <div
                  className="glass-panel-strong px-5 py-3 flex items-center gap-3"
                  style={{ borderColor: "rgba(217, 119, 6, 0.25)" }}
                >
                  <Radio size={20} style={{ color: "#d97706" }} aria-hidden="true" />
                  <div>
                    <span className="font-serif text-lg block" style={{ color: "#d97706" }}>Revvel Hail</span>
                    <span className="text-warm-400 text-xs">Band</span>
                  </div>
                </div>
              </div>

              {/* Spotify Embed */}
              <div className="pt-2">
                <div
                  className="glass-panel-strong rounded-xl overflow-hidden p-1"
                  style={{ borderColor: "rgba(22, 101, 52, 0.2)" }}
                >
                  <iframe
                    style={{ borderRadius: "12px" }}
                    src="https://open.spotify.com/embed/album/4LfS8u61VzNgmEOUBgDNn3?utm_source=generator"
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

              {/* Streaming Platform Links */}
              <div className="pt-2">
                <p className="text-warm-400 text-sm font-medium mb-3 flex items-center gap-2">
                  <Music2 size={16} aria-hidden="true" />
                  Listen on All Major Platforms
                </p>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  {streamingPlatforms.map((platform) => (
                    <a
                      key={platform.name}
                      href={platform.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center justify-center gap-2 px-4 py-3 rounded-lg font-medium text-sm transition-all duration-200 hover:scale-[1.03]"
                      style={{
                        backgroundColor: platform.bgColor,
                        border: `1px solid ${platform.borderColor}`,
                        color: platform.color,
                      }}
                    >
                      <Headphones size={16} aria-hidden="true" />
                      {platform.name}
                      <ExternalLink size={12} aria-hidden="true" />
                    </a>
                  ))}
                </div>
              </div>

              {/* Distribution Note */}
              <div
                className="glass-panel px-5 py-3 flex items-start gap-3"
                style={{
                  borderColor: "rgba(169, 149, 128, 0.2)",
                  background: "rgba(169, 149, 128, 0.05)",
                }}
              >
                <Disc3 size={18} className="mt-0.5 flex-shrink-0" style={{ color: "#d97706" }} aria-hidden="true" />
                <p className="text-warm-400 text-sm leading-relaxed">
                  All music is distributed via{" "}
                  <strong style={{ color: "#d97706" }}>LANDR</strong> to Spotify, Apple Music,
                  Amazon Music, YouTube Music, Deezer, Tidal, and 150+ additional stores and streaming services worldwide.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
