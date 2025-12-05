"use client";

import { useState, useEffect } from 'react';
import SourceForm from '@/components/Sources/SourceForm';
import SourceList from '@/components/Sources/SourceList';
import { DataSource, AddDataSourceRequest } from '@/lib/types';
import api from '@/lib/api';

export default function DataSourcesPage() {
  const [sources, setSources] = useState<DataSource[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Fetch data sources on page load
  useEffect(() => {
    fetchDataSources();
  }, []);
  
  // Fetch data sources from API
  const fetchDataSources = async () => {
    try {
      setIsLoading(true);
      const data = await api.getDataSources();
      setSources(data);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch data sources:', err);
      setError('Failed to load data sources. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  // Handle adding a new data source
  const handleAddDataSource = async (data: AddDataSourceRequest) => {
    try {
      await api.addDataSource(data);
      fetchDataSources(); // Refresh the list
    } catch (err) {
      console.error('Failed to add data source:', err);
      throw new Error('Failed to add data source');
    }
  };
  
  // Handle deleting a data source
  const handleDeleteSource = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this data source?')) {
      return;
    }
    
    try {
      await api.deleteDataSource(id);
      // Update the local state instead of refetching
      setSources(sources.filter(source => source.id !== id));
    } catch (err) {
      console.error('Failed to delete data source:', err);
      alert('Failed to delete data source. Please try again.');
    }
  };
  
  return (
    <div className="max-w-7xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Data Sources</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <div className="space-y-6">
            <SourceForm onSubmit={handleAddDataSource} />
          </div>
        </div>
        
        <div className="lg:col-span-2">
          {error && (
            <div className="bg-red-50 text-red-700 p-4 rounded-md mb-4">
              {error}
            </div>
          )}
          
          <SourceList 
            sources={sources} 
            onDelete={handleDeleteSource} 
            isLoading={isLoading} 
          />
        </div>
      </div>
    </div>
  );
}
