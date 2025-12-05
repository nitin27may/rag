import logging
import time
from typing import Dict, Any, List, Optional
import httpx

# Update imports for better compatibility
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from sqlalchemy.orm import Session

from app.services.retrieval.retriever import rag_retriever
from app.models.document import QueryLog
from app.core.config import settings

logger = logging.getLogger(__name__)


def get_httpx_client():
    """Create httpx client based on DISABLE_SSL_VERIFICATION env variable."""
    if settings.DISABLE_SSL_VERIFICATION:
        logger.warning("SSL verification is disabled for LLM. This should only be used in development/corporate proxy environments.")
        return httpx.Client(verify=False)
    return httpx.Client()


class RAGGenerator:
    """Service to generate responses using a RAG pipeline"""
    
    def __init__(self):
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the Language Model (LLM) based on configured provider"""
        if settings.LLM_PROVIDER == "azure":
            try:
                self._initialize_azure_openai()
                if self.llm is None:
                    logger.warning("Azure OpenAI initialization failed, falling back to OpenAI")
                    self._initialize_openai()
            except Exception as e:
                logger.error(f"Azure OpenAI initialization failed: {e}, falling back to OpenAI")
                self._initialize_openai()
        else:
            self._initialize_openai()
            
        # If both Azure and OpenAI failed, use a mock LLM as fallback
        if self.llm is None:
            logger.warning("All LLM initializations failed, using mock LLM as fallback")
            self._initialize_mock_llm()

    def _initialize_openai(self):
        """Initialize OpenAI LLM"""
        if not settings.OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY is not configured in the environment.")
            return
        
        try:
            logger.info(f"Initializing OpenAI LLM with model: {settings.OPENAI_MODEL}")
            
            # Initialize ChatOpenAI with the correct parameters
            self.llm = ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model_name=settings.OPENAI_MODEL,
                temperature=0.0,
                http_client=get_httpx_client(),
            )
            
            # Test the LLM to ensure it works
            test_response = self.llm.invoke("Hello, this is a test message.")
            logger.info(f"OpenAI LLM initialization test successful. Model: {settings.OPENAI_MODEL}")
            
        except Exception as e:
            logger.error(f"Error initializing OpenAI LLM: {str(e)}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            self.llm = None
    
    def _initialize_azure_openai(self):
        """Initialize Azure OpenAI LLM"""
        if not all([settings.AZURE_OPENAI_API_KEY, settings.AZURE_OPENAI_ENDPOINT, settings.AZURE_OPENAI_DEPLOYMENT]):
            logger.error("Azure OpenAI configuration is incomplete. Please check AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, and AZURE_OPENAI_DEPLOYMENT.")
            return
        
        try:
            logger.info(f"Initializing Azure OpenAI LLM with deployment: {settings.AZURE_OPENAI_DEPLOYMENT}")
            
            # Initialize AzureChatOpenAI with the correct parameters
            self.llm = AzureChatOpenAI(
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                api_key=settings.AZURE_OPENAI_API_KEY,
                azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT,
                api_version=settings.AZURE_OPENAI_API_VERSION,
                temperature=0.0,
                http_client=get_httpx_client(),
            )
            
            # Test the LLM to ensure it works
            test_response = self.llm.invoke("Hello, this is a test message.")
            logger.info(f"Azure OpenAI LLM initialization test successful. Deployment: {settings.AZURE_OPENAI_DEPLOYMENT}")
            
        except Exception as e:
            logger.error(f"Error initializing Azure OpenAI LLM: {str(e)}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            # We don't set self.llm = None here so the caller can handle fallback
            raise
            
    def _initialize_mock_llm(self):
        """Initialize a mock LLM as fallback - raises error since LLM is required"""
        logger.error("All LLM initializations failed. Please configure valid Azure OpenAI or OpenAI credentials.")
        raise RuntimeError("Failed to initialize any LLM. Please check your AZURE_OPENAI or OPENAI configuration.")
    
    def call_llm(self, prompt: str) -> str:
        """
        Direct method to call the LLM with a prompt string
        
        Args:
            prompt: The prompt text to send to the LLM
            
        Returns:
            The LLM's response as a string
        """
        if not self.llm:
            logger.error("LLM is not initialized. Cannot generate a response.")
            return "Error: Language model not available. Please check your configuration."
            
        try:
            # Use direct invocation of the LLM
            chat_response = self.llm.invoke(prompt)
            
            # Extract the content from the response
            if hasattr(chat_response, 'content'):
                return chat_response.content
            else:
                return str(chat_response)
                
        except Exception as e:
            logger.error(f"Error calling LLM: {str(e)}")
            import traceback
            logger.error(f"LLM call traceback: {traceback.format_exc()}")
            return f"Error generating response: {str(e)}"
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create a prompt template for the RAG system with guardrails"""
        template = """
        You are a helpful assistant that ONLY provides information based on the documents in the provided context.
        
        IMPORTANT GUARDRAILS:
        1. You MUST answer questions using ONLY the information in the Context section below
        2. If the answer is not found in the provided context, you MUST respond with: "I don't have information about that in the available documents."
        3. DO NOT use external knowledge, internet searches, or information outside the provided context
        4. DO NOT make assumptions or inferences beyond what is explicitly stated in the context
        5. If asked to do something outside of answering questions from the documents (like writing code, performing calculations, or accessing external resources), respond with: "I can only answer questions based on the available documents."
        
        Context from documents:
        {context}
        
        Question: {query}
        
        Answer (based ONLY on the context above):
        """
        
        return PromptTemplate(
            input_variables=["context", "query"],
            template=template.strip()
        )
    
    def generate_response(
        self, 
        query: str,
        collection_names: List[str] = None,
        filter_criteria: Optional[Dict[str, Any]] = None,
        document_id: Optional[str] = None,
        document_ids: Optional[List[str]] = None,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """Generate a response using the RAG pipeline"""
        start_time = time.time()
        
        if not self.llm:
            logger.error("LLM is not initialized. Cannot generate a response.")
            return {
                "answer": "Error: Language model not available. Please check your configuration.",
                "context": "",
                "documents": [],
                "metrics": {
                    "error": "LLM not initialized"
                }
            }
        
        try:
            # Retrieve relevant context
            retrieval_start = time.time()
            retrieval_result = rag_retriever.retrieve_for_rag(
                query=query,
                collection_names=collection_names,
                filter_criteria=filter_criteria,
                document_id=document_id,
                document_ids=document_ids,
                top_k=settings.MAX_RETRIEVED_DOCUMENTS,
                db=db
            )
            retrieval_time = time.time() - retrieval_start
            
            context = retrieval_result.get("context", "")
            documents = retrieval_result.get("documents", [])
            
            # If no context was found, return a default response
            if not context:
                return {
                    "answer": "I couldn't find any relevant information to answer your question.",
                    "context": "",
                    "documents": [],
                    "metrics": {
                        "total_time_seconds": time.time() - start_time,
                        "retrieval_time_seconds": retrieval_time,
                        "generation_time_seconds": 0,
                        "total_documents": 0
                    }
                }
            
            # Generate response using LLM directly instead of through Chain
            generation_start = time.time()
            prompt_template = self._create_prompt_template()
            prompt = prompt_template.format(context=context, query=query)
            
            try:
                # Use the call_llm method for consistency
                response = self.call_llm(prompt)
                generation_time = time.time() - generation_start
                
            except Exception as e:
                logger.error(f"Error during LLM processing: {str(e)}")
                import traceback
                logger.error(f"LLM processing traceback: {traceback.format_exc()}")
                return {
                    "answer": f"Error generating response: {str(e)}",
                    "context": context,
                    "documents": documents,
                    "metrics": {
                        "total_time_seconds": time.time() - start_time,
                        "retrieval_time_seconds": retrieval_time,
                        "error": str(e)
                    }
                }
            
            # Log the query
            if db:
                try:
                    log_entry = QueryLog(
                        query_text=query,
                        query_type="semantic",
                        parameters={
                            "collection_names": collection_names, 
                            "filter_criteria": filter_criteria,
                            "document_id": document_id
                        },
                        document_ids=[doc.metadata.get("id", "") for doc in documents if hasattr(doc, 'metadata')],
                        retrieval_time_ms=retrieval_time * 1000,
                        generation_time_ms=generation_time * 1000,
                        total_time_ms=(time.time() - start_time) * 1000
                    )
                    db.add(log_entry)
                    db.commit()
                except Exception as log_error:
                    logger.error(f"Error logging query: {str(log_error)}")
            
            total_time = time.time() - start_time
            
            return {
                "answer": response,
                "context": context,
                "documents": documents,
                "metrics": {
                    "total_time_seconds": total_time,
                    "retrieval_time_seconds": retrieval_time,
                    "generation_time_seconds": generation_time,
                    "total_documents": len(documents)
                }
            }
        
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                "answer": f"An error occurred while processing your query: {str(e)}",
                "context": "",
                "documents": [],
                "metrics": {
                    "total_time_seconds": time.time() - start_time,
                    "error": str(e)
                }
            }

# Singleton instance
rag_generator = RAGGenerator()