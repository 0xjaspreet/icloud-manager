"""iCloud Drive service."""
import json
from pyicloud import PyiCloudService


class DriveService:
    def __init__(self, api: PyiCloudService):
        self.drive = api.drive

    def list(self) -> str:
        try:
            items = list(self.drive.dir())
            out = []
            for item in items:
                out.append({
                    "name": getattr(item, "name", str(item)),
                    "type": getattr(item, "type", "?"),
                    "size": getattr(item, "size", None),
                })
            return json.dumps(out, indent=2, default=str)
        except Exception as e:
            return json.dumps({"error": str(e)})
