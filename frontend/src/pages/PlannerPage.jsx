import { useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  MapPin,
  Users,
  Wallet,
  Sparkles,
  X,
} from "lucide-react";
import "./PlannerPage.css";

const interests = [
  "Football",
  "Music",
  "Gaming",
  "Technology",
  "Fashion",
  "Food",
  "Movies",
  "Travel",
  "Fitness",
  "Art",
  "Dance",
  "Photography",
];

function PlannerPage({ onBack , onGenerate}) {
  const [selectedInterests, setSelectedInterests] = useState([]);

  const [formData, setFormData] = useState({
    eventType: "",
    location: "",
    attendees: "",
    budget: "",
    constraints: "",
  });

  const toggleInterest = (interest) => {
    setSelectedInterests((current) =>
      current.includes(interest)
        ? current.filter((item) => item !== interest)
        : [...current, interest]
    );
  };

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    console.log({
      interests: selectedInterests,
      ...formData,
    });

    onGenerate();
  };

  return (
    <div className="planner-page">
      {/* Background */}
      <div className="planner-glow planner-glow-one"></div>
      <div className="planner-glow planner-glow-two"></div>

      {/* Header */}
      <header className="planner-header">
        <button className="back-button"
        onClick={onBack}
        >
          <ArrowLeft size={18} />
          Back
        </button>

        <div className="planner-progress">
          <span className="progress-active"></span>
          <span></span>
          <span></span>
        </div>

        <div className="planner-step">
          Step 1 of 3
        </div>
      </header>

      {/* Main */}
      <main className="planner-container">

        {/* Heading */}
        <section className="planner-intro">
          <div className="planner-label">
            <Sparkles size={15} />
            AUDIENCE PROFILE
          </div>

          <h1>
            Tell us who you're
            <span> designing for.</span>
          </h1>

          <p>
            Your audience's interests help CampusCulture AI create an
            event they'll actually want to attend.
          </p>
        </section>

        <form onSubmit={handleSubmit} className="planner-form">

          {/* Interests */}
          <section className="planner-card">
            <div className="section-heading">
              <div>
                <h2>What are they into?</h2>
                <p>Select everything that describes your audience.</p>
              </div>

              <span className="selection-count">
                {selectedInterests.length} selected
              </span>
            </div>

            <div className="interest-grid">
              {interests.map((interest) => {
                const selected = selectedInterests.includes(interest);

                return (
                  <button
                    type="button"
                    key={interest}
                    className={`interest-chip ${
                      selected ? "selected" : ""
                    }`}
                    onClick={() => toggleInterest(interest)}
                  >
                    {interest}

                    {selected && (
                      <X size={15} />
                    )}
                  </button>
                );
              })}
            </div>
          </section>

          {/* Event details */}
          <section className="planner-card">

            <div className="section-heading">
              <div>
                <h2>Event details</h2>
                <p>Give us the basics of what you're planning.</p>
              </div>
            </div>

            <div className="form-grid">

              {/* Event type */}
              <div className="form-field">
                <label>Event type</label>

                <select
                  name="eventType"
                  value={formData.eventType}
                  onChange={handleChange}
                  required
                >
                  <option value="">
                    Select event type
                  </option>
                  <option value="college-fest">
                    College Fest
                  </option>
                  <option value="sports-event">
                    Sports Event
                  </option>
                  <option value="music-event">
                    Music Event
                  </option>
                  <option value="workshop">
                    Workshop
                  </option>
                  <option value="networking">
                    Networking Event
                  </option>
                  <option value="cultural-event">
                    Cultural Event
                  </option>
                  <option value="other">
                    Other
                  </option>
                </select>
              </div>

              {/* Location */}
              <div className="form-field">
                <label>Location</label>

                <div className="input-with-icon">
                  <MapPin size={18} />

                  <input
                    type="text"
                    name="location"
                    placeholder="e.g. Chandigarh"
                    value={formData.location}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>

              {/* Attendees */}
              <div className="form-field">
                <label>Expected attendees</label>

                <div className="input-with-icon">
                  <Users size={18} />

                  <input
                    type="number"
                    name="attendees"
                    placeholder="e.g. 150"
                    min="1"
                    value={formData.attendees}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>

              {/* Budget */}
              <div className="form-field">
                <label>Budget</label>

                <div className="input-with-icon">
                  <Wallet size={18} />

                  <input
                    type="number"
                    name="budget"
                    placeholder="e.g. 75000"
                    min="0"
                    value={formData.budget}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>

            </div>
          </section>

          {/* Constraints */}
          <section className="planner-card">

            <div className="section-heading">
              <div>
                <h2>Any constraints?</h2>
                <p>
                  Tell the AI anything it should keep in mind.
                </p>
              </div>

              <span className="optional-label">
                Optional
              </span>
            </div>

            <textarea
              name="constraints"
              value={formData.constraints}
              onChange={handleChange}
              placeholder="e.g. Outdoor event, evening only, vegetarian food, no alcohol..."
              rows="4"
            />

          </section>

          {/* Submit */}
          <div className="planner-actions">

            <div className="form-summary">
              <span>
                {selectedInterests.length} interests selected
              </span>

              <span>•</span>

              <span>
                Ready to generate
              </span>
            </div>

            <button
              type="submit"
              className="generate-button"
            >
              Generate Blueprint
              <ArrowRight size={19} />
            </button>

          </div>

        </form>
      </main>
    </div>
  );
}

export default PlannerPage;