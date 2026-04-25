# 🍌 iCloud Manager

> *The bridge between your AI agent and your Apple ecosystem. No iPhone required.*

Your personal AI assistant wants to add events to your calendar, set reminders,
find your phone, or check your notes — but you're on Linux and iCloud locked
you out. Not anymore.

**icloud-manager** exposes your iCloud data as a dead-simple CLI that any AI
agent (or human) can call. Built for Hermes, Claude Code, OpenClaw, or whatever
agent you've got running in your terminal.

```
┌──────────────────────────────────────────┐
│  "Hey agent, add NPower interview to     │
│   my calendar April 29 at 9am"           │
│                                          │
│  🍌 icloud-manager calendar add \       │
│     "Interview for NPower Canada" \      │
│     "2026-04-29 9:00 AM" \              │
│     "2026-04-29 10:00 AM"               │
│                                          │
│  ✅ Done. You're all set, Jaspreet.      │
└──────────────────────────────────────────┘
```

## Why?

AI agents are the future of personal computing. But agents can't tap into the
Apple ecosystem without janky workarounds. This tool gives your agent the same
iCloud access you have on your phone — calendar, reminders, notes, contacts,
Find My, and Drive — all from a Linux terminal.

**Built by an AI agent, for AI agents.** Literally. Hermes built this.

## Quick Start

```bash
# Install
pip install git+https://github.com/0xjaspreet/icloud-manager.git

# One-time setup (needs Apple ID + app-specific password)
icloud-manager setup

# Your agent can now do stuff like:
icloud-manager calendar add "Dentist 🦷" "2026-05-01 2:00 PM" "2026-05-01 3:00 PM"
icloud-manager reminders add "Buy bananas 🍌"
icloud-manager findmy sound "iPhone"
```

## What Your Agent Can Do

| 🍌 Service | Read | Write | What your agent says |
|-----------|------|-------|---------------------|
| Calendar | ✅ | ✅ | "Adding that to your calendar now" |
| Reminders | ✅ | ✅ | "I'll remind you about that" |
| Find My | ✅ | ✅ | "Your iPhone is at Tim Hortons on Portage" |
| Notes | ✅ | ❌ | "Here's what's in your notes folder" |
| Contacts | ✅ | ❌ | "Found 3 matches for 'Aman'" |
| Drive | ✅ | ❌ | "You've got 9 files in iCloud Drive" |

> ⚠️ **Notes & Contacts** are read-only (thanks, Apple). Calendar and Reminders
> are fully functional — which covers 90% of what you'd ask an agent to do.

## Setup for Your AI Agent

If you're wiring this into an AI agent (Claude, Hermes, OpenClaw, etc.), here's
what you need:

1. **Install the tool** — `pip install git+https://github.com/0xjaspreet/icloud-manager.git`
2. **Run setup once** — `icloud-manager setup` (stores creds at `~/.config/icloud-manager/`)
3. **Add to your agent's tool list** — it's just a CLI. Any agent that can run
   shell commands can use it.
4. **ADP must be OFF** — Advanced Data Protection encrypts Reminders/Notes
   end-to-end, which blocks API access. Turn it off for full functionality.

### Example: Hermes Agent skill

```yaml
# In your Hermes skill file:
icloud-manager calendar list
icloud-manager calendar add "$TITLE" "$START" "$END"
icloud-manager reminders add "$TASK"
icloud-manager findmy locate "$DEVICE"
```

## Requirements

- Python 3.10+
- `pyicloud` — iCloud API wrapper
- `pytz` — timezone handling
- An Apple ID with an app-specific password
- ADP turned **off** (Settings → iCloud → Advanced Data Protection)

## FAQ

**Q: Can my agent really manage my calendar?**
Yep. Add, list, delete events — all from terminal. Timezone defaults to your
local zone (configurable).

**Q: Why yellow?**
Because bananas. And because iCloud's blue needed competition.

**Q: Is this secure?**
Credentials stored at `~/.config/icloud-manager/creds.json` with `chmod 600`.
Session cached after first 2FA. No data leaves your machine.

**Q: Can I contribute?**
Absolutely. PRs welcome. Especially if you figure out how to write Notes or
Contacts via CloudKit — that's the holy grail.

## License

MIT — go build cool stuff. If your agent does something awesome with this,
tag [@0xjaspreet](https://github.com/0xjaspreet) — would love to see it.

---

<p align="center">
  <sub>🍌 Built by Hermes, for Hermes. Yellow because why not.</sub>
</p>
