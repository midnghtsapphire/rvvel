/*
 * Design: Earth & Canopy — Grounded Glassmorphism
 * Publications section — SSRN research papers with DOIs, metrics, and links.
 * Forest green accents for academic/research. NO blue light.
 * WCAG AAA accessible, neurodivergent-friendly.
 */
import { useInView } from "@/hooks/useInView";
import { BookOpen, ExternalLink, Download, Eye, Share2 } from "lucide-react";

const papers = [
  {
    title: "AI in Criminal Sentencing",
    doi: "10.2139/ssrn.5601452",
    url: "https://doi.org/10.2139/ssrn.5601452",
    downloads: 123,
    views: 316,
    socialShares: 16,
    description:
      "An examination of artificial intelligence applications in criminal sentencing, exploring algorithmic bias, due process implications, and the intersection of technology with justice.",
    accent: "#dc2626",
    bg: "rgba(185, 28, 28, 0.1)",
    border: "rgba(185, 28, 28, 0.25)",
  },
  {
    title: "Government Waste Exceeds Military Budget",
    doi: "10.2139/ssrn.5915102",
    url: "https://doi.org/10.2139/ssrn.5915102",
    downloads: 13,
    views: 94,
    description:
      "A data-driven analysis revealing that government waste and inefficiency surpasses the entire military budget, with policy recommendations for fiscal accountability.",
    accent: "#d97706",
    bg: "rgba(217, 119, 6, 0.1)",
    border: "rgba(217, 119, 6, 0.25)",
  },
  {
    title: "The $180 Billion Retirement Wealth Gap",
    doi: "10.2139/ssrn.5964514",
    url: "https://doi.org/10.2139/ssrn.5964514",
    downloads: 12,
    views: 81,
    description:
      "Quantifying the staggering retirement wealth gap and its disproportionate impact on marginalized communities, with proposals for systemic reform.",
    accent: "#22c55e",
    bg: "rgba(22, 101, 52, 0.1)",
    border: "rgba(22, 101, 52, 0.25)",
  },
  {
    title: "Addressing Relational Anosognosia",
    doi: "10.2139/ssrn.6106066",
    url: "https://doi.org/10.2139/ssrn.6106066",
    downloads: 16,
    views: 52,
    description:
      "Exploring relational anosognosia — the inability to recognize dysfunction within one's own relationships — and its implications for mental health, recovery, and interpersonal healing.",
    accent: "#dc2626",
    bg: "rgba(185, 28, 28, 0.1)",
    border: "rgba(185, 28, 28, 0.25)",
  },
];

export default function Publications() {
  const { ref, isVisible } = useInView();

  const totalDownloads = papers.reduce((sum, p) => sum + p.downloads, 0);
  const totalViews = papers.reduce((sum, p) => sum + p.views, 0);

  return (
    <section
      id="publications"
      aria-label="Published research papers"
      className="relative py-20 md:py-28 overflow-hidden"
    >
      {/* Background glow */}
      <div className="absolute inset-0 z-0">
        <div
          className="w-full h-full opacity-[0.04]"
          style={{
            background:
              "radial-gradient(ellipse at 70% 30%, rgba(22, 101, 52, 0.5) 0%, transparent 50%), radial-gradient(ellipse at 30% 70%, rgba(217, 119, 6, 0.3) 0%, transparent 50%)",
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
              style={{ color: "#22c55e" }}
            >
              Research
            </p>
            <h2 className="font-serif text-3xl md:text-4xl lg:text-5xl text-warm-50 mb-4">
              Published Papers
            </h2>
            <p className="text-warm-400 text-base md:text-lg max-w-2xl mb-4">
              Peer-reviewed research published on SSRN (Social Science Research Network),
              tackling systemic issues in criminal justice, fiscal policy, retirement equity,
              and relational psychology.
            </p>
            <div className="gold-line w-24" />
          </div>

          {/* Aggregate Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
            <div
              className="glass-panel p-4 text-center"
              style={{ borderColor: "rgba(22, 101, 52, 0.2)", background: "rgba(22, 101, 52, 0.08)" }}
            >
              <div className="font-serif text-2xl md:text-3xl" style={{ color: "#22c55e" }}>
                4
              </div>
              <div className="text-warm-400 text-xs md:text-sm font-medium">Papers Published</div>
            </div>
            <div
              className="glass-panel p-4 text-center"
              style={{ borderColor: "rgba(217, 119, 6, 0.2)", background: "rgba(217, 119, 6, 0.08)" }}
            >
              <div className="font-serif text-2xl md:text-3xl" style={{ color: "#d97706" }}>
                {totalDownloads}+
              </div>
              <div className="text-warm-400 text-xs md:text-sm font-medium">Total Downloads</div>
            </div>
            <div
              className="glass-panel p-4 text-center"
              style={{ borderColor: "rgba(185, 28, 28, 0.2)", background: "rgba(185, 28, 28, 0.08)" }}
            >
              <div className="font-serif text-2xl md:text-3xl" style={{ color: "#dc2626" }}>
                {totalViews}+
              </div>
              <div className="text-warm-400 text-xs md:text-sm font-medium">Total Views</div>
            </div>
            <div
              className="glass-panel p-4 text-center"
              style={{ borderColor: "rgba(22, 101, 52, 0.2)", background: "rgba(22, 101, 52, 0.08)" }}
            >
              <div className="font-serif text-2xl md:text-3xl" style={{ color: "#22c55e" }}>
                16
              </div>
              <div className="text-warm-400 text-xs md:text-sm font-medium">Social Shares</div>
            </div>
          </div>

          {/* Paper Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {papers.map((paper) => (
              <a
                key={paper.doi}
                href={paper.url}
                target="_blank"
                rel="noopener noreferrer"
                className="glass-panel p-6 group hover:bg-white/[0.06] transition-all duration-300 hover:-translate-y-1 hover:shadow-lg block"
                style={{
                  borderColor: paper.border,
                  boxShadow: `0 4px 20px ${paper.bg}`,
                }}
                aria-label={`Read "${paper.title}" on SSRN`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div
                    className="w-10 h-10 rounded-lg flex items-center justify-center"
                    style={{ backgroundColor: paper.bg }}
                  >
                    <BookOpen size={20} style={{ color: paper.accent }} aria-hidden="true" />
                  </div>
                  <ExternalLink
                    size={16}
                    className="text-warm-600 group-hover:text-warm-300 transition-colors"
                    aria-hidden="true"
                  />
                </div>

                <h3
                  className="font-semibold text-lg mb-2 group-hover:text-warm-50 transition-colors"
                  style={{ color: paper.accent }}
                >
                  {paper.title}
                </h3>

                <p className="text-warm-400 text-sm leading-relaxed mb-4">
                  {paper.description}
                </p>

                {/* DOI */}
                <p className="text-warm-500 text-xs mb-3 font-mono">
                  DOI: {paper.doi}
                </p>

                {/* Metrics */}
                <div className="flex flex-wrap items-center gap-4 text-xs">
                  <span className="inline-flex items-center gap-1.5 text-warm-400">
                    <Download size={12} style={{ color: paper.accent }} aria-hidden="true" />
                    {paper.downloads} downloads
                  </span>
                  <span className="inline-flex items-center gap-1.5 text-warm-400">
                    <Eye size={12} style={{ color: paper.accent }} aria-hidden="true" />
                    {paper.views} views
                  </span>
                  {paper.socialShares && (
                    <span className="inline-flex items-center gap-1.5 text-warm-400">
                      <Share2 size={12} style={{ color: paper.accent }} aria-hidden="true" />
                      {paper.socialShares} shares
                    </span>
                  )}
                </div>
              </a>
            ))}
          </div>

          {/* Author Page Link */}
          <div className="mt-10 text-center">
            <a
              href="https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=8516562"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-lg font-medium text-sm transition-all duration-200 hover:scale-[1.02]"
              style={{
                backgroundColor: "rgba(22, 101, 52, 0.15)",
                border: "1px solid rgba(22, 101, 52, 0.25)",
                color: "#22c55e",
              }}
            >
              <BookOpen size={18} aria-hidden="true" />
              View All Papers on SSRN
              <ExternalLink size={14} aria-hidden="true" />
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
