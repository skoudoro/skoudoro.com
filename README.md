# 🌐 skoudoro.com

Personal portfolio website built with a custom static site generator.

## 📋 Overview

This is Serge Koudoro's personal website and portfolio showcasing projects, research, and professional experience. Built with a custom Python-based static site generator that converts Markdown content into a beautiful, responsive website.

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- pip package manager

### Installation

1. Clone the repository:

```bash
git clone https://github.com/skoudoro/skoudoro.com.git
cd skoudoro.com
```

2. Install dependencies:

```bash
cd portfolio
pip install -r requirements.txt
```

### 🛠️ Development

**Development server with live reload:**

```bash
cd portfolio
python cli.py dev
```

**Simple server (build once, then serve):**

```bash
cd portfolio
python cli.py serve
```

The website will be available at `http://localhost:8000`

**Use different port:**

```bash
python cli.py serve --port 3000
```

### 🏗️ Building

**Build the static site:**

```bash
cd portfolio
python cli.py build
```

**Clean build artifacts:**

```bash
python cli.py clean
```

**Code quality checks:**

```bash
python cli.py lint          # Check code quality
python cli.py lint --fix     # Fix issues automatically
python cli.py format         # Format code
python cli.py check          # Run both lint and format
```

**Utility commands:**

```bash
python cli.py kill-port --port 8000  # Kill processes on port
python cli.py init                    # Initialize new project
```

## 📁 Project Structure

```
skoudoro.com/
├── portfolio/                    # Main website source
│   ├── cli.py                   # Command-line interface
│   ├── src/
│   │   └── generator.py         # Core site generation logic
│   ├── content/                 # Markdown content files
│   │   ├── config.yaml          # Site configuration
│   │   ├── index.md             # Homepage
│   │   ├── about.md             # About page
│   │   ├── work.md              # Work/projects page
│   │   ├── contact.md           # Contact page
│   │   └── projects/            # Project detail pages
│   ├── templates/               # Jinja2 HTML templates
│   │   ├── base.html            # Base template
│   │   ├── home.html            # Homepage template
│   │   ├── page.html            # Generic page template
│   │   └── project.html         # Project detail template
│   ├── static/                  # Static assets
│   │   └── css/
│   │       └── main.css         # Stylesheet
│   ├── dist/                    # Generated website
│   ├── requirements.txt         # Python dependencies
│   └── pyproject.toml          # Ruff configuration
├── .pre-commit-config.yaml     # Pre-commit hooks
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
└── README.md                   # This file
```

## Analytics:

To see analytics, go to https://umami.futzs.com/

## 🤝 Contributing

This is a personal website, but suggestions and improvements are welcome through issues.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
