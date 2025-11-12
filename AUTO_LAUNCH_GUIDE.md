# Auto-Launch Guide: Morning Motivation Quote Generator

## Executive Summary

### Recommended Method: Windows Startup Folder (Method 1)

**Winner: Startup Folder + Batch File**

For the Morning Motivation Quote Generator, the **Windows Startup Folder** method is recommended because:

- **Easiest setup** - Takes less than 2 minutes, no advanced technical knowledge required
- **Most reliable** - Survives Windows updates and restarts without issues
- **No admin rights required** - Works for standard user accounts
- **Easy to modify or remove** - Just delete the shortcut from the folder
- **Works with any default browser** - Automatically uses your preferred browser
- **Runs only on login** - Not on screen unlock or wake from sleep
- **Visual confirmation** - You can see what's in your startup folder

This method involves creating a simple batch file that opens the HTML file in your default browser, then placing a shortcut to that batch file in your Windows Startup folder.

---

## Method Comparison Table

| Method                | Ease of Setup        | Reliability          | Admin Required | Removal Ease         | Browser Support | Best For                       |
| --------------------- | -------------------- | -------------------- | -------------- | -------------------- | --------------- | ------------------------------ |
| **Startup Folder**    | ⭐⭐⭐⭐⭐ Very Easy | ⭐⭐⭐⭐⭐ Excellent | No             | ⭐⭐⭐⭐⭐ Very Easy | All browsers    | **Recommended for most users** |
| **Task Scheduler**    | ⭐⭐⭐ Moderate      | ⭐⭐⭐⭐ Good        | No             | ⭐⭐⭐ Moderate      | All browsers    | Advanced scheduling needs      |
| **Registry Run Key**  | ⭐⭐ Advanced        | ⭐⭐⭐⭐ Good        | No (HKCU)      | ⭐⭐ Difficult       | All browsers    | Programmatic deployment        |
| **PowerShell Script** | ⭐⭐⭐ Moderate      | ⭐⭐⭐ Good          | Maybe\*        | ⭐⭐⭐ Moderate      | All browsers    | Script enthusiasts             |

\*PowerShell may require execution policy changes

---

## Method 1: Windows Startup Folder (RECOMMENDED)

### Overview

This method places a shortcut to a batch file in your Windows Startup folder. When you log into Windows, the batch file runs automatically and opens your HTML file in your default browser.

### Prerequisites

- Windows 10 or Windows 11
- The HTML file saved to a permanent location (e.g., `C:\Users\YourName\Documents\DailyQuotes\index.html`)
- Default browser configured (Chrome, Edge, Firefox, etc.)

### Step-by-Step Instructions

#### Step 1: Create a Permanent Location for Your HTML File

1. Create a dedicated folder for your quote generator:
   - Navigate to `C:\Users\YourName\Documents\`
   - Create a new folder called `DailyQuotes` (or your preferred name)
   - Place your `index.html` file inside this folder
   - **Important:** Do NOT move this file later, or the shortcut will break

#### Step 2: Create a Batch File to Launch the HTML File

1. Open Notepad (search for "Notepad" in Start menu)

2. Copy and paste this code:

   ```batch
   @echo off
   start "" "C:\Users\YourName\Documents\DailyQuotes\index.html"
   ```

3. **Replace** `YourName` with your actual Windows username
   - To find your username: Press `Windows + R`, type `cmd`, press Enter, then type `echo %USERNAME%`

4. Save the file:
   - Click File → Save As
   - Navigate to the same folder as your HTML file (`C:\Users\YourName\Documents\DailyQuotes\`)
   - Change "Save as type" to **All Files**
   - Name it: `LaunchQuote.bat`
   - Click Save

#### Step 3: Test the Batch File

1. Double-click `LaunchQuote.bat` in your folder
2. Your default browser should open with the quote generator
3. If it opens in a text editor instead of a browser, revisit Step 2 and ensure you saved it with the `.bat` extension

#### Step 4: Open the Startup Folder

1. Press `Windows + R` to open the Run dialog
2. Type: `shell:startup`
3. Press Enter
4. The Startup folder will open (location: `C:\Users\YourName\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`)

#### Step 5: Create a Shortcut to the Batch File

**Option A: Right-Click Method**

1. Navigate to your `DailyQuotes` folder in File Explorer
2. Right-click on `LaunchQuote.bat`
3. Select "Show more options" (Windows 11) or just right-click (Windows 10)
4. Click "Send to" → "Desktop (create shortcut)"
5. Go to your Desktop
6. Drag the shortcut into the Startup folder you opened in Step 4

**Option B: Direct Method**

1. Keep the Startup folder open
2. Right-click on `LaunchQuote.bat` in your DailyQuotes folder
3. Hold `Ctrl + Shift` and drag the file to the Startup folder
4. Release mouse button to create a shortcut

#### Step 6: Customize the Shortcut (Optional)

1. In the Startup folder, right-click your shortcut
2. Select "Properties"
3. In the "Shortcut" tab:
   - **Run:** Change to "Minimized" (prevents a command window from appearing briefly)
   - **Change Icon:** Add a custom icon if desired
4. Click OK

#### Step 7: Test the Auto-Launch

1. **Option 1 (Quick Test):** Log out of Windows (press `Ctrl + Alt + Delete` → Sign out) and log back in
2. **Option 2 (Full Test):** Restart your computer
3. After logging in, the quote should appear automatically within a few seconds

### Troubleshooting

| Problem                                 | Solution                                                                   |
| --------------------------------------- | -------------------------------------------------------------------------- |
| Opens in text editor instead of browser | Ensure the batch file is saved with `.bat` extension, not `.txt`           |
| "Windows cannot find the file" error    | Check the path in the batch file matches your actual file location         |
| Command window flashes briefly          | Right-click the shortcut → Properties → Run: Minimized                     |
| Doesn't open on startup                 | Verify the shortcut is in the correct Startup folder using `shell:startup` |
| Opens multiple times                    | Check if there are duplicate shortcuts in the Startup folder               |
| Doesn't work after moving the HTML file | Update the path in the batch file to the new location                      |

### How to Remove/Disable

1. Press `Windows + R`
2. Type: `shell:startup`
3. Press Enter
4. Delete the `LaunchQuote.bat` shortcut
5. Done! The quote will no longer open on startup

---

## Method 2: Windows Task Scheduler

### Overview

Task Scheduler is a built-in Windows tool that can trigger programs to run based on various events, including user login. This method provides more control and advanced options.

### Advantages

- More precise control over when tasks run (login vs. unlock)
- Can delay execution (e.g., wait 30 seconds after login)
- Built-in logging and history
- Can run tasks for all users or specific users

### Prerequisites

- Windows 10 or Windows 11
- The HTML file saved to a permanent location
- Optional: The batch file from Method 1 (recommended for reliability)

### Step-by-Step Instructions

#### Step 1: Create a Batch File (if not already done)

Follow Step 2 from Method 1 to create `LaunchQuote.bat`

#### Step 2: Open Task Scheduler

1. Press `Windows + R`
2. Type: `taskschd.msc`
3. Press Enter
4. Task Scheduler window will open

#### Step 3: Create a New Task

1. In the right-hand "Actions" panel, click **"Create Task..."** (not "Create Basic Task")
   - Note: Use "Create Task" for more control, not "Create Basic Task"

#### Step 4: Configure General Settings

In the **General** tab:

1. **Name:** `Morning Quote Generator`
2. **Description:** `Opens daily motivational quote on login`
3. **Security options:**
   - Select "Run only when user is logged on" (allows browser window to appear)
   - Check "Run with highest privileges" only if you encounter permission issues (not typically needed)
4. **Configure for:** Select your Windows version (Windows 10 or Windows 11)

#### Step 5: Configure Triggers

1. Click the **Triggers** tab
2. Click **New...**
3. Configure:
   - **Begin the task:** Select "At log on"
   - **Settings:** Select "Specific user: [Your username]" (not "Any user")
   - **Advanced settings:**
     - Check "Enabled"
     - **Delay task for:** 10 seconds (optional, gives Windows time to fully load)
     - Leave "Stop task if it runs longer than" unchecked
4. Click **OK**

#### Step 6: Configure Actions

1. Click the **Actions** tab
2. Click **New...**
3. Configure:
   - **Action:** "Start a program"
   - **Program/script:** Browse to your batch file (e.g., `C:\Users\YourName\Documents\DailyQuotes\LaunchQuote.bat`)
   - **Add arguments:** Leave blank
   - **Start in:** Leave blank
4. Click **OK**

#### Step 7: Configure Conditions (Important!)

1. Click the **Conditions** tab
2. **Power:**
   - Uncheck "Start the task only if the computer is on AC power" (allows it to run on laptops on battery)
3. **Network:** Leave defaults
4. Click **OK**

#### Step 8: Configure Settings

1. Click the **Settings** tab
2. Configure:
   - Check "Allow task to be run on demand"
   - Uncheck "Stop the task if it runs longer than"
   - Check "Run task as soon as possible after a scheduled start is missed"
   - If task fails, select "Do not restart"
3. Click **OK** to create the task

#### Step 9: Test the Task

1. In Task Scheduler, find your task in the list
2. Right-click on "Morning Quote Generator"
3. Select **"Run"**
4. The quote should appear in your browser
5. If it works, test by logging out and back in

### Troubleshooting

| Problem                                  | Solution                                                                |
| ---------------------------------------- | ----------------------------------------------------------------------- |
| Task doesn't run on login                | Check the Conditions tab - uncheck "Only if on AC power"                |
| Task shows "Running" but nothing happens | Set "Run only when user is logged on" in General tab                    |
| Browser opens but no page loads          | Use the batch file method instead of directly calling the browser       |
| Task runs on unlock instead of login     | In Triggers, ensure it's set to "At log on" not "On workstation unlock" |
| Multiple instances open                  | Check task history to see if task is triggering multiple times          |

### Viewing Task History

1. Open Task Scheduler
2. Click "Task Scheduler Library" in the left panel
3. Find your task and click it
4. Click the "History" tab at the bottom
5. Review events to see when the task ran and if there were any errors

### How to Remove/Disable

**To Disable:**

1. Open Task Scheduler
2. Find "Morning Quote Generator"
3. Right-click → **Disable**

**To Remove:**

1. Open Task Scheduler
2. Find "Morning Quote Generator"
3. Right-click → **Delete**
4. Click Yes to confirm

---

## Method 3: Registry Run Key

### Overview

The Windows Registry contains keys that automatically run programs at startup. Adding an entry to the Run key will execute your batch file every time you log in.

### ⚠️ WARNING: Exercise Caution

Editing the registry can cause system issues if done incorrectly. Always backup the registry before making changes. This method is recommended for advanced users only.

### Advantages

- Programmatic deployment (good for IT administrators)
- Persistent across updates
- Runs before some startup programs

### Disadvantages

- Requires manual registry editing
- More difficult to remove
- Less user-friendly
- Potential security risks if misconfigured

### Prerequisites

- Windows 10 or Windows 11
- Administrator knowledge (understand risks of registry editing)
- The batch file from Method 1 created and tested

### Step-by-Step Instructions

#### Step 1: Backup Your Registry (CRITICAL)

1. Press `Windows + R`
2. Type: `regedit`
3. Press Enter (click Yes if prompted by UAC)
4. In Registry Editor, click **File** → **Export**
5. Save location: Desktop
6. File name: `registry_backup_before_quote_generator`
7. Export range: Select **All**
8. Click Save
9. Keep this file safe in case you need to restore

#### Step 2: Navigate to the Run Key

1. In Registry Editor, navigate to:

   ```
   HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
   ```

   **Tip:** Copy and paste this path into the address bar at the top of Registry Editor

2. You should see a list of existing startup programs in the right panel

#### Step 3: Create a New String Value

1. Right-click in the **right panel** (empty space)
2. Select **New** → **String Value**
3. Name it: `MorningQuoteGenerator`
4. Press Enter

#### Step 4: Set the Value Data

1. Double-click on `MorningQuoteGenerator`
2. In the "Value data" field, enter the full path to your batch file:
   ```
   C:\Users\YourName\Documents\DailyQuotes\LaunchQuote.bat
   ```
3. **Important:** Replace `YourName` with your actual username
4. Click OK

#### Step 5: Verify the Entry

1. Check that your entry appears in the list
2. The Name should be `MorningQuoteGenerator`
3. The Type should be `REG_SZ`
4. The Data should be the full path to your batch file

#### Step 6: Close Registry Editor and Test

1. Close Registry Editor
2. Log out and log back in, or restart your computer
3. The quote should appear automatically

### Alternative: Add Registry Entry via Command Line

If you're comfortable with the command line, you can add the registry entry without opening Registry Editor:

1. Press `Windows + X` and select "Terminal" or "Command Prompt"
2. Run this command (replace `YourName` with your username):
   ```cmd
   REG ADD "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /V "MorningQuoteGenerator" /t REG_SZ /F /D "C:\Users\YourName\Documents\DailyQuotes\LaunchQuote.bat"
   ```
3. You should see: "The operation completed successfully."

### Troubleshooting

| Problem                             | Solution                                                           |
| ----------------------------------- | ------------------------------------------------------------------ |
| Entry created but doesn't run       | Verify the path is correct with no typos                           |
| "Access Denied" error               | Ensure you're editing HKCU (current user) not HKLM (local machine) |
| Batch file runs but nothing happens | Test the batch file manually first                                 |
| Want to disable temporarily         | Rename the registry value (add "\_disabled" to the name)           |
| Changes don't take effect           | Restart Windows or log out/in                                      |

### How to Remove/Disable

**Method 1: Via Registry Editor**

1. Press `Windows + R`, type `regedit`, press Enter
2. Navigate to: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
3. Right-click `MorningQuoteGenerator`
4. Click **Delete**
5. Click Yes to confirm

**Method 2: Via Command Line**

1. Open Command Prompt or Terminal
2. Run:
   ```cmd
   REG DELETE "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /V "MorningQuoteGenerator" /F
   ```

### Security Considerations

- Only add entries from trusted sources
- Never edit HKLM (local machine) keys unless absolutely necessary (requires admin rights)
- Be aware that malware often uses Run keys for persistence
- Regularly audit your Run keys for unknown entries
- Keep your registry backup in a safe location

---

## Method 4: PowerShell Script

### Overview

PowerShell can open the HTML file in your default browser. This method involves creating a PowerShell script and configuring it to run at startup using one of the previous methods.

### Advantages

- More powerful scripting capabilities
- Can add logic (e.g., only run on weekdays)
- Can handle errors gracefully
- Can interact with Windows APIs

### Disadvantages

- May require execution policy changes
- Slightly more complex than batch files
- Some users have stricter PowerShell security policies

### Prerequisites

- Windows 10 or Windows 11
- PowerShell 5.1 or later (included in Windows)
- The HTML file saved to a permanent location

### Step-by-Step Instructions

#### Step 1: Create the PowerShell Script

1. Open Notepad
2. Copy and paste this code:

   ```powershell
   # Morning Motivation Quote Generator - Startup Script

   # Path to your HTML file
   $htmlFile = "C:\Users\YourName\Documents\DailyQuotes\index.html"

   # Check if file exists
   if (Test-Path $htmlFile) {
       # Open in default browser
       Start-Process $htmlFile
   } else {
       # Error handling
       [System.Windows.Forms.MessageBox]::Show("Quote file not found: $htmlFile", "Morning Quote Error")
   }
   ```

3. **Replace** `YourName` with your actual Windows username

4. Save the file:
   - Click File → Save As
   - Navigate to: `C:\Users\YourName\Documents\DailyQuotes\`
   - Change "Save as type" to **All Files**
   - Name it: `LaunchQuote.ps1`
   - Click Save

#### Step 2: Check PowerShell Execution Policy

1. Open PowerShell as Administrator:
   - Press `Windows + X`
   - Select "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. Check current policy:

   ```powershell
   Get-ExecutionPolicy
   ```

3. If it shows "Restricted", you need to change it:

   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

   - Type `Y` and press Enter to confirm

   **What this does:** Allows locally-created scripts to run, but downloaded scripts must be signed. This is a reasonable security balance.

#### Step 3: Test the PowerShell Script

1. Right-click on `LaunchQuote.ps1`
2. Select "Run with PowerShell"
3. Your browser should open with the quote
4. If you see a security warning, select "Run once" or "Always run"

#### Step 4: Configure Auto-Launch

You can use any of these methods to run your PowerShell script at startup:

**Option A: Startup Folder (Recommended)**

1. Follow Method 1 (Startup Folder), but in Step 2, create a batch file with this content instead:
   ```batch
   @echo off
   powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File "C:\Users\YourName\Documents\DailyQuotes\LaunchQuote.ps1"
   ```
2. Save as `LaunchQuotePowerShell.bat`
3. Create a shortcut to this batch file in your Startup folder

**Option B: Task Scheduler**

1. Follow Method 2 (Task Scheduler)
2. In Step 6 (Actions), configure:
   - **Program/script:** `powershell.exe`
   - **Add arguments:** `-WindowStyle Hidden -ExecutionPolicy Bypass -File "C:\Users\YourName\Documents\DailyQuotes\LaunchQuote.ps1"`

**Option C: Registry**

1. Follow Method 3 (Registry)
2. In Step 4, use this value data:
   ```
   powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File "C:\Users\YourName\Documents\DailyQuotes\LaunchQuote.ps1"
   ```

#### Step 5: Advanced Script (Optional)

For more control, use this enhanced script:

```powershell
# Morning Motivation Quote Generator - Advanced Startup Script

# Configuration
$htmlFile = "C:\Users\YourName\Documents\DailyQuotes\index.html"
$logFile = "C:\Users\YourName\Documents\DailyQuotes\launch.log"

# Only run on weekdays (optional)
$today = (Get-Date).DayOfWeek
if ($today -eq "Saturday" -or $today -eq "Sunday") {
    Add-Content -Path $logFile -Value "$(Get-Date): Skipped (weekend)"
    exit
}

# Wait for network (if quote uses online API)
$maxWaitSeconds = 10
$waitedSeconds = 0
while (-not (Test-Connection -ComputerName 8.8.8.8 -Count 1 -Quiet) -and $waitedSeconds -lt $maxWaitSeconds) {
    Start-Sleep -Seconds 1
    $waitedSeconds++
}

# Check if file exists
if (Test-Path $htmlFile) {
    # Open in default browser
    Start-Process $htmlFile
    Add-Content -Path $logFile -Value "$(Get-Date): Opened successfully"
} else {
    # Log error
    Add-Content -Path $logFile -Value "$(Get-Date): ERROR - File not found"

    # Show error message (optional)
    Add-Type -AssemblyName PresentationFramework
    [System.Windows.MessageBox]::Show("Quote file not found: $htmlFile", "Morning Quote Error", "OK", "Error")
}
```

### Troubleshooting

| Problem                            | Solution                                                                      |
| ---------------------------------- | ----------------------------------------------------------------------------- |
| "Script cannot be loaded" error    | Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell Admin |
| Script runs but nothing happens    | Test the script manually; check the log file for errors                       |
| PowerShell window flashes briefly  | Add `-WindowStyle Hidden` to the launch command                               |
| "Execution policy" warning appears | Add `-ExecutionPolicy Bypass` to the launch command                           |
| Script runs multiple times         | Check for duplicate entries in startup locations                              |

### How to Remove/Disable

Remove the startup entry using the method you chose in Step 4:

- **Startup Folder:** Delete the batch file shortcut
- **Task Scheduler:** Delete the task
- **Registry:** Delete the registry value

### PowerShell Execution Policy Reference

| Policy       | Description                                                        | Security Level  |
| ------------ | ------------------------------------------------------------------ | --------------- |
| Restricted   | No scripts can run (default on some systems)                       | Highest         |
| AllSigned    | Only signed scripts can run                                        | High            |
| RemoteSigned | Locally-created scripts can run; downloaded scripts must be signed | **Recommended** |
| Unrestricted | All scripts can run (with warnings)                                | Low             |
| Bypass       | No restrictions or warnings                                        | Lowest          |

---

## Browser-Specific Notes

### Default Browser Behavior

The `start` command in Windows and PowerShell's `Start-Process` cmdlet both respect your Windows default browser setting. The HTML file will open in whichever browser is set as default.

### How to Check Your Default Browser

1. Open **Settings** (Press `Windows + I`)
2. Go to **Apps** → **Default apps**
3. Scroll down to **Web browser**
4. You'll see your current default (e.g., Chrome, Edge, Firefox)

### How to Change Your Default Browser

1. Open **Settings** → **Apps** → **Default apps**
2. Click on the current web browser
3. Select your preferred browser from the list
4. Close Settings

### Browser-Specific Considerations

#### Microsoft Edge

- **Pre-installed:** Yes
- **Behavior:** Opens quickly, good integration with Windows
- **Full-screen mode:** The HTML can use F11 or request fullscreen via JavaScript
- **Notes:** Default browser on new Windows installations

#### Google Chrome

- **Pre-installed:** No (must install)
- **Behavior:** Fast startup, extensive extension support
- **Full-screen mode:** Supports JavaScript fullscreen API
- **Startup options:** Can be configured to restore previous tabs (disable this if you don't want interference)
- **Notes:** If Chrome has "Continue where you left off" enabled, it may restore previous tabs in addition to opening your quote

#### Mozilla Firefox

- **Pre-installed:** No (must install)
- **Behavior:** Privacy-focused, respects user settings
- **Full-screen mode:** Supports JavaScript fullscreen API
- **Notes:** May show a "Firefox is starting" screen briefly

#### Opening in a Specific Browser (Override Default)

If you want to force a specific browser regardless of the default setting, modify your batch file:

**For Chrome:**

```batch
@echo off
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" "C:\Users\YourName\Documents\DailyQuotes\index.html"
```

**For Firefox:**

```batch
@echo off
start "" "C:\Program Files\Mozilla Firefox\firefox.exe" "C:\Users\YourName\Documents\DailyQuotes\index.html"
```

**For Edge:**

```batch
@echo off
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" "C:\Users\YourName\Documents\DailyQuotes\index.html"
```

**Note:** Adjust paths if your browser is installed in a different location.

### Browser Command-Line Options

You can add flags to control browser behavior:

**Chrome Options:**

```batch
start "" "chrome.exe" --new-window "file:///C:/Users/YourName/Documents/DailyQuotes/index.html"
```

- `--new-window`: Opens in a new window instead of a tab
- `--incognito`: Opens in incognito mode
- `--kiosk`: Full-screen kiosk mode (no browser UI)

**Firefox Options:**

```batch
start "" "firefox.exe" -new-window "file:///C:/Users/YourName/Documents/DailyQuotes/index.html"
```

- `-new-window`: Opens in a new window
- `-private-window`: Opens in private browsing mode

**Edge Options:**

```batch
start "" "msedge.exe" --new-window "file:///C:/Users/YourName/Documents/DailyQuotes/index.html"
```

- `--new-window`: Opens in a new window
- `--inprivate`: Opens in InPrivate mode

---

## Troubleshooting Guide

### General Issues

#### Quote doesn't appear on startup

**Possible causes:**

1. Shortcut/task not in correct location
2. File path is incorrect
3. Permissions issue

**Solutions:**

- Verify the startup method is correctly configured
- Test the batch file manually by double-clicking it
- Check that the HTML file hasn't been moved or renamed
- Review Windows Event Viewer for errors (press `Windows + X` → Event Viewer → Windows Logs → Application)

#### Opens multiple times on startup

**Possible causes:**

1. Multiple startup entries
2. Both registry and startup folder configured
3. Task scheduler task running multiple times

**Solutions:**

- Check `shell:startup` for duplicate shortcuts
- Check Task Scheduler for duplicate tasks
- Check Registry Run key: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
- Use Autoruns utility (from Microsoft Sysinternals) to see all startup locations

#### Command prompt window flashes briefly

**Possible causes:**

1. Batch file running without hidden window mode
2. Shortcut not configured to run minimized

**Solutions:**

- Right-click shortcut → Properties → Run: Minimized
- Add `@echo off` to the beginning of your batch file
- For PowerShell: Use `-WindowStyle Hidden` parameter

#### Opens on screen unlock instead of login

**Possible causes:**

1. Task Scheduler trigger set incorrectly

**Solutions:**

- Open Task Scheduler
- Edit your task
- In Triggers tab, ensure it's set to "At log on" not "On workstation unlock"
- Ensure "Specific user" is selected, not "Any user"

### Browser-Related Issues

#### Opens in text editor instead of browser

**Possible causes:**

1. File extension association changed
2. Batch file not using correct command

**Solutions:**

- Ensure the file is named `index.html` not `index.html.txt`
- Check default app for .html files in Windows Settings
- Use `start` command in batch file: `start "" "C:\path\to\file.html"`

#### Browser opens but page is blank

**Possible causes:**

1. HTML file is empty or corrupted
2. JavaScript errors preventing page load
3. Internet not connected (if quote fetches from API)

**Solutions:**

- Open the HTML file manually to verify it works
- Check browser console for errors (press F12 → Console tab)
- Ensure network is connected before quote attempts to fetch from API
- Add a delay in Task Scheduler (10-30 seconds) to allow network to connect

#### Wrong browser opens

**Possible causes:**

1. Default browser setting is not what you expected

**Solutions:**

- Change default browser: Settings → Apps → Default apps → Web browser
- Or specify browser explicitly in batch file (see Browser-Specific Notes section)

### Permissions Issues

#### "Access Denied" error

**Possible causes:**

1. File is in a protected location
2. Execution policy blocking PowerShell

**Solutions:**

- Move HTML file to your Documents folder
- For PowerShell: Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Ensure the batch file has read permissions

#### Task runs but nothing visible happens

**Possible causes:**

1. Task configured to "Run whether user is logged on or not"
2. Task running under wrong user account

**Solutions:**

- Open Task Scheduler → Properties → General tab
- Select "Run only when user is logged on"
- Verify "When running the task, use the following user account" shows your username

### Network-Related Issues

#### Quote doesn't load (shows error message)

**Possible causes:**

1. Internet not connected yet at startup
2. API service is down
3. Firewall blocking browser

**Solutions:**

- Add a delay to allow network to connect (Method 2, Task Scheduler: "Delay task for 30 seconds")
- Implement fallback quotes in your HTML (as per project requirements)
- Check firewall settings: Settings → Privacy & Security → Windows Security → Firewall & network protection

### Windows Update Issues

#### Stopped working after Windows update

**Possible causes:**

1. Update reset some settings
2. Startup locations cleaned by update

**Solutions:**

- Recheck that your startup entry still exists
- Verify file paths haven't changed
- Re-create the startup entry if necessary
- Startup Folder method is most resistant to updates

---

## How to Uninstall / Remove Auto-Launch

### Method 1: Startup Folder

1. Press `Windows + R`
2. Type: `shell:startup`
3. Press Enter
4. Delete the shortcut file
5. ✅ Done! Quote will no longer launch on startup

**Optional: Complete Removal**

- Delete the DailyQuotes folder: `C:\Users\YourName\Documents\DailyQuotes\`
- Delete the batch file if you created one

### Method 2: Task Scheduler

1. Press `Windows + R`
2. Type: `taskschd.msc`
3. Press Enter
4. Find "Morning Quote Generator" in the task list
5. Right-click → **Delete**
6. Click **Yes** to confirm
7. ✅ Done!

### Method 3: Registry Run Key

1. Press `Windows + R`
2. Type: `regedit`
3. Press Enter
4. Navigate to: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
5. Find `MorningQuoteGenerator` in the right panel
6. Right-click → **Delete**
7. Click **Yes** to confirm
8. Close Registry Editor
9. ✅ Done!

**Alternative (Command Line):**

```cmd
REG DELETE "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /V "MorningQuoteGenerator" /F
```

### Method 4: PowerShell Script

The PowerShell script itself launches via one of the methods above, so:

1. Remove the startup entry using the appropriate method (Startup Folder, Task Scheduler, or Registry)
2. Optional: Delete the PowerShell script file: `C:\Users\YourName\Documents\DailyQuotes\LaunchQuote.ps1`

### Complete Uninstallation Checklist

To ensure complete removal:

- [ ] Remove from Startup folder (`shell:startup`)
- [ ] Remove from Task Scheduler (search for "Morning Quote" or "Quote Generator")
- [ ] Remove from Registry Run key (`HKCU\...\Run`)
- [ ] Delete the batch file (if created)
- [ ] Delete the PowerShell script (if created)
- [ ] Delete the HTML file and folder (if no longer needed)
- [ ] Restart computer to verify nothing launches

### Verification

After removal:

1. Press `Windows + R` → `shell:startup` → Verify shortcut is gone
2. Open Task Scheduler → Verify task is gone
3. Open Registry Editor → Navigate to Run key → Verify entry is gone
4. Restart computer → Quote should not appear

---

## Cross-Platform Bonus: macOS and Linux

### macOS: LaunchAgents

**Overview:** macOS uses Launch Agents (plist files) to run programs at login.

**Quick Setup:**

1. **Create the plist file:**

   ```bash
   nano ~/Library/LaunchAgents/com.user.morningquote.plist
   ```

2. **Add this content:**

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.user.morningquote</string>
       <key>ProgramArguments</key>
       <array>
           <string>open</string>
           <string>-a</string>
           <string>Safari</string>
           <string>/Users/YourName/Documents/DailyQuotes/index.html</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
   </dict>
   </plist>
   ```

3. **Replace:**
   - `YourName` with your macOS username
   - `Safari` with your preferred browser (Chrome, Firefox, etc.)

4. **Load the LaunchAgent:**

   ```bash
   launchctl load ~/Library/LaunchAgents/com.user.morningquote.plist
   ```

5. **Test:** Log out and log back in

**To Remove:**

```bash
launchctl unload ~/Library/LaunchAgents/com.user.morningquote.plist
rm ~/Library/LaunchAgents/com.user.morningquote.plist
```

**Alternative (simpler):**

- Open **System Preferences** → **Users & Groups**
- Click your username → **Login Items**
- Click the **+** button
- Navigate to a script that opens your HTML file
- Add it to the list

---

### Linux: XDG Autostart Desktop Entries

**Overview:** Most Linux desktop environments follow the XDG autostart specification using `.desktop` files.

**Quick Setup:**

1. **Create the autostart directory (if it doesn't exist):**

   ```bash
   mkdir -p ~/.config/autostart
   ```

2. **Create the desktop entry file:**

   ```bash
   nano ~/.config/autostart/morning-quote.desktop
   ```

3. **Add this content:**

   ```ini
   [Desktop Entry]
   Type=Application
   Name=Morning Motivation Quote
   Comment=Display motivational quote on login
   Exec=/bin/bash -c 'sleep 5 && xdg-open "/home/YourName/Documents/DailyQuotes/index.html"'
   Terminal=false
   X-GNOME-Autostart-enabled=true
   ```

4. **Replace:**
   - `YourName` with your Linux username
   - Adjust the sleep delay (5 seconds) as needed

5. **Make it executable:**

   ```bash
   chmod +x ~/.config/autostart/morning-quote.desktop
   ```

6. **Test:** Log out and log back in

**Alternative browsers:**

- Replace `xdg-open` with `firefox`, `google-chrome`, or `chromium-browser` for specific browsers

**To Remove:**

```bash
rm ~/.config/autostart/morning-quote.desktop
```

**Alternative (GUI method):**

- **GNOME:** Settings → Applications → Startup Applications
- **KDE Plasma:** System Settings → Startup and Shutdown → Autostart
- **XFCE:** Settings → Session and Startup → Application Autostart

---

## FAQ

### Q: Will this work on Windows 11?

**A:** Yes! All methods work on both Windows 10 and Windows 11. The Startup Folder method is identical on both versions.

### Q: Can I make it only run on weekdays?

**A:** Yes! Use the PowerShell script method (Method 4) with the advanced script that includes day-of-week checking. Or use Task Scheduler (Method 2) and configure weekly triggers for Monday-Friday only.

### Q: How do I delay the quote by 30 seconds after login?

**A:**

- **Startup Folder:** Modify the batch file to include `timeout /t 30 /nobreak` before the `start` command
- **Task Scheduler:** In the Triggers tab, set "Delay task for: 30 seconds"
- **PowerShell:** Add `Start-Sleep -Seconds 30` at the beginning of the script

### Q: Can I open multiple HTML files on startup?

**A:** Yes! Add multiple lines to your batch file:

```batch
@echo off
start "" "C:\Path\To\File1.html"
start "" "C:\Path\To\File2.html"
start "" "C:\Path\To\File3.html"
```

### Q: What if my antivirus blocks the batch file?

**A:** Some antivirus software flags batch files as potentially malicious. Solutions:

1. Add an exclusion for your DailyQuotes folder in your antivirus settings
2. Use Task Scheduler (Method 2) instead, which is less likely to be flagged
3. Digitally sign your script (advanced)

### Q: Can this open a web URL instead of a local file?

**A:** Yes! Modify the batch file to:

```batch
@echo off
start "" "https://example.com/quote.html"
```

### Q: How do I stop it from opening a new tab every time?

**A:** If your browser is already open, it will open in a new tab by default. To force a new window:

```batch
start chrome --new-window "C:\Path\To\index.html"
```

### Q: Will this work if I have multiple user accounts?

**A:** The methods shown configure auto-launch for the **current user only**. Each user account needs to set up their own startup entry. To configure for all users:

- **Startup Folder:** Use `shell:common startup` instead of `shell:startup`
- **Registry:** Use `HKEY_LOCAL_MACHINE` instead of `HKEY_CURRENT_USER` (requires admin rights)

### Q: Does this work with Microsoft Teams or other programs set to start automatically?

**A:** Yes! Your quote generator will launch alongside other startup programs. If you want it to launch before or after others, use Task Scheduler with a delay.

### Q: How do I troubleshoot if nothing happens?

**A:** Follow this checklist:

1. Test the batch file manually by double-clicking it
2. Verify the HTML file exists at the specified path
3. Check Windows Event Viewer for errors
4. Ensure your default browser is set correctly
5. Try the PowerShell method with logging enabled to see errors

### Q: Can I password-protect or hide the quote files?

**A:** You can:

1. Set folder permissions to hide from other users
2. Use the "Hidden" attribute on the folder
3. Store in a non-obvious location
4. Use BitLocker to encrypt the drive (Windows Pro/Enterprise)

### Q: What happens if Windows updates and restarts while I'm away?

**A:** The quote will launch automatically when Windows finishes updating and you log back in. However, you won't see it if you weren't there. Consider adding logging to track when it runs.

### Q: Can I make it full-screen?

**A:** Yes! Add this JavaScript to your HTML file:

```javascript
// Request fullscreen after page loads
window.onload = function () {
  document.documentElement.requestFullscreen();
};
```

Or use browser kiosk mode in your batch file:

```batch
start chrome --kiosk "C:\Path\To\index.html"
```

---

## Additional Resources

### Official Microsoft Documentation

- [Task Scheduler documentation](https://docs.microsoft.com/windows/win32/taskschd/task-scheduler-start-page)
- [Registry Run Keys](https://learn.microsoft.com/windows/win32/setupapi/run-and-runonce-registry-keys)
- [PowerShell Documentation](https://docs.microsoft.com/powershell/)

### Useful Tools

- **Autoruns** (Microsoft Sysinternals): View all startup programs
  - Download: https://docs.microsoft.com/sysinternals/downloads/autoruns
  - Shows ALL startup locations (registry, folders, scheduled tasks, etc.)
- **Process Explorer** (Microsoft Sysinternals): See running processes and their startup paths
- **Event Viewer**: Built into Windows (Windows + X → Event Viewer)

### Testing Your Setup

1. **Manual Test:** Run the batch file by double-clicking
2. **Logout Test:** Sign out and sign back in (faster than restart)
3. **Cold Boot Test:** Full restart to simulate morning login
4. **Network Test:** Disconnect network, then test (to ensure fallback quotes work)

### Best Practices

1. **Use absolute paths:** Never use relative paths (e.g., `.\file.html`) in startup scripts
2. **Test thoroughly:** Always test manually before configuring auto-launch
3. **Keep it simple:** The Startup Folder method is simplest and most reliable
4. **Document your setup:** Keep notes on which method you used
5. **Regular maintenance:** Check quarterly that it's still working
6. **Backup:** Keep a copy of your batch file and HTML file

### Performance Considerations

- **Startup impact:** Minimal - opening a single HTML file adds ~1-2 seconds to startup time
- **Memory usage:** Minimal - only the browser tab's memory footprint
- **Network usage:** Only when fetching quotes from API (small data transfer)
- **Battery impact:** Negligible on laptops

---

## Version History

**Version 1.0** - Created: 2025-01-12

- Initial comprehensive guide
- Covers Windows 10/11 primary methods
- Includes macOS and Linux cross-platform notes
- Detailed troubleshooting and browser-specific instructions

---

## Support and Feedback

If you encounter issues not covered in this guide:

1. **Check Windows Event Viewer** for specific error messages
2. **Test each component** individually (batch file, HTML file, browser)
3. **Review the Troubleshooting section** for common problems
4. **Verify file paths** have no typos or special characters
5. **Try the simplest method first** (Startup Folder) before advanced methods

---

**End of Auto-Launch Guide**

This guide is part of the **Morning Motivation Quote Generator** project.
For questions about the HTML/JavaScript implementation, see the project README.
