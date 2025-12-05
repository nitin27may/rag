"use client";

import { SourceListProps } from '@/lib/types';
import { formatDate } from '@/lib/utils';

export default function SourceList({ sources, onDelete, isLoading }: SourceListProps) {
  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64 bg-white rounded-lg border p-6">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        <span className="ml-3 text-gray-500 font-medium">Loading data sources...</span>
      </div>
    );
  }

  if (sources.length === 0) {
    return (
      <div className="bg-white rounded-lg border p-6 text-center">
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          className="h-12 w-12 text-gray-400 mx-auto mb-4" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            strokeWidth={1.5} 
            d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" 
          />
        </svg>
        <h3 className="text-lg font-medium text-gray-900 mb-1">No data sources found</h3>
        <p className="text-gray-500">
          Add a new data source to get started.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border overflow-hidden">
      <div className="p-4 bg-gray-50 border-b flex justify-between items-center">
        <h2 className="text-lg font-medium text-gray-900">Data Sources</h2>
        <span className="text-sm text-gray-500">{sources.length} sources</span>
      </div>
      
      <div className="divide-y">
        {sources.map((source) => (
          <div key={source.id} className="p-4 hover:bg-gray-50">
            <div className="flex justify-between">
              <div className="flex-1 pr-4">
                <h3 className="text-lg font-medium text-gray-900 mb-1">{source.name}</h3>
                
                <div className="flex flex-wrap gap-2 text-xs text-gray-500 mt-2">
                  <span className="inline-flex items-center px-2 py-1 rounded-md bg-gray-100">
                    Type: {source.source_type}
                  </span>
                  
                  <span className="inline-flex items-center px-2 py-1 rounded-md bg-gray-100">
                    Added: {formatDate(source.created_at)}
                  </span>
                  
                  {source.last_sync && (
                    <span className="inline-flex items-center px-2 py-1 rounded-md bg-gray-100">
                      Last synced: {formatDate(source.last_sync)}
                    </span>
                  )}
                  
                  <span className={`inline-flex items-center px-2 py-1 rounded-md ${
                    source.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {source.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                
                <div className="mt-3 p-2 bg-gray-50 rounded text-xs font-mono overflow-x-auto">
                  <pre className="whitespace-pre-wrap break-all">
                    {JSON.stringify(source.connection_details, null, 2)}
                  </pre>
                </div>
              </div>
              
              <div className="flex items-start">
                <button
                  onClick={() => onDelete(source.id)}
                  className="text-red-600 hover:text-red-800 p-1"
                  title="Delete data source"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}