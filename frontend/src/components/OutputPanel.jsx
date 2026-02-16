import ToggleTabs from './ToggleTabs';
import CodeViewer from './CodeViewer';
import PreviewFrame from './PreviewFrame';

export default function OutputPanel({ generatedHtml, activeTab, onTabChange, isLoading }) {
  return (
    <div className="output-panel">
      <ToggleTabs activeTab={activeTab} onTabChange={onTabChange} />

      {isLoading ? (
        <div className="loading-skeleton">
          <div className="skeleton-line" />
          <div className="skeleton-line" />
          <div className="skeleton-line" />
          <div className="skeleton-line" />
          <div className="skeleton-line" />
          <div className="skeleton-line" />
          <div className="skeleton-line" />
          <div className="skeleton-line" />
        </div>
      ) : (
        <>
          {activeTab === 'code' && <CodeViewer code={generatedHtml} />}
          {activeTab === 'preview' && <PreviewFrame html={generatedHtml} />}
        </>
      )}
    </div>
  );
}
