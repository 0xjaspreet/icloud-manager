"""Authentication and credential management."""
import json
import os
from pathlib import Path

CREDS_DIR = Path.home() / ".config" / "icloud-manager"
CREDS_FILE = CREDS_DIR / "creds.json"


class AuthManager:
    """Manages iCloud authentication and credentials storage."""

    def __init__(self):
        self.email = None
        self.password = None

    @property
    def is_configured(self) -> bool:
        return CREDS_FILE.exists()

    def load(self) -> bool:
        """Load stored credentials. Returns True if successful."""
        if not self.is_configured:
            return False
        with open(CREDS_FILE) as f:
            creds = json.load(f)
        self.email = creds["email"]
        self.password = creds["password"]
        return True

    def save(self, email: str, password: str):
        """Save credentials securely (chmod 600)."""
        CREDS_DIR.mkdir(parents=True, exist_ok=True)
        with open(CREDS_FILE, "w") as f:
            json.dump({"email": email, "password": password}, f)
        os.chmod(CREDS_FILE, 0o600)

    def setup_interactive(self):
        """Interactive setup wizard."""
        print("iCloud Manager — Setup")
        print("=" * 40)
        print()
        print("You'll need an app-specific password from Apple.")
        print("Generate one at: https://appleid.apple.com")
        print("  → Sign in → App-Specific Passwords → Generate")
        print()
        email = input("Apple ID (iCloud email): ").strip()
        password = input("App-specific password: ").strip()
        if not email or not password:
            print("❌ Email and password required.")
            return False
        self.save(email, password)
        print(f"✅ Credentials saved to {CREDS_FILE}")
        return True
