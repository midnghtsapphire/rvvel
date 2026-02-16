/*
 * Design: Earth & Canopy
 * Portfolio section — glass cards for each app in the ecosystem.
 * Forest green accents for tech/innovation. NO blue light.
 * Links point to LIVE GitHub Pages URLs, not repo URLs.
 */
import { useInView } from "@/hooks/useInView";
import { ExternalLink, Sparkles, FileText, Router, Mail, BarChart3, Link as LinkIcon } from "lucide-react";

const apps = [
  {
    name: "TheAltText",
    description: "Automated alt text generator that makes images accessible for screen readers, powered by AI image recognition.",
    icon: FileText,
    status: "Live",
    tags: ["Accessibility", "AI", "Web Tools"],
    liveUrl: "https://midnghtsapphire.github.io/thealttext/",
  },
  {
    name: "Universal Data Router",
    description: "Multi-source file organizer that intelligently routes, categorizes, and manages data across different platforms and formats.",
    icon: Router,
    status: "Live",
    tags: ["Data", "Automation", "Productivity"],
    liveUrl: "https://midnghtsapphire.github.io/universal-data-router/",
  },
  {
    name: "Project Face",
    description: "AI-powered skin analysis application using computer vision to provide personalized skincare insights and recommendations.",
    icon: Sparkles,
    status: "Live",
    tags: ["AI", "Computer Vision", "Healthcare"],
    liveUrl: "https://midnghtsapphire.github.io/project-face/",
  },
  {
    name: "Revvel Email Organizer",
    description: "AI-powered email categorization system that brings order to chaotic inboxes with smart filtering and priority management.",
    icon: Mail,
    status: "Live",
    tags: ["AI", "Email", "Productivity"],
    liveUrl: "https://3000-iu1pleeznhnlol7ibl7vm-16b14045.us2.manus.computer",
  },
  {
    name: "AI Benchmarking Tool",
    description: "Comprehensive benchmarking suite for evaluating and comparing AI model performance across standardized metrics.",
    icon: BarChart3,
    status: "Live",
    tags: ["AI", "Analytics", "Research"],
    liveUrl: "https://midnghtsapphire.github.io/ai-benchmarking-tool/",
  },
  {
    name: "Affiliate Links",
    description: "MCP server for managing and generating affiliate links across platforms, tracking performance and optimizing revenue.",
    icon: LinkIcon,
    status: "In Development",
    tags: ["MCP", "Affiliate", "Revenue"],
    liveUrl: "https://github.com/MIDNGHTSAPPHIRE/rvvel-affiliate-links-mcp",
  },
];

export default function Portfolio() {
  const { ref, isVisible } = useInView();

  return (
    <section
      id="portfolio"
      aria-label="Portfolio and applications"
      className="relative py-20 md:py-28 overflow-hidden"
    >
      {/* Subtle background texture */}
      <div className="absolute inset-0 z-0">
        <div
          className="w-full h-full opacity-[0.03]"
          style={{
            background:
              "radial-gradient(ellipse at 30% 50%, rgba(22, 101, 52, 0.5) 0%, transparent 50%), radial-gradient(ellipse at 70% 50%, rgba(185, 28, 28, 0.3) 0%, transparent 50%)",
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
              style={{ color: "#15803d" }}
            >
              Portfolio
            </p>
            <h2 className="font-serif text-3xl md:text-4xl lg:text-5xl text-warm-50 mb-4">
              Apps &amp; Innovations
            </h2>
            <p className="text-warm-400 text-base md:text-lg max-w-2xl">
              Each application is developed as a standalone product under the GlowStar Labs
              ecosystem. Click any card to view the live application.
            </p>
            <div className="gold-line w-24 mt-4" />
          </div>

          {/* App Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {apps.map((app) => {
              const Icon = app.icon;
              const isLive = app.status === "Live";

              const cardContent = (
                <>
                  <div className="flex items-start justify-between mb-4">
                    <div
                      className="w-10 h-10 rounded-lg flex items-center justify-center"
                      style={{ backgroundColor: "rgba(22, 101, 52, 0.15)" }}
                    >
                      <Icon size={20} style={{ color: "#22c55e" }} aria-hidden="true" />
                    </div>
                    <ExternalLink
                      size={16}
                      className="text-warm-600 group-hover:text-forest-500 transition-colors"
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
                        className="px-2 py-1 text-xs rounded"
                        style={{
                          color: "rgba(34, 197, 94, 0.8)",
                          backgroundColor: "rgba(22, 101, 52, 0.12)",
                        }}
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  <span className="inline-flex items-center gap-1.5 text-xs font-medium text-warm-500">
                    <span
                      className="w-1.5 h-1.5 rounded-full"
                      style={{
                        backgroundColor: isLive
                          ? "rgba(34, 197, 94, 0.9)"
                          : "rgba(217, 119, 6, 0.6)",
                      }}
                      aria-hidden="true"
                    />
                    {app.status}
                  </span>
                </>
              );

              return (
                <a
                  key={app.name}
                  href={app.liveUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="glass-panel p-6 text-left group hover:bg-white/[0.06] transition-all duration-300 hover:-translate-y-1 hover:shadow-lg block"
                  style={{ boxShadow: "0 4px 20px rgba(22, 101, 52, 0.05)" }}
                >
                  {cardContent}
                </a>
              );
            })}
          </div>

          {/* GitHub Link */}
          <div className="mt-10 text-center">
            <a
              href="https://github.com/MIDNGHTSAPPHIRE"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-5 py-2.5 glass-panel text-warm-300 hover:text-forest-400 hover:bg-white/[0.06] transition-all duration-200 text-sm font-medium"
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
