"use client";

import { useState, useEffect, useRef, useCallback } from 'react';
import { webSocketClient } from '@/lib/websocket';

interface WebSocketMessage {
  id: string;
  content: string;
  timestamp: string;
}

export default function WebSocketTestPage() {
  const [connected, setConnected] = useState(false);
  const [connecting, setConnecting] = useState(false);
  const [messages, setMessages] = useState<WebSocketMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Add a message to the log
  const addLogMessage = useCallback((message: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setMessages(prev => [...prev, { id: `${Date.now()}`, content: message, timestamp }]);
  }, []);

  // Handle connection request
  const handleConnect = useCallback(async () => {
    if (connected || connecting) return;
    
    setConnecting(true);
    addLogMessage('Connecting to WebSocket server...');
    
    try {
      await webSocketClient.connect();
      setConnected(true);
      addLogMessage('Connected to WebSocket server');
    } catch (error) {
      console.error('Connection error:', error);
      addLogMessage(`Connection error: ${error}`);
      setConnected(false);
    } finally {
      setConnecting(false);
    }
  }, [connected, connecting, addLogMessage]);

  // Connect to WebSocket on component mount
  useEffect(() => {
    // Add message handler
    const handleMessage = (data: unknown) => {
      let messageContent = '';
      
      if (typeof data === 'string') {
        // If the data is a string
        messageContent = data;
      } else if (typeof data === 'object') {
        // If the data is an object, stringify it
        try {
          messageContent = JSON.stringify(data);
        } catch {
          // Ignoring stringify error
          messageContent = `[Object: ${typeof data}]`;
        }
      } else {
        // For any other data type
        messageContent = String(data);
      }
      
      addLogMessage(`Received: ${messageContent}`);
    };

    webSocketClient.addMessageHandler(handleMessage);

    // Attempt initial connection
    handleConnect();

    // Cleanup on unmount
    return () => {
      webSocketClient.removeMessageHandler(handleMessage);
      webSocketClient.disconnect();
    };
  }, [handleConnect, addLogMessage]);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle disconnection request
  const handleDisconnect = () => {
    webSocketClient.disconnect();
    setConnected(false);
    addLogMessage('Disconnected from WebSocket server');
  };

  // Send a message to the WebSocket server
  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const message = {
      type: 'message',
      content: inputMessage
    };

    try {
      const success = await webSocketClient.send(message);
      if (success) {
        addLogMessage(`Sent: ${JSON.stringify(message)}`);
        setInputMessage('');
      } else {
        addLogMessage('Failed to send message');
      }
    } catch (error) {
      addLogMessage(`Error sending message: ${error}`);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">WebSocket Test</h1>
      
      <div className="mb-4 p-4 border rounded-lg bg-white">
        <div className="flex items-center mb-4">
          <div
            className={`w-3 h-3 rounded-full mr-2 ${
              connected ? 'bg-green-500' : connecting ? 'bg-yellow-500' : 'bg-red-500'
            }`}
          ></div>
          <span>
            {connected ? 'Connected to WebSocket' : 
             connecting ? 'Connecting...' : 'Disconnected'}
          </span>
        </div>
        
        <div className="flex space-x-2">
          <button
            onClick={handleConnect}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={connected || connecting}
          >
            {connecting ? 'Connecting...' : 'Connect'}
          </button>
          
          <button
            onClick={handleDisconnect}
            className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={!connected}
          >
            Disconnect
          </button>
        </div>
      </div>
      
      <div className="mb-4">
        <h2 className="text-lg font-semibold mb-2">Send Message</h2>
        <div className="flex">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type a message..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={!connected}
          />
          <button
            onClick={sendMessage}
            className="px-4 py-2 bg-blue-600 text-white rounded-r-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={!connected || !inputMessage.trim()}
          >
            Send
          </button>
        </div>
      </div>
      
      <div className="mb-4">
        <h2 className="text-lg font-semibold mb-2">Connection Log</h2>
        <div className="h-64 overflow-y-auto p-3 bg-gray-100 rounded-md font-mono text-sm">
          {messages.length === 0 ? (
            <div className="text-gray-500 text-center py-4">No messages yet</div>
          ) : (
            messages.map((msg, index) => (
              <div key={index} className="mb-1">
                {msg.timestamp} - {msg.content}
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
    </div>
  );
}