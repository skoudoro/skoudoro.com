# Portfolio Static Site Generator

A minimalistic portfolio website generator built with Python, Jinja2, and Markdown. Create beautiful, responsive portfolio sites with clean design and easy content management.

## Features

- 🎨 **Minimalistic Design**: Clean, elegant aesthetics inspired by modern portfolio sites
- 📝 **Markdown Content**: Write your content in Markdown for easy editing
- 🔧 **Jinja2 Templates**: Flexible templating system for customization
- 🚀 **Simple CLI**: Easy-to-use command-line interface
- 📱 **Responsive**: Mobile-friendly design that works on all devices
- ⚡ **Fast**: Static site generation for optimal performance
- 🔄 **Live Reload**: Development server with auto-refresh
- 🌐 **GitHub Pages**: Ready-to-deploy with GitHub Actions

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Your Site

```bash
python cli.py build
```

### 3. Preview Locally

```bash
python cli.py serve
```

Your site will be available at `http://localhost:8000`

## CLI Commands

### `build`

Generate the static website:

```bash
python cli.py build [OPTIONS]
```

Options:

- `--content`: Content directory (default: content)
- `--templates`: Templates directory (default: templates)
- `--output`: Output directory (default: dist)
- `--static`: Static files directory (default: static)

### `serve`

Build and serve the site locally:

```bash
python cli.py serve [OPTIONS]
```

Additional options:

- `--port`: Server port (default: 8000)

### `dev`

Development mode with auto-rebuild:

```bash
python cli.py dev [OPTIONS]
```

Watches for changes in content, templates, and static files, automatically rebuilding the site.

### `init`

Initialize a new portfolio project:

```bash
python cli.py init
```

## Project Structure

```
portfolio/
├── content/           # Markdown content files
│   ├── config.yaml   # Site configuration
│   ├── index.md      # Homepage content
│   ├── about.md      # About page
│   ├── work.md       # Work/projects page
│   └── contact.md    # Contact page
├── templates/         # Jinja2 templates
│   ├── base.html     # Base template
│   ├── home.html     # Homepage template
│   └── page.html     # Default page template
├── static/           # Static assets
│   └── css/
│       └── main.css  # Stylesheets
├── src/              # Source code
│   └── generator.py  # Site generator
├── dist/             # Generated site (output)
├── cli.py            # Command-line interface
└── requirements.txt  # Python dependencies
```

## Content Management

### Configuration

Edit `content/config.yaml` to customize your site:

```yaml
name: "Your Name"
initials: "yn"
title: "Your Title"
tagline: "Your tagline"
description: "Site description"
year: "2024"

skills:
  - "Skill 1"
  - "Skill 2"

featured_work:
  - title: "Project Name"
    description: "Project description"
    link: "https://project-url.com"
```

### Pages

Create Markdown files in the `content/` directory:

```markdown
---
title: Page Title
order: 1
template: page.html
---

# Your Content Here

Write your page content in Markdown.
```

### Frontmatter Options

- `title`: Page title
- `order`: Sort order for navigation
- `template`: Template to use (defaults to page.html)
- `date`: Publication date
- `subtitle`: Page subtitle

## Customization

### Templates

Modify templates in `templates/` directory:

- `base.html`: Main layout template
- `home.html`: Homepage template
- `page.html`: Default page template

### Styling

Customize the design by editing `static/css/main.css`. The CSS uses CSS custom properties for easy theming.

### Adding Pages

1. Create a new Markdown file in `content/`
2. Add frontmatter with title and order
3. Add content in Markdown format
4. The page will automatically appear in navigation

## Deployment

### GitHub Pages

1. Push your portfolio to a GitHub repository
2. Enable GitHub Pages in repository settings
3. The included GitHub Action will automatically build and deploy your site

### Manual Deployment

1. Run `python cli.py build`
2. Upload the `dist/` folder contents to your web server

## Design Philosophy

This portfolio generator follows minimalistic design principles:

- **Typography**: Combination of monospace and serif fonts for character
- **Color Palette**: Neutral grays with high contrast for readability  
- **Layout**: Single-column, centered design with strategic whitespace
- **Navigation**: Simple, unobtrusive navigation
- **Responsive**: Mobile-first approach with clean breakpoints

## Contributing

Feel free to contribute by:

- Adding new templates
- Improving the CLI interface
- Enhancing the build system
- Adding new features

## License

MIT License - feel free to use this for your own portfolio!
