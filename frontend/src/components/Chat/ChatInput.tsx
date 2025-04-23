"use client";

import { useState } from 'react';
import { PaperAirplaneIcon, DocumentTextIcon } from '@heroicons/react/24/outline';
import { ChatInputProps } from '@/lib/types';

export default function ChatInput({ onSendMessage, isDisabled = false }: ChatInputProps) {
  const [message, setMessage] = useState('');
  const [documentId, setDocumentId] = useState('');
  const [showDocumentIdField, setShowDocumentIdField] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const trimmedMessage = message.trim();
    if (!trimmedMessage) return;
    
    // Send both the message and optional documentId
    onSendMessage(trimmedMessage, documentId.trim() || undefined);
    setMessage('');
    // Keep the document ID for potential follow-up questions
  };
  
  return (
    <div className="border-t border-gray-200 p-4 bg-white">
      <form onSubmit={handleSubmit} className="flex flex-col gap-2">
        {showDocumentIdField && (
          <div className="flex">
            <div className="flex items-center px-3 bg-gray-100 border border-r-0 border-gray-300 rounded-l-md text-sm text-gray-500">
              Document ID
            </div>
            <input
              type="text"
              placeholder="Enter document ID (optional)"
              className="flex-1 px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              value={documentId}
              onChange={(e) => setDocumentId(e.target.value)}
              disabled={isDisabled}
            />
            <button
              type="button"
              className="p-2 bg-gray-200 hover:bg-gray-300 border border-gray-300 rounded-r-md"
              onClick={() => setDocumentId('')}
              title="Clear document ID"
            >
              ×
            </button>
          </div>
        )}
        
        <div className="flex">
          <button
            type="button"
            onClick={() => setShowDocumentIdField(!showDocumentIdField)}
            className={`p-2 ${showDocumentIdField ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600'} border border-gray-300 rounded-l-md hover:bg-gray-200`}
            title={showDocumentIdField ? "Hide document ID field" : "Filter by document ID"}
          >
            <DocumentTextIcon className="h-5 w-5" />
          </button>
          <input
            type="text"
            placeholder="Ask a question..."
            className="flex-1 px-4 py-2 border border-l-0 border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            disabled={isDisabled}
          />
          <button
            type="submit"
            disabled={isDisabled || !message.trim()}
            className="p-2 bg-blue-600 text-white rounded-r-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <PaperAirplaneIcon className="h-5 w-5" />
          </button>
        </div>
      </form>
    </div>
  );
}