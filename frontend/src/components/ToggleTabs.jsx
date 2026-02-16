export default function ToggleTabs({ activeTab, onTabChange }) {
  return (
    <div className="toggle-tabs">
      <button
        className={`tab-btn ${activeTab === 'code' ? 'active' : ''}`}
        onClick={() => onTabChange('code')}
        id="tab-code"
      >
        <span className="tab-icon">{'</>'}</span>
        Generated Code
      </button>
      <button
        className={`tab-btn ${activeTab === 'preview' ? 'active' : ''}`}
        onClick={() => onTabChange('preview')}
        id="tab-preview"
      >
        <span className="tab-icon">▶</span>
        Preview
      </button>
    </div>
  );
}
