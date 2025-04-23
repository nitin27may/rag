"use client";

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { HeartPulse, Book, Menu, X } from 'lucide-react';
import api from '@/lib/api';
import { HealthStatus } from '@/lib/types';

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isHealthModalOpen, setIsHealthModalOpen] = useState(false);
  const [healthData, setHealthData] = useState<HealthStatus | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [apiBaseUrl, setApiBaseUrl] = useState('http://localhost:8080/docs');
  const apiUrlInitialized = useRef(false);

  const pathname = usePathname();

  // Use a different approach with useRef to track initialization
  useEffect(() => {
    // Only run this once
    if (!apiUrlInitialized.current) {
      console.log('Header component initializing API URL');

      // Get the API URL with a fallback
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';
      const docsUrl = `${apiUrl}/docs`;

      console.log('API URL set to:', docsUrl);
      setApiBaseUrl(docsUrl);

      apiUrlInitialized.current = true;
    }
  }, []);

  // For troubleshooting - log every render
  console.log('Header component rendered with API URL:', apiBaseUrl);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const checkHealth = async () => {
    setIsLoading(true);
    setIsHealthModalOpen(true);

    try {
      const data = await api.checkHealth();
      setHealthData(data);
    } catch (error) {
      console.error('Error checking health:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <header className="bg-gray-800 text-white">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            {/* Logo and title */}
            <Link href="/" className="flex items-center space-x-2 text-xl font-bold">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <span>Comprehensive RAG System</span>
            </Link>

            {/* Mobile menu button */}
            <button
              onClick={toggleMenu}
              className="md:hidden text-white focus:outline-none"
            >
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>

            {/* Desktop navigation */}
            <nav className="hidden md:flex items-center space-x-4">
              <Link
                href="/"
                className={`px-3 py-2 rounded-md ${pathname === '/' ? 'bg-gray-700' : 'hover:bg-gray-700'}`}
              >
                Chat
              </Link>
              <Link
                href="/documents"
                className={`px-3 py-2 rounded-md ${pathname === '/documents' ? 'bg-gray-700' : 'hover:bg-gray-700'}`}
              >
                Documents
              </Link>
              <Link
                href="/sources"
                className={`px-3 py-2 rounded-md ${pathname === '/sources' ? 'bg-gray-700' : 'hover:bg-gray-700'}`}
              >
                Sources
              </Link>
              <button
                onClick={checkHealth}
                className="px-3 py-2 rounded-md hover:bg-gray-700 flex items-center space-x-1"
              >
                <HeartPulse size={18} />
                <span>Health</span>
              </button>
              <a
                href={apiBaseUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="px-3 py-2 rounded-md hover:bg-gray-700 flex items-center space-x-1"
                onClick={() => console.log('API Docs clicked:', apiBaseUrl)}
              >
                <Book size={18} />
                <span>API Docs</span>
              </a>
            </nav>
          </div>

          {/* Mobile navigation */}
          {isMenuOpen && (
            <nav className="mt-2 pt-2 pb-4 border-t border-gray-700 md:hidden">
              <Link
                href="/"
                className={`block px-3 py-2 rounded-md ${pathname === '/' ? 'bg-gray-700' : 'hover:bg-gray-700'}`}
                onClick={() => setIsMenuOpen(false)}
              >
                Chat
              </Link>
              <Link
                href="/documents"
                className={`block px-3 py-2 rounded-md ${pathname === '/documents' ? 'bg-gray-700' : 'hover:bg-gray-700'}`}
                onClick={() => setIsMenuOpen(false)}
              >
                Documents
              </Link>
              <Link
                href="/sources"
                className={`block px-3 py-2 rounded-md ${pathname === '/sources' ? 'bg-gray-700' : 'hover:bg-gray-700'}`}
                onClick={() => setIsMenuOpen(false)}
              >
                Sources
              </Link>
              <button
                onClick={() => {
                  checkHealth();
                  setIsMenuOpen(false);
                }}
                className="w-full text-left px-3 py-2 rounded-md hover:bg-gray-700 flex items-center space-x-1"
              >
                <HeartPulse size={18} />
                <span>Health</span>
              </button>
              <a
                href={apiBaseUrl}
                target="_blank" 
                rel="noopener noreferrer"
                className="block px-3 py-2 rounded-md hover:bg-gray-700 flex items-center space-x-1"
                onClick={() => {
                  console.log('Mobile API Docs clicked:', apiBaseUrl);
                  setIsMenuOpen(false);
                }}
              >
                <Book size={18} />
                <span>API Docs</span>
              </a>
            </nav>
          )}
        </div>
      </header>

      {/* Health Modal */}
      {isHealthModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[80vh] overflow-hidden">
            <div className="p-4 border-b border-gray-200 flex justify-between items-center">
              <h2 className="text-xl font-bold">System Health</h2>
              <button
                onClick={() => setIsHealthModalOpen(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                <X size={20} />
              </button>
            </div>

            <div className="p-4 overflow-y-auto max-h-[calc(80vh-8rem)]">
              {isLoading ? (
                <div className="flex justify-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-800"></div>
                </div>
              ) : healthData ? (
                <>
                  <div className={`p-3 rounded-md mb-4 ${
                    healthData.status === 'ok' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    <div className="font-bold">Overall Status: {healthData.status.toUpperCase()}</div>
                  </div>

                  <table className="w-full border-collapse">
                    <thead>
                      <tr className="bg-gray-100">
                        <th className="p-2 text-left border">Service</th>
                        <th className="p-2 text-left border">Status</th>
                        <th className="p-2 text-left border">Message</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(healthData.services).map(([service, info]) => (
                        <tr key={service}>
                          <td className="p-2 border">{service}</td>
                          <td className="p-2 border">
                            <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                              info.status === 'ok' ? 'bg-green-100 text-green-800' : 
                              info.status === 'warning' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-red-100 text-red-800'
                            }`}>
                              {info.status}
                            </span>
                          </td>
                          <td className="p-2 border">{info.message || ''}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </>
              ) : (
                <div className="text-red-500 p-4">
                  Error loading health data. Please try again.
                </div>
              )}
            </div>

            <div className="p-4 border-t border-gray-200">
              <button
                onClick={() => setIsHealthModalOpen(false)}
                className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}