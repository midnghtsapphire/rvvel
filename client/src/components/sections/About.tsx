/*
 * Design: Amber Glass Atelier
 * About section — full bio with secondary photo. Glass panels, warm amber accents.
 */
import { useInView } from "@/hooks/useInView";

const SECONDARY_PHOTO = "https://files.manuscdn.com/user_upload_by_module/session_file/310419663032705003/jxxwYcKDntcRofOG.jpeg";

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
      {/* Subtle ambient glow */}
      <div
        className="absolute top-0 right-0 w-[500px] h-[500px] opacity-10 pointer-events-none"
        style={{
          background: "radial-gradient(circle, rgba(234, 88, 12, 0.3) 0%, transparent 70%)",
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
            <p className="text-amber-400 font-medium text-sm tracking-widest uppercase mb-2">
              About Me
            </p>
            <h2 className="font-serif text-3xl md:text-4xl lg:text-5xl text-warm-50 mb-4">
              The Story So Far
            </h2>
            <div className="gold-line w-24" />
          </div>

          <div className="flex flex-col lg:flex-row gap-10 lg:gap-16 items-start">
            {/* Photo Column */}
            <div className="flex-shrink-0 w-full lg:w-auto flex justify-center lg:justify-start">
              <div className="relative w-56 h-72 md:w-64 md:h-80 rounded-xl overflow-hidden glass-panel shadow-xl shadow-amber-900/10">
                <img
                  src={SECONDARY_PHOTO}
                  alt="Audrey Evans in a purple sequin and satin gown against a mountain sunset"
                  className="w-full h-full object-cover object-top"
                  loading="lazy"
                />
              </div>
            </div>

            {/* Bio Content */}
            <div className="flex-1 space-y-5">
              <p className="text-warm-200 text-base md:text-lg leading-relaxed">
                Audrey Evans is a proud and responsible Native Hawaiian with over three decades of
                experience in information technology. Her career spans the full spectrum of the tech
                industry — from software engineering and database architecture to geospatial engineering,
                data science, business intelligence, and program/project management.
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
                is a published author on SSRN, a published musician performing as Revvel and Hailstorm,
                a Paralegal De Facto in Colorado, and a CLE instructor/sponsor for the Colorado Supreme
                Court and Orange County DA Criminal Division.
              </p>
              <p className="text-warm-300 text-base md:text-lg leading-relaxed">
                As the founder of Freedom Angel Corps, Audrey dedicates herself to retraining trafficking
                survivors and providing peer support. With over 20 years of volunteer service spanning
                animal rescue, veterans' support, children's advocacy, domestic violence, trafficking
                awareness, and homelessness — her mission is clear: rescue, retrain, reinvent, and restore.
              </p>

              {/* Stats Grid */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-6">
                {highlights.map((item) => (
                  <div
                    key={item.label}
                    className="glass-panel p-4 text-center"
                  >
                    <div className="font-serif text-2xl md:text-3xl text-amber-400 mb-1">
                      {item.value}
                    </div>
                    <div className="text-warm-400 text-xs md:text-sm font-medium">
                      {item.label}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
