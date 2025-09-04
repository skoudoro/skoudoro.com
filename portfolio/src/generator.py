#!/usr/bin/env python3
import re
import shutil
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader


class PortfolioGenerator:
    def __init__(
        self,
        content_dir="content",
        templates_dir="templates",
        output_dir="dist",
        static_dir="static",
    ):
        self.content_dir = Path(content_dir)
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.static_dir = Path(static_dir)

        # Setup Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))

        # Setup Markdown processor
        self.md = markdown.Markdown(extensions=["meta", "codehilite", "toc"])

    def clean_output(self):
        """Clean the output directory"""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def copy_static_files(self):
        """Copy static files to output directory"""
        if self.static_dir.exists():
            shutil.copytree(
                self.static_dir, self.output_dir / "static", dirs_exist_ok=True
            )

    def load_config(self):
        """Load site configuration"""
        config_path = self.content_dir / "config.yaml"
        if config_path.exists():
            with open(config_path) as f:
                return yaml.safe_load(f)
        return {}

    def process_custom_directives(self, content):
        """Process custom directives and return content and extracted sections"""
        extracted = {}

        # Process [personal_work_intro]...[/personal_work_intro] blocks
        pattern = r"\[personal_work_intro\](.*?)\[/personal_work_intro\]"

        def extract_and_remove(match):
            inner_content = match.group(1).strip()
            # Convert the inner content to HTML using markdown
            temp_md = markdown.Markdown(extensions=["meta", "codehilite", "toc"])
            extracted["personal_work_intro"] = temp_md.convert(inner_content)
            return ""  # Remove the directive from the main content

        content = re.sub(pattern, extract_and_remove, content, flags=re.DOTALL)
        return content, extracted

    def process_markdown_file(self, file_path):
        """Process a markdown file and extract content and metadata"""
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Process custom directives first
        content, extracted = self.process_custom_directives(content)

        html = self.md.convert(content)
        meta = getattr(self.md, "Meta", {})

        # Reset markdown instance for next use
        self.md.reset()

        result = {
            "content": html,
            "meta": {k: v[0] if v else "" for k, v in meta.items()},
            "raw": content,
        }

        # Add extracted custom sections
        result.update(extracted)

        return result

    def get_pages(self):
        """Get all markdown pages from content directory"""
        pages = []
        if not self.content_dir.exists():
            return pages

        for md_file in self.content_dir.glob("*.md"):
            if md_file.name == "config.yaml":
                continue

            page_data = self.process_markdown_file(md_file)
            page_data["slug"] = md_file.stem
            page_data["filename"] = md_file.name
            pages.append(page_data)

        # Sort pages by order if specified in meta, otherwise by filename
        pages.sort(key=lambda x: int(x["meta"].get("order", 999)))
        return pages

    def generate_page(self, page_data, config, all_pages):
        """Generate a single HTML page"""
        template_name = page_data["meta"].get("template", "page.html")
        template = self.env.get_template(template_name)

        html = template.render(page=page_data, config=config, pages=all_pages)

        # Determine output filename
        if page_data["slug"] == "index":
            output_file = self.output_dir / "index.html"
        else:
            output_file = self.output_dir / f"{page_data['slug']}.html"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

        return output_file

    def generate_project_pages(self, config):
        """Generate project detail pages from personal_work in config"""
        generated_files = []

        if not config.get("personal_work"):
            return generated_files

        # Create projects directory
        projects_dir = self.output_dir / "projects"
        projects_dir.mkdir(exist_ok=True)

        # Check if project template exists, fallback to page template
        try:
            template = self.env.get_template("project.html")
        except Exception:
            template = self.env.get_template("page.html")

        for project in config["personal_work"]:
            if not project.get("slug"):
                continue

            # Create project content directory if it doesn't exist
            project_content_dir = self.content_dir / "projects"
            project_content_dir.mkdir(exist_ok=True)

            # Look for existing project markdown file
            project_md_file = project_content_dir / f"{project['slug']}.md"

            if project_md_file.exists():
                # Use existing markdown content
                project_data = self.process_markdown_file(project_md_file)
                project_content = project_data["content"]
                project_title = project_data["meta"].get("title", project["title"])
            else:
                # Generate basic content from config
                project_content = f"""
                <h1>{project["title"]}</h1>
                <p class="project-description">{project["description"]}</p>
                <div class="project-placeholder">
                    <p><em>This project page is automatically generated. To customize it, create a file at <code>content/projects/{project["slug"]}.md</code> with your project details.</em></p>
                </div>
                """
                project_title = project["title"]

            # Render project page
            html = template.render(
                page={"content": project_content, "meta": {"title": project_title}},
                config=config,
                project=project,
            )

            # Write project file
            project_file = projects_dir / f"{project['slug']}.html"
            with open(project_file, "w", encoding="utf-8") as f:
                f.write(html)

            generated_files.append(project_file)
            print(f"🚀 Generated project page: {project_file}")

        return generated_files

    def generate(self):
        """Generate the complete site"""
        print("🚀 Generating portfolio...")

        # Clean and setup output directory
        self.clean_output()

        # Copy static files
        self.copy_static_files()
        print("📁 Static files copied")

        # Load configuration
        config = self.load_config()

        # Get all pages
        pages = self.get_pages()
        print(f"📄 Found {len(pages)} pages")

        # Generate each page
        generated_files = []
        for page in pages:
            output_file = self.generate_page(page, config, pages)
            generated_files.append(output_file)
            print(f"✅ Generated {output_file}")

        # Generate project pages from config
        project_files = self.generate_project_pages(config)
        generated_files.extend(project_files)

        print(
            f"🎉 Portfolio generated successfully! {len(generated_files)} pages created in {self.output_dir}"
        )
        return generated_files


if __name__ == "__main__":
    generator = PortfolioGenerator()
    generator.generate()
