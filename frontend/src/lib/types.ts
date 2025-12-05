// API Response Types
export interface Document {
    id: string;
    title: string;
    filename: string;
    mime_type: string;
    source_type: string;
    storage_path?: string;
    file_size?: number;
    is_processed: boolean;
    is_indexed: boolean;
    processing_error?: string;
    created_at: string;
    updated_at?: string;
    description?: string;
}

export interface DocumentChunk {
    id: string;
    document_id: string;
    chunk_index: number;
    content: string;
    vector_id?: string;
    metadata?: Record<string, unknown>;
}

export interface DataSource {
    id: string;
    name: string;
    source_type: string;
    connection_details: Record<string, unknown>;
    is_active: boolean;
    last_sync?: string;
    created_at: string;
    updated_at?: string;
}

// Request Types
export interface QueryRequest {
    query: string;
    collection_names?: string[];
    filter_criteria?: Record<string, unknown>;
    document_id?: string;  // Single document ID (deprecated, use document_ids)
    document_ids?: string[];  // Multiple document IDs to filter by
    top_k?: number;
}

export interface UploadDocumentRequest {
    file: File;
    description?: string;
}

export interface ProcessUrlRequest {
    url: string;
    description?: string;
}

export interface AddDataSourceRequest {
    name: string;
    source_type: string;
    connection_details: Record<string, unknown>;
}

// Response Types
export interface QueryResponse {
    query: string;
    answer: string;
    context?: string;
    documents?: Array<{
        content: string;
        metadata: Record<string, unknown>;
    }>;
    metrics: {
        total_time_seconds: number;
        retrieval_time_seconds: number;
        generation_time_seconds: number;
        total_documents: number;
    };
}

export interface ProcessingResponse {
    id?: string;
    status: string;
    message?: string;
    error?: string;
}

export interface HealthStatus {
    status: string;
    services: Record<string, {
        status: string;
        message?: string;
    }>;
}

// UI Types
export interface Message {
    id: string;
    content: string;
    role: 'user' | 'assistant';
    timestamp: Date;
    document_ids?: string[];  // Track which documents were queried
    documents?: Array<{
        content: string;
        metadata: Record<string, unknown>;
    }>;
}

export interface ChatInputProps {
    onSendMessage: (message: string, documentIds?: string[]) => void;
    isDisabled?: boolean;
    availableDocuments?: Document[];  // List of documents for selection
    selectedDocumentIds?: string[];  // Currently selected document IDs
    onDocumentSelectionChange?: (ids: string[]) => void;  // Handler for selection changes
}

export interface ChatMessageProps {
    message: Message;
}

export interface ChatWindowProps {
    messages: Message[];
    isLoading: boolean;
    onSendMessage: (message: string, documentIds?: string[]) => void;
    availableDocuments?: Document[];
    selectedDocumentIds?: string[];
    onDocumentSelectionChange?: (ids: string[]) => void;
}

export interface DocumentListProps {
    documents: Document[];
    onDelete: (id: string) => void;
    isLoading?: boolean;
}

export interface DocumentUploadProps {
    onUpload: (data: UploadDocumentRequest) => void;
    onProcessUrl: (data: ProcessUrlRequest) => void;
}

export interface SourceListProps {
    sources: DataSource[];
    onDelete: (id: string) => void;
    isLoading?: boolean;
}

export interface SourceFormProps {
    onSubmit: (data: AddDataSourceRequest) => void;
}

export interface ModalProps {
    isOpen: boolean;
    onClose: () => void;
    title: string;
    children: React.ReactNode;
}