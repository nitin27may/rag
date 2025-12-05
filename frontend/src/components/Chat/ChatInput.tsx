"use client";

import { useState, useRef, useEffect } from 'react';
import { PaperAirplaneIcon, DocumentTextIcon, XMarkIcon, ChevronDownIcon } from '@heroicons/react/24/outline';
import { ChatInputProps } from '@/lib/types';

export default function ChatInput({ 
  onSendMessage, 
  isDisabled = false,
  availableDocuments = [],
  selectedDocumentIds = [],
  onDocumentSelectionChange
}: ChatInputProps) {
  const [message, setMessage] = useState('');
  const [showDocumentSelector, setShowDocumentSelector] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDocumentSelector(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const trimmedMessage = message.trim();
    if (!trimmedMessage) return;
    
    // Send the message with selected document IDs (empty array means search all)
    onSendMessage(trimmedMessage, selectedDocumentIds.length > 0 ? selectedDocumentIds : undefined);
    setMessage('');
  };

  const toggleDocumentSelection = (docId: string) => {
    if (!onDocumentSelectionChange) return;
    
    if (selectedDocumentIds.includes(docId)) {
      onDocumentSelectionChange(selectedDocumentIds.filter(id => id !== docId));
    } else {
      onDocumentSelectionChange([...selectedDocumentIds, docId]);
    }
  };

  const clearAllSelections = () => {
    if (onDocumentSelectionChange) {
      onDocumentSelectionChange([]);
    }
  };

  const getSelectedDocumentNames = () => {
    if (selectedDocumentIds.length === 0) return 'All Documents';
    if (selectedDocumentIds.length === 1) {
      const doc = availableDocuments.find(d => d.id === selectedDocumentIds[0]);
      return doc?.title || doc?.filename || 'Selected';
    }
    return `${selectedDocumentIds.length} documents selected`;
  };
  
  return (
    <div className="border-t border-gray-200 p-4 bg-white">
      <form onSubmit={handleSubmit} className="flex flex-col gap-2">
        {/* Document Selection Display */}
        {selectedDocumentIds.length > 0 && (
          <div className="flex flex-wrap gap-1 mb-1">
            {selectedDocumentIds.map(docId => {
              const doc = availableDocuments.find(d => d.id === docId);
              return (
                <span 
                  key={docId}
                  className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs"
                >
                  {doc?.title || doc?.filename || docId.substring(0, 8)}
                  <button
                    type="button"
                    onClick={() => toggleDocumentSelection(docId)}
                    className="hover:bg-blue-200 rounded-full p-0.5"
                  >
                    <XMarkIcon className="h-3 w-3" />
                  </button>
                </span>
              );
            })}
            <button
              type="button"
              onClick={clearAllSelections}
              className="text-xs text-gray-500 hover:text-gray-700 px-2"
            >
              Clear all
            </button>
          </div>
        )}
        
        <div className="flex relative">
          {/* Document Selector Button */}
          <div className="relative" ref={dropdownRef}>
            <button
              type="button"
              onClick={() => setShowDocumentSelector(!showDocumentSelector)}
              className={`p-2 flex items-center gap-1 ${
                selectedDocumentIds.length > 0 ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600'
              } border border-gray-300 rounded-l-md hover:bg-gray-200`}
              title="Select documents to search"
            >
              <DocumentTextIcon className="h-5 w-5" />
              <ChevronDownIcon className="h-3 w-3" />
            </button>
            
            {/* Document Dropdown */}
            {showDocumentSelector && (
              <div className="absolute bottom-full left-0 mb-1 w-72 bg-white border border-gray-300 rounded-md shadow-lg z-50 max-h-64 overflow-y-auto">
                <div className="p-2 border-b border-gray-200 bg-gray-50">
                  <div className="text-xs font-medium text-gray-600">
                    {getSelectedDocumentNames()}
                  </div>
                  <div className="text-xs text-gray-400 mt-1">
                    {selectedDocumentIds.length === 0 
                      ? 'Select documents to filter search, or leave empty to search all'
                      : 'Click to toggle selection'}
                  </div>
                </div>
                
                {availableDocuments.length === 0 ? (
                  <div className="p-3 text-sm text-gray-500 text-center">
                    No documents available
                  </div>
                ) : (
                  <div className="py-1">
                    {availableDocuments.filter(doc => doc.is_indexed).map(doc => (
                      <button
                        key={doc.id}
                        type="button"
                        onClick={() => toggleDocumentSelection(doc.id)}
                        className={`w-full px-3 py-2 text-left text-sm flex items-center gap-2 hover:bg-gray-100 ${
                          selectedDocumentIds.includes(doc.id) ? 'bg-blue-50' : ''
                        }`}
                      >
                        <input
                          type="checkbox"
                          checked={selectedDocumentIds.includes(doc.id)}
                          onChange={() => {}}
                          className="h-4 w-4 text-blue-600 rounded border-gray-300"
                        />
                        <div className="flex-1 min-w-0">
                          <div className="truncate font-medium">
                            {doc.title || doc.filename}
                          </div>
                          <div className="text-xs text-gray-400 truncate">
                            {doc.source_type === 'web' ? 'Web Page' : doc.mime_type}
                          </div>
                        </div>
                      </button>
                    ))}
                    {availableDocuments.filter(doc => !doc.is_indexed).length > 0 && (
                      <div className="px-3 py-2 text-xs text-gray-400 border-t">
                        {availableDocuments.filter(doc => !doc.is_indexed).length} document(s) not yet indexed
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
          
          <input
            type="text"
            placeholder={selectedDocumentIds.length > 0 
              ? `Ask about ${selectedDocumentIds.length} selected document(s)...` 
              : "Ask a question (searches all documents)..."
            }
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