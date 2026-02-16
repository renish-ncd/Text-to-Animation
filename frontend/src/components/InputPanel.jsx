import { useState, useEffect } from 'react';

const SUGGESTIONS = [
  'Detailed cherry blossom tree with falling petals and wind',
  'Cyberpunk city street with neon rain and glowing signs',
  'Cosmic nebula with swirling stars and 3D depth',
  'Liquid metal morphing sphere with reflective surface',
  'Isometric 3D room with floating furniture and lighting',
  'Matrix digital rain with glowing green characters',
];

export default function InputPanel({ onGenerate, isLoading }) {
  const [prompt, setPrompt] = useState('');
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const saved = localStorage.getItem('prompt_history');
    if (saved) {
      setHistory(JSON.parse(saved));
    }
  }, []);

  const saveToHistory = (text) => {
    const newHistory = [text, ...history.filter(h => h !== text)].slice(0, 10);
    setHistory(newHistory);
    localStorage.setItem('prompt_history', JSON.stringify(newHistory));
  };

  const handleSubmit = () => {
    if (prompt.trim() && !isLoading) {
      saveToHistory(prompt.trim());
      onGenerate(prompt.trim());
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      handleSubmit();
    }
  };

  const handleSuggestionClick = (text) => {
    setPrompt(text);
  };

  return (
    <div className="input-panel">
      <div className="input-panel-header">
        <span className="icon">✨</span>
        <h2>Describe Your Animation</h2>
      </div>

      <div className="prompt-area">
        <textarea
          className="prompt-textarea"
          placeholder="Describe the animation you want to create in detail...&#10;&#10;Example: A majestic oak tree with textured bark, swaying branches, and hundreds of individual leaves falling in the wind..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
        />
        
        <div className="prompt-footer">
          <span className="char-count">{prompt.length} chars</span>
        </div>
      </div>

      <div className="suggestions">
        {SUGGESTIONS.map((text, i) => (
          <button
            key={i}
            className="suggestion-chip"
            onClick={() => handleSuggestionClick(text)}
            disabled={isLoading}
          >
            {text}
          </button>
        ))}
      </div>

      {history.length > 0 && (
        <div className="history-section">
          <div className="input-panel-header" style={{ marginTop: '20px', marginBottom: '10px' }}>
            <span className="icon">🕒</span>
            <h2>Recent</h2>
          </div>
          <div className="suggestions">
            {history.map((text, i) => (
              <button
                key={`hist-${i}`}
                className="suggestion-chip history-chip"
                onClick={() => handleSuggestionClick(text)}
                disabled={isLoading}
                title={text}
              >
                {text.length > 50 ? text.substring(0, 50) + '...' : text}
              </button>
            ))}
          </div>
        </div>
      )}

      <button 
        className="generate-btn"
        onClick={handleSubmit}
        disabled={isLoading || !prompt.trim()}
      >
        {isLoading ? (
          <>
            <div className="spinner" />
            Dreaming up your animation...
          </>
        ) : (
          <>
            <span>🚀</span> Generate Animation
          </>
        )}
      </button>
    </div>
  );
}
