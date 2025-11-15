# PRD: Security Audit - Production Code Review

**Version:** 1.0.0
**Status:** Draft
**Created:** 2025-11-15
**Owner:** Production Readiness Initiative

## Executive Summary

Conduct a comprehensive security audit of `quote_overlay.py` to identify and remediate vulnerabilities before public release on GitHub. Ensure the application follows security best practices and does not expose users to risks.

## Security Scope

**In Scope:**
- Python source code (`quote_overlay.py`)
- External dependencies (`requests`, `Pillow`)
- User data handling (`user_settings.json`)
- Network communication (DummyJSON API)
- File system operations
- Web browser integration

**Out of Scope:**
- Windows OS vulnerabilities
- Tkinter framework vulnerabilities (standard library)
- User's system security posture
- Network infrastructure security

## Threat Model

### Attacker Profiles

**1. Malicious API Response**
- **Goal:** Inject malicious content via API
- **Attack Vector:** Compromised DummyJSON API returns malicious JSON
- **Impact:** Code execution, XSS in browser, file system access

**2. Local File System Attacker**
- **Goal:** Manipulate user settings to cause harm
- **Attack Vector:** Edit user_settings.json with malicious content
- **Impact:** Code execution, path traversal, DoS

**3. Dependency Supply Chain Attack**
- **Goal:** Execute malicious code via compromised dependency
- **Attack Vector:** Malicious version of requests or Pillow
- **Impact:** Full system compromise

**4. Social Engineering**
- **Goal:** Trick user into running malicious fork
- **Attack Vector:** Cloned repository with malicious code
- **Impact:** Full system compromise

### Assets to Protect

**Primary Assets:**
1. User's system integrity (no code execution)
2. User's data privacy (settings file)
3. User's network security (API calls)

**Secondary Assets:**
1. Application availability (no DoS)
2. Code integrity (no tampering)
3. Reputation (no vulnerabilities in public repo)

## Security Audit Checklist

### 1. Input Validation

#### 1.1 API Response Validation
**File:** `quote_overlay.py:678-707`

**Current Implementation:**
```python
response = requests.get(CONFIG["api_url"], timeout=CONFIG["api_timeout"])
if response.status_code == 200:
    data = response.json()
    quote_text = data.get("quote", "")
    # ... normalize and use
```

**Checks:**
- [ ] **JSON structure validation** - Does code validate expected keys exist?
- [ ] **Data type validation** - Does code check if values are strings?
- [ ] **Length limits** - Are there maximum length checks on quote/author?
- [ ] **Character sanitization** - Are dangerous characters filtered?
- [ ] **Encoding validation** - Is UTF-8 handled safely?

**Potential Vulnerabilities:**
- ❌ **No length limits** - Extremely long quote could cause UI overflow or memory issues
- ❌ **No type checking** - API could return non-string data causing TypeError
- ✅ **normalize_text() handles unicode** - Good! Uses re.UNICODE
- ✅ **URL encoding in search_quote()** - Good! Uses url_quote()

**Recommendations:**
1. Add maximum length validation (e.g., 1000 chars for quote, 100 for author)
2. Add type checking: `isinstance(quote_text, str)`
3. Add JSON schema validation

#### 1.2 User Settings File Validation
**File:** `quote_overlay.py:371-398`

**Current Implementation:**
```python
with open(SETTINGS_FILE, 'r') as f:
    saved = json.load(f)
    # Merge with defaults
    return {**defaults, **saved}
```

**Checks:**
- [ ] **JSON parsing error handling** - try/except present?
- [ ] **Schema validation** - Are values validated against expected types?
- [ ] **Range validation** - Are numeric values within expected ranges?
- [ ] **Enum validation** - Are string values from expected set?
- [ ] **Path traversal** - Can SETTINGS_FILE be manipulated?

**Potential Vulnerabilities:**
- ✅ **Exception handling present** - Good! Returns defaults on error
- ✅ **Path is fixed** - Good! Uses `os.path.dirname(__file__)`
- ❌ **No value validation** - timerDuration could be negative or huge
- ❌ **No enum validation** - position/fontSize/category could be arbitrary strings

**Recommendations:**
1. Validate timerDuration range (5-60)
2. Validate position against allowed values
3. Validate fontSize against ['small', 'medium', 'large']
4. Validate category against allowed values + 'all'

#### 1.3 Command Injection Prevention
**File:** `quote_overlay.py:944-948`

**Current Implementation:**
```python
def search_quote(self, text):
    """Open Google search for the quote"""
    import webbrowser
    search_query = url_quote(f'"{text}"')
    webbrowser.open(f'https://www.google.com/search?q={search_query}')
```

**Checks:**
- [ ] **URL encoding** - Is user input properly encoded?
- [ ] **Protocol validation** - Is HTTPS enforced?
- [ ] **Command injection** - Can shell commands be injected?

**Potential Vulnerabilities:**
- ✅ **URL encoding used** - Good! `url_quote()` prevents injection
- ✅ **HTTPS enforced** - Good! Hardcoded to Google HTTPS
- ✅ **No shell execution** - Good! Uses webbrowser module (safe)

**Status:** ✅ SECURE

### 2. File System Security

#### 2.1 File Path Validation
**File:** `quote_overlay.py:158`

**Current Implementation:**
```python
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'user_settings.json')
```

**Checks:**
- [ ] **Path traversal prevention** - Can attacker manipulate path?
- [ ] **Write permissions** - Are write operations safe?
- [ ] **File creation** - Are permissions set correctly on creation?

**Potential Vulnerabilities:**
- ✅ **Fixed path** - Good! No user input in path construction
- ✅ **Same directory as script** - Good! No ability to write elsewhere
- ⚠️ **No explicit file permissions** - Default OS permissions apply

**Recommendations:**
1. Document that user_settings.json should have user-only permissions
2. Consider adding permission check on first run (Windows: file permissions API)

#### 2.2 File Write Operations
**File:** `quote_overlay.py:392-398`

**Current Implementation:**
```python
def save_settings(self):
    """Save settings to JSON file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(self.settings, f, indent=2)
    except Exception as e:
        print(f"Error saving settings: {e}")
```

**Checks:**
- [ ] **Atomic writes** - Is write operation atomic?
- [ ] **Error handling** - Are write failures handled gracefully?
- [ ] **Data integrity** - Is JSON validated before writing?

**Potential Vulnerabilities:**
- ⚠️ **Non-atomic writes** - File could be corrupted if interrupted
- ✅ **Exception handling** - Good! Errors caught and logged
- ❌ **No validation before write** - Could write invalid data

**Recommendations:**
1. Use atomic write pattern (write to temp file, then rename)
2. Validate settings data before writing
3. Consider backup of previous settings file

### 3. Network Security

#### 3.1 HTTPS Enforcement
**File:** `quote_overlay.py:150`

**Current Implementation:**
```python
"api_url": "https://dummyjson.com/quotes/random",
```

**Checks:**
- [ ] **HTTPS used** - Is TLS enforced?
- [ ] **Certificate validation** - Are SSL certs verified?
- [ ] **Timeout configured** - Is there a network timeout?

**Potential Vulnerabilities:**
- ✅ **HTTPS enforced** - Good! Hardcoded HTTPS URL
- ✅ **Certificate validation** - Good! requests library validates by default
- ✅ **Timeout configured** - Good! 5 second timeout

**Status:** ✅ SECURE

#### 3.2 Request Library Security
**File:** `requirements.txt`

**Current Implementation:**
```
requests>=2.31.0
```

**Checks:**
- [ ] **Version pinning** - Is version explicitly pinned?
- [ ] **Known vulnerabilities** - Any CVEs in this version?
- [ ] **SSL/TLS support** - Does version support modern TLS?

**Potential Vulnerabilities:**
- ⚠️ **Minimum version only** - Using >= allows future versions with vulnerabilities
- ✅ **Modern version** - 2.31.0 is recent (released 2023)

**Recommendations:**
1. Pin exact version: `requests==2.31.0` (or latest stable)
2. Document that users should update periodically
3. Consider adding dependency scanning (pip-audit or safety)

### 4. Dependency Security

#### 4.1 Pillow (PIL) Security
**File:** `requirements.txt:2`

**Current Implementation:**
```python
# Pillow>=10.0.0
```

**Checks:**
- [ ] **Optional dependency** - Is failure handled gracefully?
- [ ] **Known vulnerabilities** - Any CVEs in Pillow 10.x?
- [ ] **Image parsing** - Is image data from trusted sources?

**Potential Vulnerabilities:**
- ✅ **Graceful degradation** - Good! PIL_AVAILABLE flag, app works without it
- ✅ **No external images** - Good! Only generates images, doesn't parse external data
- ⚠️ **Commented out** - Currently not enforced in requirements.txt

**Recommendations:**
1. Uncomment Pillow in requirements.txt (already present in code)
2. Pin exact version
3. Document that Pillow is required for advanced visual features

#### 4.2 Supply Chain Security
**File:** `requirements.txt`

**Checks:**
- [ ] **Dependency sources** - Are packages from PyPI?
- [ ] **Hash verification** - Are package hashes verified?
- [ ] **Minimal dependencies** - Only necessary packages?

**Potential Vulnerabilities:**
- ✅ **PyPI source** - Good! Standard package manager
- ⚠️ **No hash pinning** - Could install tampered package
- ✅ **Minimal deps** - Good! Only 2 external dependencies

**Recommendations:**
1. Use `pip freeze > requirements.txt` for exact versions
2. Consider using `pip-tools` for hash pinning
3. Document: "Use pip install --require-hashes for production"

### 5. Code Quality & Logic Security

#### 5.1 Dangerous Function Usage
**Search Pattern:** `eval(`, `exec(`, `__import__`, `compile(`

**Checks:**
- [ ] **Dynamic code execution** - Are eval/exec used?
- [ ] **Dynamic imports** - Are imports from user input?
- [ ] **Reflection** - Is `getattr`/`setattr` used unsafely?

**Results:**
- ✅ **No eval() usage**
- ✅ **No exec() usage**
- ✅ **No dynamic imports**
- ✅ **No dangerous reflection**

**Status:** ✅ SECURE

#### 5.2 Infinite Loop Prevention
**File:** Multiple locations with `while` or recursion

**Checks:**
- [ ] **Timer loops** - Do they have exit conditions?
- [ ] **Recursion** - Is there a depth limit?
- [ ] **Resource limits** - Are there caps on memory/CPU?

**Potential Vulnerabilities:**
- ✅ **Timer has exit** - Good! progress >= 1.0 stops timer
- ✅ **Fade animations bounded** - Good! alpha <= 0.96 and >= 0 limits
- ✅ **API retries limited** - Good! max_attempts = 5
- ✅ **No user-controlled loops** - Good! All loops are fixed

**Status:** ✅ SECURE

#### 5.3 Memory Safety
**File:** `quote_overlay.py:161-213` (gradient generation)

**Current Implementation:**
```python
pixels = []
for y in range(height):
    for x in range(width):
        # Calculate color for each pixel
        pixels.append((r, g, b))
```

**Checks:**
- [ ] **Memory allocation** - Can attacker cause excessive allocation?
- [ ] **Resource cleanup** - Are resources freed properly?
- [ ] **Image size limits** - Are there bounds on dimensions?

**Potential Vulnerabilities:**
- ⚠️ **No size limits** - Could create huge image if window size manipulated
- ✅ **Window size constrained** - Good! max 800px width, 200px height
- ✅ **Resource cleanup** - Good! Python GC handles cleanup

**Recommendations:**
1. Add explicit size validation in create_diagonal_gradient()
2. Maximum size: 1920x1080 (largest reasonable screen)

### 6. Privacy & Data Protection

#### 6.1 Data Collection
**File:** Entire codebase

**Checks:**
- [ ] **No telemetry** - Is data sent to external servers?
- [ ] **No logging of personal data** - Are logs safe?
- [ ] **No tracking cookies** - Any web tracking?

**Results:**
- ✅ **No telemetry** - Good! Only fetches quotes, sends no data
- ✅ **Minimal logging** - Good! Only error messages to console
- ✅ **No cookies/tracking** - Good! Desktop app, no web tracking

**Status:** ✅ SECURE - Privacy-first design

#### 6.2 User Settings Privacy
**File:** `user_settings.json`

**Checks:**
- [ ] **No sensitive data** - Are passwords/tokens stored?
- [ ] **Local storage only** - Data stays on user's machine?
- [ ] **Clear text OK** - Is encryption needed?

**Results:**
- ✅ **No sensitive data** - Good! Only UI preferences
- ✅ **Local only** - Good! Never transmitted
- ✅ **Clear text acceptable** - Good! No sensitive info

**Status:** ✅ SECURE

### 7. Error Handling & Information Disclosure

#### 7.1 Error Messages
**File:** Multiple locations with `except Exception as e:`

**Current Implementation:**
```python
except Exception as e:
    print(f"Error loading settings: {e}")
```

**Checks:**
- [ ] **Stack traces exposed** - Are full traces shown to user?
- [ ] **System paths revealed** - Do errors expose file paths?
- [ ] **Version info leaked** - Do errors reveal software versions?

**Potential Vulnerabilities:**
- ⚠️ **Console output** - Error messages print to console (visible if run from terminal)
- ⚠️ **Exception details** - Full exception message included
- ✅ **No user-facing errors** - Good! Fails gracefully, uses defaults

**Recommendations:**
1. Consider logging errors to file instead of console
2. Sanitize error messages in production (remove full exception text)
3. Add --debug flag for verbose error output

#### 7.2 Graceful Degradation
**File:** Multiple try/except blocks

**Checks:**
- [ ] **API failure** - Does app work offline?
- [ ] **PIL failure** - Does app work without Pillow?
- [ ] **Settings failure** - Does app work with corrupted settings?

**Results:**
- ✅ **Offline mode** - Good! Fallback quotes available
- ✅ **PIL optional** - Good! PIL_AVAILABLE flag
- ✅ **Settings resilient** - Good! Returns defaults on error

**Status:** ✅ SECURE - Excellent error handling

### 8. Windows Security Considerations

#### 8.1 Batch File Security
**File:** `LaunchQuote.bat`

**Checks:**
- [ ] **No command injection** - Are user inputs used?
- [ ] **Path validation** - Are paths properly quoted?
- [ ] **Privilege escalation** - Does script request admin?

**Need to review:** LaunchQuote.bat content

#### 8.2 Auto-Launch Security
**File:** Referenced in AUTO_LAUNCH_GUIDE.md

**Checks:**
- [ ] **Startup persistence** - Is mechanism documented?
- [ ] **User consent** - Is auto-launch opt-in?
- [ ] **Easy removal** - Can user disable easily?

**Need to review:** AUTO_LAUNCH_GUIDE.md content

## Security Requirements (MUST FIX before production)

### Critical (P0) - Must fix
1. ❌ **Input validation for API responses** - Add length limits and type checking
2. ❌ **Settings value validation** - Validate ranges and enums
3. ❌ **Dependency version pinning** - Pin exact versions in requirements.txt

### High (P1) - Should fix
4. ⚠️ **Atomic file writes** - Use atomic write pattern for settings
5. ⚠️ **Image size limits** - Add explicit bounds on gradient generation
6. ⚠️ **Error message sanitization** - Remove sensitive details from errors

### Medium (P2) - Consider fixing
7. ⚠️ **File permissions** - Document recommended permissions for user_settings.json
8. ⚠️ **Dependency hashing** - Consider pip --require-hashes
9. ⚠️ **Debug mode** - Add --debug flag for verbose errors

### Low (P3) - Nice to have
10. ℹ️ **Dependency scanning** - Add pip-audit to development workflow
11. ℹ️ **Code signing** - Sign .bat files (Windows)
12. ℹ️ **Security.md** - Add security policy to repository

## Remediation Plan

### Phase 1: Critical Fixes (P0)

**Fix 1: API Response Validation**
```python
def get_quote(self):
    # ... existing code ...
    if response.status_code == 200:
        data = response.json()
        quote_text = data.get("quote", "")
        author = data.get("author", "Unknown")

        # ADD VALIDATION:
        if not isinstance(quote_text, str) or not isinstance(author, str):
            continue  # Skip to next attempt

        if len(quote_text) > 1000 or len(author) > 100:
            continue  # Skip overly long quotes

        # ... rest of code ...
```

**Fix 2: Settings Validation**
```python
def load_settings(self):
    defaults = {
        "timerDuration": 15,
        "position": "bottomRight",
        "fontSize": "medium",
        "category": "motivation",
        "theme": "light"
    }

    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                saved = json.load(f)

                # ADD VALIDATION:
                validated = {}

                # Validate timerDuration
                if 'timerDuration' in saved:
                    timer = saved['timerDuration']
                    if isinstance(timer, (int, float)) and 5 <= timer <= 60:
                        validated['timerDuration'] = int(timer)

                # Validate position
                if 'position' in saved:
                    if saved['position'] in ['bottomRight', 'bottomLeft', 'topRight', 'topLeft']:
                        validated['position'] = saved['position']

                # Validate fontSize
                if 'fontSize' in saved:
                    if saved['fontSize'] in ['small', 'medium', 'large']:
                        validated['fontSize'] = saved['fontSize']

                # Validate category
                if 'category' in saved:
                    allowed_categories = ['motivation', 'learning', 'creativity', 'productivity', 'all']
                    if saved['category'] in allowed_categories:
                        validated['category'] = saved['category']

                # Validate theme
                if 'theme' in saved:
                    if saved['theme'] in ['light', 'dark']:
                        validated['theme'] = saved['theme']

                return {**defaults, **validated}
    except Exception as e:
        print(f"Error loading settings: {e}")

    return defaults
```

**Fix 3: Pin Dependencies**
```
# requirements.txt
requests==2.32.3
Pillow==11.0.0
```

### Phase 2: High Priority Fixes (P1)

**Fix 4: Atomic File Writes**
```python
import tempfile
import shutil

def save_settings(self):
    """Save settings to JSON file atomically"""
    try:
        # Write to temporary file first
        with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=os.path.dirname(SETTINGS_FILE)) as tmp:
            json.dump(self.settings, tmp, indent=2)
            tmp_path = tmp.name

        # Atomic rename
        shutil.move(tmp_path, SETTINGS_FILE)
    except Exception as e:
        print(f"Error saving settings: {e}")
        # Clean up temp file if it exists
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)
```

**Fix 5: Image Size Limits**
```python
def create_diagonal_gradient(width, height, color1, color2):
    """..."""
    if not PIL_AVAILABLE:
        return None

    # ADD SIZE VALIDATION:
    MAX_WIDTH = 1920
    MAX_HEIGHT = 1080

    if width > MAX_WIDTH or height > MAX_HEIGHT or width <= 0 or height <= 0:
        print(f"Warning: Invalid gradient size {width}x{height}, using fallback")
        return None

    # ... rest of code ...
```

**Fix 6: Sanitize Error Messages**
```python
# Add at top of file
DEBUG_MODE = '--debug' in sys.argv

# Update error handling
def load_settings(self):
    # ...
    except Exception as e:
        if DEBUG_MODE:
            print(f"Error loading settings: {e}")
        else:
            print("Error loading settings, using defaults")
    # ...
```

## Testing Plan

### Security Test Cases

1. **Malicious API Response**
   - Test with mock server returning huge JSON (10MB+)
   - Test with non-string values
   - Test with missing keys
   - Test with special characters (SQL injection attempts, XSS)

2. **Corrupted Settings File**
   - Test with invalid JSON
   - Test with out-of-range values
   - Test with wrong types
   - Test with extra keys

3. **File System Edge Cases**
   - Test with read-only settings file
   - Test with full disk
   - Test with concurrent writes
   - Test settings file deletion during runtime

4. **Network Edge Cases**
   - Test with no internet connection
   - Test with slow API (10+ second response)
   - Test with API timeout
   - Test with SSL certificate errors

5. **Resource Exhaustion**
   - Test with extremely long quote text
   - Test with rapid-fire settings changes
   - Test memory usage over 24 hours

## Compliance & Best Practices

### OWASP Top 10 (Desktop Application Context)

1. **Injection** - ✅ Protected (URL encoding, no SQL, no command injection)
2. **Broken Authentication** - N/A (no auth)
3. **Sensitive Data Exposure** - ✅ Protected (no sensitive data)
4. **XML External Entities** - N/A (no XML)
5. **Broken Access Control** - ✅ Protected (local app only)
6. **Security Misconfiguration** - ⚠️ Review (default file permissions)
7. **XSS** - ✅ Protected (no web rendering except browser search - properly encoded)
8. **Insecure Deserialization** - ⚠️ Review (JSON parsing without validation)
9. **Using Components with Known Vulnerabilities** - ⚠️ Review (dependency versions)
10. **Insufficient Logging & Monitoring** - ⚠️ Limited logging (acceptable for desktop app)

### CWE (Common Weakness Enumeration)

- **CWE-20** (Input Validation) - ⚠️ NEEDS FIX
- **CWE-78** (OS Command Injection) - ✅ SECURE
- **CWE-79** (XSS) - ✅ SECURE
- **CWE-89** (SQL Injection) - N/A
- **CWE-119** (Buffer Overflow) - ✅ SECURE (Python memory safe)
- **CWE-200** (Information Disclosure) - ✅ SECURE
- **CWE-22** (Path Traversal) - ✅ SECURE
- **CWE-352** (CSRF) - N/A
- **CWE-434** (File Upload) - N/A
- **CWE-502** (Deserialization) - ⚠️ NEEDS FIX (JSON validation)

## Success Criteria

- [ ] All P0 (Critical) issues resolved
- [ ] All P1 (High) issues resolved or documented as accepted risk
- [ ] Security testing completed with all tests passing
- [ ] No secrets or credentials in code
- [ ] Dependencies pinned to specific versions
- [ ] Input validation on all external data sources
- [ ] Error handling does not expose sensitive information
- [ ] Code passes automated security scanner (bandit)
- [ ] README includes security considerations section
- [ ] SECURITY.md file created with vulnerability reporting process

## Deliverables

1. **Remediated Code** - quote_overlay.py with all P0/P1 fixes applied
2. **Updated requirements.txt** - Pinned dependency versions
3. **Security Test Results** - Documentation of all test cases passed
4. **SECURITY.md** - Responsible disclosure policy
5. **README Security Section** - User-facing security documentation

## Next Steps

1. User reviews this PRD
2. Run automated security scanner (bandit):
   ```bash
   pip install bandit
   bandit -r quote_overlay.py
   ```
3. Implement P0 (Critical) fixes
4. Implement P1 (High) fixes
5. Run security test suite
6. Create SECURITY.md
7. Update README with security notes
8. Move to Code Cleanup PRD
