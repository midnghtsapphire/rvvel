/*
 * Design: Amber Glass Atelier
 * Footer — minimal, warm, with brand links and copyright.
 */

const currentYear = new Date().getFullYear();

export default function Footer() {
  return (
    <footer
      role="contentinfo"
      className="border-t border-amber-500/10 py-8 md:py-10"
    >
      <div className="container">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="text-center md:text-left">
            <p className="font-serif text-lg text-amber-400">Audrey Evans</p>
            <p className="text-warm-500 text-xs mt-1">
              &copy; {currentYear} Audrey Evans / GlowStar Labs. All rights reserved.
            </p>
          </div>

          <div className="flex items-center gap-6">
            <a
              href="https://github.com/MIDNGHTSAPPHIRE"
              target="_blank"
              rel="noopener noreferrer"
              className="text-warm-500 hover:text-amber-400 transition-colors text-sm"
              aria-label="GitHub profile"
            >
              GitHub
            </a>
            <a
              href="https://www.linkedin.com/in/audrey-evans-96a56552/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-warm-500 hover:text-amber-400 transition-colors text-sm"
              aria-label="LinkedIn profile"
            >
              LinkedIn
            </a>
            <a
              href="mailto:angelreporters@gmail.com"
              className="text-warm-500 hover:text-amber-400 transition-colors text-sm"
              aria-label="Send email"
            >
              Email
            </a>
          </div>
        </div>

        {/* Eco badge */}
        <div className="mt-6 pt-4 border-t border-amber-500/5 text-center">
          <p className="text-warm-600 text-xs">
            Built with carbon efficiency in mind — minimal dependencies, optimized assets, dark theme for OLED power savings.
          </p>
        </div>
      </div>
    </footer>
  );
}
