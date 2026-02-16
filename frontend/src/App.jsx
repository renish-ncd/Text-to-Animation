import { useState } from 'react';
import InputPanel from './components/InputPanel';
import OutputPanel from './components/OutputPanel';
import { generateAnimation } from './services/apiService';

export default function App() {
  const [generatedHtml, setGeneratedHtml] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('code');

  const handleGenerate = async (prompt) => {
    setIsLoading(true);
    setError('');
    setGeneratedHtml('');

    try {
      const html = await generateAnimation(prompt);
      setGeneratedHtml(html);
      setActiveTab('preview'); // Auto-switch to preview on success
    } catch (err) {
      setError(err.message || 'Failed to generate animation. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="logo">
          <div className="logo-icon">⚡</div>
          <h1>AnimateAI</h1>
          <span className="logo-badge">Powered by Groq</span>
        </div>
      </header>

      <main className="app-main">
        <InputPanel onGenerate={handleGenerate} isLoading={isLoading} />
        <OutputPanel
          generatedHtml={generatedHtml}
          activeTab={activeTab}
          onTabChange={setActiveTab}
          isLoading={isLoading}
        />
      </main>

      {error && (
        <div className="error-banner" style={{ margin: '0 24px 16px' }}>
          <span className="error-icon">⚠️</span>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}
