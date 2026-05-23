import './TypingIndicator.css';

export default function TypingIndicator() {
  return (
    <div className="typing-wrapper animate-in">
      <div className="avatar kali-avatar">✺</div>
      <div className="typing-bubble">
        <span className="dot" style={{ animationDelay: '0ms' }} />
        <span className="dot" style={{ animationDelay: '150ms' }} />
        <span className="dot" style={{ animationDelay: '300ms' }} />
      </div>
    </div>
  );
}
