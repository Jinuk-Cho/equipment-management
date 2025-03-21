import hashlib
import json
from pathlib import Path

def load_users():
    """사용자 정보를 로드합니다."""
    users_file = Path("config/users.json")
    if not users_file.exists():
        return {}
    
    with open(users_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    """사용자 정보를 저장합니다."""
    users_file = Path("config/users.json")
    users_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(users_file, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def hash_password(password):
    """비밀번호를 해시화합니다."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(username, password):
    """사용자 인증을 수행합니다."""
    users = load_users()
    if username not in users:
        return False
    
    hashed_password = hash_password(password)
    return users[username]["password"] == hashed_password

def login_user(username):
    """사용자 로그인 처리를 수행합니다."""
    users = load_users()
    if username in users:
        return users[username]["role"]
    return None

def create_user(username, password, role="user"):
    """새로운 사용자를 생성합니다."""
    users = load_users()
    if username in users:
        return False
    
    users[username] = {
        "password": hash_password(password),
        "role": role
    }
    save_users(users)
    return True

def update_user_role(username, new_role):
    """사용자의 역할을 업데이트합니다."""
    users = load_users()
    if username not in users:
        return False
    
    users[username]["role"] = new_role
    save_users(users)
    return True

def delete_user(username):
    """사용자를 삭제합니다."""
    users = load_users()
    if username not in users:
        return False
    
    del users[username]
    save_users(users)
    return True 