import { useState } from 'react';
import './InputBar.css';

export default function InputBar({ onSend, disabled }) {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!text.trim() || disabled) return;
    onSend(text);
    setText('');
  };

  return (
    <form className="input-bar-form" onSubmit={handleSubmit}>
      <div className="input-container glass">
        <input
          type="text"
          placeholder="Apne software idea ke baare mein baat karo..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={disabled}
          className="chat-input"
        />
        <button
          type="submit"
          disabled={!text.trim() || disabled}
          className="send-btn"
          style={{
            background: text.trim() ? 'var(--grad-main)' : 'var(--bg-card)',
            color: text.trim() ? '#fff' : 'var(--text-muted)'
          }}
        >
          ➔
        </button>
      </div>
    </form>
  );
}
