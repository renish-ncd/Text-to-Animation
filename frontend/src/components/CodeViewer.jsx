import { useState } from 'react';

export default function CodeViewer({ code }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
      const textarea = document.createElement('textarea');
      textarea.value = code;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (!code) {
    return (
      <div className="empty-state">
        <span className="empty-icon">{'</>'}</span>
        <h3>No Code Generated Yet</h3>
        <p>Describe an animation and hit Generate to see the HTML code here.</p>
      </div>
    );
  }

  return (
    <div className="code-viewer">
      <div className="code-viewer-header">
        <span>HTML • {code.split('\n').length} lines</span>
        <button
          className={`copy-btn ${copied ? 'copied' : ''}`}
          onClick={handleCopy}
          id="copy-code-btn"
        >
          {copied ? '✓ Copied!' : '📋 Copy Code'}
        </button>
      </div>
      <div className="code-block">
        <pre><code>{code}</code></pre>
      </div>
    </div>
  );
}
