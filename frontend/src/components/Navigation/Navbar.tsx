"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import HealthCheckModal from '@/components/Modals/HealthCheckModal';

interface NavLink {
  name: string;
  href: string;
  icon: React.ReactNode;
}

export default function Navbar() {
  const pathname = usePathname();
  const [showHealthModal, setShowHealthModal] = useState(false);

  const links: NavLink[] = [
    {
      name: 'Chat',
      href: '/',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clipRule="evenodd" />
        </svg>
      ),
    },
    {
      name: 'Documents',
      href: '/documents',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
        </svg>
      ),
    },
    {
      name: 'Data Sources',
      href: '/datasources',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path d="M3 12v3c0 1.657 3.134 3 7 3s7-1.343 7-3v-3c0 1.657-3.134 3-7 3s-7-1.343-7-3z" />
          <path d="M3 7v3c0 1.657 3.134 3 7 3s7-1.343 7-3V7c0 1.657-3.134 3-7 3S3 8.657 3 7z" />
          <path d="M17 5c0 1.657-3.134 3-7 3S3 6.657 3 5s3.134-3 7-3 7 1.343 7 3z" />
        </svg>
      ),
    },
    {
      name: 'WebSocket Test',
      href: '/websocket',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M4.31 2.47a6.5 6.5 0 0110.21 7.43l-.02.03-.01.02-.3.3H14a1 1 0 110 2h-3.26a1 1 0 01-1-1v-3.26a1 1 0 112 0v.26l.13-.14.13-.13a8.5 8.5 0 10-4.91 4.91l.13-.13.14-.13h-.26a1 1 0 010-2h3.26a1 1 0 011 1V14a1 1 0 11-2 0h-.3l-.3-.3-.02-.01-.02-.02a6.5 6.5 0 01-7.43-10.21z" clipRule="evenodd" />
        </svg>
      ),
    },
  ];

  return (
    <>
      <header className="bg-blue-700 text-white shadow-md">
        <div className="container mx-auto py-4 px-6">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clipRule="evenodd" />
              </svg>
              RAG System
            </h1>
            
            <nav className="hidden md:flex space-x-6">
              {links.map((link) => (
                <Link 
                  key={link.href} 
                  href={link.href}
                  className={`flex items-center space-x-1 px-3 py-2 rounded transition hover:bg-blue-600 ${
                    pathname === link.href ? 'bg-blue-800' : ''
                  }`}
                >
                  {link.icon}
                  <span>{link.name}</span>
                </Link>
              ))}
              
              <button
                onClick={() => setShowHealthModal(true)}
                className="flex items-center space-x-1 px-3 py-2 rounded transition hover:bg-blue-600"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
                </svg>
                <span>Health</span>
              </button>
              
              <a
                href="/docs"
                target="_blank"
                rel="noopener noreferrer" 
                className="flex items-center space-x-1 px-3 py-2 rounded transition hover:bg-blue-600"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c-1.255 0-2.443.29-3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
                </svg>
                <span>API Docs</span>
              </a>
            </nav>
            
            <div className="md:hidden">
              {/* Mobile menu button */}
              <button className="text-white">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </header>
      
      <HealthCheckModal isOpen={showHealthModal} onClose={() => setShowHealthModal(false)} />
    </>
  );
}
