"""Reminders service."""
import json
from pyicloud import PyiCloudService


class RemindersService:
    def __init__(self, api: PyiCloudService):
        self.rem = api.reminders

    def lists(self) -> str:
        lst = self.rem.lists()
        return json.dumps([{"title": l.title, "guid": l.guid} for l in lst], indent=2)

    def list(self, guid: str = None) -> str:
        lists = [l for l in self.rem.lists() if l.guid == guid] if guid else self.rem.lists()
        result = []
        for lst in lists:
            tasks = []
            for t in self.rem.reminders(lst.guid):
                tasks.append({
                    "title": t.title or "",
                    "completed": bool(t.completed),
                    "due": str(t.due_date) if t.due_date else None,
                })
            result.append({"list": lst.title, "guid": lst.guid, "tasks": tasks})
        return json.dumps(result, indent=2)

    def add(self, title: str, guid: str = None, due: str = None) -> str:
        if not guid:
            guid = self.rem.lists()[0].guid
        self.rem.create(title, guid, due_date=due)
        return json.dumps({"status": "created", "title": title})
