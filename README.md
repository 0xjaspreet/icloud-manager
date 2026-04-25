# iCloud Manager

Manage your iCloud data from the Linux terminal — no Apple device required.

**Calendar • Reminders • Notes • Contacts • Find My • Drive**

## Why?

iCloud works great on Apple devices, but on Linux you're locked out. iCloud Manager
bridges that gap using pyicloud — giving you full terminal access to your iCloud
Calendar, Reminders, Notes, Contacts, Find My iPhone, and iCloud Drive.

## Quick Start

```bash
pip install icloud-manager
icloud-manager setup
```

Or from source:

```bash
git clone https://github.com/jjaspreetsingh/icloud-manager
cd icloud-manager
pip install -e .
icloud-manager setup
```

## Usage

```bash
# Calendar — default timezone is your local zone
icloud-manager calendar list
icloud-manager calendar add "Team Standup" "2026-05-01 9:00 AM" "2026-05-01 9:30 AM"
icloud-manager calendar delete <event-id>

# Reminders
icloud-manager reminders lists
icloud-manager reminders list
icloud-manager reminders add "Buy groceries" --due "2026-05-01"

# Notes
icloud-manager notes folders
icloud-manager notes list
icloud-manager notes list --folder "workRelated"

# Contacts (read-only)
icloud-manager contacts list
icloud-manager contacts search "John"

# Find My iPhone
icloud-manager findmy list
icloud-manager findmy locate "iPhone"
icloud-manager findmy sound "iPhone"

# iCloud Drive
icloud-manager drive list
```

## Setup

You'll need:
1. Your Apple ID (iCloud email)
2. An app-specific password (Settings → Apple ID → App-Specific Passwords)
3. 2FA access (one-time, session persists afterward)

**Important:** Advanced Data Protection (ADP) must be OFF for Reminders and Notes access.

Run `icloud-manager setup` and follow the prompts. Credentials are stored at
`~/.config/icloud-manager/creds.json` (chmod 600).

## What Works

| Service  | Read | Write | Notes |
|----------|------|-------|-------|
| Calendar | ✅   | ✅    | Events with timezone support |
| Reminders| ✅   | ✅    | Lists, create tasks with due dates |
| Notes    | ✅   | ❌    | Read-only via pyicloud |
| Contacts | ✅   | ❌    | 265+ contacts searchable |
| Find My  | ✅   | ✅    | Locate, play sound on devices |
| Drive    | ✅   | ❌    | Browse root directory |

## Requirements

- Python 3.10+
- pyicloud (for iCloud API access)
- pytz (for timezone handling)

## License

MIT
