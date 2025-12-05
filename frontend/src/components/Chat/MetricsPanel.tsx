interface MetricsPanelProps {
  metrics: {
    total_time_seconds?: number;
    retrieval_time_seconds?: number;
    generation_time_seconds?: number;
    total_documents?: number;
  } | null;
}

export default function MetricsPanel({ metrics }: MetricsPanelProps) {
  if (!metrics) {
    return (
      <div className="bg-white border rounded-lg p-4 text-gray-500 text-sm">
        No metrics available yet.
      </div>
    );
  }

  return (
    <div className="bg-white border rounded-lg overflow-hidden">
      <div className="bg-gray-600 text-white p-3 font-medium flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 0l-2 2a1 1 0 101.414 1.414L8 10.414l1.293 1.293a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
        </svg>
        Response Metrics
      </div>
      <div className="p-4 text-sm text-gray-600 space-y-2">
        <div className="flex justify-between">
          <span>Total Time:</span>
          <span className="font-medium">{metrics.total_time_seconds?.toFixed(2) || 'N/A'} seconds</span>
        </div>
        <div className="flex justify-between">
          <span>Retrieval Time:</span>
          <span className="font-medium">{metrics.retrieval_time_seconds?.toFixed(2) || 'N/A'} seconds</span>
        </div>
        <div className="flex justify-between">
          <span>Generation Time:</span>
          <span className="font-medium">{metrics.generation_time_seconds?.toFixed(2) || 'N/A'} seconds</span>
        </div>
        <div className="flex justify-between">
          <span>Retrieved Documents:</span>
          <span className="font-medium">{metrics.total_documents || 0}</span>
        </div>
      </div>
    </div>
  );
}