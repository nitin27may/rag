"use client";

import { useEffect, useState } from 'react';
import { DataSource } from '@/lib/types';
import { formatDate } from '@/lib/utils';
import api from '@/lib/api';

export default function SourcesTab() {
  const [sources, setSources] = useState<DataSource[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [name, setName] = useState('');
  const [sourceType, setSourceType] = useState('file_system');
  const [connectionDetails, setConnectionDetails] = useState('');
  const [isAdding, setIsAdding] = useState(false);
  const [formError, setFormError] = useState('');

  useEffect(() => {
    loadSources();
  }, []);

  const loadSources = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const data = await api.getDataSources();
      setSources(data);
    } catch (err) {
      console.error('Error loading sources:', err);
      setError('Failed to load data sources. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this data source?')) {
      return;
    }
    
    try {
      await api.deleteDataSource(id);
      // Update list by filtering out the deleted source
      setSources(sources.filter(source => source.id !== id));
    } catch (err) {
      console.error('Error deleting source:', err);
      alert('Failed to delete data source. Please try again.');
    }
  };

  const handleAddSource = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError('');
    
    try {
      // Parse connection details
      let parsedDetails;
      try {
        parsedDetails = JSON.parse(connectionDetails);
      } catch {
        setFormError('Invalid JSON in connection details');
        return;
      }
      
      setIsAdding(true);
      await api.addDataSource({
        name,
        source_type: sourceType,
        connection_details: parsedDetails
      });
      
      // Reset form
      setName('');
      setSourceType('file_system');
      setConnectionDetails('');
      setShowAddForm(false);
      
      // Reload sources
      await loadSources();
    } catch (err) {
      console.error('Error adding source:', err);
      setFormError('Failed to add data source');
    } finally {
      setIsAdding(false);
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

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-40">
        <div className="animate-spin rounded-full h-10 w-10 border-4 border-blue-500 border-t-transparent"></div>
      </div>
    );
  }

  if (showAddForm) {
    return (
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-medium">Add Data Source</h3>
          <button 
            onClick={() => setShowAddForm(false)}
            className="text-gray-500 hover:text-gray-700"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
        
        {formError && (
          <div className="bg-red-100 border border-red-200 text-red-700 px-4 py-3 rounded-md text-sm">
            {formError}
          </div>
        )}
        
        <form onSubmit={handleAddSource}>
          <div className="mb-3">
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
              Name
            </label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              required
            />
          </div>
          
          <div className="mb-3">
            <label htmlFor="type" className="block text-sm font-medium text-gray-700 mb-1">
              Type
            </label>
            <select
              id="type"
              value={sourceType}
              onChange={handleSourceTypeChange}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="file_system">File System</option>
              <option value="database">Database</option>
              <option value="website">Website</option>
              <option value="api">API</option>
            </select>
          </div>
          
          <div className="mb-3">
            <label htmlFor="connectionDetails" className="block text-sm font-medium text-gray-700 mb-1">
              Connection Details (JSON)
            </label>
            <textarea
              id="connectionDetails"
              value={connectionDetails}
              onChange={(e) => setConnectionDetails(e.target.value)}
              rows={5}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 font-mono text-sm"
              placeholder="{}"
              required
            />
          </div>
          
          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={() => setShowAddForm(false)}
              className="px-4 py-2 text-sm border border-gray-300 rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isAdding || !name.trim() || !connectionDetails.trim()}
              className="px-4 py-2 text-sm border border-transparent rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {isAdding ? 'Adding...' : 'Add Source'}
            </button>
          </div>
        </form>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {error && (
        <div className="bg-red-100 border border-red-200 text-red-700 px-4 py-3 rounded-md text-sm">
          {error}
        </div>
      )}
      
      <button
        onClick={() => setShowAddForm(true)}
        className="w-full py-2 px-4 bg-blue-50 text-blue-600 border border-blue-200 rounded-md hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 flex items-center justify-center"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
        </svg>
        Add Data Source
      </button>
      
      {sources.length === 0 ? (
        <div className="text-center py-6">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
          </svg>
          <h3 className="text-lg font-medium text-gray-900 mb-1">No data sources</h3>
          <p className="text-gray-500 text-sm">
            Add a data source to connect to external repositories.
          </p>
        </div>
      ) : (
        <div className="max-h-[400px] overflow-y-auto">
          {sources.map((source) => (
            <div key={source.id} className="border rounded-md p-3 bg-gray-50 relative mb-3 hover:bg-gray-100 transition-colors">
              <button
                onClick={() => handleDelete(source.id)}
                className="absolute top-2 right-2 text-gray-400 hover:text-red-600"
                title="Delete data source"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </button>
              
              <h3 className="font-medium text-gray-900 mb-1">
                {source.name}
              </h3>
              
              <div className="flex flex-wrap gap-2 mt-2">
                <span className="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-200 text-gray-800">
                  Type: {source.source_type}
                </span>
                
                <span className={`inline-flex items-center px-2 py-1 rounded text-xs 
                  ${source.is_active 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'}`}
                >
                  {source.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              
              <div className="mt-2 p-2 bg-gray-200 rounded text-xs overflow-x-auto">
                <pre className="font-mono whitespace-pre-wrap break-all">
                  {JSON.stringify(source.connection_details, null, 2)}
                </pre>
              </div>
              
              <div className="text-xs text-gray-500 mt-2">
                Added: {formatDate(source.created_at)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
