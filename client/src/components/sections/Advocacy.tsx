/*
 * Design: Amber Glass Atelier
 * Advocacy section — Freedom Angel Corps, trafficking awareness, recovery coaching.
 * Angel wings background, warm coral/gold accents.
 */
import { useInView } from "@/hooks/useInView";
import { Heart, Shield, Users, HandHeart } from "lucide-react";

const ADVOCACY_BG = "https://private-us-east-1.manuscdn.com/sessionFile/x4BxLyx19pDLdlci38lXjR/sandbox/jdvSFsOCL7DD4VSFYX6xJK-img-2_1771202621000_na1fn_YWR2b2NhY3ktYmc.jpg?x-oss-process=image/resize,w_1920,h_1920/format,webp/quality,q_80&Expires=1798761600&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUveDRCeEx5eDE5cERMZGxjaTM4bFhqUi9zYW5kYm94L2pkdlNGc09DTDdERDRWU0ZZWDZ4SkstaW1nLTJfMTc3MTIwMjYyMTAwMF9uYTFmbl9ZV1IyYjJOaFkza3RZbWMuanBnP3gtb3NzLXByb2Nlc3M9aW1hZ2UvcmVzaXplLHdfMTkyMCxoXzE5MjAvZm9ybWF0LHdlYnAvcXVhbGl0eSxxXzgwIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzk4NzYxNjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=b84BeOLq2txpv3UM-WibRrSAGo-PkCr8~UyIn2n1Oc~JJL7SkGKmBq3JupEc8qvDheY0j~W7WppKR-t5TRR7NzZtCdi9aoaadK8YLlkXfST0PzSKJrrQQndzyUJNAz2ry9wytbpkO~mqDaAUY1YQ4U6Ajcs~2NBaWc1cq1UulFrtelFsE6VYnxoQqAueIzAOuVoA2zw8vHC3-5DzRLcm6k8j~0EwaWkuJZeOb4rWYozIl-P-4wyB0MNf5ElXJeqGbwNvR07D5qjyimy5N~QZXiMgC4WhpVmIORFpmi7npL3bMqfyic8n7~5phmaopL8bnenleJL9nbxIPw5Sf~C0yQ__";
const SILVER_PHOTO = "https://files.manuscdn.com/user_upload_by_module/session_file/310419663032705003/kZfdHngVoRbqbymN.jpeg";

const pillars = [
  {
    icon: Shield,
    title: "Trafficking Awareness",
    description:
      "Certified through Sarah's House and CSPD in Sex Trafficking 101 & 102. Dedicated to raising awareness and supporting survivors through education and direct action.",
  },
  {
    icon: HandHeart,
    title: "Recovery Coaching",
    description:
      "CCAR Recovery Coach Academy graduate with ethical training. Currently pursuing Recovery Coach Professional, Family Peer Support Specialist, and Certified Addiction Technician certifications.",
  },
  {
    icon: Users,
    title: "Peer Support",
    description:
      "Over 20 years of volunteer service spanning animal rescue, veterans' support, children's advocacy, domestic violence intervention, and homelessness outreach.",
  },
  {
    icon: Heart,
    title: "Retraining & Restoration",
    description:
      "Freedom Angel Corps retrains trafficking survivors with real-world skills in technology, business, and self-sufficiency — because the mission is to restore, never to terminate.",
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
      {/* Background */}
      <div className="absolute inset-0 z-0">
        <img
          src={ADVOCACY_BG}
          alt=""
          role="presentation"
          className="w-full h-full object-cover opacity-10"
          loading="lazy"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-background via-background/95 to-background" />
      </div>

      <div className="container relative z-10">
        <div ref={ref} className={`fade-in-section ${isVisible ? "visible" : ""}`}>
          {/* Section Header */}
          <div className="mb-12 md:mb-16">
            <p className="text-amber-400 font-medium text-sm tracking-widest uppercase mb-2">
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
              <div className="glass-panel-strong p-6 md:p-8">
                <blockquote className="text-warm-100 text-lg md:text-xl font-serif italic leading-relaxed">
                  "Rescue, retrain, reinvent &amp; restore — do not terminate."
                </blockquote>
                <p className="text-amber-400/80 text-sm mt-3 font-medium">
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
                        <div className="w-8 h-8 rounded-lg bg-amber-500/15 flex items-center justify-center">
                          <Icon size={16} className="text-amber-400" aria-hidden="true" />
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

            {/* Photo */}
            <div className="flex-shrink-0 w-full lg:w-auto flex justify-center lg:justify-start">
              <div className="relative w-56 h-72 md:w-64 md:h-80 rounded-xl overflow-hidden glass-panel shadow-xl shadow-amber-900/10">
                <img
                  src={SILVER_PHOTO}
                  alt="Audrey Evans in a silver gown — portrait representing her advocacy and community leadership"
                  className="w-full h-full object-cover object-top"
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
