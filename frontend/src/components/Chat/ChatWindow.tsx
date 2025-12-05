"use client";

import { useRef, useEffect } from 'react';
import { ChatWindowProps } from '@/lib/types';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

export default function ChatWindow({ 
  messages, 
  isLoading, 
  onSendMessage,
  availableDocuments = [],
  selectedDocumentIds = [],
  onDocumentSelectionChange
}: ChatWindowProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Force inline styles to ensure layout works properly
  const containerStyle = {
    display: 'flex',
    flexDirection: 'column' as const,
    height: 'calc(100vh - 200px)',
    border: '1px solid #e5e7eb',
    borderRadius: '0.5rem',
    boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    backgroundColor: '#ffffff',
    overflow: 'hidden',
  };

  const headerStyle = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#2563eb',
    color: '#ffffff',
    padding: '1rem',
    fontWeight: 500,
    borderTopLeftRadius: '0.5rem',
    borderTopRightRadius: '0.5rem',
  };

  const contentStyle = {
    flex: 1,
    overflowY: 'auto' as const,
    padding: '1rem',
  };

  const footerStyle = {
    borderTop: '1px solid #e5e7eb',
  };

  return (
    <div style={containerStyle} className="flex flex-col h-[calc(100vh-200px)] border border-gray-200 rounded-lg shadow-sm bg-white overflow-hidden">
      <div style={headerStyle} className="bg-blue-600 text-white p-4 font-medium rounded-t-lg flex items-center justify-between">
        <span>RAG Chat</span>
        {messages.length > 0 && (
          <span style={{ fontSize: '0.75rem', backgroundColor: '#3b82f6', padding: '0.25rem 0.5rem', borderRadius: '9999px' }} className="text-xs bg-blue-500 px-2 py-1 rounded-full">
            {messages.length} messages
          </span>
        )}
      </div>
      
      <div style={contentStyle} className="flex-1 overflow-y-auto p-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 py-8 h-full flex flex-col items-center justify-center">
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              className="h-12 w-12 text-gray-400 mb-4" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={1.5} 
                d="M8 12h.01M12 12h.01M16 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9 10a1 1 0 11-2 0 1 1 0 012 0zm6 0a1 1 0 11-2 0 1 1 0 012 0z" 
              />
            </svg>
            <p className="text-lg font-medium">Welcome to the RAG Chat</p>
            <p className="mt-2">
              Let&apos;s get started! What information are you looking for?
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
          </div>
        )}
        
        {isLoading && (
          <div className="flex items-center justify-center py-6 mt-4">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            <span className="ml-3 text-gray-500 font-medium">Generating response...</span>
          </div>
        )}
        
        <div ref={messagesEndRef} className="pt-2" />
      </div>
      
      <div style={footerStyle} className="border-t border-gray-200">
        <ChatInput 
          onSendMessage={onSendMessage} 
          isDisabled={isLoading}
          availableDocuments={availableDocuments}
          selectedDocumentIds={selectedDocumentIds}
          onDocumentSelectionChange={onDocumentSelectionChange}
        />
      </div>
    </div>
  );
}