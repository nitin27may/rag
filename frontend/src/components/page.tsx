"use client";

import { useState, useEffect } from 'react';
import DocumentList from '@/components/Documents/DocumentList';
import DocumentUpload from '@/components/Documents/DocumentUpload';
import { Document, UploadDocumentRequest, ProcessUrlRequest } from '@/lib/types';
import api from '@/lib/api';

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  
  // Fetch documents on component mount
  useEffect(() => {
    fetchDocuments();
  }, []);
  
  // Fetch documents from API
  const fetchDocuments = async () => {
    setIsLoading(true);
    try {
      const docs = await api.getDocuments();
      setDocuments(docs);
    } catch (error) {
      console.error('Error fetching documents:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Upload a document
  const handleUpload = async (data: UploadDocumentRequest) => {
    try {
      await api.uploadDocument(data);
      // Refetch documents after upload
      fetchDocuments();
      return Promise.resolve();
    } catch (error) {
      console.error('Error uploading document:', error);
      return Promise.reject(error);
    }
  };
  
  // Process a URL
  const handleProcessUrl = async (data: ProcessUrlRequest) => {
    try {
      await api.processUrl(data);
      // Refetch documents after processing
      fetchDocuments();
      return Promise.resolve();
    } catch (error) {
      console.error('Error processing URL:', error);
      return Promise.reject(error);
    }
  };
  
  // Delete a document
  const handleDeleteDocument = async (id: string) => {
    if (!confirm('Are you sure you want to delete this document?')) {
      return;
    }
    
    try {
      await api.deleteDocument(id);
      // Update local state
      setDocuments((prev) => prev.filter((doc) => doc.id !== id));
    } catch (error) {
      console.error('Error deleting document:', error);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2">
        <h1 className="text-2xl font-bold mb-4">Documents</h1>
        <DocumentList
          documents={documents}
          onDelete={handleDeleteDocument}
          isLoading={isLoading}
        />
      </div>
      
      <div className="lg:col-span-1">
        <h2 className="text-xl font-bold mb-4">Add Content</h2>
        <DocumentUpload
          onUpload={handleUpload}
          onProcessUrl={handleProcessUrl}
        />
      </div>
    </div>
  );
}