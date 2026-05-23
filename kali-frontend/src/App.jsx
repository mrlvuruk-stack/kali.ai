import { useState, useRef, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import LootCratePanel from './components/LootCratePanel';
import Header from './components/Header';
import './App.css';

const INITIAL_PROJECTS = [
  { id: 1, name: 'Default Project', sessions: [
    { id: 1, name: 'General Chat' },
    { id: 2, name: 'App Ideas' }
  ]},
  { id: 2, name: 'Task Manager App', sessions: [
    { id: 3, name: 'Planning' }
  ]}
];

export default function App() {
  const [projects, setProjects] = useState(INITIAL_PROJECTS);
  const [activeProjectId, setActiveProjectId] = useState(1);
  const [activeSessionId, setActiveSessionId] = useState(1);
  const [mode, setMode] = useState('chat'); // 'chat' | 'lootcrate'
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const activeProject = projects.find(p => p.id === activeProjectId);

  const addProject = () => {
    const newId = Date.now();
    const newProject = {
      id: newId,
      name: `Project ${projects.length + 1}`,
      sessions: [{ id: Date.now() + 1, name: 'General Chat' }]
    };
    setProjects(prev => [newProject, ...prev]);
    setActiveProjectId(newId);
    setActiveSessionId(newProject.sessions[0].id);
  };

  const addSession = () => {
    const proj = projects.find(p => p.id === activeProjectId);
    const newSession = { id: Date.now(), name: `Chat ${proj.sessions.length + 1}` };
    setProjects(prev => prev.map(p =>
      p.id === activeProjectId ? { ...p, sessions: [newSession, ...p.sessions] } : p
    ));
    setActiveSessionId(newSession.id);
  };

  return (
    <div className="app-shell">
      {/* Ambient Orbs */}
      <div className="gradient-orb orb-1" />
      <div className="gradient-orb orb-2" />
      <div className="gradient-orb orb-3" />

      {/* Sidebar */}
      <Sidebar
        open={sidebarOpen}
        projects={projects}
        activeProjectId={activeProjectId}
        activeSessionId={activeSessionId}
        mode={mode}
        onSelectProject={setActiveProjectId}
        onSelectSession={setActiveSessionId}
        onAddProject={addProject}
        onAddSession={addSession}
        onModeChange={setMode}
      />

      {/* Main Content */}
      <div className={`main-content ${!sidebarOpen ? 'sidebar-collapsed' : ''}`}>
        <Header
          sidebarOpen={sidebarOpen}
          onToggleSidebar={() => setSidebarOpen(o => !o)}
          mode={mode}
          projectName={activeProject?.name}
        />

        {mode === 'chat' ? (
          <ChatArea
            sessionId={activeSessionId}
            projectName={activeProject?.name}
            onLootCrateDetected={() => setMode('lootcrate')}
          />
        ) : (
          <LootCratePanel
            projectName={activeProject?.name}
            sessionId={activeSessionId}
            onBack={() => setMode('chat')}
          />
        )}
      </div>
    </div>
  );
}
