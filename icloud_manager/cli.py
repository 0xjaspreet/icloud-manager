#!/usr/bin/env python3
"""
iCloud Manager — Terminal access to iCloud services.

Usage:
    icloud-manager setup
    icloud-manager calendar list|add|delete [...]
    icloud-manager reminders lists|list|add [...]
    icloud-manager notes folders|list [...]
    icloud-manager contacts list|search [...]
    icloud-manager findmy list|locate|sound [...]
    icloud-manager drive list
"""

import sys
import traceback
from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudServiceNotActivatedException

from icloud_manager.services.auth import AuthManager
from icloud_manager.services.calendar import CalendarService
from icloud_manager.services.reminders import RemindersService
from icloud_manager.services.notes import NotesService
from icloud_manager.services.contacts import ContactsService
from icloud_manager.services.findmy import FindMyService
from icloud_manager.services.drive import DriveService

# Sensitive strings to redact from unexpected tracebacks.
_sensitive_strings = []


def _redact_traceback(exc_type, exc_value, exc_tb):
    """sys.excepthook that redacts sensitive strings from tracebacks."""
    text = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    for s in _sensitive_strings:
        if s:
            text = text.replace(s, "***REDACTED***")
    print(text, file=sys.stderr)


def get_api() -> PyiCloudService:
    """Authenticate and return a PyiCloudService instance."""
    auth = AuthManager()
    if not auth.load():
        print("❌ Not configured. Run: icloud-manager setup")
        sys.exit(1)
    try:
        api = PyiCloudService(auth.email, auth.password)
    except PyiCloudServiceNotActivatedException:
        auth.clear()
        print("❌ Authentication failed. Check your credentials.")
        print("   Run: icloud-manager setup")
        sys.exit(1)
    except Exception:
        auth.clear()
        print("❌ Failed to connect to iCloud.")
        sys.exit(1)
    # Register sensitive strings for excepthook redaction, then wipe.
    _sensitive_strings.extend([auth.email or "", auth.password or ""])
    auth.clear()
    return api


def safe_run(fn, *args):
    """Run a service function, catching and reporting errors cleanly."""
    try:
        result = fn(*args)
        if result:
            print(result)
    except Exception as e:
        print(f"❌ Error: {e}")


def cmd_setup():
    auth = AuthManager()
    auth.setup_interactive()


def cmd_calendar(args):
    api = get_api()
    svc = CalendarService(api)
    if not args:
        print("Usage: icloud-manager calendar <list|add|delete>")
        return
    if args[0] == "list":
        safe_run(svc.list)
    elif args[0] == "add" and len(args) >= 4:
        safe_run(svc.add, args[1], args[2], args[3])
    elif args[0] == "delete" and len(args) >= 2:
        safe_run(svc.delete, args[1])
    else:
        print("Usage: calendar list | add <title> <start> <end> | delete <id>")


def cmd_reminders(args):
    api = get_api()
    svc = RemindersService(api)
    if not args:
        print("Usage: icloud-manager reminders <lists|list|add>")
        return
    if args[0] == "lists":
        safe_run(svc.lists)
    elif args[0] == "list":
        safe_run(svc.list, args[1] if len(args) > 1 else None)
    elif args[0] == "add" and len(args) >= 2:
        guid = args[2] if len(args) > 2 else None
        due = args[3] if len(args) > 3 else None
        safe_run(svc.add, args[1], guid, due)
    else:
        print("Usage: reminders lists | list [guid] | add <title> [guid] [due]")


def cmd_notes(args):
    api = get_api()
    svc = NotesService(api)
    if not args:
        print("Usage: icloud-manager notes <folders|list>")
        return
    if args[0] == "folders":
        safe_run(svc.folders)
    elif args[0] == "list":
        safe_run(svc.list, args[1] if len(args) > 1 else None)
    else:
        print("Usage: notes folders | list [folder-id]")


def cmd_contacts(args):
    api = get_api()
    svc = ContactsService(api)
    if not args:
        print("Usage: icloud-manager contacts <list|search>")
        return
    if args[0] == "list":
        safe_run(svc.list)
    elif args[0] == "search" and len(args) >= 2:
        safe_run(svc.search, " ".join(args[1:]))
    else:
        print("Usage: contacts list | search <name>")


def cmd_findmy(args):
    api = get_api()
    svc = FindMyService(api)
    if not args:
        print("Usage: icloud-manager findmy <list|locate|sound>")
        return
    if args[0] == "list":
        safe_run(svc.list)
    elif args[0] == "locate" and len(args) >= 2:
        safe_run(svc.locate, " ".join(args[1:]))
    elif args[0] == "sound" and len(args) >= 2:
        safe_run(svc.sound, " ".join(args[1:]))
    else:
        print("Usage: findmy list | locate <name> | sound <name>")


def cmd_drive(args):
    api = get_api()
    svc = DriveService(api)
    safe_run(svc.list)


COMMANDS = {
    "setup": cmd_setup,
    "calendar": cmd_calendar,
    "reminders": cmd_reminders,
    "notes": cmd_notes,
    "contacts": cmd_contacts,
    "findmy": cmd_findmy,
    "drive": cmd_drive,
}


def main():
    # Install excepthook that redacts credentials from unexpected tracebacks.
    sys.excepthook = _redact_traceback

    if len(sys.argv) < 2:
        print("iCloud Manager — manage iCloud from the terminal")
        print()
        print("Services: calendar, reminders, notes, contacts, findmy, drive")
        print("Setup:    icloud-manager setup")
        print("Help:     icloud-manager <service>   (shows usage)")
        return

    cmd = sys.argv[1]
    if cmd not in COMMANDS:
        print(f"Unknown: {cmd}. Available: {', '.join(COMMANDS)}")
        sys.exit(1)

    COMMANDS[cmd](sys.argv[2:])


if __name__ == "__main__":
    main()
