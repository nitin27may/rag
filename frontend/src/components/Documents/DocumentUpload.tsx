"use client";

import { useState, useRef } from 'react';
import { DocumentUploadProps } from '@/lib/types';

export default function DocumentUpload({ onUpload, onProcessUrl }: DocumentUploadProps) {
  const [activeTab, setActiveTab] = useState<'file' | 'url'>('file');
  const [file, setFile] = useState<File | null>(null);
  const [url, setUrl] = useState('');
  const [description, setDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Handle file change
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setError('');
    }
  };

  // Handle file upload
  const handleFileUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a file to upload');
      return;
    }
    
    try {
      setIsLoading(true);
      setError('');
      
      await onUpload({
        file,
        description: description.trim() || undefined,
      });
      
      // Reset form
      setFile(null);
      setDescription('');
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch {
      // Ignoring specific error details
      setError('Failed to upload file. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Handle URL processing
  const handleUrlProcess = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!url.trim()) {
      setError('Please enter a URL');
      return;
    }
    
    try {
      setIsLoading(true);
      setError('');
      
      await onProcessUrl({
        url: url.trim(),
        description: description.trim() || undefined,
      });
      
      // Reset form
      setUrl('');
      setDescription('');
    } catch {
      // Ignoring specific error details
      setError('Failed to process URL. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg border overflow-hidden">
      <div className="p-4 bg-gray-50 border-b">
        <h2 className="text-lg font-medium text-gray-900">Add Document</h2>
      </div>
      
      <div className="p-4">
        {/* Tab Navigation */}
        <div className="flex border-b mb-4">
          <button
            onClick={() => setActiveTab('file')}
            className={`py-2 px-4 font-medium ${
              activeTab === 'file'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Upload File
          </button>
          <button
            onClick={() => setActiveTab('url')}
            className={`py-2 px-4 font-medium ${
              activeTab === 'url'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Process URL
          </button>
        </div>
        
        {error && (
          <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-md text-sm">
            {error}
          </div>
        )}
        
        {/* File Upload Form */}
        {activeTab === 'file' && (
          <form onSubmit={handleFileUpload}>
            <div className="mb-4">
              <label htmlFor="file-upload" className="block text-sm font-medium text-gray-700 mb-1">
                File
              </label>
              <input
                id="file-upload"
                ref={fileInputRef}
                type="file"
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                disabled={isLoading}
              />
              {file && (
                <p className="mt-1 text-xs text-gray-500">
                  Selected file: {file.name} ({Math.round(file.size / 1024)} KB)
                </p>
              )}
            </div>
            
            <div className="mb-4">
              <label htmlFor="file-description" className="block text-sm font-medium text-gray-700 mb-1">
                Description (optional)
              </label>
              <input
                id="file-description"
                type="text"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="Brief description of this document"
                disabled={isLoading}
              />
            </div>
            
            <div className="flex justify-end">
              <button
                type="submit"
                disabled={isLoading || !file}
                className="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <>
                    <span className="inline-block h-4 w-4 rounded-full border-2 border-white border-t-transparent animate-spin mr-2"></span>
                    Uploading...
                  </>
                ) : (
                  'Upload'
                )}
              </button>
            </div>
          </form>
        )}
        
        {/* URL Processing Form */}
        {activeTab === 'url' && (
          <form onSubmit={handleUrlProcess}>
            <div className="mb-4">
              <label htmlFor="url-input" className="block text-sm font-medium text-gray-700 mb-1">
                URL
              </label>
              <input
                id="url-input"
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="https://example.com/document"
                required
                disabled={isLoading}
              />
            </div>
            
            <div className="mb-4">
              <label htmlFor="url-description" className="block text-sm font-medium text-gray-700 mb-1">
                Description (optional)
              </label>
              <input
                id="url-description"
                type="text"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="Brief description of this content"
                disabled={isLoading}
              />
            </div>
            
            <div className="flex justify-end">
              <button
                type="submit"
                disabled={isLoading || !url.trim()}
                className="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <>
                    <span className="inline-block h-4 w-4 rounded-full border-2 border-white border-t-transparent animate-spin mr-2"></span>
                    Processing...
                  </>
                ) : (
                  'Process URL'
                )}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}