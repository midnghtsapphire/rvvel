/*
 * Design: Earth & Canopy
 * Glassmorphism navbar with earthy warm accents — crimson, forest green, gold.
 * Sticky top nav with frosted glass effect. NO blue light.
 */
import { useState, useEffect } from "react";
import { Menu, X } from "lucide-react";

const navLinks = [
  { label: "About", href: "#about" },
  { label: "Journey", href: "#journey" },
  { label: "Research", href: "#publications" },
  { label: "Inventions", href: "#inventions" },
  { label: "Resume", href: "#resume" },
  { label: "Portfolio", href: "#portfolio" },
  { label: "Music", href: "#music" },
  { label: "Advocacy", href: "#advocacy" },
  { label: "Contact", href: "#contact" },
];

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const handleNavClick = (href: string) => {
    setIsOpen(false);
    const el = document.querySelector(href);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  return (
    <nav
      role="navigation"
      aria-label="Main navigation"
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? "glass-panel-strong shadow-lg"
          : "bg-transparent"
      }`}
      style={scrolled ? { boxShadow: "0 4px 20px rgba(26, 21, 16, 0.5)" } : undefined}
    >
      <div className="container flex items-center justify-between h-16 md:h-18">
        {/* Logo / Name — crimson accent */}
        <a
          href="#hero"
          onClick={(e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: "smooth" });
          }}
          className="font-serif text-xl md:text-2xl transition-colors duration-200"
          style={{ color: "#dc2626" }}
          onMouseEnter={(e) => (e.currentTarget.style.color = "#ef4444")}
          onMouseLeave={(e) => (e.currentTarget.style.color = "#dc2626")}
          aria-label="Scroll to top"
        >
          Audrey Evans
        </a>

        {/* Desktop Nav */}
        <ul className="hidden lg:flex items-center gap-0.5" role="list">
          {navLinks.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                onClick={(e) => {
                  e.preventDefault();
                  handleNavClick(link.href);
                }}
                className="px-2.5 py-2 text-sm font-medium text-warm-200 hover:text-warm-50 transition-colors duration-200 rounded-md hover:bg-white/5"
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="lg:hidden p-2 text-warm-200 transition-colors"
          style={{ color: isOpen ? "#dc2626" : undefined }}
          aria-expanded={isOpen}
          aria-controls="mobile-menu"
          aria-label={isOpen ? "Close menu" : "Open menu"}
        >
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div
          id="mobile-menu"
          className="lg:hidden glass-panel-strong"
          style={{ borderTop: "1px solid rgba(169, 149, 128, 0.1)" }}
          role="menu"
        >
          <ul className="container py-4 space-y-1" role="list">
            {navLinks.map((link) => (
              <li key={link.href} role="menuitem">
                <a
                  href={link.href}
                  onClick={(e) => {
                    e.preventDefault();
                    handleNavClick(link.href);
                  }}
                  className="block px-4 py-3 text-base font-medium text-warm-200 hover:text-warm-50 hover:bg-white/5 rounded-lg transition-colors duration-200"
                >
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </nav>
  );
}
