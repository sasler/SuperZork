#!/usr/bin/env python3
"""
AI Client implementations for SuperZork
Supports both Ollama and Hugging Face MCP backends
"""

import json
import requests
import asyncio
from abc import ABC, abstractmethod
from typing import Iterator, List, Dict, Any, Optional
from pathlib import Path


class Message:
    """Type definition for chat messages"""
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
    
    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


class AIClient(ABC):
    """Abstract base class for AI clients"""
    
    def __init__(self, model: str, **kwargs):
        self.model = model
        self.config = kwargs
    
    @abstractmethod
    def stream_chat(self, messages: List[Message]) -> Iterator[str]:
        """Stream chat response from the AI model"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the AI backend is available"""
        pass


class OllamaClient(AIClient):
    """Ollama AI client implementation"""
    
    def __init__(self, model: str = "phi4-mini", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = kwargs.get('ollama_url', 'http://localhost:11434')
        self.num_ctx = kwargs.get('num_tokens', 4096)
        self.temperature = kwargs.get('temperature', 0.7)
    
    def stream_chat(self, messages: List[Message]) -> Iterator[str]:
        """Stream response from Ollama LLM"""
        # Convert messages to dict format
        message_dicts = [msg.to_dict() for msg in messages]
        
        # Prepare request payload
        payload = {
            "model": self.model,
            "messages": message_dicts,
            "stream": True,
            "options": {
                "num_ctx": self.num_ctx,
                "temperature": self.temperature,
            }
        }
        
        try:
            # Increase timeout and add connection timeout
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                stream=True,
                timeout=(10, 120)  # (connection timeout, read timeout)
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    try:
                        json_data = json.loads(line)
                        if 'message' in json_data and 'content' in json_data['message']:
                            content = json_data['message']['content']
                            if content:
                                yield content
                        # Check if we've reached the end of the response
                        if json_data.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue
                        
        except requests.exceptions.Timeout:
            yield "The ancient spirits are taking their time to respond... Perhaps try a simpler command or restart the game if this persists."
        except requests.exceptions.ConnectionError:
            yield "The magical connection to the underground realm has been severed. Please ensure Ollama is running and try again."
        except requests.exceptions.RequestException as e:
            yield f"The mystical AI oracle has encountered an error: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False


class HuggingFaceClient(AIClient):
    """Hugging Face client implementation using HTTP API"""
    
    def __init__(self, model: str = "microsoft/DialoGPT-large", **kwargs):
        super().__init__(model, **kwargs)
        self.max_tokens = kwargs.get('max_tokens', 1024)
        self.temperature = kwargs.get('temperature', 0.7)
        self.api_token = kwargs.get('hf_token', None)
        
        # Set up API endpoint
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        
        # Headers for API requests
        self.headers = {
            "Content-Type": "application/json",
        }
        if self.api_token:
            self.headers["Authorization"] = f"Bearer {self.api_token}"
    
    def stream_chat(self, messages: List[Message]) -> Iterator[str]:
        """Stream response from Hugging Face model"""
        try:
            # Convert messages to prompt format for Hugging Face
            prompt = self._messages_to_prompt(messages)
            
            # Use Hugging Face Inference API
            result = self._query_huggingface_api(prompt)
            
            # Stream the response word by word for consistency with Ollama
            if result:
                words = result.split()
                for word in words:
                    yield word + " "
            else:
                yield "The cloud-based AI oracle remains silent..."
                
        except Exception as e:
            yield f"The Hugging Face oracle encounters an error: {str(e)}"
    
    def _messages_to_prompt(self, messages: List[Message]) -> str:
        """Convert message history to a single prompt"""
        prompt_parts = []
        
        # Skip system message for now as it's very long
        for message in messages[1:]:  # Skip system message
            if message.role == "user":
                prompt_parts.append(f"Human: {message.content}")
            elif message.role == "assistant":
                prompt_parts.append(f"Assistant: {message.content}")
        
        # Add the prompt for the next assistant response
        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)
    
    def _query_huggingface_api(self, prompt: str) -> str:
        """Query Hugging Face Inference API"""
        try:
            import requests
            
            # Prepare payload for text generation
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": min(self.max_tokens, 200),  # Conservative limit
                    "temperature": self.temperature,
                    "return_full_text": False,
                    "do_sample": True,
                }
            }
            
            # Make request to Hugging Face API
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    return generated_text
                else:
                    return "The cloud spirits whisper mysteriously..."
            elif response.status_code == 401:
                return "The Hugging Face oracle requires authentication. Please provide an HF token in your story configuration (hf_token field) to access cloud models."
            elif response.status_code == 503:
                return "The Hugging Face model is loading... Please try again in a moment."
            elif response.status_code == 429:
                return "The cloud oracle is experiencing high demand. Please try again shortly."
            else:
                return f"The cloud oracle responds with status {response.status_code}. For better access, consider providing an API token."
                
        except ImportError:
            return "The requests library is required for Hugging Face API access."
        except Exception as e:
            raise Exception(f"HuggingFace API query failed: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if Hugging Face API is available"""
        try:
            import requests
            # Test with a simple request to check API availability
            test_response = requests.get(
                "https://api-inference.huggingface.co/models/gpt2",
                headers=self.headers,
                timeout=5
            )
            # Accept 200 (OK), 401 (needs token), 503 (model loading) as "available"
            # 401 means the API is accessible but needs authentication
            return test_response.status_code in [200, 401, 503]
        except:
            return False


def create_ai_client(backend: str, model: str, **kwargs) -> AIClient:
    """Factory function to create AI clients"""
    if backend.lower() == "ollama":
        return OllamaClient(model, **kwargs)
    elif backend.lower() == "huggingface":
        return HuggingFaceClient(model, **kwargs)
    else:
        raise ValueError(f"Unknown AI backend: {backend}")


def get_available_backends() -> List[str]:
    """Get list of available AI backends"""
    available = []
    
    # Check Ollama
    try:
        ollama_client = OllamaClient()
        if ollama_client.is_available():
            available.append("ollama")
    except:
        pass
    
    # Check Hugging Face MCP
    try:
        hf_client = HuggingFaceClient()
        if hf_client.is_available():
            available.append("huggingface")
    except:
        pass
    
    return available
