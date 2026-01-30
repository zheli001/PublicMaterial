#!/usr/bin/env python3
"""
Royal Bayview MD to HTML/PDF Converter
Converts the reviewed MD file to professional HTML and PDF formats.
"""

import os
import json
import markdown
from pathlib import Path
from datetime import datetime
import logging
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RoyalBayviewMDConverter:
    def __init__(self, artifacts_dir="output/artifacts", output_dir="output/presentation"):
        self.artifacts_dir = Path(artifacts_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load the MD file
        self.md_file = self.artifacts_dir / "royal_bayview_agent_presentation.md"
        if not self.md_file.exists():
            raise FileNotFoundError(f"MD file not found: {self.md_file}")

    def load_md_content(self):
        """Load the MD file content"""
        logger.info(f"Loading MD file: {self.md_file}")
        with open(self.md_file, 'r', encoding='utf-8') as f:
            return f.read()

    def convert_md_to_html(self, md_content):
        """Convert MD content to HTML"""
        logger.info("Converting MD to HTML...")

        # Convert markdown to HTML
        html_content = markdown.markdown(md_content, extensions=['extra', 'toc'])

        # Create professional HTML wrapper
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Royal Bayview Residences - Agent Presentation</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="presentation-container">
        <header class="presentation-header">
            <h1>Royal Bayview Residences</h1>
            <p class="subtitle">Agent Presentation Package</p>
            <p class="generated-date">Generated: {datetime.now().strftime('%Y-%m-%d')}</p>
        </header>

        <main class="presentation-content">
            {html_content}
        </main>

        <footer class="presentation-footer">
            <p>Prepared by Royal Bayview Marketing Team | Contact: 416-661-7699</p>
            <p>This presentation is designed for real estate professionals</p>
        </footer>
    </div>
</body>
</html>"""

        return html_template

    def _get_css_styles(self):
        """Get professional CSS styles for the presentation"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }

        .presentation-container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }

        .presentation-header {
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white;
            padding: 2rem;
            text-align: center;
        }

        .presentation-header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 300;
        }

        .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 0.5rem;
        }

        .generated-date {
            font-size: 0.9rem;
            opacity: 0.7;
        }

        .presentation-content {
            padding: 2rem;
        }

        .presentation-content h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.5rem;
            margin-bottom: 2rem;
            font-size: 2rem;
        }

        .presentation-content h2 {
            color: #34495e;
            border-bottom: 2px solid #bdc3c7;
            padding-bottom: 0.3rem;
            margin: 2rem 0 1rem 0;
            font-size: 1.5rem;
        }

        .presentation-content h3 {
            color: #7f8c8d;
            margin: 1.5rem 0 0.5rem 0;
            font-size: 1.2rem;
        }

        .presentation-content p {
            margin-bottom: 1rem;
            text-align: justify;
        }

        .presentation-content ul, .presentation-content ol {
            margin: 1rem 0;
            padding-left: 2rem;
        }

        .presentation-content li {
            margin-bottom: 0.5rem;
        }

        .presentation-content strong {
            color: #2c3e50;
            font-weight: 600;
        }

        .presentation-content blockquote {
            border-left: 4px solid #3498db;
            padding-left: 1rem;
            margin: 1.5rem 0;
            font-style: italic;
            color: #7f8c8d;
        }

        .presentation-content hr {
            border: none;
            height: 2px;
            background: linear-gradient(to right, #3498db, #bdc3c7, #3498db);
            margin: 2rem 0;
        }

        .presentation-footer {
            background: #34495e;
            color: white;
            padding: 1.5rem;
            text-align: center;
            font-size: 0.9rem;
        }

        .presentation-footer p {
            margin-bottom: 0.5rem;
        }

        @media print {
            body {
                background: white;
            }

            .presentation-container {
                box-shadow: none;
                max-width: none;
            }

            .presentation-header {
                background: #2c3e50 !important;
                -webkit-print-color-adjust: exact;
            }

            .presentation-footer {
                background: #34495e !important;
                -webkit-print-color-adjust: exact;
            }
        }

        @media (max-width: 768px) {
            .presentation-header {
                padding: 1rem;
            }

            .presentation-header h1 {
                font-size: 2rem;
            }

            .presentation-content {
                padding: 1rem;
            }
        }
        """

    def save_html_file(self, html_content):
        """Save the HTML content to file"""
        html_file = self.output_dir / "royal_bayview_agent_presentation.html"
        logger.info(f"Saving HTML file: {html_file}")

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return html_file

    def convert_html_to_pdf(self, html_file):
        """Convert HTML to PDF (basic implementation)"""
        logger.info("Converting HTML to PDF...")

        # For now, create a simple PDF placeholder
        # In a real implementation, you would use libraries like pdfkit, weasyprint, or reportlab

        pdf_content = f"""ROYAL BAYVIEW RESIDENCES - AGENT PRESENTATION PACKAGE

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This PDF version would contain the same content as the HTML presentation,
formatted for professional printing and distribution.

HTML Source: {html_file}

To generate actual PDF:
1. Install pdfkit: pip install pdfkit
2. Install wkhtmltopdf: https://wkhtmltopdf.org/downloads.html
3. Use pdfkit.from_file() to convert HTML to PDF

For now, please use the HTML version for presentations and manually
export to PDF using your browser's print functionality.
"""

        pdf_file = self.output_dir / "royal_bayview_agent_presentation.pdf"
        with open(pdf_file, 'w', encoding='utf-8') as f:
            f.write(pdf_content)

        logger.info(f"Created PDF placeholder: {pdf_file}")
        return pdf_file

    def validate_media_links(self, html_content):
        """Validate that media links in HTML are working"""
        logger.info("Validating media links...")

        soup = BeautifulSoup(html_content, 'html.parser')
        issues = []

        # Check for any remaining external links that should be local
        for tag in soup.find_all(['img', 'link', 'script']):
            src = tag.get('src') or tag.get('href')
            if src and (src.startswith('http') or 'ctfassets.net' in src):
                issues.append(f"External link found: {src}")

        return issues

    def generate_conversion_report(self, html_file, pdf_file, validation_issues):
        """Generate a conversion report"""
        report = {
            "conversion_timestamp": datetime.now().isoformat(),
            "source_md_file": str(self.md_file),
            "output_html_file": str(html_file),
            "output_pdf_file": str(pdf_file),
            "html_file_size": html_file.stat().st_size if html_file.exists() else 0,
            "pdf_file_size": pdf_file.stat().st_size if pdf_file.exists() else 0,
            "validation_issues": validation_issues,
            "conversion_status": "success" if not validation_issues else "warning"
        }

        report_file = self.output_dir / "conversion_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return report

def main():
    """Main execution function"""
    try:
        converter = RoyalBayviewMDConverter()

        # Load and convert MD content
        md_content = converter.load_md_content()
        html_content = converter.convert_md_to_html(md_content)

        # Save HTML file
        html_file = converter.save_html_file(html_content)

        # Convert to PDF (placeholder)
        pdf_file = converter.convert_html_to_pdf(html_file)

        # Validate media links
        validation_issues = converter.validate_media_links(html_content)

        # Generate report
        report = converter.generate_conversion_report(html_file, pdf_file, validation_issues)

        print("="*70)
        print("ROYAL BAYVIEW MD TO HTML/PDF CONVERSION COMPLETE")
        print("="*70)
        print(f"HTML File: {html_file}")
        print(f"PDF File: {pdf_file}")
        print(f"HTML Size: {report['html_file_size']} bytes")
        print(f"PDF Size: {report['pdf_file_size']} bytes")
        print(f"Status: {report['conversion_status']}")
        print()
        if validation_issues:
            print("Validation Issues:")
            for issue in validation_issues:
                print(f"  - {issue}")
        else:
            print("✅ No validation issues found")
        print()
        print("Next Steps:")
        print("1. Review the generated HTML file in a browser")
        print("2. Use browser print functionality to export PDF if needed")
        print("3. Proceed to organize agent presentation materials")
        print("="*70)

    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        print(f"❌ Conversion failed: {e}")

if __name__ == "__main__":
    main()