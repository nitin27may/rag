import ReactMarkdown from 'react-markdown';
import { ChatMessageProps } from '@/lib/types';
import { getUniqueSources } from '@/lib/utils';
import { DocumentTextIcon } from '@heroicons/react/24/outline';
import type { Components } from 'react-markdown';
import type { ReactNode, ClassAttributes, HTMLAttributes } from 'react';

// Define CodeProps interface that specifically includes the 'inline' property
interface CodeProps extends ClassAttributes<HTMLElement>, HTMLAttributes<HTMLElement> {
  inline?: boolean;
  className?: string;
  children?: ReactNode;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  // Get unique sources with counts
  const sources = message.documents ? getUniqueSources(message.documents) : [];
  
  // Define custom components for markdown rendering based on message role
  const components: Components = {
    p: ({ children }) => (
      <p className={`my-2 ${message.role === 'user' ? 'text-white' : 'text-gray-800'}`}>
        {children}
      </p>
    ),
    pre: ({ children }) => (
      <pre className="bg-gray-800 text-white p-2 rounded my-2 overflow-x-auto">
        {children}
      </pre>
    ),
    code: ({ inline, className, children, ...props }: CodeProps) => {
      if (inline) {
        return (
          <code 
            className={`px-1 rounded ${
              message.role === 'user' 
                ? 'bg-blue-700 text-white' 
                : 'bg-gray-200 text-gray-800'
            }`} 
            {...props}
          >
            {children}
          </code>
        );
      }
      return (
        <code className={className || "text-sm block"} {...props}>
          {children}
        </code>
      );
    },
    ul: ({ children }) => (
      <ul className={`list-disc pl-5 my-2 ${message.role === 'user' ? 'text-white' : ''}`}>
        {children}
      </ul>
    ),
    ol: ({ children }) => (
      <ol className={`list-decimal pl-5 my-2 ${message.role === 'user' ? 'text-white' : ''}`}>
        {children}
      </ol>
    ),
    li: ({ children }) => (
      <li className={`mb-1 ${message.role === 'user' ? 'text-white' : ''}`}>
        {children}
      </li>
    ),
    a: ({ children, ...props }) => (
      <a 
        className={`hover:underline ${message.role === 'user' ? 'text-blue-200' : 'text-blue-600'}`} 
        target="_blank" 
        rel="noopener noreferrer" 
        {...props}
      >
        {children}
      </a>
    ),
    h1: ({ children }) => (
      <h1 className={`text-2xl font-bold my-4 ${message.role === 'user' ? 'text-white' : ''}`}>
        {children}
      </h1>
    ),
    h2: ({ children }) => (
      <h2 className={`text-xl font-bold my-3 ${message.role === 'user' ? 'text-white' : ''}`}>
        {children}
      </h2>
    ),
    h3: ({ children }) => (
      <h3 className={`text-lg font-bold my-2 ${message.role === 'user' ? 'text-white' : ''}`}>
        {children}
      </h3>
    ),
    blockquote: ({ children }) => (
      <blockquote className={`pl-4 border-l-4 ${
        message.role === 'user' 
          ? 'border-blue-400 text-blue-100' 
          : 'border-gray-300 text-gray-700'
        } italic my-2`}>
        {children}
      </blockquote>
    ),
    hr: () => <hr className={`my-4 ${message.role === 'user' ? 'border-blue-300' : 'border-gray-300'}`} />
  };
  
  return (
    <div
      className={`mb-4 w-full ${
        message.role === 'user'
          ? 'ml-auto text-right flex justify-end'
          : 'mr-auto'
      }`}
    >
      <div
        className={`inline-block text-left ${
          message.role === 'user'
            ? 'bg-blue-600 text-white rounded-tl-xl rounded-bl-xl rounded-tr-xl max-w-xl'
            : 'bg-gray-100 text-gray-900 rounded-tr-xl rounded-br-xl rounded-tl-xl max-w-3xl'
        }`}
      >
        <div className="p-4">
          {/* Display document IDs badge if present */}
          {message.document_ids && message.document_ids.length > 0 && (
            <div className={`mb-2 flex items-center ${
              message.role === 'user' ? 'text-blue-200' : 'text-blue-700'
            }`}>
              <DocumentTextIcon className="h-4 w-4 mr-1" />
              <span className="text-xs font-medium">
                {message.document_ids.length === 1 
                  ? `Document: ${message.document_ids[0].substring(0, 8)}...`
                  : `${message.document_ids.length} documents selected`}
              </span>
            </div>
          )}
          
          <ReactMarkdown components={components}>
            {message.content}
          </ReactMarkdown>
          
          {sources.length > 0 && (
            <div className="mt-4 pt-2 border-t border-gray-200 text-xs text-gray-500">
              <span className="font-semibold">Sources:</span>{' '}
              {sources.map((source, index) => (
                <span key={source.source} className="inline-block">
                  {index > 0 && ', '}
                  {source.source}
                  {source.count > 1 ? ` (${source.count} chunks)` : ''}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}