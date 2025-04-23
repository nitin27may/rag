"use client";

import { DocumentListProps } from '@/lib/types';
import { formatDate, formatFileSize, truncateText } from '@/lib/utils';
import { useState } from 'react';

export default function DocumentList({ documents, onDelete, isLoading }: DocumentListProps) {
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(text);
    setTimeout(() => setCopiedId(null), 2000); // Reset copied state after 2 seconds
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64 bg-white rounded-lg border p-6">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        <span className="ml-3 text-gray-500 font-medium">Loading documents...</span>
      </div>
    );
  }

  if (documents.length === 0) {
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
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
          />
        </svg>
        <h3 className="text-lg font-medium text-gray-900 mb-1">No documents found</h3>
        <p className="text-gray-500">
          Upload a new document or process a URL to get started.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border overflow-hidden">
      <div className="p-4 bg-gray-50 border-b flex justify-between items-center">
        <h2 className="text-lg font-medium text-gray-900">Documents</h2>
        <span className="text-sm text-gray-500">{documents.length} documents</span>
      </div>
      
      <div className="divide-y">
        {documents.map((doc) => (
          <div key={doc.id} className="p-4 hover:bg-gray-50">
            <div className="flex justify-between">
              <div className="flex-1 pr-4">
                <h3 className="text-lg font-medium text-gray-900 mb-1">{doc.title || doc.filename || 'Untitled'}</h3>
                
                {/* Document ID with Copy Button */}
                <div className="flex items-center mb-2">
                  <span className="text-sm text-gray-500 mr-2">ID: {doc.id}</span>
                  <button
                    onClick={() => copyToClipboard(doc.id)}
                    className="text-blue-600 hover:text-blue-800 p-1"
                    title="Copy ID"
                  >
                    {copiedId === doc.id ? (
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    ) : (
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
                        <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
                      </svg>
                    )}
                  </button>
                </div>
                
                {doc.description && (
                  <p className="text-gray-500 text-sm mb-2">
                    {truncateText(doc.description, 150)}
                  </p>
                )}
                
                <div className="flex flex-wrap gap-2 text-xs text-gray-500 mt-2">
                  {doc.mime_type && (
                    <span className="inline-flex items-center px-2 py-1 rounded-md bg-gray-100">
                      {doc.mime_type}
                    </span>
                  )}
                  
                  {typeof doc.file_size === 'number' && (
                    <span className="inline-flex items-center px-2 py-1 rounded-md bg-gray-100">
                      {formatFileSize(doc.file_size)}
                    </span>
                  )}
                  
                  <span className="inline-flex items-center px-2 py-1 rounded-md bg-gray-100">
                    Added: {formatDate(doc.created_at)}
                  </span>
                  
                  <span className={`inline-flex items-center px-2 py-1 rounded-md ${
                    doc.is_processed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {doc.is_processed ? 'Processed' : 'Processing'}
                  </span>
                  
                  <span className={`inline-flex items-center px-2 py-1 rounded-md ${
                    doc.is_indexed ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {doc.is_indexed ? 'Indexed' : 'Not Indexed'}
                  </span>
                </div>
              </div>
              
              <div className="flex items-start">
                <button
                  onClick={() => onDelete(doc.id)}
                  className="text-red-600 hover:text-red-800 p-1"
                  title="Delete document"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
            
            {doc.processing_error && (
              <div className="mt-2 p-2 bg-red-50 text-red-700 text-sm rounded">
                Error: {doc.processing_error}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}