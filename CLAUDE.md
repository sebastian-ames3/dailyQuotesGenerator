# Morning Motivation Quote Generator

## Project Overview
A simple, open-source web app that displays a random motivational quote when I log into my laptop. The quote should inspire learning, growth, and persistence. Displays in a corner pop-up and auto-closes after 15 seconds.

## Technical Approach
- **Single HTML file** with embedded JavaScript and CSS
- **Fetch quotes via API** (free quotes API - to be determined via sub-agent research)
- **Auto-launch on startup** (setup instructions for Windows)
- **Configurable auto-close timer** (15 seconds default, user-adjustable)
- **Interactive features** (hover-to-stay, click-to-search)

## Core Features (V1)
1. Fetch random motivational/wisdom/learning quote from API on page load
2. Display quote in clean corner pop-up (minimal/modern/professional design)
3. Auto-close after 15 seconds (configurable)
4. Hover to keep quote visible (timer pauses on hover)
5. Click quote to Google search it or link to source
6. Manual close button (X in corner)
7. Error handling if API fails (fallback to 10-15 hardcoded quotes)

## Success Criteria
- Opens automatically on every login
- Shows a different quote each time
- Clean, minimal, professional appearance
- Smooth interactions (hover, click, close)
- Works offline (fallback quotes)
- Well-documented for open source community

## Tech Stack
- **Frontend:** HTML5, CSS3, JavaScript (vanilla, no frameworks)
- **API:** Free quotes API (no authentication required)
- **Version Control:** Git + GitHub
- **License:** MIT (open source)
- **Platform:** Windows (primary), cross-platform compatible

## Development Workflow

### GitHub & Version Control
- All development on feature branches
- Pull Requests for all changes
- CHANGELOG.md maintained for every update
- Main branch always deployable

### Branch Naming Convention
- `feature/[feature-name]` - New features
- `fix/[bug-name]` - Bug fixes
- `docs/[doc-name]` - Documentation updates
- `research/[topic]` - Research and discovery

### Documentation
- **PRD.md** - Product Requirements Document (detailed specs)
- **CHANGELOG.md** - Version history and change tracking
- **README.md** - User-facing documentation
- **CLAUDE.md** - This file (development guide)

## Sub-Agent Strategy

To ensure high-quality development, Claude Code will use specialized sub-agents (AI agents) for research and development tasks:

### 1. API Research Agent
**Purpose:** Research and compare quote APIs
**Tasks:**
- Compare ZenQuotes, Quotable, Forismatic, API Ninjas, etc.
- Evaluate: rate limits, reliability, quote quality, CORS support, no-auth requirements
- Test API endpoints and response formats
- Recommend best option with backup API

### 2. UI/UX Research Agent
**Purpose:** Research best practices for pop-up notifications
**Tasks:**
- Corner placement conventions (least intrusive position)
- Toast/notification design patterns
- Animation best practices (fade, slide, scale)
- Timing studies (reading time for quotes)
- Accessibility guidelines for pop-ups

### 3. Quote Curation Agent
**Purpose:** Build fallback quote collection
**Tasks:**
- Compile 10-15 high-quality motivational quotes
- Focus on learning, growth, persistence themes
- Ensure proper attribution
- Verify quotes are public domain/permissible use

### 4. A/B Design Agent
**Purpose:** Create multiple design mockups
**Tasks:**
- Generate 2-3 CSS design variations
- Test different color schemes (minimal/modern/professional)
- Create different layouts (compact vs spacious)
- Propose animation styles

### 5. Auto-Launch Research Agent
**Purpose:** Research startup methods for Windows
**Tasks:**
- Windows Task Scheduler approach
- Startup folder method
- Registry options
- Compare pros/cons, recommend best method

## Development Phases

### Phase 1: Setup & Research ✓
- [x] Create PRD.md with detailed requirements
- [ ] Initialize git repository
- [ ] Create LICENSE (MIT)
- [ ] Create CHANGELOG.md
- [ ] Create/update README.md
- [ ] Set up GitHub repository
- [ ] Launch sub-agents for research

### Phase 2: Core Development
- [ ] Select quotes API based on research
- [ ] Build HTML structure
- [ ] Implement CSS styling (based on A/B test results)
- [ ] Implement JavaScript quote fetching
- [ ] Add timer and interaction logic
- [ ] Implement fallback quote system

### Phase 3: Polish & Testing
- [ ] Add animations and transitions
- [ ] Implement configuration options
- [ ] Test online/offline scenarios
- [ ] Cross-browser testing
- [ ] Accessibility testing

### Phase 4: Deployment & Launch
- [ ] Write comprehensive README
- [ ] Create auto-launch instructions for Windows
- [ ] Final testing
- [ ] Open source release on GitHub
- [ ] (Optional) GitHub Pages deployment

## Future Enhancements (V2)
- Quote history/favorites
- Category/theme customization
- Dark/light mode toggle
- Quote sharing functionality
- Multi-language support
- Browser extension version