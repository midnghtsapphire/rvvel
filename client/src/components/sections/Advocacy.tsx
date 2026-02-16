/*
 * Design: Earth & Canopy
 * Advocacy section — Freedom Angel Corps, trafficking awareness, recovery coaching.
 * Gold/amber accents for warmth and hope. Forest green for growth. NO blue light.
 */
import { useInView } from "@/hooks/useInView";
import { Heart, Shield, Users, HandHeart } from "lucide-react";

const PRIMARY_PHOTO = "https://files.manuscdn.com/user_upload_by_module/session_file/310419663032705003/GrSpBEVXdxZidAEe.png";

const pillars = [
  {
    icon: Shield,
    title: "Trafficking Awareness",
    description:
      "Certified through Sarah's House and CSPD in Sex Trafficking 101 & 102. Dedicated to raising awareness and supporting survivors through education and direct action.",
    color: "#dc2626",
    bg: "rgba(185, 28, 28, 0.12)",
  },
  {
    icon: HandHeart,
    title: "Recovery Coaching",
    description:
      "CCAR Recovery Coach Academy graduate with ethical training. Currently pursuing Recovery Coach Professional, Family Peer Support Specialist, and Certified Addiction Technician certifications.",
    color: "#22c55e",
    bg: "rgba(22, 101, 52, 0.12)",
  },
  {
    icon: Users,
    title: "Peer Support",
    description:
      "Over 20 years of volunteer service spanning animal rescue, veterans' support, children's advocacy, domestic violence intervention, and homelessness outreach.",
    color: "#d97706",
    bg: "rgba(217, 119, 6, 0.12)",
  },
  {
    icon: Heart,
    title: "Retraining & Restoration",
    description:
      "Freedom Angel Corps retrains trafficking survivors with real-world skills in technology, business, and self-sufficiency — because the mission is to restore, never to terminate.",
    color: "#dc2626",
    bg: "rgba(185, 28, 28, 0.12)",
  },
];

export default function Advocacy() {
  const { ref, isVisible } = useInView();

  return (
    <section
      id="advocacy"
      aria-label="Advocacy and community work"
      className="relative py-20 md:py-28 overflow-hidden"
    >
      {/* Background — subtle warm glow */}
      <div className="absolute inset-0 z-0">
        <div
          className="w-full h-full opacity-[0.04]"
          style={{
            background:
              "radial-gradient(ellipse at 60% 40%, rgba(217, 119, 6, 0.4) 0%, transparent 60%), radial-gradient(ellipse at 30% 70%, rgba(22, 101, 52, 0.3) 0%, transparent 50%)",
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
              style={{ color: "#d97706" }}
            >
              Advocacy
            </p>
            <h2 className="font-serif text-3xl md:text-4xl lg:text-5xl text-warm-50 mb-4">
              Freedom Angel Corps
            </h2>
            <div className="gold-line w-24" />
          </div>

          <div className="flex flex-col lg:flex-row gap-10 lg:gap-16 items-start">
            {/* Content */}
            <div className="flex-1 space-y-6">
              <div
                className="glass-panel-strong p-6 md:p-8"
                style={{ borderColor: "rgba(217, 119, 6, 0.2)" }}
              >
                <blockquote className="text-warm-100 text-lg md:text-xl font-serif italic leading-relaxed">
                  "Rescue, retrain, reinvent &amp; restore — do not terminate."
                </blockquote>
                <p
                  className="text-sm mt-3 font-medium"
                  style={{ color: "rgba(217, 119, 6, 0.8)" }}
                >
                  — Audrey Evans, Founder
                </p>
              </div>

              <p className="text-warm-200 text-base md:text-lg leading-relaxed">
                Freedom Angel Corps is a Colorado nonprofit (EIN on file, CO Secretary of State
                good standing since 2018/2019) founded by Audrey Evans to retrain trafficking
                victims and provide them with pathways to independence and self-sufficiency.
              </p>
              <p className="text-warm-300 text-base md:text-lg leading-relaxed">
                As a trafficking survivor advocate, CLE instructor for the Colorado Supreme Court
                and Orange County DA Criminal Division, and Narconon graduate, Audrey brings both
                lived experience and professional expertise to the fight against human trafficking.
              </p>

              {/* Pillars Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4">
                {pillars.map((pillar) => {
                  const Icon = pillar.icon;
                  return (
                    <div key={pillar.title} className="glass-panel p-5">
                      <div className="flex items-center gap-3 mb-3">
                        <div
                          className="w-8 h-8 rounded-lg flex items-center justify-center"
                          style={{ backgroundColor: pillar.bg }}
                        >
                          <Icon size={16} style={{ color: pillar.color }} aria-hidden="true" />
                        </div>
                        <h3 className="text-warm-100 font-semibold text-sm md:text-base">
                          {pillar.title}
                        </h3>
                      </div>
                      <p className="text-warm-400 text-sm leading-relaxed">
                        {pillar.description}
                      </p>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Photo — tree photo reused as advocacy image */}
            <div className="flex-shrink-0 w-full lg:w-auto flex justify-center lg:justify-start">
              <div
                className="relative w-56 h-72 md:w-64 md:h-80 rounded-xl overflow-hidden glass-panel shadow-xl"
                style={{ boxShadow: "0 10px 40px rgba(217, 119, 6, 0.1)" }}
              >
                <img
                  src={PRIMARY_PHOTO}
                  alt="Audrey Evans sitting in a tree — representing her grounded advocacy and community leadership"
                  className="w-full h-full object-cover object-center"
                  loading="lazy"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
