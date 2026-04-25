"""Find My iPhone service."""
import json
from pyicloud import PyiCloudService


class FindMyService:
    def __init__(self, api: PyiCloudService):
        self.devices = api.devices

    def list(self) -> str:
        devices = []
        for d in self.devices:
            devices.append({
                "name": getattr(d, "name", "?"),
                "model": getattr(d, "modelDisplayName", "?"),
                "battery": getattr(d, "batteryLevel", None),
                "location": getattr(d, "location", None),
            })
        return json.dumps(devices, indent=2, default=str)

    def locate(self, name: str) -> str:
        q = name.lower()
        for d in self.devices:
            if q in str(getattr(d, "name", "")).lower():
                loc = getattr(d, "location", None) or {}
                return json.dumps({
                    "name": getattr(d, "name", "?"),
                    "battery": getattr(d, "batteryLevel", None),
                    "lat": loc.get("latitude") if loc else None,
                    "lon": loc.get("longitude") if loc else None,
                    "timestamp": loc.get("timeStamp") if loc else None,
                }, indent=2)
        return json.dumps({"error": "not found"})

    def sound(self, name: str) -> str:
        q = name.lower()
        for d in self.devices:
            if q in str(getattr(d, "name", "")).lower():
                self.devices.play_sound(d)
                return json.dumps({"status": "playing", "device": getattr(d, "name", "?")})
        return json.dumps({"error": "not found"})
