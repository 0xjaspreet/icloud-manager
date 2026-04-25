"""Notes service (read-only)."""
import json
from pyicloud import PyiCloudService

MAX_FOLDER_ID_LENGTH = 256


class NotesService:
    def __init__(self, api: PyiCloudService):
        self.notes = api.notes

    def folders(self) -> str:
        folders = self.notes.folders()
        return json.dumps([{"name": f.name, "id": f.id} for f in folders], indent=2)

    def list(self, folder_id: str = None) -> str:
        if folder_id is not None:
            folder_id = folder_id.strip()
            if not folder_id or len(folder_id) > MAX_FOLDER_ID_LENGTH:
                return json.dumps({"error": "invalid folder id"})
        folders = [(f.name, f.id) for f in self.notes.folders()
                   if not folder_id or f.id == folder_id]
        result = []
        for name, fid in folders:
            ns = []
            for i, note in enumerate(self.notes.in_folder(fid)):
                if i >= 20:
                    break
                ns.append({
                    "title": note.title or "Untitled",
                    "snippet": (note.snippet or "")[:200],
                })
            result.append({"folder": name, "id": fid, "notes": ns})
        return json.dumps(result, indent=2)
