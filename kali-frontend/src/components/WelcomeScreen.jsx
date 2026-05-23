import './WelcomeScreen.css';

const SUGGESTIONS = [
  "Build a task management mobile app with local SQLite storage.",
  "Design a SaaS landing page for an AI image generator.",
  "Plan a Chrome extension that summarizes YouTube videos.",
];

export default function WelcomeScreen({ projectName, onSend }) {
  return (
    <div className="welcome-screen animate-in">
      <div className="welcome-center">
        <div className="pulsing-logo">✺</div>
        <h1 className="welcome-title font-sans">
          Namaste, I am <span className="gradient-text">Kali</span>
        </h1>
        <p className="welcome-subtitle">
          Your personal local AI companion. Let's build your next software idea.
        </p>

        <div className="suggestions-grid">
          {SUGGESTIONS.map((s, idx) => (
            <button
              key={idx}
              className="suggestion-card glass"
              onClick={() => onSend(s)}
            >
              <div className="suggestion-icon">💡</div>
              <p className="suggestion-text">{s}</p>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
