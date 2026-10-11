import {
  ArrowLeft,
  ArrowRight,
  Sparkles,
  Music,
  Zap,
  Utensils,
  Wallet,
  RefreshCw,
  Users,
  MapPin,
  Check,
} from "lucide-react";

import "./ResultsPage.css";

function ResultsPage({ onBack, onRegenerate }) {
  return (
    <div className="results-page">

      {/* TOP BAR */}
      <header className="results-header">
        <button className="results-back" onClick={onBack}>
          <ArrowLeft size={17} />
          Back
        </button>

        <div className="results-brand">
          <Sparkles size={17} />
          CampusCulture <span>AI</span>
        </div>

        <div className="mock-badge">
          MOCK PREVIEW
        </div>
      </header>


      {/* HERO */}
      <main className="results-container">

        <section className="results-intro">

          <div className="results-eyebrow">
            <Sparkles size={15} />
            YOUR EVENT BLUEPRINT
          </div>

          <h1>
            Built around your{" "}
            <span>audience.</span>
          </h1>

          <p>
            A complete event concept designed from the cultural
            interests you selected.
          </p>

          <div className="audience-summary">

            <div className="summary-item">
              <Users size={16} />
              <span>150 attendees</span>
            </div>

            <div className="summary-item">
              <MapPin size={16} />
              <span>Chandigarh</span>
            </div>

            <div className="summary-item">
              <Wallet size={16} />
              <span>₹75,000 budget</span>
            </div>

          </div>

        </section>


        {/* MAIN THEME CARD */}
        <section className="theme-card">

          <div className="theme-content">

            <div className="theme-label">
              RECOMMENDED EXPERIENCE
            </div>

            <h2>Campus Champions</h2>

            <p className="theme-subtitle">
              Sports × Music × Gaming
            </p>

            <p className="theme-description">
              A high-energy campus experience combining
              competitive sports, live music and interactive
              gaming zones to keep the audience engaged
              throughout the event.
            </p>

            <div className="theme-tags">
              <span>Football</span>
              <span>Music</span>
              <span>Gaming</span>
            </div>

          </div>

          <div className="fit-score">

            <div className="fit-ring">
              <strong>91%</strong>
            </div>

            <span>Audience fit</span>

            <small>
              Strong match
            </small>

          </div>

        </section>


        {/* RECOMMENDATION GRID */}
        <section className="recommendation-grid">

          {/* MUSIC */}
          <div className="recommendation-card">

            <div className="card-icon">
              <Music size={20} />
            </div>

            <div className="card-label">
              MUSIC
            </div>

            <h3>Punjabi Pop</h3>

            <p>
              Punjabi pop with energetic hip-hop
              transitions for peak-event moments.
            </p>

            <div className="card-match">
              <Check size={14} />
              Strong audience match
            </div>

          </div>


          {/* ACTIVITIES */}
          <div className="recommendation-card">

            <div className="card-icon">
              <Zap size={20} />
            </div>

            <div className="card-label">
              ACTIVITIES
            </div>

            <h3>3v3 Football</h3>

            <p>
              Fast tournament-style matches followed
              by an interactive gaming zone.
            </p>

            <div className="card-match">
              <Check size={14} />
              High engagement potential
            </div>

          </div>


          {/* FOOD */}
          <div className="recommendation-card">

            <div className="card-icon">
              <Utensils size={20} />
            </div>

            <div className="card-label">
              FOOD
            </div>

            <h3>Campus Street Food</h3>

            <p>
              Popular street-food stations with
              vegetarian and quick-service options.
            </p>

            <div className="card-match">
              <Check size={14} />
              Easy to serve at scale
            </div>

          </div>


          {/* BUDGET */}
          <div className="recommendation-card">

            <div className="card-icon">
              <Wallet size={20} />
            </div>

            <div className="card-label">
              BUDGET
            </div>

            <h3>₹75,000</h3>

            <p>
              Balanced allocation across activities,
              music, food and event infrastructure.
            </p>

            <div className="budget-bar">
              <span style={{ width: "72%" }}></span>
            </div>

            <small className="budget-note">
              ₹68,000 projected spend
            </small>

          </div>

        </section>


        {/* WHY THIS PLAN */}
        <section className="why-card">

          <div className="why-heading">
            <Sparkles size={18} />
            <div>
              <div className="card-label">
                WHY THIS PLAN?
              </div>

              <h3>
                Designed around your audience signals.
              </h3>
            </div>
          </div>

          <p>
            The selected interests suggest that this audience
            is likely to respond well to a combination of
            competitive activities, music and social
            experiences. The blueprint therefore prioritizes
            participation rather than passive attendance.
          </p>

          <div className="signal-row">

            <div>
              <strong>Sports</strong>
              <span>Core interest</span>
            </div>

            <div>
              <strong>Music</strong>
              <span>Engagement driver</span>
            </div>

            <div>
              <strong>Gaming</strong>
              <span>Social activity</span>
            </div>

          </div>

        </section>


        {/* COMPARISON */}
        <section className="comparison-section">

          <div className="section-heading">
            <div>
              <div className="results-eyebrow">
                <Sparkles size={14} />
                THE DIFFERENCE
              </div>

              <h2>
                Qloo-informed vs generic AI
              </h2>

              <p>
                See how audience-aware planning changes the
                event blueprint.
              </p>
            </div>
          </div>


          <div className="comparison-grid">

            <div className="comparison-card highlighted">

              <div className="comparison-top">
                <span>QLOO-INFORMED PLAN</span>
                <div className="recommended">
                  Recommended
                </div>
              </div>

              <h3>Campus Champions</h3>

              <ul>
                <li>
                  <Check size={15} />
                  Audience-specific theme
                </li>

                <li>
                  <Check size={15} />
                  Culture-aware recommendations
                </li>

                <li>
                  <Check size={15} />
                  Stronger interest alignment
                </li>
              </ul>

            </div>


            <div className="comparison-card">

              <div className="comparison-top">
                <span>GENERIC AI BASELINE</span>
              </div>

              <h3>Campus Fest</h3>

              <ul>
                <li>
                  <Check size={15} />
                  General event format
                </li>

                <li>
                  <Check size={15} />
                  Broad recommendations
                </li>

                <li>
                  <Check size={15} />
                  No audience-specific signals
                </li>
              </ul>

            </div>

          </div>

        </section>


        {/* ACTIONS */}
        <section className="results-actions">

          <button
            className="secondary-result-button"
            onClick={onRegenerate}
          >
            <RefreshCw size={17} />
            Try another plan
          </button>

          <button className="primary-result-button">
            Continue with this plan
            <ArrowRight size={17} />
          </button>

        </section>


        <div className="mock-disclaimer">
          ✦ Preview uses mock recommendations for frontend development.
          Real Qloo-powered results will appear after backend integration.
        </div>

      </main>

    </div>
  );
}

export default ResultsPage;