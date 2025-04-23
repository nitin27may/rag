"use client";

import { useState } from 'react';
import { SourceFormProps } from '@/lib/types';

export default function SourceForm({ onSubmit }: SourceFormProps) {
  const [name, setName] = useState('');
  const [sourceType, setSourceType] = useState('file_system');
  const [connectionDetails, setConnectionDetails] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    try {
      // Parse connection details
      let parsedDetails;
      try {
        parsedDetails = JSON.parse(connectionDetails);
      } catch {
        setError('Invalid JSON in connection details');
        return;
      }
      
      setIsLoading(true);
      await onSubmit({
        name,
        source_type: sourceType,
        connection_details: parsedDetails
      });
      
      // Reset form
      setName('');
      setSourceType('file_system');
      setConnectionDetails('');
    } catch {
      setError('Failed to add data source');
      console.error();
    } finally {
      setIsLoading(false);
    }
  };
  
  const getDefaultConnectionDetails = (type: string): string => {
    switch (type) {
      case 'file_system':
        return JSON.stringify({ base_path: "./data/uploads" }, null, 2);
      case 'database':
        return JSON.stringify({
          connection_string: "postgresql://user:pass@localhost:5432/db",
          type: "postgresql"
        }, null, 2);
      case 'website':
        return JSON.stringify({ timeout: 30 }, null, 2);
      case 'api':
        return JSON.stringify({
          base_url: "https://api.example.com",
          headers: {
            "Authorization": "Bearer YOUR_API_KEY"
          }
        }, null, 2);
      default:
        return '';
    }
  };
  
  const handleSourceTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newType = e.target.value;
    setSourceType(newType);
    setConnectionDetails(getDefaultConnectionDetails(newType));
  };

  return (
    <div className="bg-white rounded-lg border overflow-hidden">
      <div className="p-4 bg-gray-50 border-b">
        <h2 className="text-lg font-medium text-gray-900">Add Data Source</h2>
      </div>
      
      <form onSubmit={handleSubmit} className="p-4">
        {error && (
          <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-md text-sm">
            {error}
          </div>
        )}
        
        <div className="mb-4">
          <label htmlFor="source-name" className="block text-sm font-medium text-gray-700 mb-1">
            Name
          </label>
          <input
            type="text"
            id="source-name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="My Data Source"
            required
            disabled={isLoading}
          />
        </div>
        
        <div className="mb-4">
          <label htmlFor="source-type" className="block text-sm font-medium text-gray-700 mb-1">
            Type
          </label>
          <select
            id="source-type"
            value={sourceType}
            onChange={handleSourceTypeChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            required
            disabled={isLoading}
          >
            <option value="file_system">File System</option>
            <option value="database">Database</option>
            <option value="website">Website</option>
            <option value="api">API</option>
          </select>
        </div>
        
        <div className="mb-4">
          <label htmlFor="connection-details" className="block text-sm font-medium text-gray-700 mb-1">
            Connection Details (JSON)
          </label>
          <textarea
            id="connection-details"
            value={connectionDetails}
            onChange={(e) => setConnectionDetails(e.target.value)}
            rows={6}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 font-mono text-sm"
            placeholder="{}"
            required
            disabled={isLoading}
          />
          <p className="mt-1 text-xs text-gray-500">
            Enter the connection details as a valid JSON object
          </p>
        </div>
        
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isLoading || !name.trim() || !connectionDetails.trim()}
            className="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2 inline-block"></div>
                <span>Adding...</span>
              </>
            ) : (
              'Add Data Source'
            )}
          </button>
        </div>
      </form>
    </div>
  );
}