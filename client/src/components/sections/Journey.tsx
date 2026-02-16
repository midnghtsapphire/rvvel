/*
 * Design: Earth & Canopy — Grounded Glassmorphism
 * Journey / Origin Story section — Audrey's brand story.
 * The rejection that sparked an entire portfolio of innovation.
 * Earthy warm tones: deep reds, forest greens, gold accents. NO blue light.
 * WCAG AAA accessible, neurodivergent-friendly.
 */
import { useInView } from "@/hooks/useInView";
import { Flame, Droplets, Lightbulb, BookOpen, Cpu, FlaskConical, Rocket } from "lucide-react";

const milestones = [
  {
    icon: Droplets,
    title: "The Water Plan",
    description:
      "Determined to prove her worth, Audrey set out to deliver Wellington the best water conservation plan they'd ever seen — one so thorough it couldn't be ignored.",
    color: "#22c55e",
    bg: "rgba(22, 101, 52, 0.12)",
    border: "rgba(22, 101, 52, 0.25)",
  },
  {
    icon: Lightbulb,
    title: "The Tiki Washbot",
    description:
      "That water plan evolved into something bigger — the Washbot, a water-saving smart washing system. Inspired by her Hawaiian heritage, it became the Tiki Washbot, blending innovation with cultural identity.",
    color: "#d97706",
    bg: "rgba(217, 119, 6, 0.12)",
    border: "rgba(217, 119, 6, 0.25)",
  },
  {
    icon: FlaskConical,
    title: "The Dishruptor & BELL",
    description:
      "One invention led to the next. The Dishruptor reimagined dishwashing entirely. Then came BELL — the Biopolymer Eco Laundry Lubricant — a biodegradable, plant-based cleaning compound designed to replace toxic detergents.",
    color: "#dc2626",
    bg: "rgba(185, 28, 28, 0.12)",
    border: "rgba(185, 28, 28, 0.25)",
  },
  {
    icon: BookOpen,
    title: "Published Research",
    description:
      "Audrey turned her analytical mind to systemic problems — publishing four peer-reviewed papers on SSRN covering criminal sentencing AI, retirement wealth gaps, government waste, and relational anosognosia.",
    color: "#22c55e",
    bg: "rgba(22, 101, 52, 0.12)",
    border: "rgba(22, 101, 52, 0.25)",
  },
  {
    icon: Cpu,
    title: "Apps & the Collatz Conjecture",
    description:
      "She built a full portfolio of applications — from AI accessibility tools to data routers to email organizers. Along the way, she proved a mathematical conjecture (Collatz) that had stumped mathematicians for decades.",
    color: "#d97706",
    bg: "rgba(217, 119, 6, 0.12)",
    border: "rgba(217, 119, 6, 0.25)",
  },
  {
    icon: Rocket,
    title: "GlowStar Labs",
    description:
      "All of it — every invention, every paper, every app — came together under one roof. GlowStar Labs became the home for Audrey's entire ecosystem of innovation, built from nothing but determination.",
    color: "#dc2626",
    bg: "rgba(185, 28, 28, 0.12)",
    border: "rgba(185, 28, 28, 0.25)",
  },
];

export default function Journey() {
  const { ref, isVisible } = useInView();

  return (
    <section
      id="journey"
      aria-label="Audrey's origin story and journey"
      className="relative py-20 md:py-28 overflow-hidden"
    >
      {/* Background glow */}
      <div className="absolute inset-0 z-0">
        <div
          className="w-full h-full opacity-[0.04]"
          style={{
            background:
              "radial-gradient(ellipse at 20% 30%, rgba(185, 28, 28, 0.5) 0%, transparent 50%), radial-gradient(ellipse at 80% 70%, rgba(217, 119, 6, 0.4) 0%, transparent 50%), radial-gradient(ellipse at 50% 50%, rgba(22, 101, 52, 0.3) 0%, transparent 60%)",
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
              Origin Story
            </p>
            <h2 className="font-serif text-3xl md:text-4xl lg:text-5xl text-warm-50 mb-4">
              The Rejection That Built an Empire
            </h2>
            <div className="gold-line w-24" />
          </div>

          {/* The Story — Opening */}
          <div className="max-w-4xl mb-14">
            <div
              className="glass-panel-strong p-6 md:p-8 mb-8"
              style={{
                borderColor: "rgba(185, 28, 28, 0.25)",
                background:
                  "linear-gradient(135deg, rgba(185, 28, 28, 0.1) 0%, rgba(217, 119, 6, 0.06) 50%, rgba(22, 101, 52, 0.06) 100%)",
              }}
            >
              <div className="flex items-start gap-4">
                <div
                  className="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0"
                  style={{ backgroundColor: "rgba(185, 28, 28, 0.2)" }}
                >
                  <Flame size={24} style={{ color: "#dc2626" }} aria-hidden="true" />
                </div>
                <div>
                  <blockquote className="text-warm-100 text-lg md:text-xl lg:text-2xl font-serif italic leading-relaxed">
                    "I'll show them."
                  </blockquote>
                  <p className="text-warm-400 text-sm md:text-base mt-2">
                    — Audrey Evans, after being rejected from the Wellington, CO finance committee
                  </p>
                </div>
              </div>
            </div>

            <p className="text-warm-200 text-base md:text-lg leading-relaxed mb-5">
              It started with a simple application. Audrey Evans applied to serve on the finance
              committee for the Town of Wellington, Colorado. She wanted to contribute — to bring
              her three decades of IT, project management, and analytical expertise to her community.
              They said no.
            </p>
            <p className="text-warm-300 text-base md:text-lg leading-relaxed mb-5">
              Most people would have moved on. Audrey is not most people. That rejection didn't
              discourage her — it ignited something. She decided that if they wouldn't let her
              serve on a committee, she'd give them something they couldn't ignore: the best
              water conservation plan Wellington had ever seen.
            </p>
            <p className="text-warm-300 text-base md:text-lg leading-relaxed">
              What happened next was a chain reaction of invention, research, and creation that
              nobody — least of all that finance committee — could have predicted. One idea led
              to the next, and the next, and the next. A single rejection became the foundation
              of an entire portfolio of innovation.
            </p>
          </div>

          {/* Milestone Timeline */}
          <div className="relative">
            {/* Vertical timeline line */}
            <div
              className="absolute left-4 md:left-8 top-0 bottom-0 w-px hidden md:block"
              style={{
                background:
                  "linear-gradient(to bottom, rgba(185, 28, 28, 0.5), rgba(217, 119, 6, 0.4), rgba(22, 101, 52, 0.4), transparent)",
              }}
              aria-hidden="true"
            />

            <div className="space-y-6">
              {milestones.map((milestone, idx) => {
                const Icon = milestone.icon;
                return (
                  <div key={milestone.title} className="relative pl-0 md:pl-20">
                    {/* Timeline dot */}
                    <div
                      className="absolute left-2 md:left-6 top-6 w-4 h-4 rounded-full z-10 hidden md:block"
                      style={{
                        backgroundColor: milestone.bg,
                        border: `2px solid ${milestone.color}`,
                      }}
                      aria-hidden="true"
                    />

                    <div
                      className="glass-panel p-5 md:p-6 transition-all duration-200 hover:bg-white/[0.04]"
                      style={{ borderColor: milestone.border }}
                    >
                      <div className="flex items-start gap-4">
                        <div
                          className="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
                          style={{ backgroundColor: milestone.bg }}
                        >
                          <Icon size={20} style={{ color: milestone.color }} aria-hidden="true" />
                        </div>
                        <div>
                          <div className="flex items-center gap-2 mb-1">
                            <span
                              className="text-xs font-medium uppercase tracking-wider"
                              style={{ color: milestone.color }}
                            >
                              Step {idx + 1}
                            </span>
                          </div>
                          <h3 className="text-warm-100 font-semibold text-lg mb-2">
                            {milestone.title}
                          </h3>
                          <p className="text-warm-300 text-sm md:text-base leading-relaxed">
                            {milestone.description}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Closing Statement */}
          <div className="mt-12 max-w-3xl">
            <div
              className="glass-panel p-6 md:p-8"
              style={{
                borderColor: "rgba(217, 119, 6, 0.25)",
                background:
                  "linear-gradient(135deg, rgba(217, 119, 6, 0.08) 0%, rgba(22, 101, 52, 0.06) 100%)",
              }}
            >
              <p className="text-warm-100 text-base md:text-lg leading-relaxed font-medium">
                From a rejected committee application to a tech company, four published papers,
                multiple inventions, a portfolio of applications, a proven mathematical conjecture,
                and a published music career — every single piece of it traces back to one moment
                and three words:{" "}
                <span className="font-serif italic text-lg md:text-xl" style={{ color: "#dc2626" }}>
                  "I'll show them."
                </span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
