import './Header.css';

export default function Header({ sidebarOpen, onToggleSidebar, mode, projectName }) {
  return (
    <header className="header glass">
      <div className="header-left">
        <button className="toggle-btn" onClick={onToggleSidebar}>
          {sidebarOpen ? '◀' : '▶'}
        </button>
        <div className="breadcrumb">
          <span className="breadcrumb-project">{projectName}</span>
          <span className="breadcrumb-sep">›</span>
          <span className={`breadcrumb-mode ${mode}`}>
            {mode === 'chat' ? '✺ Kali Chat' : '🎁 Loot Crate'}
          </span>
        </div>
      </div>
      <div className="header-right">
        <div className="model-badges">
          <span className="badge badge-ollama">⚡ Ollama</span>
          <span className="badge badge-gemini">✨ Gemini</span>
        </div>
      </div>
    </header>
  );
}
