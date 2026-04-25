"""Authentication and credential management.

SECURITY NOTE: Credentials are stored as plaintext JSON with chmod 600.
This protects against other users on the system, but any process running
as the same user can read them. This is the standard approach for CLI tools
(AWS CLI, kubectl, etc.). For stronger protection, use full-disk encryption
or a dedicated secrets manager.
"""
import json
import os
import tempfile
import getpass
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
        try:
            with open(CREDS_FILE) as f:
                creds = json.load(f)
            self.email = creds["email"]
            self.password = creds["password"]
            return True
        except (json.JSONDecodeError, KeyError, OSError) as e:
            print(f"❌ Failed to load credentials: {e}")
            return False

    def save(self, email: str, password: str):
        """Save credentials atomically with restricted permissions."""
        CREDS_DIR.mkdir(parents=True, exist_ok=True)
        # Write to temp file first, then atomic rename
        tmp_fd, tmp_path = tempfile.mkstemp(dir=CREDS_DIR, prefix=".creds-")
        try:
            with os.fdopen(tmp_fd, "w") as f:
                json.dump({"email": email, "password": password}, f)
            os.chmod(tmp_path, 0o600)
            os.rename(tmp_path, CREDS_FILE)
        except Exception:
            # Clean up temp file on failure
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise

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
        password = getpass.getpass("App-specific password: ").strip()
        if not email or not password:
            print("❌ Email and password required.")
            return False
        self.save(email, password)
        print(f"✅ Credentials saved to {CREDS_FILE}")
        return True
