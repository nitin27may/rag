"use client";

import { useState } from 'react';
import ChatWindow from '@/components/Chat/ChatWindow';
import MetricsPanel from '@/components/Chat/MetricsPanel';
import SidePanel from '@/components/SidePanel/SidePanel';
import { Message, QueryRequest } from '@/lib/types';
import api from '@/lib/api';

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([{
    id: '0',
    content: "Hello! I'm your RAG assistant. Ask me a question, and I'll retrieve information from your documents to provide an answer.",
    role: 'assistant',
    timestamp: new Date(),
  }]);
  
  const [isLoading, setIsLoading] = useState(false);
  const [metrics, setMetrics] = useState<{
    total_time_seconds?: number;
    retrieval_time_seconds?: number;
    generation_time_seconds?: number;
    total_documents?: number;
  } | null>(null);

  // Send a message to the RAG system
  const handleSendMessage = async (content: string, documentId?: string) => {
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user',
      timestamp: new Date(),
      document_id: documentId,
    };
    
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setMetrics(null); // Reset metrics when sending a new message
    
    try {
      // Prepare query request
      const queryRequest: QueryRequest = {
        query: content,
        top_k: 5,
      };
      
      // Add document_id if provided
      if (documentId) {
        queryRequest.document_id = documentId;
      }
      
      // Send query to API
      const response = await api.generateAnswer(queryRequest);
      
      // Add assistant response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.answer,
        role: 'assistant',
        timestamp: new Date(),
        document_id: documentId,  // Store the document ID with the response
        documents: response.documents,
      };
      
      setMessages((prev) => [...prev, assistantMessage]);
      
      // Update metrics
      setMetrics(response.metrics);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error processing your request. Please try again later.',
        role: 'assistant',
        timestamp: new Date(),
      };
      
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto py-4">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        <div className="lg:col-span-8">
          <ChatWindow 
            messages={messages} 
            isLoading={isLoading} 
            onSendMessage={handleSendMessage} 
          />
          
          <div className="mt-4">
            <MetricsPanel metrics={metrics} />
          </div>
        </div>
        
        <div className="lg:col-span-4">
          <SidePanel />
        </div>
      </div>
    </div>
  );
}