"use client";

import { useState, useEffect } from 'react';
import DocumentUpload from '@/components/Documents/DocumentUpload';
import DocumentList from '@/components/Documents/DocumentList';
import { Document, UploadDocumentRequest, ProcessUrlRequest } from '@/lib/types';
import api from '@/lib/api';

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch documents on page load
  useEffect(() => {
    fetchDocuments();
  }, []);

  // Fetch documents from API
  const fetchDocuments = async () => {
    try {
      setIsLoading(true);
      const data = await api.getDocuments();
      setDocuments(data);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch documents:', err);
      setError('Failed to load documents. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Handle document upload
  const handleUpload = async (data: UploadDocumentRequest) => {
    try {
      await api.uploadDocument(data);
      fetchDocuments(); // Refresh the list
    } catch (err) {
      console.error('Failed to upload document:', err);
      throw new Error('Failed to upload document');
    }
  };

  // Handle URL processing
  const handleProcessUrl = async (data: ProcessUrlRequest) => {
    try {
      await api.processUrl(data);
      fetchDocuments(); // Refresh the list
    } catch (err) {
      console.error('Failed to process URL:', err);
      throw new Error('Failed to process URL');
    }
  };

  // Handle document deletion
  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this document?')) {
      return;
    }
    
    try {
      await api.deleteDocument(id);
      // Update the local state instead of refetching
      setDocuments(documents.filter(doc => doc.id !== id));
    } catch (err) {
      console.error('Failed to delete document:', err);
      alert('Failed to delete document. Please try again.');
    }
  };

  return (
    <div className="max-w-7xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Document Management</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <div className="space-y-6">
            <DocumentUpload onUpload={handleUpload} onProcessUrl={handleProcessUrl} />
          </div>
        </div>
        
        <div className="lg:col-span-2">
          {error && (
            <div className="bg-red-50 text-red-700 p-4 rounded-md mb-4">
              {error}
            </div>
          )}
          
          <DocumentList 
            documents={documents} 
            onDelete={handleDelete} 
            isLoading={isLoading} 
          />
        </div>
      </div>
    </div>
  );
}
