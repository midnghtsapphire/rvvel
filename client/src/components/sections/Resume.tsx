/*
 * Design: Earth & Canopy
 * Resume section — interactive timeline with glass cards, skill badges, certifications.
 * Earthy accents: crimson timeline, forest green skill badges, gold cert icons.
 * NO blue light. WCAG AAA accessible.
 */
import { useState } from "react";
import { useInView } from "@/hooks/useInView";
import {
  Briefcase,
  GraduationCap,
  Award,
  Code,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

const experience = [
  {
    period: "2008 – Present",
    title: "Founder & CEO",
    company: "Multiple Ventures",
    description:
      "Founded and led RisingAloha, TikiWashbot, TuTu The Dishruptor, PawPals Rescue, AdultStrong, Freedom Angel Corp, Angel Reporter LLC, Avappa, Dater Basics, Apparentals, PB Dry Bar, XI Website Solutions, and Fast Macros.",
    icon: Briefcase,
  },
  {
    period: "2006 – 2008",
    title: "Programmer Analyst 5",
    company: "Safeguard",
    description:
      "Advanced programming and systems analysis in a security-focused environment.",
    icon: Code,
  },
  {
    period: "2006",
    title: "Web Application Dev Manager",
    company: "Ellison Educational Equipment",
    description:
      "Led web application development team and managed full software lifecycle.",
    icon: Briefcase,
  },
  {
    period: "2005 – 2006",
    title: "Systems Analyst / Business Analyst",
    company: "Lending Tree",
    description:
      "Systems and business analysis for one of the nation's leading online lending marketplaces.",
    icon: Briefcase,
  },
  {
    period: "2005",
    title: "Project Manager / Scrum Master",
    company: "Gateway",
    description:
      "Managed agile projects and facilitated scrum ceremonies for product development teams.",
    icon: Briefcase,
  },
  {
    period: "2000 – 2005",
    title: "Sr. Program Manager",
    company: "Buy.com / United Commerce",
    description:
      "Promoted from Software Engineer to Sr. Program Manager. Received out-of-cycle bonuses for MTV/Swell implementations. Managed 200+ person matrix environment.",
    icon: Award,
  },
  {
    period: "1996 – 2000",
    title: "Sr. Software Engineer",
    company: "Orange County District Attorney",
    description:
      "Promoted from Trainee Tech to Sr. Software Engineer. Built critical systems for the DA's office.",
    icon: Code,
  },
];

const skills = [
  { category: "Languages", items: ["Python", "Java", "C#", "JavaScript", "PHP", "SQL", "HTML/CSS", "XML", "ASP.NET"] },
  { category: "Databases", items: ["MySQL", "PostgreSQL", "MS SQL Server", "Informix"] },
  { category: "Methodologies", items: ["PMP", "Agile", "Scrum", "Kanban", "SAFe", "Six Sigma", "Human-Centered Design"] },
  { category: "PM Tools", items: ["Jira", "GitHub", "Salesforce", "Slack", "Asana", "Basecamp"] },
];

const certifications = [
  "PMP Certified (2015, Texas)",
  "CCAR Recovery Coach Academy",
  "Ethical Considerations for Recovery Coaches",
  "Sex Trafficking 101 & 102 (Sarah's House / CSPD)",
  "ADA Social Media",
  "Narconon Graduate",
  "Stenography School — 200 WPM",
  "Recovery Coach Professional (in process)",
  "Family Peer Support Specialist (in process)",
  "Certified Addiction Technician (in process)",
];

export default function Resume() {
  const { ref, isVisible } = useInView();
  const [expandedIdx, setExpandedIdx] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<"experience" | "skills" | "certs">("experience");

  const tabStyles = {
    experience: { active: "#b91c1c", activeBg: "rgba(185, 28, 28, 0.15)", activeBorder: "rgba(185, 28, 28, 0.3)" },
    skills: { active: "#22c55e", activeBg: "rgba(22, 101, 52, 0.15)", activeBorder: "rgba(22, 101, 52, 0.3)" },
    certs: { active: "#d97706", activeBg: "rgba(217, 119, 6, 0.15)", activeBorder: "rgba(217, 119, 6, 0.3)" },
  };

  return (
    <section
      id="resume"
      aria-label="Resume and professional experience"
      className="relative py-20 md:py-28"
    >
      <div className="container">
        <div ref={ref} className={`fade-in-section ${isVisible ? "visible" : ""}`}>
          {/* Section Header */}
          <div className="mb-12 md:mb-16">
            <p
              className="font-medium text-sm tracking-widest uppercase mb-2"
              style={{ color: "#d97706" }}
            >
              Resume
            </p>
            <h2 className="font-serif text-3xl md:text-4xl lg:text-5xl text-warm-50 mb-4">
              Professional Journey
            </h2>
            <div className="gold-line w-24" />
          </div>

          {/* Tab Navigation */}
          <div className="flex flex-wrap gap-2 mb-10" role="tablist" aria-label="Resume sections">
            {[
              { id: "experience" as const, label: "Experience", icon: Briefcase },
              { id: "skills" as const, label: "Skills", icon: Code },
              { id: "certs" as const, label: "Certifications", icon: GraduationCap },
            ].map((tab) => {
              const ts = tabStyles[tab.id];
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  role="tab"
                  aria-selected={isActive}
                  aria-controls={`panel-${tab.id}`}
                  onClick={() => setActiveTab(tab.id)}
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-medium transition-all duration-200"
                  style={
                    isActive
                      ? { backgroundColor: ts.activeBg, color: ts.active, border: `1px solid ${ts.activeBorder}` }
                      : { border: "1px solid transparent" }
                  }
                >
                  <tab.icon size={16} />
                  {tab.label}
                </button>
              );
            })}
          </div>

          {/* Experience Timeline */}
          {activeTab === "experience" && (
            <div id="panel-experience" role="tabpanel" aria-label="Professional experience timeline">
              <div className="relative">
                {/* Timeline line — crimson gradient */}
                <div
                  className="absolute left-4 md:left-8 top-0 bottom-0 w-px"
                  style={{
                    background: "linear-gradient(to bottom, rgba(185, 28, 28, 0.5), rgba(185, 28, 28, 0.2), transparent)",
                  }}
                  aria-hidden="true"
                />

                <div className="space-y-6">
                  {experience.map((item, idx) => {
                    const Icon = item.icon;
                    const isExpanded = expandedIdx === idx;
                    return (
                      <div key={idx} className="relative pl-12 md:pl-20">
                        {/* Timeline dot — crimson */}
                        <div
                          className="absolute left-2 md:left-6 top-4 w-4 h-4 rounded-full z-10"
                          style={{
                            backgroundColor: "rgba(185, 28, 28, 0.3)",
                            border: "2px solid #b91c1c",
                          }}
                          aria-hidden="true"
                        />

                        <button
                          onClick={() => setExpandedIdx(isExpanded ? null : idx)}
                          aria-expanded={isExpanded}
                          className="w-full text-left glass-panel p-5 md:p-6 hover:bg-white/[0.06] transition-all duration-200 group"
                        >
                          <div className="flex items-start justify-between gap-4">
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-1">
                                <Icon size={16} style={{ color: "#b91c1c" }} aria-hidden="true" />
                                <span
                                  className="text-xs md:text-sm font-medium"
                                  style={{ color: "rgba(220, 38, 38, 0.8)" }}
                                >
                                  {item.period}
                                </span>
                              </div>
                              <h3 className="text-warm-100 font-semibold text-base md:text-lg">
                                {item.title}
                              </h3>
                              <p className="text-warm-400 text-sm">{item.company}</p>
                            </div>
                            <span className="text-warm-500 group-hover:text-crimson-500 transition-colors mt-1" aria-hidden="true">
                              {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                            </span>
                          </div>
                          {isExpanded && (
                            <p className="mt-3 text-warm-300 text-sm md:text-base leading-relaxed">
                              {item.description}
                            </p>
                          )}
                        </button>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {/* Skills */}
          {activeTab === "skills" && (
            <div id="panel-skills" role="tabpanel" aria-label="Technical skills">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {skills.map((group) => (
                  <div key={group.category} className="glass-panel p-6">
                    <h3
                      className="font-semibold text-base mb-4"
                      style={{ color: "#22c55e" }}
                    >
                      {group.category}
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {group.items.map((skill) => (
                        <span
                          key={skill}
                          className="px-3 py-1.5 text-xs md:text-sm font-medium text-warm-200 rounded-md"
                          style={{
                            backgroundColor: "rgba(22, 101, 52, 0.15)",
                            border: "1px solid rgba(22, 163, 74, 0.2)",
                          }}
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}

                {/* Additional info */}
                <div className="glass-panel p-6 md:col-span-2">
                  <h3
                    className="font-semibold text-base mb-4"
                    style={{ color: "#22c55e" }}
                  >
                    Compliance &amp; Governance
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {["SOX", "SOC", "IT Governance", "Waterfall", "RUP", "XP"].map((item) => (
                      <span
                        key={item}
                        className="px-3 py-1.5 text-xs md:text-sm font-medium text-warm-200 rounded-md"
                        style={{
                          backgroundColor: "rgba(22, 101, 52, 0.15)",
                          border: "1px solid rgba(22, 163, 74, 0.2)",
                        }}
                      >
                        {item}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Certifications */}
          {activeTab === "certs" && (
            <div id="panel-certs" role="tabpanel" aria-label="Certifications and training">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {certifications.map((cert, idx) => (
                  <div
                    key={idx}
                    className="glass-panel p-4 md:p-5 flex items-start gap-3"
                  >
                    <Award size={18} style={{ color: "#d97706" }} className="flex-shrink-0 mt-0.5" aria-hidden="true" />
                    <span className="text-warm-200 text-sm md:text-base">{cert}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
