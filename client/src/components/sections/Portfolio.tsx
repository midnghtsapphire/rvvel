/*
 * Design: Amber Glass Atelier
 * Portfolio section — glass cards for each app in the ecosystem.
 * Tech pattern background, warm amber accents. Placeholder links for now.
 */
import { useInView } from "@/hooks/useInView";
import { ExternalLink, Sparkles, FileText, Router, Mail, BarChart3 } from "lucide-react";
import { toast } from "sonner";

const TECH_BG = "https://private-us-east-1.manuscdn.com/sessionFile/x4BxLyx19pDLdlci38lXjR/sandbox/jdvSFsOCL7DD4VSFYX6xJK-img-4_1771202609000_na1fn_dGVjaC1wYXR0ZXJu.jpg?x-oss-process=image/resize,w_1920,h_1920/format,webp/quality,q_80&Expires=1798761600&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUveDRCeEx5eDE5cERMZGxjaTM4bFhqUi9zYW5kYm94L2pkdlNGc09DTDdERDRWU0ZZWDZ4SkstaW1nLTRfMTc3MTIwMjYwOTAwMF9uYTFmbl9kR1ZqYUMxd1lYUjBaWEp1LmpwZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSx3XzE5MjAsaF8xOTIwL2Zvcm1hdCx3ZWJwL3F1YWxpdHkscV84MCIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=GRT5nIq8A9pF7jdZ52FNzpBJD0DXJ2rbZTV41Exx-DnisDMhIjLNV~V5tgzlyeTs9YfMESpLNUFHHNdGhtGtzLj4aC0agTzoUXuLi1sb6HP3LPsHe-Lte4PFBN20hUtfBkj~wUKq1UT8O0WtPj3M2q1JEtpZICNmFD-DnWtJfTctH3f7ZKfwvaekS6yGO-GO5Zgp8IqfQxy1IlRdRlpPi-Eyfai7tPYU42v10hd270gweRbKlRS2l-sAhyJdwbQpogz8MDcHJ3rTYZ3gPQj6W-v2FyGS-qs0hJukXNt-90N5~IlZZi4rY5hDup39WZpq0F0CZD9WiOxmcEgvRTWM-w__";

const apps = [
  {
    name: "Project Face",
    description: "AI-powered skin analysis application using computer vision to provide personalized skincare insights and recommendations.",
    icon: Sparkles,
    status: "In Development",
    tags: ["AI", "Computer Vision", "Healthcare"],
  },
  {
    name: "TheAltText",
    description: "Automated alt text generator that makes images accessible for screen readers, powered by AI image recognition.",
    icon: FileText,
    status: "In Development",
    tags: ["Accessibility", "AI", "Web Tools"],
  },
  {
    name: "Universal Data Router",
    description: "Multi-source file organizer that intelligently routes, categorizes, and manages data across different platforms and formats.",
    icon: Router,
    status: "In Development",
    tags: ["Data", "Automation", "Productivity"],
  },
  {
    name: "Revvel Email Organizer",
    description: "AI-powered email categorization system that brings order to chaotic inboxes with smart filtering and priority management.",
    icon: Mail,
    status: "In Development",
    tags: ["AI", "Email", "Productivity"],
  },
  {
    name: "AI Benchmarking Tool",
    description: "Comprehensive benchmarking suite for evaluating and comparing AI model performance across standardized metrics.",
    icon: BarChart3,
    status: "In Development",
    tags: ["AI", "Analytics", "Research"],
  },
];

export default function Portfolio() {
  const { ref, isVisible } = useInView();

  const handleAppClick = (appName: string) => {
    toast(`${appName} — Standalone deployment coming soon.`);
  };

  return (
    <section
      id="portfolio"
      aria-label="Portfolio and applications"
      className="relative py-20 md:py-28 overflow-hidden"
    >
      {/* Background */}
      <div className="absolute inset-0 z-0">
        <img
          src={TECH_BG}
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
              Portfolio
            </p>
            <h2 className="font-serif text-3xl md:text-4xl lg:text-5xl text-warm-50 mb-4">
              Apps &amp; Innovations
            </h2>
            <p className="text-warm-400 text-base md:text-lg max-w-2xl">
              Each application is being developed as a standalone product under the GlowStar Labs
              ecosystem. Click any card to learn more as they launch.
            </p>
            <div className="gold-line w-24 mt-4" />
          </div>

          {/* App Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {apps.map((app) => {
              const Icon = app.icon;
              return (
                <button
                  key={app.name}
                  onClick={() => handleAppClick(app.name)}
                  className="glass-panel p-6 text-left group hover:bg-white/[0.08] transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-amber-900/10"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="w-10 h-10 rounded-lg bg-amber-500/15 flex items-center justify-center">
                      <Icon size={20} className="text-amber-400" aria-hidden="true" />
                    </div>
                    <ExternalLink
                      size={16}
                      className="text-warm-600 group-hover:text-amber-400 transition-colors"
                      aria-hidden="true"
                    />
                  </div>
                  <h3 className="text-warm-100 font-semibold text-lg mb-2">
                    {app.name}
                  </h3>
                  <p className="text-warm-400 text-sm leading-relaxed mb-4">
                    {app.description}
                  </p>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {app.tags.map((tag) => (
                      <span
                        key={tag}
                        className="px-2 py-1 text-xs text-amber-400/80 bg-amber-500/10 rounded"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  <span className="inline-flex items-center gap-1.5 text-xs font-medium text-warm-500">
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-500/60" aria-hidden="true" />
                    {app.status}
                  </span>
                </button>
              );
            })}
          </div>

          {/* GitHub Link */}
          <div className="mt-10 text-center">
            <a
              href="https://github.com/MIDNGHTSAPPHIRE"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-5 py-2.5 glass-panel text-warm-300 hover:text-amber-400 hover:bg-white/[0.08] transition-all duration-200 text-sm font-medium"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
              </svg>
              View All Projects on GitHub
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
