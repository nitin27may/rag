"use client";

import { useState } from 'react';
import DocumentUploadTab from "./DocumentUploadTab";
import DocumentListTab from "./DocumentListTab";
import SourcesTab from "./SourcesTab";

interface SidePanelProps {
  onDocumentsChanged?: () => void;
}

export default function SidePanel({ onDocumentsChanged }: SidePanelProps) {
  const [activeTab, setActiveTab] = useState('upload');

  return (
    <div className="bg-white border rounded-lg overflow-hidden h-full">
      <div className="bg-green-600 p-0">
        <nav className="flex">
          <button 
            onClick={() => setActiveTab('upload')}
            className={`px-4 py-2 text-sm font-medium ${
              activeTab === 'upload' 
                ? 'bg-white text-gray-800' 
                : 'text-white hover:bg-green-700'
            }`}
          >
            Upload
          </button>
          <button 
            onClick={() => setActiveTab('documents')}
            className={`px-4 py-2 text-sm font-medium ${
              activeTab === 'documents' 
                ? 'bg-white text-gray-800' 
                : 'text-white hover:bg-green-700'
            }`}
          >
            Documents
          </button>
          <button 
            onClick={() => setActiveTab('sources')}
            className={`px-4 py-2 text-sm font-medium ${
              activeTab === 'sources' 
                ? 'bg-white text-gray-800' 
                : 'text-white hover:bg-green-700'
            }`}
          >
            Sources
          </button>
        </nav>
      </div>

      <div className="p-4">
        {activeTab === 'upload' && <DocumentUploadTab onUploadComplete={onDocumentsChanged} />}
        {activeTab === 'documents' && <DocumentListTab onDocumentDeleted={onDocumentsChanged} />}
        {activeTab === 'sources' && <SourcesTab />}
      </div>
      
      <div className="p-4 border-t">
        <a 
          href="/websocket" 
          className="inline-flex items-center px-3 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M9.38 13.329l-1.95-1.95a.75.75 0 111.06-1.06l1.95 1.95 1.95-1.95a.75.75 0 111.06 1.06l-1.95 1.95 1.95 1.95a.75.75 0 11-1.06 1.06l-1.95-1.95-1.95 1.95a.75.75 0 11-1.06-1.06l1.95-1.95z" clipRule="evenodd" />
            <path fillRule="evenodd" d="M10 2a8 8 0 100 16 8 8 0 000-16zM4 10a6 6 0 1112 0 6 6 0 01-12 0z" clipRule="evenodd" />
          </svg>
          WebSocket Test
        </a>
      </div>
    </div>
  );
}
