/*
 * Design: Earth & Canopy
 * About section — full bio with secondary photo. Earthy glass panels, crimson/green/gold accents.
 * NO blue light. WCAG AAA accessible.
 */
import { useInView } from "@/hooks/useInView";

const SECONDARY_PHOTO = "https://files.manuscdn.com/user_upload_by_module/session_file/310419663032705003/NLYAnKrlUHPmCagF.jpeg";

const highlights = [
  { label: "Years in IT", value: "30+" },
  { label: "PMP Certified", value: "2015" },
  { label: "Ventures Founded", value: "10+" },
  { label: "Volunteer Years", value: "20+" },
];

export default function About() {
  const { ref, isVisible } = useInView();

  return (
    <section
      id="about"
      aria-label="About Audrey Evans"
      className="relative py-20 md:py-28"
    >
      {/* Subtle ambient glow — forest green */}
      <div
        className="absolute top-0 right-0 w-[500px] h-[500px] opacity-[0.06] pointer-events-none"
        style={{
          background: "radial-gradient(circle, rgba(22, 101, 52, 0.4) 0%, transparent 70%)",
        }}
        aria-hidden="true"
      />

      <div className="container">
        <div
          ref={ref}
          className={`fade-in-section ${isVisible ? "visible" : ""}`}
        >
          {/* Section Header */}
          <div className="mb-12 md:mb-16">
            <p
              className="font-medium text-sm tracking-widest uppercase mb-2"
              style={{ color: "#22c55e" }}
            >
              About Me
            </p>
            <h2 className="font-serif text-3xl md:text-4xl lg:text-5xl text-warm-50 mb-4">
              The Story So Far
            </h2>
            <div className="gold-line w-24" />
          </div>

          <div className="flex flex-col lg:flex-row gap-10 lg:gap-16 items-start">
            {/* Photo Column — blue dress, mountain backdrop */}
            <div className="flex-shrink-0 w-full lg:w-auto flex justify-center lg:justify-start">
              <div className="relative w-56 h-72 md:w-64 md:h-80 rounded-xl overflow-hidden glass-panel shadow-xl" style={{ boxShadow: "0 10px 40px rgba(22, 101, 52, 0.1)" }}>
                <img
                  src={SECONDARY_PHOTO}
                  alt="Audrey Evans in a blue dress against a mountain sunset backdrop — professional portrait"
                  className="w-full h-full object-cover object-top"
                  loading="lazy"
                />
              </div>
            </div>

            {/* Bio Content */}
            <div className="flex-1 space-y-5">
              {/* Heritage Statement — prominently featured */}
              <div
                className="glass-panel p-5 rounded-xl"
                style={{
                  borderColor: "rgba(217, 119, 6, 0.3)",
                  background: "linear-gradient(135deg, rgba(217, 119, 6, 0.08) 0%, rgba(185, 28, 28, 0.06) 50%, rgba(22, 101, 52, 0.06) 100%)",
                }}
              >
                <p className="text-warm-100 text-lg md:text-xl leading-relaxed font-medium">
                  I am{" "}
                  <span style={{ color: "#d97706" }}>M&#257;ori New Zealander</span>,{" "}
                  <span style={{ color: "#dc2626" }}>Portuguese</span>, and{" "}
                  <span style={{ color: "#22c55e" }}>Native Hawaiian</span>.
                </p>
                <p className="text-warm-300 text-sm md:text-base mt-2 leading-relaxed">
                  My heritage is the foundation of everything I build — from technology to music to advocacy.
                  These roots ground my work in resilience, community, and a deep respect for the land and its people.
                </p>
              </div>

              <p className="text-warm-200 text-base md:text-lg leading-relaxed">
                Audrey Evans is a proud and responsible Native Hawaiian, M&#257;ori New Zealander, and Portuguese
                woman with over three decades of experience in information technology. Her career spans the full
                spectrum of the tech industry — from software engineering and database architecture to geospatial
                engineering, data science, business intelligence, and program/project management.
              </p>
              <p className="text-warm-300 text-base md:text-lg leading-relaxed">
                A PMP-certified professional since 2015, Audrey has held roles at the Orange County
                District Attorney's office, Buy.com, Lending Tree, Gateway, and Safeguard, among others.
                She was promoted from Trainee Tech to Senior Software Engineer at the OC DA, and rose
                from Software Engineer to Senior Program Manager at Buy.com, managing a 200+ person
                matrix environment.
              </p>
              <p className="text-warm-300 text-base md:text-lg leading-relaxed">
                Beyond corporate tech, Audrey is an inventor of businesses, biopolymers, biocomposites,
                bio filaments for 3D printing, and the Manta Explorer — a self-repairing UAS drone. She
                is a published author on SSRN, a published musician performing as Revvel and Hail,
                a Paralegal De Facto in Colorado, and a CLE instructor/sponsor for the Colorado Supreme
                Court and Orange County DA Criminal Division.
              </p>
              <p className="text-warm-300 text-base md:text-lg leading-relaxed">
                As the founder of Freedom Angel Corps, Audrey dedicates herself to retraining trafficking
                survivors and providing peer support. With over 20 years of volunteer service spanning
                animal rescue, veterans' support, children's advocacy, domestic violence, trafficking
                awareness, and homelessness — her mission is clear: rescue, retrain, reinvent, and restore.
              </p>

              {/* Stats Grid — earthy glass with alternating accent colors */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-6">
                {highlights.map((item, idx) => {
                  const colors = [
                    { text: "#dc2626", bg: "rgba(185, 28, 28, 0.1)", border: "rgba(185, 28, 28, 0.2)" },
                    { text: "#22c55e", bg: "rgba(22, 101, 52, 0.1)", border: "rgba(22, 101, 52, 0.2)" },
                    { text: "#d97706", bg: "rgba(217, 119, 6, 0.1)", border: "rgba(217, 119, 6, 0.2)" },
                    { text: "#dc2626", bg: "rgba(185, 28, 28, 0.1)", border: "rgba(185, 28, 28, 0.2)" },
                  ];
                  const c = colors[idx % colors.length];
                  return (
                    <div
                      key={item.label}
                      className="glass-panel p-4 text-center"
                      style={{ borderColor: c.border, background: c.bg }}
                    >
                      <div
                        className="font-serif text-2xl md:text-3xl mb-1"
                        style={{ color: c.text }}
                      >
                        {item.value}
                      </div>
                      <div className="text-warm-400 text-xs md:text-sm font-medium">
                        {item.label}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
