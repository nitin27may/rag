"use client";

import { useState } from 'react';
import { PaperAirplaneIcon } from '@heroicons/react/24/outline';
import { ChatInputProps } from '@/lib/types';

export default function ChatInput({ onSendMessage, isDisabled = false }: ChatInputProps) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const trimmedMessage = message.trim();
    if (!trimmedMessage) return;
    
    onSendMessage(trimmedMessage);
    setMessage('');
  };
  
  return (
    <div className="border-t border-gray-200 p-4 bg-white">
      <form onSubmit={handleSubmit} className="flex">
        <input
          type="text"
          placeholder="Ask a question..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
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
      </form>
    </div>
  );
}