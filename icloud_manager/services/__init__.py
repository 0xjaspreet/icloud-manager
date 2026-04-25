"""All service modules."""
from .calendar import CalendarService
from .reminders import RemindersService
from .notes import NotesService
from .contacts import ContactsService
from .findmy import FindMyService
from .drive import DriveService

__all__ = [
    "CalendarService", "RemindersService", "NotesService",
    "ContactsService", "FindMyService", "DriveService",
]
