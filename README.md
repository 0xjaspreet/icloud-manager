# iCloud Manager

> **Let your personal AI agent manage your iCloud.**
> Calendar. Reminders. Notes. Contacts. Find My. Drive.
> No iPhone needed. Just your agent and a terminal.

---

Your AI agent lives in your terminal. It manages your email, your files,
your schedule. But iCloud? That's been a walled garden.

Not anymore.

**icloud-manager** is the missing bridge — a CLI your agent can call to add
calendar events, set reminders, ping your lost phone, pull up contacts, and
more. Built specifically so a personal AI agent (Hermes, Claude Code,
OpenClaw — yours) can fully participate in your Apple ecosystem from Linux.

```
Your agent: "Want me to add that to your calendar?"
     iCloud: 🔒
icloud-manager: 🔓 Go ahead.

$ icloud-manager calendar add \
    "NPower Interview" \
    "2026-04-29 9:00 AM" \
    "2026-04-29 10:00 AM"

✅ Done. You're all set.
```

## The Pitch

Your personal AI agent should be able to do everything you can do on your
phone. That includes iCloud. This tool makes that real — your agent reads
your calendar, adds reminders while you're driving, finds your phone when
you lose it, checks your notes during a conversation. All from the terminal
it already lives in.

**Main theme:** Your AI agent manages your iCloud.
**Main purpose:** So you don't have to switch contexts. Ask your agent. It
handles it.

## What Your Agent Can Do

| Service  | Agent Reads | Agent Writes | Example |
|----------|:-----------:|:------------:|---------|
| Calendar | ✅ | ✅ | "Added to your calendar" |
| Reminders| ✅ | ✅ | "I'll remind you at 6pm" |
| Find My  | ✅ | ✅ | "iPhone's at 123 Portage Ave" |
| Notes    | ✅ | ❌ | "Here's your shopping list" |
| Contacts | ✅ | ❌ | "Found Aman's number" |
| Drive    | ✅ | ❌ | "12 files in your Drive" |

> **Notes & Contacts are read-only** — Apple's CloudKit API doesn't expose
> write access (yet). Calendar and Reminders cover 90% of agent use cases.

## Quick Start

```bash
# Install
pip install git+https://github.com/0xjaspreet/icloud-manager.git

# One-time setup (Apple ID + app-specific password)
icloud-manager setup

# Now your agent can:
icloud-manager calendar add "Dinner with Mom" "2026-05-01 7:00 PM" "2026-05-01 9:00 PM"
icloud-manager reminders add "Pick up dry cleaning" --due "2026-05-02"
icloud-manager findmy sound "iPhone"
icloud-manager contacts search "Aman"
```

## Wiring It Into Your Agent

This is a CLI. Any agent that runs shell commands can use it.

### Hermes / Claude Code / OpenClaw

Add these to your agent's tool definitions:

```bash
icloud-manager calendar list
icloud-manager calendar add "<title>" "<start>" "<end>"
icloud-manager calendar delete <event-id>

icloud-manager reminders lists
icloud-manager reminders list
icloud-manager reminders add "<title>" --due "<date>"

icloud-manager notes folders
icloud-manager notes list --folder "<folder>"

icloud-manager contacts list
icloud-manager contacts search "<name>"

icloud-manager findmy list
icloud-manager findmy locate "<device>"
icloud-manager findmy sound "<device>"

icloud-manager drive list
```

That's it. No API keys, no webhooks, no cloud services. Your agent talks to
iCloud directly from your machine.

## Prerequisites

- Python 3.10+
- `pyicloud` and `pytz`
- Apple ID with [app-specific password](https://support.apple.com/en-us/102654)
- **ADP turned OFF** (Settings → iCloud → Advanced Data Protection)
- A personal AI agent (optional, but that's the whole point)

## Security

- Credentials live at `~/.config/icloud-manager/creds.json` — `chmod 600`
- Session cached after first 2FA
- Everything stays on your machine. Zero telemetry. Zero cloud middlemen.

## FAQ

**Why not just use my phone?**
Because your AI agent can't tap your phone's screen. It can run a CLI.

**Is this production-ready?**
It's production-ready for a personal agent. Not for a SaaS product. Not for
managing 10,000 iCloud accounts. One human, one agent, one iCloud.

**Can I write to Notes or Contacts?**
Not yet. Apple's CloudKit API is the bottleneck. If you reverse-engineer it,
PRs are wide open.

**Who made this?**
Hermes — an AI agent. Built by an agent, for agents.
Repo owned by [@0xjaspreet](https://github.com/0xjaspreet).

## License

MIT. Take it, wire it into your agent, make it yours.

---

<p align="center">
  <sub>Main theme: your AI agent manages your iCloud.</sub><br>
  <sub>Built by Hermes, powered by pyicloud, running on Linux.</sub>
</p>
