import os
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

def check_backend_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=3)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

def format_chat_message(role, content):
    return {"role": role, "content": content}

def process_memory_api(messages, context_window, session_id="default"):
    try:
        payload = {
            "session_id": session_id,
            "messages": messages,
            "context_window": context_window
        }
        response = requests.post(f"{API_BASE_URL}/memory/process", json=payload, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        pass
    return None

def improve_prompt_api(prompt):
    try:
        response = requests.post(f"{API_BASE_URL}/improve-prompt", json={"original_prompt": prompt}, timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        pass
    return None

def chat_stream_api(messages, model, session_id="default", **kwargs):
    import json
    try:
        payload = {
            "session_id": session_id,
            "messages": messages, 
            "model": model,
            "search_strategy": kwargs.get("search_strategy", "similarity"),
            "top_k": kwargs.get("top_k", 4),
            "similarity_threshold": kwargs.get("similarity_threshold", 0.5)
        }
        response = requests.post(f"{API_BASE_URL}/chat/stream", json=payload, stream=True, timeout=60)
        
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith("data: "):
                        data_str = decoded_line[6:]
                        try:
                            data = json.loads(data_str)
                            if data.get("type") == "content":
                                yield data.get("content", "")
                            elif data.get("type") == "metrics":
                                st.session_state["last_generation_metrics"] = data.get("metrics")
                        except json.JSONDecodeError:
                            pass
        else:
            yield f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        yield f"Connection Exception: {str(e)}"

def upload_document_api(file_obj, session_id="default"):
    try:
        files = {"file": (file_obj.name, file_obj, file_obj.type)}
        data = {"session_id": session_id}
        response = requests.post(f"{API_BASE_URL}/upload", files=files, data=data, timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        pass
    return None

def get_documents_api(session_id="default"):
    try:
        response = requests.get(f"{API_BASE_URL}/documents", params={"session_id": session_id}, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        pass
    return []

def delete_document_api(document_id, session_id="default"):
    try:
        response = requests.delete(f"{API_BASE_URL}/documents/{document_id}", params={"session_id": session_id}, timeout=5)
        if response.status_code == 200:
            return True
    except Exception as e:
        pass
    return False

def get_diagnostics_api():
    try:
        response = requests.get(f"{API_BASE_URL}/diagnostics/state", timeout=2)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        pass
    return None

