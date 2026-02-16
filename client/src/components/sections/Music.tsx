/*
 * Design: Amber Glass Atelier
 * Music section — Revvel / Hailstorm brand showcase.
 * Music-themed background, warm amber accents, SoundCloud link.
 */
import { useInView } from "@/hooks/useInView";
import { Music2, Headphones, ExternalLink } from "lucide-react";

const MUSIC_BG = "https://private-us-east-1.manuscdn.com/sessionFile/x4BxLyx19pDLdlci38lXjR/sandbox/jdvSFsOCL7DD4VSFYX6xJK-img-3_1771202610000_na1fn_bXVzaWMtYmc.jpg?x-oss-process=image/resize,w_1920,h_1920/format,webp/quality,q_80&Expires=1798761600&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUveDRCeEx5eDE5cERMZGxjaTM4bFhqUi9zYW5kYm94L2pkdlNGc09DTDdERDRWU0ZZWDZ4SkstaW1nLTNfMTc3MTIwMjYxMDAwMF9uYTFmbl9iWFZ6YVdNdFltYy5qcGc~eC1vc3MtcHJvY2Vzcz1pbWFnZS9yZXNpemUsd18xOTIwLGhfMTkyMC9mb3JtYXQsd2VicC9xdWFsaXR5LHFfODAiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=fFf5~H7ctE53BLcuG7u07WhrtsufPrDyFESZUx4YQegDW0foIb-JeTHLnZmV7COAFWVYR3Wv7ET9TjKuPbGdXHEH8~yXELh9qhJ7WwrhfVaggkNO1c-IxhIv0X5N48SzzBcaG8gQ7qPvNiXGRjvWYAs~g8oNw-jIsHayNW1jxA9bQFcn6GhDEU7ZV4Ic3kjHyNaxrmbF6LawcCZ3MHHI1HpfbLQI3dCXE4Hoa8gFsXJQjJ8-BelkFe4maN6RFf4svsFlpz3zLFBh5li5DPyUEahR5sP04vI~B83lVE2Bu9pZKY9NtDhC5CXhVIMn0Rybv7o11~MWBJZvZpDnC6puQg__";
const ORANGE_PHOTO = "https://files.manuscdn.com/user_upload_by_module/session_file/310419663032705003/feDWdXZkdhLhMAVf.jpeg";

export default function MusicSection() {
  const { ref, isVisible } = useInView();

  return (
    <section
      id="music"
      aria-label="Music — Revvel and Hailstorm"
      className="relative py-20 md:py-28 overflow-hidden"
    >
      {/* Background */}
      <div className="absolute inset-0 z-0">
        <img
          src={MUSIC_BG}
          alt=""
          role="presentation"
          className="w-full h-full object-cover opacity-15"
          loading="lazy"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-background via-background/90 to-background" />
      </div>

      <div className="container relative z-10">
        <div ref={ref} className={`fade-in-section ${isVisible ? "visible" : ""}`}>
          {/* Section Header */}
          <div className="mb-12 md:mb-16">
            <p className="text-amber-400 font-medium text-sm tracking-widest uppercase mb-2">
              Music
            </p>
            <h2 className="font-serif text-3xl md:text-4xl lg:text-5xl text-warm-50 mb-4">
              Revvel &amp; Hailstorm
            </h2>
            <div className="gold-line w-24" />
          </div>

          <div className="flex flex-col lg:flex-row gap-10 lg:gap-16 items-center">
            {/* Music Photo */}
            <div className="flex-shrink-0">
              <div className="relative w-56 h-72 md:w-64 md:h-80 rounded-xl overflow-hidden glass-panel-strong shadow-xl shadow-amber-900/15">
                <img
                  src={ORANGE_PHOTO}
                  alt="Audrey Evans in an orange gown — artist portrait for Revvel music brand"
                  className="w-full h-full object-cover object-top"
                  loading="lazy"
                />
              </div>
            </div>

            {/* Music Content */}
            <div className="flex-1 space-y-6">
              <p className="text-warm-200 text-base md:text-lg leading-relaxed">
                As a published musician, Audrey performs and produces under two artist names —
                <strong className="text-amber-400"> Revvel</strong> and
                <strong className="text-amber-400"> Hailstorm</strong>. Her music blends
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
                  className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-amber-500/15 border border-amber-500/25 text-amber-400 font-medium text-sm hover:bg-amber-500/25 transition-all duration-200"
                >
                  <Headphones size={18} aria-hidden="true" />
                  Listen on SoundCloud
                  <ExternalLink size={14} aria-hidden="true" />
                </a>
                <div className="glass-panel px-6 py-3 flex items-center gap-2">
                  <Music2 size={18} className="text-amber-500" aria-hidden="true" />
                  <span className="text-warm-300 text-sm">
                    More platforms coming soon
                  </span>
                </div>
              </div>

              {/* Brand badges */}
              <div className="flex gap-4 pt-2">
                <div className="glass-panel px-4 py-2">
                  <span className="font-serif text-lg text-amber-400">Revvel</span>
                </div>
                <div className="glass-panel px-4 py-2">
                  <span className="font-serif text-lg text-warm-300">Hailstorm</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
