import axios, { AxiosInstance } from 'axios';
import { 
  Document, 
  DataSource, 
  QueryRequest, 
  QueryResponse,
  ProcessingResponse,
  HealthStatus,
  UploadDocumentRequest,
  ProcessUrlRequest,
  AddDataSourceRequest
} from './types';

interface UploadResponse {
  success: boolean;
  message?: string;
  fileId?: string;
  // ...other fields
}

class Api {
  private client: AxiosInstance;
  private API_BASE_URL: string;

  constructor() {
    // Always use relative path for browser requests - let Next.js rewrites handle proxying to backend
    // This works both in development and production Docker environments
    this.API_BASE_URL = '/api/v1';
     
    console.log(`Using API base URL: ${this.API_BASE_URL}`);
     
    this.client = axios.create({
      baseURL: this.API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Chat & Query

  async generateAnswer(data: QueryRequest): Promise<QueryResponse> {
    // Use the general query endpoint - it handles both single and multiple document filtering
    const response = await this.client.post<QueryResponse>('/query/generate', data);
    return response.data;
  }

  async retrieveDocuments(data: QueryRequest): Promise<{ documents: Array<{content: string; metadata: Record<string, unknown>}> }> {
    const response = await this.client.post('/query/retrieve', data);
    return response.data;
  }

  // Documents

  async getDocuments(): Promise<Document[]> {
    const response = await this.client.get<Document[]>('/documents');
    return response.data;
  }

  async getDocument(id: string): Promise<Document> {
    const response = await this.client.get<Document>(`/documents/${id}`);
    return response.data;
  }

  async uploadDocument({ file, description }: UploadDocumentRequest): Promise<ProcessingResponse> {
    const formData = new FormData();
    formData.append('file', file);
    
    if (description) {
      formData.append('description', description);
    }
    
    const response = await this.client.post<ProcessingResponse>(
      '/documents/upload', 
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    
    return response.data;
  }

  async processUrl(data: ProcessUrlRequest): Promise<ProcessingResponse> {
    const response = await this.client.post<ProcessingResponse>('/documents/web', data);
    return response.data;
  }

  async deleteDocument(id: string): Promise<ProcessingResponse> {
    const response = await this.client.delete<ProcessingResponse>(`/documents/${id}`);
    return response.data;
  }

  // Data Sources

  async getDataSources(): Promise<DataSource[]> {
    const response = await this.client.get<DataSource[]>('/datasources');
    return response.data;
  }

  async addDataSource(data: AddDataSourceRequest): Promise<DataSource> {
    const response = await this.client.post<DataSource>('/datasources', data);
    return response.data;
  }

  async deleteDataSource(id: string): Promise<ProcessingResponse> {
    const response = await this.client.delete<ProcessingResponse>(`/datasources/${id}`);
    return response.data;
  }

  // System Health

  async checkHealth(): Promise<HealthStatus> {
    const response = await this.client.get<HealthStatus>('/health/');
    return response.data;
  }
}

export const uploadFile = async (formData: FormData): Promise<UploadResponse> => {
  const response = await axios.post<UploadResponse>('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

const api = new Api();
export default api;