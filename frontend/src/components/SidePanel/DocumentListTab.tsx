"use client";

import { useEffect, useState } from 'react';
import { Document } from '@/lib/types';
import { formatDate, formatFileSize, truncateText } from '@/lib/utils';
import api from '@/lib/api';

interface DocumentListTabProps {
  onDocumentDeleted?: () => void;
}

export default function DocumentListTab({ onDocumentDeleted }: DocumentListTabProps) {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const data = await api.getDocuments();
      setDocuments(data);
    } catch (err) {
      console.error('Error loading documents:', err);
      setError('Failed to load documents. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this document?')) {
      return;
    }
    
    try {
      await api.deleteDocument(id);
      // Update list by filtering out the deleted document
      setDocuments(documents.filter(doc => doc.id !== id));
      // Notify parent that documents have changed
      if (onDocumentDeleted) {
        onDocumentDeleted();
      }
    } catch (err) {
      console.error('Error deleting document:', err);
      alert('Failed to delete document. Please try again.');
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(text);
    setTimeout(() => setCopiedId(null), 2000); // Reset copied state after 2 seconds
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-40">
        <div className="animate-spin rounded-full h-10 w-10 border-4 border-blue-500 border-t-transparent"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-200 text-red-700 px-4 py-3 rounded-md">
        {error}
      </div>
    );
  }

  if (documents.length === 0) {
    return (
      <div className="text-center py-6">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 className="text-lg font-medium text-gray-900 mb-1">No documents found</h3>
        <p className="text-gray-500 text-sm">
          Upload a new document or process a URL to get started.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4 max-h-[400px] overflow-y-auto">
      {documents.map((doc) => (
        <div key={doc.id} className="border rounded-md p-3 bg-gray-50 relative hover:bg-gray-100 transition-colors">
          <button
            onClick={() => handleDelete(doc.id)}
            className="absolute top-2 right-2 text-gray-400 hover:text-red-600"
            title="Delete document"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </button>
          
          <h3 className="font-medium text-gray-900 mb-1">
            {doc.title || doc.filename || 'Untitled Document'}
          </h3>
          
          {/* Document ID with Copy Button */}
          <div className="flex items-center mb-1">
            <span className="text-xs text-gray-500 mr-1">ID:</span>
            <span className="text-xs text-gray-500 truncate max-w-[160px]">{doc.id}</span>
            <button
              onClick={() => copyToClipboard(doc.id)}
              className="ml-1 text-blue-600 hover:text-blue-800"
              title="Copy ID"
            >
              {copiedId === doc.id ? (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
                  <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
                </svg>
              )}
            </button>
          </div>
          
          {doc.description && (
            <p className="text-sm text-gray-500 mb-2">
              {truncateText(doc.description, 100)}
            </p>
          )}
          
          <div className="flex flex-wrap gap-2 mt-2">
            {doc.mime_type && (
              <span className="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-200 text-gray-800">
                {doc.mime_type}
              </span>
            )}
            
            {typeof doc.file_size === 'number' && (
              <span className="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-200 text-gray-800">
                {formatFileSize(doc.file_size)}
              </span>
            )}
            
            <span className={`inline-flex items-center px-2 py-1 rounded text-xs 
              ${doc.is_indexed 
                ? 'bg-blue-100 text-blue-800' 
                : 'bg-yellow-100 text-yellow-800'}`}
            >
              {doc.is_indexed ? 'Indexed' : 'Processing'}
            </span>
          </div>
          
          <div className="text-xs text-gray-500 mt-2">
            Added: {formatDate(doc.created_at)}
          </div>
        </div>
      ))}
    </div>
  );
}
