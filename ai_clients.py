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
    """Hugging Face MCP client implementation"""
    
    def __init__(self, model: str = "microsoft/DialoGPT-large", **kwargs):
        super().__init__(model, **kwargs)
        self.max_tokens = kwargs.get('max_tokens', 1024)
        self.temperature = kwargs.get('temperature', 0.7)
        self.api_token = kwargs.get('hf_token', None)
        
        # Try to import MCP client
        try:
            import mcp
            self.mcp = mcp
            self._mcp_available = True
        except ImportError:
            self._mcp_available = False
    
    def stream_chat(self, messages: List[Message]) -> Iterator[str]:
        """Stream response from Hugging Face model via MCP"""
        if not self._mcp_available:
            yield "Hugging Face MCP is not available. Please install the 'mcp' package: pip install mcp"
            return
        
        try:
            # Convert messages to prompt format for Hugging Face
            prompt = self._messages_to_prompt(messages)
            
            # Use MCP to query Hugging Face model
            result = self._query_huggingface_model(prompt)
            
            # Stream the response word by word for consistency with Ollama
            if result:
                words = result.split()
                for word in words:
                    yield word + " "
            else:
                yield "The mystical AI oracle remains silent..."
                
        except Exception as e:
            yield f"The Hugging Face oracle encounters an error: {str(e)}"
    
    def _messages_to_prompt(self, messages: List[Message]) -> str:
        """Convert message history to a single prompt"""
        prompt_parts = []
        
        for message in messages:
            if message.role == "system":
                prompt_parts.append(f"System: {message.content}")
            elif message.role == "user":
                prompt_parts.append(f"Human: {message.content}")
            elif message.role == "assistant":
                prompt_parts.append(f"Assistant: {message.content}")
        
        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)
    
    def _query_huggingface_model(self, prompt: str) -> str:
        """Query Hugging Face model using MCP tools"""
        try:
            # Use the Hugging Face MCP tools to generate text
            # This is a simplified implementation - in practice, you'd use the actual MCP tools
            
            # For text generation models, we'll use a simple approach
            # In a real implementation, you'd use the specific MCP tools available
            
            # Placeholder for actual MCP implementation
            # This would be replaced with actual MCP tool calls
            
            # Simulate text generation for now
            return self._simulate_text_generation(prompt)
            
        except Exception as e:
            raise Exception(f"HuggingFace MCP query failed: {str(e)}")
    
    def _simulate_text_generation(self, prompt: str) -> str:
        """Simulate text generation - replace with actual MCP calls"""
        # This is a placeholder that would be replaced with actual Hugging Face MCP calls
        # For now, we'll return a simple response to demonstrate the architecture
        
        # Extract the last user input to provide a contextual response
        lines = prompt.split('\n')
        last_human_input = ""
        for line in reversed(lines):
            if line.startswith("Human:"):
                last_human_input = line[6:].strip()
                break
        
        # Simple rule-based responses for demonstration
        responses = [
            f"The underground empire echoes with your words: '{last_human_input}'. Ancient magic swirls around you as new possibilities unfold.",
            f"Your action '{last_human_input}' resonates through the chambers of Zork. The stone walls seem to shimmer with otherworldly energy.",
            f"As you {last_human_input.lower()}, the mystical forces of the empire respond. Shadows dance in the flickering light of your lantern.",
        ]
        
        # Simple hash-based selection for consistency
        import hashlib
        hash_value = int(hashlib.md5(last_human_input.encode()).hexdigest()[:8], 16)
        return responses[hash_value % len(responses)]
    
    def is_available(self) -> bool:
        """Check if Hugging Face MCP is available"""
        return self._mcp_available


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
