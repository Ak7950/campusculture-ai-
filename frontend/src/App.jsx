import { useState } from "react";
import {
  ArrowRight,
  Sparkles,
  Users,
  MapPin,
  Music,
  Palette,
  Zap,
  ChevronDown,
} from "lucide-react";
import "./App.css";
import PlannerPage from "./pages/PlannerPage";
import ResultsPage from "./pages/ResultsPage";
function App() {
  const [page, setPage] = useState("home");

  if (page === "planner") {
  return (
    <PlannerPage
      onBack={() => setPage("home")}
      onGenerate={() => setPage("results")}
    />
  );
}

if (page === "results") {
  return (
    <ResultsPage
      onBack={() => setPage("planner")}
      onRegenerate={() => setPage("planner")}
    />
  );
}

  return (
    <div className="app">
      {/* Navigation */}
      <nav className="navbar">
        <div className="brand">
          <div className="brand-mark">
            <Sparkles size={17} />
          </div>
          <span>CampusCulture</span>
          <span className="brand-ai">AI</span>
        </div>

        <div className="nav-links">
          <a href="#how-it-works">How it works</a>
          <a href="#planner">Planner</a>
        </div>

        <button className="nav-button"
        onClick={() => setPage("planner")}
        >
          Start planning
          <ArrowRight size={16} />
        </button>
      </nav>

      {/* Hero */}
      <main>
        <section className="hero">
          <div className="hero-glow glow-one"></div>
          <div className="hero-glow glow-two"></div>

          <div className="hero-content">
            <div className="eyebrow">
              <Sparkles size={15} />
              <span>Powered by cultural intelligence</span>
            </div>

            <h1>
              Don't plan an event.
              <br />
              <span>Design an experience.</span>
            </h1>

            <p className="hero-description">
              CampusCulture AI transforms your audience's cultural tastes
              into events they'll actually want to attend.
            </p>

            <div className="hero-actions">
              <button className="primary-button"
              onClick={() => setPage("planner")}
              >
                Start planning
                <ArrowRight size={18} />
              </button>

              <button className="secondary-button">
                See how it works
                <ChevronDown size={17} />
              </button>
            </div>

            <div className="hero-trust">
              <div className="trust-item">
                <div className="trust-icon">
                  <Sparkles size={15} />
                </div>
                <span>Qloo-powered</span>
              </div>

              <div className="trust-divider"></div>

              <div className="trust-item">
                <Users size={15} />
                <span>Audience-first</span>
              </div>

              <div className="trust-divider"></div>

              <div className="trust-item">
                <Zap size={15} />
                <span>AI-generated</span>
              </div>
            </div>
          </div>

          {/* Hero visual */}
          <div className="hero-preview">
            <div className="preview-window">
              <div className="preview-topbar">
                <div className="window-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>

                <span className="preview-label">
                  EVENT BLUEPRINT
                </span>

                <div className="preview-status">
                  <span></span>
                  Live
                </div>
              </div>

              <div className="preview-content">
                <div className="preview-heading">
                  <div>
                    <p className="mini-label">BUILT FOR</p>
                    <h3>Campus Champions</h3>
                  </div>

                  <div className="match-score">
                    <span>91%</span>
                    <small>audience fit</small>
                  </div>
                </div>

                <div className="preview-tags">
                  <span>⚽ Football</span>
                  <span>🎵 Music</span>
                  <span>🎮 Gaming</span>
                </div>

                <div className="preview-grid">
                  <div className="preview-card large">
                    <div className="card-icon">
                      <Palette size={17} />
                    </div>
                    <p>THEME</p>
                    <h4>Campus Champions</h4>
                    <span>
                      High-energy sports × music festival
                    </span>
                  </div>

                  <div className="preview-card">
                    <div className="card-icon">
                      <Music size={17} />
                    </div>
                    <p>MUSIC</p>
                    <h4>Punjabi Pop</h4>
                    <span>+ Hip Hop</span>
                  </div>

                  <div className="preview-card">
                    <div className="card-icon">
                      <Zap size={17} />
                    </div>
                    <p>ACTIVITY</p>
                    <h4>3v3 Football</h4>
                    <span>+ DJ Challenge</span>
                  </div>
                </div>

                <div className="preview-footer">
                  <div className="preview-location">
                    <MapPin size={14} />
                    Chandigarh · 150 attendees
                  </div>

                  <div className="preview-budget">
                    ₹68K <span>/ ₹75K</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="floating-card floating-top">
              <Sparkles size={14} />
              <span>Qloo insight</span>
              <strong>+27%</strong>
            </div>

            <div className="floating-card floating-bottom">
              <div className="pulse-dot"></div>
              <span>Audience match</span>
              <strong>Excellent</strong>
            </div>
          </div>
        </section>

        {/* How it works */}
        <section className="how-section" id="how-it-works">
          <div className="section-heading">
            <div className="eyebrow">
              <Sparkles size={14} />
              <span>HOW IT WORKS</span>
            </div>

            <h2>
              From audience insight
              <br />
              <span>to event blueprint.</span>
            </h2>

            <p>
              Tell us who you're designing for. We handle the rest.
            </p>
          </div>

          <div className="steps">
            <div className="step">
              <div className="step-number">01</div>
              <div className="step-icon">
                <Users size={21} />
              </div>
              <h3>Define your audience</h3>
              <p>
                Share their interests, event type, location,
                attendance and budget.
              </p>
            </div>

            <div className="step-line"></div>

            <div className="step">
              <div className="step-number">02</div>
              <div className="step-icon">
                <Sparkles size={21} />
              </div>
              <h3>Discover their culture</h3>
              <p>
                Qloo's Taste Graph identifies cultural affinities
                that matter to your audience.
              </p>
            </div>

            <div className="step-line"></div>

            <div className="step">
              <div className="step-number">03</div>
              <div className="step-icon">
                <Zap size={21} />
              </div>
              <h3>Build the experience</h3>
              <p>
                Our AI turns those signals into a coherent,
                ready-to-use event blueprint.
              </p>
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="bottom-cta" id="planner">
          <div>
            <div className="eyebrow">
              <Sparkles size={14} />
              <span>READY WHEN YOU ARE</span>
            </div>

            <h2>
              Let's build an event
              <br />
              <span>your audience remembers.</span>
            </h2>
          </div>

          <button className="primary-button">
            Start planning
            <ArrowRight size={18} />
          </button>
        </section>
      </main>

      <footer>
        <div className="brand">
          <div className="brand-mark">
            <Sparkles size={15} />
          </div>
          <span>CampusCulture</span>
          <span className="brand-ai">AI</span>
        </div>

        <p>Culture-aware event planning for campus communities.</p>
      </footer>
    </div>
  );
}

export default App;