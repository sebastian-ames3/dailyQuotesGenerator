# Morning Motivation Quote Generator - Quick Setup Guide

This guide will help you set up the Morning Motivation Quote Generator to launch automatically when you log into Windows.

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Download/Clone the Project

If you haven't already, download or clone this repository to a permanent location on your computer.

**Recommended location:** `C:\Users\YourName\Documents\MorningQuotes\`

**Important:** Once you place the files here, don't move them, or the auto-launch will break.

---

### Step 2: Test the Quote Generator

Before setting up auto-launch, make sure it works:

1. Open `index.html` in your browser (double-click the file)
2. You should see a motivational quote appear in the bottom-right corner
3. Test the interactions:
   - Hover over the quote (timer should pause)
   - Click the quote (should open Google search)
   - Press `Esc` or click the X to close

If it works, proceed to Step 3. If not, check that you have an internet connection (or the fallback quotes will display).

---

### Step 3: Set Up Auto-Launch on Windows

#### Option A: Automatic Setup (Easiest - Windows 10/11)

1. **Double-click** `LaunchQuote.bat` in the project folder
   - This tests that the batch file works correctly
   - Your browser should open with the quote

2. **Open the Windows Startup folder:**
   - Press `Windows + R`
   - Type: `shell:startup`
   - Press Enter

3. **Create a shortcut:**
   - Go back to your project folder
   - **Right-click** on `LaunchQuote.bat`
   - Select "Show more options" (Windows 11) or just right-click (Windows 10)
   - Click "Send to" → "Desktop (create shortcut)"
   - **Drag** the shortcut from your Desktop into the Startup folder

4. **Optional: Hide the command window flash**
   - In the Startup folder, right-click your shortcut
   - Select "Properties"
   - In the "Shortcut" tab, change "Run:" to "**Minimized**"
   - Click OK

5. **Test it:**
   - Log out of Windows (Ctrl + Alt + Delete → Sign out)
   - Log back in
   - The quote should appear automatically!

✅ **Done!** Your motivational quote will now greet you every time you log into Windows.

---

#### Option B: Advanced Setup (More Control)

For advanced users who want more control (e.g., delay the quote by 30 seconds, only run on weekdays, etc.), see the comprehensive [AUTO_LAUNCH_GUIDE.md](./AUTO_LAUNCH_GUIDE.md) which covers:

- **Task Scheduler** (with scheduling options)
- **Registry Run Keys** (programmatic deployment)
- **PowerShell Scripts** (advanced scripting with logging)
- **macOS and Linux** setup instructions

---

## 🛠️ Customization

### Change the Auto-Close Timer

By default, the quote closes after **15 seconds**. To change this:

1. Open `index.html` in a text editor (Notepad, VS Code, etc.)
2. Find this line (around line 11):
   ```javascript
   const TIMER_DURATION = 15000; // 15 seconds in milliseconds
   ```
3. Change `15000` to your preferred duration:
   - `10000` = 10 seconds
   - `20000` = 20 seconds
   - `30000` = 30 seconds
4. Save the file

### Change the Quote Position

By default, the quote appears in the **bottom-right corner**. To change this:

1. Open `index.html` in a text editor
2. Find the CSS section (around line 40-50) with:
   ```css
   bottom: 20px;
   right: 20px;
   ```
3. Change to one of these options:
   - **Top-right:** `top: 20px; right: 20px;`
   - **Top-left:** `top: 20px; left: 20px;`
   - **Bottom-left:** `bottom: 20px; left: 20px;`
4. Save the file

### Use a Specific Browser (Instead of Default)

If you want the quote to always open in a specific browser (e.g., Chrome, Edge, Firefox), edit `LaunchQuote.bat`:

**For Google Chrome:**
```batch
@echo off
set "SCRIPT_DIR=%~dp0"
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" "%SCRIPT_DIR%index.html"
```

**For Firefox:**
```batch
@echo off
set "SCRIPT_DIR=%~dp0"
start "" "C:\Program Files\Mozilla Firefox\firefox.exe" "%SCRIPT_DIR%index.html"
```

**For Microsoft Edge:**
```batch
@echo off
set "SCRIPT_DIR=%~dp0"
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" "%SCRIPT_DIR%index.html"
```

---

## 🐛 Troubleshooting

### The quote doesn't appear on startup

**Solutions:**
1. Check that the shortcut is in the Startup folder (`shell:startup`)
2. Verify `LaunchQuote.bat` is in the same folder as `index.html`
3. Test the batch file manually by double-clicking it
4. Check that you didn't move the project folder after setting up the shortcut

### Opens in a text editor instead of a browser

**Solution:**
- Ensure the file is named `LaunchQuote.bat` (not `LaunchQuote.bat.txt`)
- Check your file extension settings in Windows Explorer (View → Show → File name extensions)

### Command window flashes briefly

**Solution:**
- Right-click the shortcut in the Startup folder
- Properties → Run: **Minimized**
- Click OK

### Quote appears multiple times on startup

**Solution:**
- Check the Startup folder for duplicate shortcuts
- Press `Windows + R`, type `shell:startup`, and remove duplicates

### For more troubleshooting, see [AUTO_LAUNCH_GUIDE.md](./AUTO_LAUNCH_GUIDE.md)

---

## 🗑️ How to Uninstall / Disable

To stop the quote from launching automatically:

1. Press `Windows + R`
2. Type: `shell:startup`
3. Press Enter
4. **Delete** the `LaunchQuote.bat` shortcut
5. Done! (The files remain in your Documents folder if you want to use them manually)

To completely remove everything:
- Delete the entire project folder from your Documents

---

## 🌍 Cross-Platform (macOS & Linux)

This project works on macOS and Linux too! See [AUTO_LAUNCH_GUIDE.md](./AUTO_LAUNCH_GUIDE.md) for setup instructions for:

- **macOS:** Using LaunchAgents or Login Items
- **Linux:** Using XDG Autostart (GNOME, KDE, XFCE)

---

## 📚 Additional Resources

- **Full auto-launch guide:** [AUTO_LAUNCH_GUIDE.md](./AUTO_LAUNCH_GUIDE.md)
- **Project documentation:** [README.md](./README.md)
- **Product requirements:** [PRD.md](./PRD.md)
- **API research:** [API_RESEARCH_REPORT.md](./API_RESEARCH_REPORT.md)
- **UX research:** [UX_RESEARCH_REPORT.md](./UX_RESEARCH_REPORT.md)

---

## ❓ FAQ

### Q: Will this slow down my computer startup?

**A:** No. It adds less than 1-2 seconds to startup time and uses minimal memory (just one browser tab).

### Q: What if I don't have internet?

**A:** The quote generator includes 15 high-quality fallback quotes. It will work offline!

### Q: Can I customize the quotes?

**A:** Yes! See [CURATED_QUOTES.md](./CURATED_QUOTES.md) for the fallback quotes, or edit `index.html` to add your own.

### Q: Does this work on laptops?

**A:** Yes! It works on both desktop and laptop computers.

### Q: Can I share this with friends?

**A:** Absolutely! This is open-source (MIT License). Feel free to share, modify, and distribute.

---

## 💬 Support

If you encounter issues:

1. Check the **Troubleshooting** section above
2. See the comprehensive [AUTO_LAUNCH_GUIDE.md](./AUTO_LAUNCH_GUIDE.md)
3. Open an issue on GitHub (if this project is hosted there)

---

**Enjoy your daily dose of motivation!** 🎯✨
