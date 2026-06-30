/**
 * Home.jsx — Godly Authority Editorial Theme
 * Direct structural port of the Stitch mock (hero / infrastructure grid /
 * bento grid / footer), using Tailwind utility classes exactly as Stitch
 * generated them. Only copy, brand, and nav links are ours — visual
 * structure, spacing, and animation classes are faithful to the mock.
 */
import { useEffect, useRef } from "react";
import GuardianEye from "../assets/GuardianEye.jsx";
import ArchitecturalGrid from "../assets/ArchitecturalGrid.jsx";

const NAV_LINKS = ["MONITOR", "POLICIES", "INSIGHTS"];

export default function Home({ onEnterSession }) {
  const containerRef = useRef(null);

  // Scroll perspective shift — ported from Stitch's vanilla JS
  useEffect(() => {
    function onScroll() {
      const el = containerRef.current;
      if (!el) return;
      const scrolled = window.pageYOffset;
      const rotation = (scrolled * 0.02) % 5;
      el.style.transform = `rotateX(${rotation}deg)`;
    }
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  function scrollToInfrastructure() {
    document
      .getElementById("infrastructure-of-vigilance")
      ?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  return (
    <>
      {/* ── Navigation ── */}
      <nav className="fixed top-0 w-full z-50 glass-nav border-b border-outline-variant/30 flex justify-between items-center px-padding-desktop py-8 transition-all duration-500">
        <div className="font-headline-h2 text-2xl font-bold tracking-tighter text-primary">
          MEETING WATCHDOG
        </div>
        <div className="flex items-center gap-12">
          <div className="hidden md:flex gap-8 font-body-md text-body-md uppercase tracking-widest">
            {NAV_LINKS.map((label, i) => (
              <a
                key={label}
                className={`nav-link ${i === 0 ? "text-primary font-bold" : "text-on-surface-variant"}`}
                href="#"
              >
                {label}
              </a>
            ))}
          </div>
          <div className="flex items-center gap-6">
            <button
              className="material-symbols-outlined text-primary text-2xl hover:scale-110 transition-transform"
              aria-label="Toggle audio"
            >
              graphic_eq
            </button>
            <div className="h-6 w-[1px] bg-outline-variant/50" />
            <button
              className="font-label-caps text-label-caps border border-primary/30 text-primary px-6 py-2 hover:bg-primary hover:text-black transition-all duration-300"
              onClick={onEnterSession}
            >
              OPEN SESSION
            </button>
          </div>
        </div>
      </nav>

      <main ref={containerRef} className="relative z-10 pt-40 perspective-container">

        {/* ── Hero Section ── */}
        <section className="min-h-screen px-padding-desktop flex flex-col justify-center relative overflow-hidden">
          <div className="relative z-10">
            <div className="animate-slide font-label-caps text-label-caps text-authority-blue mb-8">
              REAL-TIME CONTRADICTION DETECTION // LIVE
            </div>
            <h1 className="font-display-hero text-display-hero uppercase animate-heading leading-none">
              <span className="hover-underline">MEETING</span>
              <br />
              <span className="text-outline-variant">WATCHDOG</span>
            </h1>
          </div>

          <div className="godly-grid mt-24 items-end">
            <div className="col-span-12 md:col-span-8 relative aspect-video overflow-hidden group border border-outline-variant/30">
              <GuardianEye className="w-full h-full object-cover grayscale brightness-75 transition-all duration-1000 group-hover:grayscale-0 group-hover:scale-105" />
              <div className="absolute bottom-8 left-8 text-primary">
                <div className="font-label-caps text-label-caps mb-2">SYSTEM SCAN ACTIVE</div>
                <div className="font-headline-h2 text-4xl font-bold">
                  <span className="hover-underline">VIRTUAL GUARDIAN NODE</span>
                </div>
              </div>
            </div>
            <div className="col-span-12 md:col-span-4 flex flex-col justify-between h-full py-4">
              <p className="font-body-lg text-body-lg text-on-surface-variant max-w-sm">
                Real-time AI scans every spoken word against your policy documents.
                Contradictions surface the instant they happen — not in the debrief.
              </p>
              <div className="flex flex-col gap-4">
                <div className="editorial-line" />
                <div className="flex justify-between items-center">
                  <span className="font-label-caps text-label-caps">LATENCY: &lt;1S</span>
                  <span className="font-label-caps text-label-caps text-authority-blue">PROTOCOL: ACTIVE</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── Infrastructure / Vertical Grid Feature ── */}
        <section className="py-margin-section bg-surface-container-lowest">
          <div className="px-padding-desktop mb-24">
            <h2 id="infrastructure-of-vigilance" className="font-headline-h1 text-headline-h1 max-w-4xl leading-tight">
              <span className="hover-underline">THE INFRASTRUCTURE OF VIGILANCE</span>
            </h2>
          </div>
          <div className="godly-grid h-[80vh]">
            <div className="col-span-12 md:col-span-4 relative overflow-hidden h-full">
              <ArchitecturalGrid className="w-full h-full object-cover transition-transform duration-1000 hover:scale-110" />
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent" />
              <div className="absolute bottom-12 left-8 p-4">
                <h3 className="font-headline-h2 text-3xl mb-4">
                  <span className="hover-underline">DEPLOYMENT</span>
                </h3>
                <p className="font-body-md text-on-surface-variant">
                  Live detection across every enterprise meeting room, no extra hardware required.
                </p>
              </div>
            </div>

            <div className="col-span-12 md:col-span-4 bg-surface-container flex flex-col justify-center px-12 border-x border-outline-variant/30">
              <h3 className="font-headline-h2 text-3xl mb-8">
                <span className="hover-underline">ABOUT</span>
              </h3>
              <p className="font-body-md text-on-surface-variant mb-12">
                Meeting Watchdog is an AI contradiction detector for enterprise meetings.
                It listens, cross-references your policy documents, and flags conflicts
                the instant they're spoken — not in the post-meeting debrief.
              </p>
              <button
                className="w-fit px-12 py-4 border border-primary hover:bg-primary hover:text-black transition-all duration-300 font-label-caps text-label-caps"
                onClick={onEnterSession}
              >
                START A SESSION
              </button>
            </div>

            <div className="col-span-12 md:col-span-4 flex flex-col justify-between py-12 px-8">
              <div>
                <h3 className="font-headline-h2 text-3xl mb-4">
                  <button
                    type="button"
                    onClick={scrollToInfrastructure}
                    className="hover-underline bg-transparent border-0 p-0 m-0 cursor-pointer text-inherit font-inherit"
                  >
                    HOW IT WORKS
                  </button>
                </h3>
                <div className="editorial-line mb-8" />
                <div className="space-y-4">
                  <div className="flex justify-between font-label-caps text-label-caps">
                    <span className="text-outline">STEP 01</span>
                    <span>UPLOAD POLICY</span>
                  </div>
                  <div className="flex justify-between font-label-caps text-label-caps">
                    <span className="text-outline">STEP 02</span>
                    <span>START MEETING</span>
                  </div>
                  <div className="flex justify-between font-label-caps text-label-caps">
                    <span className="text-outline">STEP 03</span>
                    <span>CATCH CONTRADICTIONS</span>
                  </div>
                </div>
              </div>
              <div className="relative h-48 overflow-hidden group">
                <div className="absolute inset-0 flex items-center justify-center">
                  <button
                    className="font-label-caps text-label-caps tracking-widest group-hover:scale-110 transition-transform cursor-pointer"
                    onClick={onEnterSession}
                  >
                    OPEN SESSION TERMINAL
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── Bento Intelligence Grid ── */}
        <section className="px-padding-desktop py-margin-section">
          <div className="godly-grid">
            <div className="col-span-12 md:col-span-6 bg-surface-container-high p-12 hover:bg-surface-variant transition-colors duration-500 cursor-pointer">
              <div className="flex justify-between mb-24">
                <span
                  className="material-symbols-outlined text-4xl text-authority-blue"
                  style={{ fontVariationSettings: "'FILL' 1" }}
                >
                  shield
                </span>
                <div className="text-right">
                  <div className="font-label-caps text-label-caps text-tertiary-fixed">POLICY-AWARE</div>
                  <div className="text-[0.6rem] text-outline">LOCAL AUDIO — NO CLOUD MIC</div>
                </div>
              </div>
              <h4 className="font-headline-h1 text-4xl mb-6">
                <span className="hover-underline">REAL-TIME CONTRADICTION DETECTION</span>
              </h4>
              <p className="font-body-md text-on-surface-variant">
                Live speech analysis cross-references every spoken word against your
                policy documents to predict and flag contradictions before they compound.
              </p>
            </div>

            <div className="col-span-12 md:col-span-3 border border-outline-variant/30 p-8 flex flex-col justify-between group">
              <div className="space-y-2">
                <div className="h-1 w-full bg-outline-variant overflow-hidden">
                  <div className="h-full bg-primary w-2/3 group-hover:w-full transition-all duration-1000" />
                </div>
                <div className="flex justify-between font-label-caps text-[0.6rem]">
                  <span>RESPONSE TIME</span>
                  <span>UNDER 1S</span>
                </div>
              </div>
              <div>
                <div className="font-headline-h2 text-6xl font-black opacity-10 mb-4">01</div>
                <div className="font-label-caps text-label-caps">SECOND DETECTION LATENCY</div>
              </div>
            </div>

            <div className="col-span-12 md:col-span-3 bg-authority-blue p-8 flex flex-col justify-between text-black">
              <span className="material-symbols-outlined text-4xl">psychology</span>
              <div>
                <h5 className="font-headline-h2 text-2xl font-bold mb-4 uppercase">
                  Policy
                  <br />
                  Aware AI
                </h5>
                <p className="font-body-md text-sm">
                  Parses any PDF, DOCX, or TXT policy doc and indexes every rule automatically.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* ── Footer ── */}
      <footer className="w-full relative bottom-0 bg-surface-container-lowest border-t border-outline-variant/50 grid grid-cols-12 gap-gutter-desktop px-padding-desktop py-margin-section overflow-hidden">
        <div className="col-span-12 md:col-span-6 mb-12">
          <div className="font-headline-h1 text-headline-h1 font-black opacity-10 leading-none select-none">
            MEETING WATCHDOG
          </div>
          <p className="mt-8 font-body-md text-on-surface-variant max-w-md">
            Real-time AI contradiction detection for enterprise meetings.
            Catch conflicts the instant they're spoken, not in the debrief.
          </p>
        </div>
        <div className="col-span-12 md:col-span-6 grid grid-cols-2 gap-8">
          <div className="space-y-4">
            <h6 className="font-label-caps text-label-caps text-primary border-b border-outline-variant/30 pb-2">
              PRODUCT
            </h6>
            <ul className="space-y-2 font-body-md text-on-surface-variant">
              <li>
                <a
                  className="hover:text-primary transition-opacity duration-300"
                  href="#infrastructure-of-vigilance"
                  onClick={(e) => {
                    e.preventDefault();
                    scrollToInfrastructure();
                  }}
                >
                  HOW IT WORKS
                </a>
              </li>
              <li><a className="hover:text-primary transition-opacity duration-300" href="#">POLICIES</a></li>
              <li><a className="hover:text-primary transition-opacity duration-300" href="#">INSIGHTS</a></li>
            </ul>
          </div>
          <div className="space-y-4">
            <h6 className="font-label-caps text-label-caps text-primary border-b border-outline-variant/30 pb-2">
              ACCESS
            </h6>
            <ul className="space-y-2 font-body-md text-on-surface-variant">
              <li><a className="hover:text-primary transition-opacity duration-300" href="#">API DOCUMENTATION</a></li>
              <li><a className="hover:text-primary transition-opacity duration-300" href="#">SYSTEM STATUS</a></li>
              <li>
                <button
                  className="hover:text-primary transition-opacity duration-300 text-left"
                  onClick={onEnterSession}
                >
                  OPEN SESSION
                </button>
              </li>
            </ul>
          </div>
        </div>
        <div className="col-span-12 pt-24 border-t border-outline-variant/20 flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="font-body-md text-body-md opacity-50 uppercase tracking-widest text-[0.7rem]">
            © 2026 MEETING WATCHDOG. CONTRADICTION DETECTION FOR ENTERPRISE MEETINGS.
          </div>
          <div className="flex gap-8">
            <span className="material-symbols-outlined opacity-30 hover:opacity-100 cursor-pointer transition-opacity">public</span>
            <span className="material-symbols-outlined opacity-30 hover:opacity-100 cursor-pointer transition-opacity">lock</span>
            <span className="material-symbols-outlined opacity-30 hover:opacity-100 cursor-pointer transition-opacity">graphic_eq</span>
          </div>
        </div>
      </footer>
    </>
  );
}