/**
 * WebSocket client for real-time communication with the RAG system
 */

type WebSocketMessage = {
  type: string;
  content: unknown;
};

type MessageHandler = (message: WebSocketMessage | string) => void;

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private connectionPromise: Promise<WebSocket> | null = null;
  private messageHandlers: MessageHandler[] = [];
  private reconnectTimer: NodeJS.Timeout | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 3000; // 3 seconds

  /**
   * Connect to the WebSocket server
   */
  connect(): Promise<WebSocket> {
    if (this.connectionPromise) {
      return this.connectionPromise;
    }

    this.connectionPromise = new Promise((resolve, reject) => {
      try {
        // Use environment variable for API URL if available
        const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';
        const protocol = apiBaseUrl.startsWith('https') ? 'wss:' : 'ws:';
        
        // Extract host from API URL or use default
        let host = 'localhost:8080';
        if (apiBaseUrl) {
          try {
            const url = new URL(apiBaseUrl);
            host = url.host;
          } catch {
            // Ignoring URL parsing error
            console.warn('Invalid API URL format, using default host');
          }
        }
        
        const wsUrl = `${protocol}//${host}/api/ws`;
        console.log('Connecting to WebSocket:', wsUrl);
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
          console.log('WebSocket connected');
          this.reconnectAttempts = 0;
          resolve(this.ws as WebSocket);
        };
        
        this.ws.onmessage = (event) => {
          try {
            // First try to parse as JSON
            let data;
            try {
              data = JSON.parse(event.data);
            } catch {
              // If it's not valid JSON, treat it as a plain text message
              console.log('Received non-JSON message:', event.data);
              data = {
                type: 'text',
                content: event.data
              };
            }
            
            // Notify all message handlers
            this.messageHandlers.forEach(handler => handler(data));
          } catch (error) {
            console.error('Error handling WebSocket message:', error);
          }
        };
        
        this.ws.onclose = () => {
          console.log('WebSocket disconnected');
          this.ws = null;
          this.connectionPromise = null;
          
          this.attemptReconnect();
        };
        
        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          reject(error);
        };
      } catch (error) {
        console.error('Error creating WebSocket:', error);
        this.connectionPromise = null;
        reject(error);
      }
    });
    
    return this.connectionPromise;
  }
  
  /**
   * Attempt to reconnect to the WebSocket server
   */
  private attemptReconnect() {
    if (this.reconnectTimer || this.reconnectAttempts >= this.maxReconnectAttempts) {
      return;
    }
    
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null;
      this.reconnectAttempts++;
      
      console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
      
      this.connect().catch(() => {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.attemptReconnect();
        } else {
          console.error('Max reconnect attempts reached');
        }
      });
    }, this.reconnectDelay);
  }
  
  /**
   * Send a message to the WebSocket server
   */
  async send(message: WebSocketMessage): Promise<boolean> {
    try {
      const ws = await this.connect();
      ws.send(JSON.stringify(message));
      return true;
    } catch (error) {
      console.error('Error sending WebSocket message:', error);
      return false;
    }
  }
  
  /**
   * Add a message handler
   */
  addMessageHandler(handler: MessageHandler): void {
    this.messageHandlers.push(handler);
  }
  
  /**
   * Remove a message handler
   */
  removeMessageHandler(handler: MessageHandler): void {
    this.messageHandlers = this.messageHandlers.filter(h => h !== handler);
  }
  
  /**
   * Disconnect from the WebSocket server
   */
  disconnect(): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.close();
    }
    
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    
    this.ws = null;
    this.connectionPromise = null;
    this.messageHandlers = [];
  }
}

// Singleton instance
export const webSocketClient = new WebSocketClient();

export default webSocketClient;