#!/usr/bin/env python3
"""
Portfolio Static Site Generator CLI

A simple command-line tool to generate a static portfolio website from Markdown content.
"""

import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

import click
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Add src directory to path so we can import generator
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from generator import PortfolioGenerator


class PortfolioReloadHandler(FileSystemEventHandler):
    def __init__(self, generator):
        self.generator = generator
        self.last_build = 0

    def on_modified(self, event):
        if event.is_directory:
            return

        # Debounce rapid file changes
        now = time.time()
        if now - self.last_build < 1:
            return

        file_path = Path(event.src_path)

        # Only rebuild for content, template, or static file changes
        if any(
            str(file_path).startswith(str(self.generator.content_dir / path))
            for path in ["", "../templates", "../static"]
        ):
            click.echo(f"📝 File changed: {file_path}")
            try:
                self.generator.generate()
                self.last_build = now
            except Exception as e:
                click.echo(f"❌ Build failed: {e}", err=True)


@click.group()
def cli():
    """Portfolio Static Site Generator

    Generate a beautiful, minimalistic portfolio website from Markdown content.
    """


@cli.command()
@click.option("--content", default="content", help="Content directory path")
@click.option("--templates", default="templates", help="Templates directory path")
@click.option("--output", default="dist", help="Output directory path")
@click.option("--static", default="static", help="Static files directory path")
def build(content, templates, output, static):
    """Generate the static website"""
    try:
        generator = PortfolioGenerator(
            content_dir=content,
            templates_dir=templates,
            output_dir=output,
            static_dir=static,
        )
        generated_files = generator.generate()
        click.echo(f"🎉 Successfully built {len(generated_files)} pages!")

        # Show the generated files
        for file_path in generated_files:
            click.echo(f"   📄 {file_path}")

    except Exception as e:
        click.echo(f"❌ Build failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--content", default="content", help="Content directory path")
@click.option("--templates", default="templates", help="Templates directory path")
@click.option("--output", default="dist", help="Output directory path")
@click.option("--static", default="static", help="Static files directory path")
@click.option("--port", default=8000, help="Server port")
def serve(content, templates, output, static, port):
    """Build the site and serve it locally"""
    import http.server
    import socketserver
    import threading
    import webbrowser

    # First, build the site
    try:
        generator = PortfolioGenerator(
            content_dir=content,
            templates_dir=templates,
            output_dir=output,
            static_dir=static,
        )
        generator.generate()
        click.echo("🔨 Initial build complete")
    except Exception as e:
        click.echo(f"❌ Initial build failed: {e}", err=True)
        sys.exit(1)

    # Change to output directory for serving
    os.chdir(output)

    # Start the HTTP server in a separate thread
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        url = f"http://localhost:{port}"
        click.echo(f"🌐 Serving at {url}")
        click.echo("📝 Press Ctrl+C to stop")

        # Open browser
        webbrowser.open(url)

        try:
            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            click.echo("\n👋 Server stopped")


@cli.command()
@click.option("--content", default="content", help="Content directory path")
@click.option("--templates", default="templates", help="Templates directory path")
@click.option("--output", default="dist", help="Output directory path")
@click.option("--static", default="static", help="Static files directory path")
@click.option("--port", default=8000, help="Server port")
def dev(content, templates, output, static, port):
    """Development mode with auto-rebuild and live server"""
    import http.server
    import socketserver
    import threading
    import webbrowser

    # Initial build
    generator = PortfolioGenerator(
        content_dir=content,
        templates_dir=templates,
        output_dir=output,
        static_dir=static,
    )

    try:
        generator.generate()
        click.echo("🔨 Initial build complete")
    except Exception as e:
        click.echo(f"❌ Initial build failed: {e}", err=True)
        sys.exit(1)

    # Setup file watcher
    event_handler = PortfolioReloadHandler(generator)
    observer = Observer()
    observer.schedule(event_handler, content, recursive=True)
    observer.schedule(event_handler, templates, recursive=True)
    observer.schedule(event_handler, static, recursive=True)
    observer.start()

    click.echo("👀 Watching for file changes...")

    # Change to output directory for serving
    os.chdir(output)

    # Start HTTP server
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        url = f"http://localhost:{port}"
        click.echo(f"🌐 Development server running at {url}")
        click.echo("📝 Press Ctrl+C to stop")

        # Open browser
        webbrowser.open(url)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            click.echo("\n👋 Development server stopped")

    observer.join()


@cli.command()
def init():
    """Initialize a new portfolio project"""
    click.echo("🚀 Initializing new portfolio project...")

    # Create directory structure
    dirs = ["content", "templates", "static/css", "static/js", "src", "dist"]
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        click.echo(f"📁 Created {dir_name}/")

    # Create sample content file if it doesn't exist
    if not os.path.exists("content/index.md"):
        with open("content/index.md", "w") as f:
            f.write("""---
template: home.html
title: Home
order: 0
---

# Welcome to your portfolio

Edit this file to customize your homepage content.
""")
        click.echo("📄 Created content/index.md")

    # Create config file if it doesn't exist
    if not os.path.exists("content/config.yaml"):
        with open("content/config.yaml", "w") as f:
            f.write("""name: "Your Name"
initials: "yn"
title: "Your Title"
tagline: "Your tagline here"
description: "Your portfolio description"
year: "2024"

skills:
  - "Skill 1"
  - "Skill 2"
  - "Skill 3"

featured_work:
  - title: "Project 1"
    description: "Description of your first project"
    link: "https://example.com"
""")
        click.echo("⚙️  Created content/config.yaml")

    click.echo("✅ Portfolio project initialized!")
    click.echo("📝 Edit the files in content/ to customize your portfolio")
    click.echo("🔨 Run 'python cli.py build' to generate your site")


@cli.command()
@click.option("--port", default=8000, help="Port to kill processes on")
def kill_port(port):
    """Kill processes using the specified port"""
    click.echo(f"🔍 Looking for processes using port {port}...")

    system = platform.system().lower()

    try:
        if system == "windows":
            # Windows command
            result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
            lines = result.stdout.split("\n")
            pids = []

            for line in lines:
                if f":{port}" in line and "LISTENING" in line:
                    parts = line.split()
                    if parts:
                        pid = parts[-1]
                        pids.append(pid)

            if pids:
                for pid in pids:
                    subprocess.run(["taskkill", "/PID", pid, "/F"], capture_output=True)
                    click.echo(f"🔥 Killed process {pid}")
            else:
                click.echo(f"✅ No processes found using port {port}")

        else:
            # Unix-like systems (Linux, macOS)
            result = subprocess.run(
                ["lsof", "-ti", f":{port}"], capture_output=True, text=True
            )
            pids = result.stdout.strip().split("\n")

            if pids and pids[0]:
                for pid in pids:
                    if pid.strip():
                        subprocess.run(["kill", "-9", pid.strip()], capture_output=True)
                        click.echo(f"🔥 Killed process {pid.strip()}")
            else:
                click.echo(f"✅ No processes found using port {port}")

    except subprocess.CalledProcessError:
        click.echo(f"❌ Error finding processes on port {port}")
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
@click.option("--output", default="dist", help="Output directory to clean")
def clean(output):
    """Clean/delete the output directory"""
    output_path = Path(output)

    if output_path.exists():
        click.echo(f"🧹 Cleaning {output} directory...")
        try:
            shutil.rmtree(output_path)
            click.echo(f"✅ Successfully removed {output} directory")
        except Exception as e:
            click.echo(f"❌ Error removing directory: {e}")
    else:
        click.echo(f"✅ Directory {output} doesn't exist, nothing to clean")


@cli.command()
@click.option("--fix", is_flag=True, help="Automatically fix linting issues")
def lint(fix):
    """Run ruff linting on Python files"""
    try:
        cmd = ["ruff", "check", "."]
        if fix:
            cmd.append("--fix")
            click.echo("🔧 Running linter with auto-fix...")
        else:
            click.echo("🔍 Running linter...")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            if fix:
                click.echo("✅ All Python files fixed and pass linting")
            else:
                click.echo("✅ All Python files pass linting")
        else:
            if fix:
                click.echo("🔧 Fixed issues found:")
            else:
                click.echo("❌ Linting issues found:")
            click.echo(result.stdout)
            if result.stderr:
                click.echo(result.stderr)
    except FileNotFoundError:
        click.echo("❌ Ruff not found. Install with: pip install ruff")


@cli.command()
def format():
    """Format Python files with ruff"""
    try:
        result = subprocess.run(["ruff", "format", "."], capture_output=True, text=True)
        if result.returncode == 0:
            click.echo("✅ Python files formatted successfully")
        else:
            click.echo("❌ Formatting failed:")
            click.echo(result.stdout)
            if result.stderr:
                click.echo(result.stderr)
    except FileNotFoundError:
        click.echo("❌ Ruff not found. Install with: pip install ruff")


@cli.command()
def check():
    """Run both linting and formatting checks"""
    click.echo("🔍 Running linting...")
    lint.callback()

    click.echo("\n🎨 Running formatter...")
    format.callback()


if __name__ == "__main__":
    cli()
