import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Combines class names with Tailwind's merge function
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Formats a date for display
 */
export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleString();
}

/**
 * Gets a human-readable file size
 */
export function formatFileSize(bytes?: number | null): string {
  if (bytes === undefined || bytes === null) return 'Unknown size';
  
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let size = bytes;
  let unitIndex = 0;
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }
  
  return `${size.toFixed(1)} ${units[unitIndex]}`;
}

/**
 * Extracts a unique source identifier from document metadata
 */
export function getSourceIdentifier(metadata: Record<string, unknown>): string {
  const filename = metadata.filename as string | undefined;
  const url = metadata.url as string | undefined;
  const title = metadata.title as string | undefined;
  const id = metadata.id as string | number | undefined;
  
  return filename || 
         url || 
         title ||
         `Source ${id || 'unknown'}`;
}

/**
 * Gets unique sources from a list of documents with counts
 */
export function getUniqueSources(documents: Array<{content: string; metadata: Record<string, unknown>}>): Array<{source: string; count: number}> {
  const sourceCounts: Record<string, number> = {};
  
  documents.forEach(doc => {
    const source = getSourceIdentifier(doc.metadata);
    sourceCounts[source] = (sourceCounts[source] || 0) + 1;
  });
  
  return Object.entries(sourceCounts).map(([source, count]) => ({
    source,
    count
  }));
}

/**
 * Truncates text to a maximum length with ellipsis
 */
export function truncateText(text: string, maxLength: number = 100): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}

/**
 * Creates a WebSocket connection
 */
export function createWebSocket(): WebSocket | null {
  try {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/api/ws`;
    
    return new WebSocket(wsUrl);
  } catch (error) {
    console.error('Error creating WebSocket:', error);
    return null;
  }
}