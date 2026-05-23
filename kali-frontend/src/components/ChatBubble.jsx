import './ChatBubble.css';

// Simple markdown-like renderer
function renderContent(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br/>');
}

export default function ChatBubble({ message, onSwitch }) {
  const isUser = message.role === 'user';
  const time = message.ts?.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  return (
    <div className={`bubble-wrapper ${isUser ? 'user' : 'assistant'} animate-in`}>
      {!isUser && (
        <div className="avatar kali-avatar">✺</div>
      )}
      <div className={`bubble ${isUser ? 'bubble-user' : 'bubble-assistant'} ${message.isError ? 'bubble-error' : ''} ${message.isNudge ? 'bubble-nudge' : ''}`}>
        <div
          className="bubble-content"
          dangerouslySetInnerHTML={{ __html: renderContent(message.content) }}
        />
        {message.isNudge && onSwitch && (
          <button className="nudge-btn" onClick={onSwitch}>
            🎁 Open Loot Crate Mode
          </button>
        )}
        <span className="bubble-time">{time}</span>
      </div>
      {isUser && (
        <div className="avatar user-avatar">U</div>
      )}
    </div>
  );
}
