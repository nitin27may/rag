"use client";

import { useEffect, useState } from 'react';
import api from '@/lib/api';

interface HealthCheckModalProps {
  isOpen: boolean;
  onClose: () => void;
}

interface ServiceHealth {
  status: string;
  message?: string;
}

interface HealthData {
  status: string;
  services: Record<string, ServiceHealth>;
}

export default function HealthCheckModal({ isOpen, onClose }: HealthCheckModalProps) {
  const [loading, setLoading] = useState(true);
  const [healthData, setHealthData] = useState<HealthData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      checkHealth();
    }
  }, [isOpen]);

  const checkHealth = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await api.checkHealth();
      setHealthData(data);
    } catch (err) {
      console.error('Health check error:', err);
      setError('Failed to retrieve system health information');
    } finally {
      setLoading(false);
    }
  };

  // Don't render anything if modal is not open
  if (!isOpen) return null;

  const getStatusClass = (status: string) => {
    switch (status) {
      case 'ok': return 'bg-green-100 text-green-800';
      case 'warning': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-red-100 text-red-800';
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-hidden">
        <div className="border-b px-4 py-3 flex justify-between items-center">
          <h3 className="text-lg font-medium">System Health</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-500 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div className="p-4 overflow-y-auto max-h-[calc(90vh-60px)]">
          {loading ? (
            <div className="flex justify-center items-center py-10">
              <div className="animate-spin rounded-full h-10 w-10 border-4 border-blue-500 border-t-transparent"></div>
            </div>
          ) : error ? (
            <div className="bg-red-100 text-red-700 p-4 rounded-md">
              {error}
            </div>
          ) : healthData ? (
            <>
              <div className={`p-4 rounded-md mb-4 ${getStatusClass(healthData.status)}`}>
                <span className="font-bold">Overall Status:</span> {healthData.status.toUpperCase()}
              </div>
              
              <div className="overflow-x-auto">
                <table className="w-full border-collapse">
                  <thead>
                    <tr className="bg-gray-50">
                      <th className="px-4 py-2 text-left border">Service</th>
                      <th className="px-4 py-2 text-left border">Status</th>
                      <th className="px-4 py-2 text-left border">Message</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(healthData.services).map(([service, info]) => (
                      <tr key={service} className="border-b">
                        <td className="px-4 py-2 border">{service}</td>
                        <td className="px-4 py-2 border">
                          <span className={`inline-block px-2 py-1 rounded-full text-xs font-semibold ${getStatusClass(info.status)}`}>
                            {info.status}
                          </span>
                        </td>
                        <td className="px-4 py-2 border">{info.message || ''}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          ) : (
            <div className="text-center py-10 text-gray-500">
              No health data available
            </div>
          )}
        </div>
        
        <div className="border-t px-4 py-3 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-md transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
