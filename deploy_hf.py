import os
from huggingface_hub import HfApi
api_key = None
base_url = None
with open(".env", "r") as f:
    for line in f:
        if line.startswith("OPENAI_API_KEY="):
            api_key = line.split("=", 1)[1].strip()
        elif line.startswith("OPENAI_BASE_URL="):
            base_url = line.split("=", 1)[1].strip()

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
