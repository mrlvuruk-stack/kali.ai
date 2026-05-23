import { useState, useRef, useEffect } from 'react';
import ChatBubble from './ChatBubble';
import TypingIndicator from './TypingIndicator';
import InputBar from './InputBar';
import WelcomeScreen from './WelcomeScreen';
import { sendToGemini } from '../services/geminiService';
import './ChatArea.css';

const DOC_TRIGGERS = ['prd', 'trd', 'drd', 'documentation', 'document', 'docs',
  'banana hai', 'app banana', 'build', 'loot crate', 'architecture', 'project plan'];

export default function ChatArea({ sessionId, projectName, onLootCrateDetected }) {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    setMessages([]);
  }, [sessionId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const sendMessage = async (text) => {
    if (!text.trim()) return;

    const userMsg = { id: Date.now(), role: 'user', content: text, ts: new Date() };
    setMessages(prev => [...prev, userMsg]);
    setIsTyping(true);

    // Check if DOC_GEN trigger
    const lowerText = text.toLowerCase();
    const isDocRequest = DOC_TRIGGERS.some(t => lowerText.includes(t));

    try {
      const response = await sendToGemini(text, messages);
      const assistantMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response,
        ts: new Date()
      };
      setMessages(prev => [...prev, assistantMsg]);

      // Auto-detect if user wants doc generation
      if (isDocRequest) {
        setTimeout(() => {
          const nudge = {
            id: Date.now() + 2,
            role: 'assistant',
            content: '🎁 **Lagta hai tum ek project plan chahte ho!** Kya main tumhare liye poora **Loot Crate** generate karun? (PRD + TRD + DRD + QA docs)\n\nAbhi **Loot Crate mode** switch karo ya yahan continue karo.',
            ts: new Date(),
            isNudge: true,
            onSwitch: onLootCrateDetected
          };
          setMessages(prev => [...prev, nudge]);
        }, 800);
      }
    } catch (err) {
      const errMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        content: '⚠️ Connection error. Make sure Ollama is running locally or Gemini API key is configured.',
        ts: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="chat-area">
      {messages.length === 0 ? (
        <WelcomeScreen projectName={projectName} onSend={sendMessage} />
      ) : (
        <div className="messages-container">
          {messages.map(msg => (
            <ChatBubble key={msg.id} message={msg} onSwitch={msg.onSwitch} />
          ))}
          {isTyping && <TypingIndicator />}
          <div ref={bottomRef} />
        </div>
      )}
      <InputBar onSend={sendMessage} disabled={isTyping} />
    </div>
  );
}
