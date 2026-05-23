import { useState } from 'react';
import { generateLootCrate } from '../services/geminiService';
import './LootCratePanel.css';

export default function LootCratePanel({ projectName, sessionId, onBack }) {
  const [idea, setIdea] = useState('');
  const [generating, setGenerating] = useState(false);
  const [progress, setProgress] = useState('');
  const [docs, setDocs] = useState(null);
  const [activeTab, setActiveTab] = useState('PRD');

  const handleGenerate = async () => {
    if (!idea.trim()) return;
    setGenerating(true);
    setDocs(null);

    try {
      setProgress('Drafting via local concept logic...');
      await new Promise(r => setTimeout(r, 1200));

      setProgress('Polishing through high-performance engine...');
      const result = await generateLootCrate(idea);

      setProgress('Formatting sections...');
      await new Promise(r => setTimeout(r, 800));

      setDocs(result);
    } catch (e) {
      alert("Doc generation failed. Verify network or API settings.");
    } finally {
      setGenerating(false);
      setProgress('');
    }
  };

  const handleDownload = (type, content) => {
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${projectName.toLowerCase().replace(/\s+/g, '_')}_${type.toLowerCase()}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const tabColors = {
    PRD: 'var(--kali-purple)',
    TRD: 'var(--kali-green)',
    DRD: 'var(--kali-yellow)',
    QA: 'var(--kali-red)'
  };

  return (
    <div className="loot-crate-panel">
      <div className="loot-header-row">
        <button className="back-btn" onClick={onBack}>➔ Back to Chat</button>
        <h2 className="panel-title gradient-text-loot">🎁 Loot Crate Generator</h2>
      </div>

      {!docs ? (
        <div className="input-state animate-in">
          <div className="doc-box-decor">
            <span className="decor-icon">📦</span>
          </div>
          <h3>What are you building today?</h3>
          <p>Provide description, platform details, target stack, and features to construct your document package.</p>
          <textarea
            placeholder="Example: A Flutter task manager with offline SQLite sync, modern dark UI, local notifications, and clean architecture..."
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
            disabled={generating}
          />
          <button
            className="generate-action-btn"
            onClick={handleGenerate}
            disabled={!idea.trim() || generating}
          >
            {generating ? (
              <span className="spinner-loader">
                <span className="spin" /> {progress}
              </span>
            ) : (
              '🎁 Generate Documentation Package'
            )}
          </button>
        </div>
      ) : (
        <div className="docs-state animate-in">
          <div className="tabs-header">
            {Object.keys(docs).map(tab => (
              <button
                key={tab}
                className={`tab-selector-btn ${activeTab === tab ? 'active' : ''}`}
                style={{ '--tab-color': tabColors[tab] }}
                onClick={() => setActiveTab(tab)}
              >
                {tab}
              </button>
            ))}
          </div>

          <div className="doc-content-body glass">
            <div className="doc-header">
              <span className="doc-type-badge" style={{ background: tabColors[activeTab] }}>
                {activeTab} Document
              </span>
              <button
                className="export-doc-btn"
                onClick={() => handleDownload(activeTab, docs[activeTab])}
              >
                📥 Download .md
              </button>
            </div>
            <pre className="doc-text">{docs[activeTab]}</pre>
          </div>
        </div>
      )}
    </div>
  );
}
