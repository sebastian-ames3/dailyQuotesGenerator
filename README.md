# Morning Motivation Quote Generator

> Start your day with inspiration. A simple, elegant web app that displays motivational quotes when you log into your computer.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## Overview

**Morning Motivation Quote Generator** is a lightweight, open-source web application that displays inspiring quotes about learning, growth, and persistence when you log into your computer. It's designed to foster a positive, motivated mindset at the start of your day.

### Key Features

- **Random Motivational Quotes** - Fetches fresh, inspiring quotes from a curated API
- **Clean Corner Pop-up** - Minimal, professional design that doesn't interrupt your workflow
- **Smart Auto-close** - Disappears after 15 seconds (configurable)
- **Hover to Keep** - Pause the timer by hovering over the quote
- **Click to Learn More** - Click the quote to search or explore its source
- **Offline Support** - Works without internet using fallback quotes
- **Auto-launch** - Opens automatically on system login
- **Zero Dependencies** - Pure HTML, CSS, and JavaScript

## Demo

<!-- TODO: Add screenshot/GIF here once UI is built -->

## Quick Start

### Installation

1. **Download the file:**

   ```bash
   git clone https://github.com/sebastian-ames3/dailyQuotesGenerator.git
   cd dailyQuotesGenerator
   ```

2. **Open `index.html` in your browser:**

   ```bash
   # Windows
   start index.html

   # Mac
   open index.html

   # Linux
   xdg-open index.html
   ```

3. **Set up auto-launch** (optional):
   See [Auto-Launch Instructions](#auto-launch-setup) below.

## Configuration

You can customize the quote display behavior by editing the configuration in `index.html`:

```javascript
// Example configuration (coming soon)
const config = {
  timerDuration: 15, // seconds
  position: 'bottom-right', // corner placement
  // ... more options
};
```

## Auto-Launch Setup

### Windows

<!-- TODO: Add Windows startup instructions after research -->

Coming soon - detailed instructions for auto-launching on Windows using Task Scheduler or Startup folder.

### macOS

<!-- TODO: Add macOS instructions if needed -->

### Linux

<!-- TODO: Add Linux instructions if needed -->

## Development

This project is actively developed with a focus on simplicity and user experience.

### Project Structure

```
dailyQuotesGenerator/
├── index.html          # Main application (coming soon)
├── README.md           # This file
├── PRD.md              # Product Requirements Document
├── CLAUDE.md           # Development guide
├── CHANGELOG.md        # Version history
├── LICENSE             # MIT License
└── .gitignore          # Git ignore rules
```

### Built With

- **HTML5** - Structure
- **CSS3** - Styling and animations
- **JavaScript (ES6+)** - Logic and API integration
- **Free Quotes API** - Quote source (TBD via research)

### Development Workflow

We use a structured development process:

1. **Feature branches** - All work done on dedicated branches
2. **Pull Requests** - All changes reviewed via PRs
3. **Documentation** - CHANGELOG.md updated for every change
4. **Sub-agents** - AI agents used for research and design decisions

See [CLAUDE.md](CLAUDE.md) for detailed development guidelines.

## Contributing

Contributions are welcome! Whether it's bug fixes, new features, or improvements to documentation.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [PRD.md](PRD.md) for details on our product requirements and [CLAUDE.md](CLAUDE.md) for development guidelines.

## Roadmap

### V1 (Current)

- [x] Project setup and documentation
- [ ] API research and selection
- [ ] Core HTML/CSS/JS implementation
- [ ] Offline fallback quotes
- [ ] Auto-launch instructions
- [ ] Initial release

### V2 (Future)

- [ ] Quote history/favorites
- [ ] Theme customization
- [ ] Dark/light mode
- [ ] Quote sharing
- [ ] Multi-language support
- [ ] Browser extension version

See the [CHANGELOG.md](CHANGELOG.md) for a detailed version history.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Quote APIs (TBD - research in progress)
- Inspired by the desire to start each day with purpose and motivation
- Built with Claude Code for efficient AI-assisted development

## Support

Found a bug? Have a suggestion?

- **Issues:** [GitHub Issues](https://github.com/sebastian-ames3/dailyQuotesGenerator/issues)
- **Discussions:** [GitHub Discussions](https://github.com/sebastian-ames3/dailyQuotesGenerator/discussions)

---

**Start your day inspired.** ⭐ Star this repo if you find it helpful!
