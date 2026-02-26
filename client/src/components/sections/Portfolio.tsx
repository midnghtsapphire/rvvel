/*
 * Design: Earth & Canopy
 * Portfolio section — glass cards for each app in the ecosystem.
 * Forest green accents for tech/innovation. NO blue light.
 * Links: Live deployed apps on droplet; GitHub repo URLs for apps not yet live.
 */
import { useInView } from "@/hooks/useInView";
import { 
  ExternalLink, 
  Sparkles, 
  FileText, 
  Router, 
  Mail, 
  BarChart3, 
  Link as LinkIcon, 
  Dog, 
  Brain,
  Eye,
  Leaf,
  Zap,
  Star,
  Search
} from "lucide-react";

const apps = [
  {
    name: "PawSitting",
    description: "Professional pet sitting and animal care management platform. Streamlining scheduling, client updates, and care tracking for furry friends.",
    icon: Dog,
    status: "Live",
    tags: ["Animal Care", "Management", "Service"],
    liveUrl: "http://164.90.148.7/pawsitting/",
    dividerBefore: true,
  },
  {
    name: "MindMappr",
    description: "Intelligent cognitive mapping and brainstorming tool. Visualize complex ideas and automate workflows through AI-powered node generation.",
    icon: Brain,
    status: "Live",
    tags: ["AI", "Cognitive", "Productivity"],
    liveUrl: "https://github.com/MIDNGHTSAPPHIRE/mindmappr",
  },
  {
    name: "TheAltText",
    description: "Automated alt text generator that makes images accessible for screen readers, powered by AI image recognition.",
    icon: FileText,
    status: "Live",
    tags: ["Accessibility", "AI", "Web Tools"],
    liveUrl: "http://164.90.148.7/thealttext/",
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
    liveUrl: "https://midnghtsapphire.github.io/revvel-email-organizer/",
  },
  {
    name: "Reese Reviews",
    description: "Review aggregation and management platform for tracking and displaying customer reviews across multiple services.",
    icon: Star,
    status: "Live",
    tags: ["Reviews", "Management", "Service"],
    liveUrl: "http://164.90.148.7/reesereviews/",
  },
  {
    name: "Forensic Studio",
    description: "Advanced image analysis and AI-powered forensic reconstruction tool for batch processing and visual analysis.",
    icon: Search,
    status: "In Development",
    tags: ["AI", "Forensics", "Image Analysis"],
    liveUrl: "https://github.com/MIDNGHTSAPPHIRE/revvel-forensic-studio",
  },
  {
    name: "AI Benchmarking Tool",
    description: "Comprehensive benchmarking suite for evaluating and comparing AI model performance across standardized metrics.",
    icon: BarChart3,
    status: "In Development",
    tags: ["AI", "Analytics", "Research"],
    liveUrl: "https://github.com/MIDNGHTSAPPHIRE/ai-benchmarking-tool",
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

const accessibilityModes = [
  {
    name: "Neurodivergent",
    description: "High-contrast, reduced animation, and dyslexia-friendly typography designed for cognitive ease.",
    icon: Brain,
    color: "#d97706",
    bg: "rgba(217, 119, 6, 0.12)",
  },
  {
    name: "ECO CODE",
    description: "Optimized for carbon efficiency with minimal asset loading and dark-mode power savings.",
    icon: Leaf,
    color: "#22c55e",
    bg: "rgba(22, 101, 52, 0.12)",
  },
  {
    name: "No Blue Light",
    description: "Warm-spectrum palette eliminating blue light frequencies to reduce eye strain and support circadian health.",
    icon: Eye,
    color: "#dc2626",
    bg: "rgba(185, 28, 28, 0.12)",
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

          {/* Accessibility Modes Display */}
          <div className="mb-16">
            <h3 className="text-warm-200 font-serif text-2xl mb-6">Priority Accessibility Modes</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {accessibilityModes.map((mode) => {
                const Icon = mode.icon;
                return (
                  <div 
                    key={mode.name}
                    className="glass-panel p-6 flex flex-col gap-3"
                    style={{ borderColor: "rgba(169, 149, 128, 0.1)" }}
                  >
                    <div 
                      className="w-10 h-10 rounded-lg flex items-center justify-center"
                      style={{ backgroundColor: mode.bg }}
                    >
                      <Icon size={20} style={{ color: mode.color }} />
                    </div>
                    <h4 className="text-warm-100 font-semibold">{mode.name}</h4>
                    <p className="text-warm-400 text-sm leading-relaxed">{mode.description}</p>
                  </div>
                );
              })}
            </div>
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
                <div key={app.name} className="contents">
                  {app.dividerBefore && (
                    <div
                      className="col-span-1 md:col-span-2 lg:col-span-3"
                      aria-hidden="true"
                    >
                      <hr
                        style={{
                          border: "none",
                          borderTop: "1px solid rgba(169, 149, 128, 0.18)",
                          margin: "0.25rem 0",
                        }}
                      />
                    </div>
                  )}
                  <a
                    href={app.liveUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="glass-panel p-6 text-left group hover:bg-white/[0.06] transition-all duration-300 hover:-translate-y-1 hover:shadow-lg block"
                    style={{ boxShadow: "0 4px 20px rgba(22, 101, 52, 0.05)" }}
                  >
                    {cardContent}
                  </a>
                </div>
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
