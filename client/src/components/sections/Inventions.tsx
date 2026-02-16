/*
 * Design: Earth & Canopy — Grounded Glassmorphism
 * Inventions section — Tiki Washbot, Dishruptor, BELL, Kinetic Wash Pod.
 * Gold/amber accents for innovation. NO blue light.
 * WCAG AAA accessible, neurodivergent-friendly.
 */
import { useInView } from "@/hooks/useInView";
import { Droplets, Sparkles, FlaskConical, Zap, Leaf, Cog } from "lucide-react";

const inventions = [
  {
    name: "Tiki Washbot",
    tagline: "Water-Saving Smart Washing System",
    description:
      "Born from a water conservation plan for Wellington, CO, the Tiki Washbot is a smart washing system designed to dramatically reduce water usage. Inspired by Audrey's Native Hawaiian heritage, the Hawaiian-themed design reflects the deep cultural connection between island communities and water stewardship. What started as the \"Washbot\" evolved into a culturally grounded innovation that merges sustainability engineering with indigenous values.",
    icon: Droplets,
    features: ["Smart water metering", "Hawaiian-inspired design", "IoT-connected controls", "Conservation analytics"],
    color: "#22c55e",
    bg: "rgba(22, 101, 52, 0.12)",
    border: "rgba(22, 101, 52, 0.25)",
  },
  {
    name: "The Dishruptor",
    tagline: "Dishwashing, Reimagined",
    description:
      "The Dishruptor challenges everything we accept about conventional dishwashing. Designed to reduce water waste, energy consumption, and chemical dependency, this invention rethinks the entire dishwashing process from first principles. It's not an incremental improvement — it's a disruption of the category itself.",
    icon: Sparkles,
    features: ["Reduced water consumption", "Energy-efficient design", "Chemical reduction", "Compact form factor"],
    color: "#d97706",
    bg: "rgba(217, 119, 6, 0.12)",
    border: "rgba(217, 119, 6, 0.25)",
  },
  {
    name: "BELL",
    tagline: "Biopolymer Eco Laundry Lubricant",
    description:
      "BELL — the Biopolymer Eco Laundry Lubricant — is a biodegradable, plant-based cleaning compound engineered to replace toxic detergents. Built on Audrey's research into biopolymers and biocomposites, BELL represents the intersection of green chemistry and practical household innovation. It's cleaning technology that doesn't poison the water it's meant to save.",
    icon: FlaskConical,
    features: ["100% biodegradable", "Plant-based formula", "Non-toxic compounds", "Biopolymer technology"],
    color: "#dc2626",
    bg: "rgba(185, 28, 28, 0.12)",
    border: "rgba(185, 28, 28, 0.25)",
  },
  {
    name: "Kinetic Wash Pod",
    tagline: "Automatic Washer Load Detection",
    description:
      "The Kinetic Wash Pod uses sensor technology to automatically detect washer load size and optimize water, detergent, and cycle settings in real time. No more guessing, no more waste. It's the missing intelligence layer for every washing machine — turning a dumb appliance into a smart, resource-conscious system.",
    icon: Zap,
    features: ["Automatic load detection", "Real-time optimization", "Universal compatibility", "Resource savings"],
    color: "#d97706",
    bg: "rgba(217, 119, 6, 0.12)",
    border: "rgba(217, 119, 6, 0.25)",
  },
];

export default function Inventions() {
  const { ref, isVisible } = useInView();

  return (
    <section
      id="inventions"
      aria-label="Inventions and hardware innovations"
      className="relative py-20 md:py-28 overflow-hidden"
    >
      {/* Background glow */}
      <div className="absolute inset-0 z-0">
        <div
          className="w-full h-full opacity-[0.04]"
          style={{
            background:
              "radial-gradient(ellipse at 60% 30%, rgba(217, 119, 6, 0.5) 0%, transparent 50%), radial-gradient(ellipse at 30% 70%, rgba(22, 101, 52, 0.3) 0%, transparent 50%)",
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
              Inventions
            </p>
            <h2 className="font-serif text-3xl md:text-4xl lg:text-5xl text-warm-50 mb-4">
              Hardware &amp; Innovation
            </h2>
            <p className="text-warm-400 text-base md:text-lg max-w-2xl mb-4">
              Physical inventions and sustainable technology — each one born from the same
              drive to solve real problems with engineering, not excuses.
            </p>
            <div className="gold-line w-24" />
          </div>

          {/* Sustainability Badge */}
          <div
            className="glass-panel inline-flex items-center gap-3 px-5 py-3 mb-10"
            style={{
              borderColor: "rgba(22, 101, 52, 0.25)",
              background: "rgba(22, 101, 52, 0.08)",
            }}
          >
            <Leaf size={18} style={{ color: "#22c55e" }} aria-hidden="true" />
            <span className="text-warm-200 text-sm font-medium">
              Every invention prioritizes{" "}
              <strong style={{ color: "#22c55e" }}>water conservation</strong>,{" "}
              <strong style={{ color: "#22c55e" }}>sustainability</strong>, and{" "}
              <strong style={{ color: "#22c55e" }}>non-toxic materials</strong>
            </span>
          </div>

          {/* Invention Cards */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {inventions.map((inv) => {
              const Icon = inv.icon;
              return (
                <div
                  key={inv.name}
                  className="glass-panel p-6 md:p-8 transition-all duration-200 hover:bg-white/[0.04]"
                  style={{ borderColor: inv.border }}
                >
                  {/* Header */}
                  <div className="flex items-start gap-4 mb-4">
                    <div
                      className="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0"
                      style={{ backgroundColor: inv.bg }}
                    >
                      <Icon size={24} style={{ color: inv.color }} aria-hidden="true" />
                    </div>
                    <div>
                      <h3
                        className="font-semibold text-xl mb-1"
                        style={{ color: inv.color }}
                      >
                        {inv.name}
                      </h3>
                      <p className="text-warm-400 text-sm font-medium">{inv.tagline}</p>
                    </div>
                  </div>

                  {/* Description */}
                  <p className="text-warm-300 text-sm md:text-base leading-relaxed mb-5">
                    {inv.description}
                  </p>

                  {/* Features */}
                  <div className="flex flex-wrap gap-2">
                    {inv.features.map((feature) => (
                      <span
                        key={feature}
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md"
                        style={{
                          color: inv.color,
                          backgroundColor: inv.bg,
                          border: `1px solid ${inv.border}`,
                        }}
                      >
                        <Cog size={10} aria-hidden="true" />
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
