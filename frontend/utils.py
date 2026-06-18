import os
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

def check_backend_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

def format_chat_message(role, content):
    return {"role": role, "content": content}

def process_memory_api(messages, context_window):
    try:
        payload = {
            "session_id": "default",
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

def chat_api(messages, model):
    try:
        payload = {"messages": messages, "model": model}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection Exception: {e}")
    return None
