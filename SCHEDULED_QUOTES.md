# Scheduled Quotes - Setup Guide

This guide explains how to set up automatic quotes that appear when you log in during specific time windows.

---

## Quick Start

### Install Scheduled Quotes

1. **Double-click** `install_scheduled_quotes.bat`
2. Click "OK" through the prompts
3. Done! Quotes will now show on login during time windows

### Uninstall

1. **Double-click** `uninstall_scheduled_quotes.bat`
2. Scheduled quotes removed

---

## How It Works

### Time Windows

Quotes appear when you log in during these windows:

| Window  | Time Range       | Shows          |
| ------- | ---------------- | -------------- |
| Morning | 5:00 AM - 11:00 AM | Once per day   |
| Midday  | 12:00 PM - 5:00 PM | Once per day   |

### Behavior Examples

**Scenario 1: Morning routine**
- 7:00 AM - Turn on laptop, log in → **Morning quote appears** ✅
- 9:00 AM - Wake from sleep, log in → **No quote** (already shown today)
- 1:00 PM - Return from lunch, log in → **Midday quote appears** ✅

**Scenario 2: Late night work**
- 11:00 PM - Log in → **No quote** (outside time windows)

**Scenario 3: Multiple logins**
- 8:00 AM - First login → **Morning quote shows**
- 8:30 AM - Second login → **No quote** (already shown)
- Next day 7:00 AM → **Morning quote shows** (new day)

### Technical Details

- **No background process** - Only runs on login
- **Smart tracking** - Remembers which quotes shown today (stored in `.quote_tracker.json`)
- **Windows Task Scheduler** - Uses native Windows scheduling
- **Zero overhead** - Doesn't run when you're not logging in

---

## Customizing Time Windows

You can edit the time windows by modifying `quote_scheduler.py`:

```python
SCHEDULE_CONFIG = {
    "time_windows": [
        {"name": "morning", "trigger_time": "05:00", "window_hours": 6},  # 5am-11am
        {"name": "midday", "trigger_time": "12:00", "window_hours": 5},   # 12pm-5pm
    ]
}
```

**Examples:**

Add an evening window (6pm-9pm):
```python
{"name": "evening", "trigger_time": "18:00", "window_hours": 3},
```

Change morning to 6am-10am:
```python
{"name": "morning", "trigger_time": "06:00", "window_hours": 4},
```

After editing, run `uninstall_scheduled_quotes.bat` then `install_scheduled_quotes.bat` to apply changes.

---

## Manual Mode

If you don't want scheduled quotes, you can still use manual mode:

- **Double-click** `LaunchQuote.bat` anytime to see a quote
- No installation needed
- No automatic behavior

---

## Troubleshooting

### Quote doesn't appear on login

**Check:**
1. Are you logging in during a time window? (5-11am or 12-5pm)
2. Did you already see a quote in that window today?
3. Is the task installed? Run `install_scheduled_quotes.bat`

**Verify installation:**
```cmd
schtasks /query /tn "MorningQuoteScheduled"
```

Should show the task details. If not found, run install script.

### Quote appears every login

**This shouldn't happen.** If it does:
1. Check `.quote_tracker.json` - should have today's date
2. Delete the tracker file and let it regenerate
3. Reinstall: Run uninstall, then install

### Want to test immediately

Temporarily edit `quote_scheduler.py` to match current time:

```python
"time_windows": [
    {"name": "test", "trigger_time": "19:00", "window_hours": 2},  # 7pm-9pm
]
```

Run `python quote_scheduler.py` to test.

### Windows says "Access Denied"

Run the install script as Administrator:
1. Right-click `install_scheduled_quotes.bat`
2. Select "Run as administrator"

---

## Files

| File                           | Purpose                                  |
| ------------------------------ | ---------------------------------------- |
| `quote_scheduler.py`           | Checks time windows and shows quotes     |
| `install_scheduled_quotes.bat` | Installs Task Scheduler entry            |
| `uninstall_scheduled_quotes.bat` | Removes Task Scheduler entry           |
| `.quote_tracker.json`          | Tracks which quotes shown today (auto-generated) |

---

## FAQ

### Q: Does this slow down login?

**A:** No. The scheduler check takes <100ms. You won't notice it.

### Q: What if I'm not connected to internet?

**A:** The quote system has 15 fallback quotes. Always works offline.

### Q: Can I change the 15-second display time?

**A:** Yes. Edit `quote_overlay.py`, line 82:
```python
"timer_duration": 15000,  # Change to 20000 for 20 seconds
```

### Q: Will this work on Mac or Linux?

**A:** The Python code works cross-platform, but the install scripts are Windows-only. On Mac/Linux, you'd use cron or launchd instead of Task Scheduler.

### Q: How do I temporarily disable?

**A:** Run `uninstall_scheduled_quotes.bat`. To re-enable, run `install_scheduled_quotes.bat`.

---

## Support

If quotes aren't working:
1. Test manually: `python quote_scheduler.py`
2. Check Task Scheduler (Windows + R → `taskschd.msc`)
3. Review this troubleshooting guide

---

**Enjoy your daily motivation!** 🎯
