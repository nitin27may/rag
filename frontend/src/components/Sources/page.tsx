"use client";

import { useState, useEffect } from 'react';
import SourceList from '@/components/Sources/SourceList';
import SourceForm from '@/components/Sources/SourceForm';
import { DataSource, AddDataSourceRequest } from '@/lib/types';
import api from '@/lib/api';

export default function SourcesPage() {
  const [sources, setSources] = useState<DataSource[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  
  // Fetch sources on component mount
  useEffect(() => {
    fetchSources();
  }, []);
  
  // Fetch sources from API
  const fetchSources = async () => {
    setIsLoading(true);
    try {
      const dataSources = await api.getDataSources();
      setSources(dataSources);
    } catch (error) {
      console.error('Error fetching data sources:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Add a new data source
  const handleAddSource = async (data: AddDataSourceRequest) => {
    try {
      const newSource = await api.addDataSource(data);
      // Update local state
      setSources((prev) => [...prev, newSource]);
      return Promise.resolve();
    } catch (error) {
      console.error('Error adding data source:', error);
      return Promise.reject(error);
    }
  };
  
  // Delete a data source
  const handleDeleteSource = async (id: string) => {
    if (!confirm('Are you sure you want to delete this data source?')) {
      return;
    }
    
    try {
      await api.deleteDataSource(id);
      // Update local state
      setSources((prev) => prev.filter((source) => source.id !== id));
    } catch (error) {
      console.error('Error deleting data source:', error);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2">
        <h1 className="text-2xl font-bold mb-4">Data Sources</h1>
        <SourceList
          sources={sources}
          onDelete={handleDeleteSource}
          isLoading={isLoading}
        />
      </div>
      
      <div className="lg:col-span-1">
        <h2 className="text-xl font-bold mb-4">Add Data Source</h2>
        <SourceForm onSubmit={handleAddSource} />
      </div>
    </div>
  );
}