"""Calendar service — list, add, delete iCloud events."""
import json
import re
from datetime import datetime

import pytz
from pyicloud import PyiCloudService
from pyicloud.services.calendar import EventObject

# Reasonable limits for calendar event data.
MAX_TITLE_LENGTH = 1024


class CalendarService:
    """Manage iCloud Calendar events."""

    def __init__(self, api: PyiCloudService, timezone: str = "America/Winnipeg"):
        self.cal = api.calendar
        self.tz = pytz.timezone(timezone)

    def list(self) -> str:
        """List all events as JSON."""
        events = self.cal.get_events(datetime(2024, 1, 1), datetime(2027, 1, 1))
        out = []
        for ev in events:
            start = ev.get("startDate", "")
            end = ev.get("endDate", "")
            title = ev.get("title", "")
            start_str = self._format_date(start)
            end_str = self._format_date(end, short=True)
            out.append({
                "id": ev.get("guid", ""),
                "title": title,
                "start": start_str,
                "end": end_str,
            })
        return json.dumps(out, indent=2)

    def add(self, title: str, start_str: str, end_str: str) -> str:
        """Add an event. Accepts '2026-04-29 9:00 AM' or ISO format."""
        # Validate and sanitize title.
        title = self._sanitize_title(title)
        if not title:
            return json.dumps({
                "error": "invalid title",
                "detail": "Title must not be empty or contain only control characters.",
            })

        start = self._parse_datetime(start_str)
        end = self._parse_datetime(end_str)
        if start is None or end is None:
            return json.dumps({
                "error": "invalid date",
                "detail": "Use format: '2026-04-29 9:00 AM' or ISO 8601",
            })
        calendars = self.cal.get_calendars()
        if not calendars:
            return json.dumps({"error": "no calendars found"})
        pguid = calendars[0]["guid"]
        event = EventObject(pguid=pguid, title=title, start_date=start, end_date=end, tz=str(self.tz))
        result = self.cal.add_event(event)
        return json.dumps({"status": "created", "id": result.get("guid", ""), "title": title})

    def delete(self, event_id: str) -> str:
        """Delete an event by GUID."""
        if not event_id or not event_id.strip():
            return json.dumps({"error": "event id required"})
        events = self.cal.get_events(datetime(2024, 1, 1), datetime(2027, 1, 1))
        for ev in events:
            if ev.get("guid") == event_id:
                try:
                    sd = ev["startDate"]
                    ed = ev["endDate"]
                    event = EventObject(
                        pguid=ev["pGuid"],
                        guid=ev["guid"],
                        title=ev.get("title", ""),
                        start_date=datetime(sd[1], sd[2], sd[3], sd[4], sd[5]),
                        end_date=datetime(ed[1], ed[2], ed[3], ed[4], ed[5]),
                        etag=ev.get("etag", ""),
                    )
                except (IndexError, KeyError, ValueError):
                    return json.dumps({"error": "malformed event data", "id": event_id})
                self.cal.remove_event(event)
                return json.dumps({"status": "deleted", "id": event_id})
        return json.dumps({"error": "not found", "id": event_id})

    @staticmethod
    def _sanitize_title(title: str) -> str:
        """Strip surrounding whitespace and remove control characters.
        Truncate to MAX_TITLE_LENGTH. Returns empty string if the result is blank."""
        # Strip leading/trailing whitespace.
        title = title.strip()
        # Remove control characters (ASCII 0x00–0x1F and 0x7F) except tab and newline
        title = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", title)
        # Truncate to max length.
        if len(title) > MAX_TITLE_LENGTH:
            title = title[:MAX_TITLE_LENGTH]
        return title.strip()

    def _parse_datetime(self, value: str):
        """Parse '2026-04-29 9:00 AM' or ISO format, localizing to default tz.
        Returns a datetime or None on failure."""
        try:
            dt = datetime.fromisoformat(value)
        except ValueError:
            try:
                dt = datetime.strptime(value, "%Y-%m-%d %I:%M %p")
            except ValueError:
                return None
        # Only localize naive datetimes; pytz throws on already-aware ones
        if dt.tzinfo is None:
            dt = self.tz.localize(dt)
        elif hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
            # Already timezone-aware — convert to configured tz
            dt = dt.astimezone(self.tz)
        return dt

    @staticmethod
    def _format_date(value, short: bool = False) -> str:
        """Convert iCloud date array to readable string."""
        if isinstance(value, list) and len(value) >= 6:
            try:
                dt = datetime(value[1], value[2], value[3], value[4], value[5])
                fmt = "%I:%M %p" if short else "%b %d, %Y %I:%M %p"
                return dt.strftime(fmt)
            except (ValueError, IndexError):
                pass
        return str(value)
