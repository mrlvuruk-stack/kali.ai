import './Sidebar.css';

const MODE_ITEMS = [
  { id: 'chat', icon: '✺', label: 'Kali Chat', color: 'var(--kali-purple)' },
  { id: 'lootcrate', icon: '🎁', label: 'Loot Crate', color: 'var(--kali-orange)' },
];

export default function Sidebar({
  open, projects, activeProjectId, activeSessionId, mode,
  onSelectProject, onSelectSession, onAddProject, onAddSession, onModeChange
}) {
  const activeProject = projects.find(p => p.id === activeProjectId);

  return (
    <aside className={`sidebar ${open ? 'open' : 'closed'}`}>
      {/* Logo */}
      <div className="sidebar-logo">
        <div className="logo-icon">✺</div>
        <div className="logo-text">
          <span className="logo-name gradient-text">Kali</span>
          <span className="logo-sub">AI Workspace</span>
        </div>
      </div>

      {/* Mode Switcher */}
      <div className="sidebar-section">
        <p className="section-label">MODE</p>
        <div className="mode-switcher">
          {MODE_ITEMS.map(item => (
            <button
              key={item.id}
              className={`mode-btn ${mode === item.id ? 'active' : ''}`}
              style={{ '--accent': item.color }}
              onClick={() => onModeChange(item.id)}
            >
              <span className="mode-icon">{item.icon}</span>
              <span>{item.label}</span>
              {mode === item.id && <div className="mode-active-dot" style={{ background: item.color }} />}
            </button>
          ))}
        </div>
      </div>

      <div className="sidebar-divider" />

      {/* Projects */}
      <div className="sidebar-section flex-1">
        <div className="section-header">
          <p className="section-label">PROJECTS</p>
          <button className="icon-btn" onClick={onAddProject} title="New Project">+</button>
        </div>
        <div className="projects-list">
          {projects.map(proj => (
            <div key={proj.id} className="project-item">
              <button
                className={`project-btn ${proj.id === activeProjectId ? 'active' : ''}`}
                onClick={() => {
                  onSelectProject(proj.id);
                  onSelectSession(proj.sessions[0]?.id);
                }}
              >
                <span className="proj-dot" style={{
                  background: `hsl(${(proj.id * 60) % 360}, 70%, 60%)`
                }} />
                <span className="proj-name">{proj.name}</span>
              </button>

              {/* Sessions under active project */}
              {proj.id === activeProjectId && (
                <div className="sessions-list">
                  {proj.sessions.map(sess => (
                    <button
                      key={sess.id}
                      className={`session-btn ${sess.id === activeSessionId ? 'active' : ''}`}
                      onClick={() => onSelectSession(sess.id)}
                    >
                      <span className="sess-icon">💬</span>
                      <span>{sess.name}</span>
                    </button>
                  ))}
                  <button className="new-session-btn" onClick={onAddSession}>
                    <span>＋</span> New Chat
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="sidebar-divider" />

      {/* Footer */}
      <div className="sidebar-footer">
        <div className="status-badge">
          <div className="status-dot pulse-green" />
          <span>Ollama Connected</span>
        </div>
        <div className="status-badge">
          <div className="status-dot pulse-blue" />
          <span>Gemini Ready</span>
        </div>
        <div className="version-tag">Kali AI v2.0 · DocBFF</div>
      </div>
    </aside>
  );
}
