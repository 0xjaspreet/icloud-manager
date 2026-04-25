"""Contacts service."""
import json
from pyicloud import PyiCloudService

MAX_QUERY_LENGTH = 256


class ContactsService:
    def __init__(self, api: PyiCloudService):
        self.contacts = api.contacts.all

    def list(self) -> str:
        out = []
        for c in self.contacts:
            out.append({
                "name": f"{c.get('firstName', '')} {c.get('lastName', '')}".strip(),
                "phones": [p.get("field", "") for p in (c.get("phones") or [])],
                "emails": [e.get("field", "") for e in (c.get("emails") or [])],
            })
        return json.dumps(out, indent=2)

    def search(self, query: str) -> str:
        if len(query) > MAX_QUERY_LENGTH:
            return json.dumps({"error": "query too long"})
        q = query.lower()
        out = []
        for c in self.contacts:
            name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip().lower()
            phones = " ".join([p.get("field", "") for p in (c.get("phones") or [])])
            if q in name or q in phones:
                out.append({
                    "name": f"{c.get('firstName', '')} {c.get('lastName', '')}".strip(),
                    "phones": [p.get("field", "") for p in (c.get("phones") or [])],
                })
        return json.dumps(out, indent=2)
