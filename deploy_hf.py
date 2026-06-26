import os
from huggingface_hub import HfApi
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

# Credentials
token = os.getenv("HF_TOKEN", "")
username = "vKrish14"
repo_name = "chatbot-v2"
repo_id = f"{username}/{repo_name}"

api = HfApi(token=token)

print(f"Creating Space: {repo_id}...")
try:
    api.create_repo(repo_id=repo_id, repo_type="space", space_sdk="docker", exist_ok=True)
except Exception as e:
    print(f"Repo might already exist or error: {e}")

print("Setting secrets...")
if api_key:
    api.add_space_secret(repo_id=repo_id, key="OPENAI_API_KEY", value=api_key)
if base_url:
    api.add_space_secret(repo_id=repo_id, key="OPENAI_BASE_URL", value=base_url)

print("Uploading files...")
# Upload necessary files and folders
api.upload_folder(
    folder_path=".",
    repo_id=repo_id,
    repo_type="space",
    allow_patterns=["Dockerfile", "start.sh", "backend/**", "frontend/**", "find_models.py"],
    ignore_patterns=[".env", ".env.example", ".git/**", "__pycache__/**"]
)

print(f"Done! Your space is live at: https://huggingface.co/spaces/{repo_id}")
