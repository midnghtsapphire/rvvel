/*
 * Design: Amber Glass Atelier
 * Contact section — email, LinkedIn, GitHub, TikTok links.
 * Glass cards, warm amber accents. Visual-only (no audio dependency).
 */
import { useInView } from "@/hooks/useInView";
import { Mail, Linkedin, Github, Video, MapPin } from "lucide-react";

const contactLinks = [
  {
    icon: Mail,
    label: "Email",
    value: "angelreporters@gmail.com",
    href: "mailto:angelreporters@gmail.com",
    description: "Primary contact email",
  },
  {
    icon: Linkedin,
    label: "LinkedIn",
    value: "Audrey Evans",
    href: "https://www.linkedin.com/in/audrey-evans-96a56552/",
    description: "Professional network profile",
  },
  {
    icon: Github,
    label: "GitHub",
    value: "MIDNGHTSAPPHIRE",
    href: "https://github.com/MIDNGHTSAPPHIRE",
    description: "Open source projects and code",
  },
  {
    icon: Video,
    label: "TikTok",
    value: "#MeetAudreyEvans",
    href: "https://www.tiktok.com/@meetaudreyevans",
    description: "Video content and updates",
  },
];

export default function Contact() {
  const { ref, isVisible } = useInView();

  return (
    <section
      id="contact"
      aria-label="Contact information"
      className="relative py-20 md:py-28"
    >
      <div className="container">
        <div ref={ref} className={`fade-in-section ${isVisible ? "visible" : ""}`}>
          {/* Section Header */}
          <div className="mb-12 md:mb-16">
            <p className="text-amber-400 font-medium text-sm tracking-widest uppercase mb-2">
              Contact
            </p>
            <h2 className="font-serif text-3xl md:text-4xl lg:text-5xl text-warm-50 mb-4">
              Let's Connect
            </h2>
            <p className="text-warm-400 text-base md:text-lg max-w-2xl">
              Whether you're interested in collaboration, have a project in mind, or want to
              learn more about Freedom Angel Corps — I'd love to hear from you.
            </p>
            <div className="gold-line w-24 mt-4" />
          </div>

          {/* Contact Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-3xl">
            {contactLinks.map((link) => {
              const Icon = link.icon;
              return (
                <a
                  key={link.label}
                  href={link.href}
                  target={link.href.startsWith("mailto") ? undefined : "_blank"}
                  rel={link.href.startsWith("mailto") ? undefined : "noopener noreferrer"}
                  className="glass-panel p-5 md:p-6 group hover:bg-white/[0.08] transition-all duration-200 hover:-translate-y-0.5"
                  aria-label={`${link.label}: ${link.value}`}
                >
                  <div className="flex items-start gap-4">
                    <div className="w-10 h-10 rounded-lg bg-amber-500/15 flex items-center justify-center flex-shrink-0">
                      <Icon size={20} className="text-amber-400" aria-hidden="true" />
                    </div>
                    <div>
                      <p className="text-warm-500 text-xs font-medium uppercase tracking-wider mb-1">
                        {link.label}
                      </p>
                      <p className="text-warm-100 font-medium text-base group-hover:text-amber-400 transition-colors">
                        {link.value}
                      </p>
                      <p className="text-warm-500 text-xs mt-1">
                        {link.description}
                      </p>
                    </div>
                  </div>
                </a>
              );
            })}
          </div>

          {/* Location */}
          <div className="mt-8 flex items-center gap-3 text-warm-500">
            <MapPin size={16} className="text-amber-500/60" aria-hidden="true" />
            <span className="text-sm">Fort Collins / Wellington, Colorado</span>
          </div>
        </div>
      </div>
    </section>
  );
}
