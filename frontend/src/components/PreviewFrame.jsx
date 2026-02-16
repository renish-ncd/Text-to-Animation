import { useRef, useState, useCallback } from 'react';
import { generateGif } from '../services/apiService';

export default function PreviewFrame({ html }) {
  const iframeRef = useRef(null);
  const [isRecording, setIsRecording] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleRefresh = () => {
    setRefreshKey((k) => k + 1);
  };

  const handleDownloadGif = useCallback(async () => {
    if (!html || isRecording) return;

    setIsRecording(true);

    try {
      // detailed HTML needs to be sent to backend
      const blob = await generateGif(html);
      
      // Create download link
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `animation-${Date.now()}.gif`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('GIF generation failed:', err);
      alert(`Failed to generate GIF: ${err.message}`);
    } finally {
      setIsRecording(false);
    }
  }, [html, isRecording]);

  if (!html) {
    return (
      <div className="empty-state">
        <span className="empty-icon">▶</span>
        <h3>No Preview Available</h3>
        <p>Generate an animation to see the live preview here.</p>
      </div>
    );
  }

  return (
    <div className="preview-frame">
      <div className="preview-toolbar">
        <button
          className="preview-action-btn refresh-btn"
          onClick={handleRefresh}
          disabled={isRecording}
          title="Refresh preview"
          id="refresh-btn"
        >
          🔄 Refresh
        </button>
        <button
          className={`preview-action-btn download-gif-btn ${isRecording ? 'recording' : ''}`}
          onClick={handleDownloadGif}
          disabled={isRecording}
          title="Download as GIF"
          id="download-gif-btn"
        >
          {isRecording ? (
            <>
              <span className="spinner small" />
              Generating GIF via Backend...
            </>
          ) : (
            <>🎞️ Download GIF (High Quality)</>
          )}
        </button>
      </div>

      <div className="preview-container">
        <iframe
          key={refreshKey}
          ref={iframeRef}
          className="preview-iframe"
          sandbox="allow-scripts"
          srcDoc={html}
          title="Animation Preview"
          id="preview-iframe"
        />
      </div>
    </div>
  );
}
