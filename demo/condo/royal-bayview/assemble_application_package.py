#!/usr/bin/env python3
"""
Royal Bayview Application Package Assembler
Compile all materials into a comprehensive client application package.
"""

import os
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RoyalBayviewPackageAssembler:
    def __init__(self, artifacts_dir="output/artifacts", materials_dir="output/agent_materials",
                 presentation_dir="output/presentation", output_dir="output/final_package"):
        self.artifacts_dir = Path(artifacts_dir)
        self.materials_dir = Path(materials_dir)
        self.presentation_dir = Path(presentation_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_package_structure(self):
        """Create the final package directory structure"""
        logger.info("Creating final package structure...")

        structure = {
            "presentation": self.output_dir / "presentation",
            "media": self.output_dir / "media",
            "documents": self.output_dir / "documents",
            "marketing_materials": self.output_dir / "marketing_materials",
            "client_resources": self.output_dir / "client_resources",
            "agent_resources": self.output_dir / "agent_resources"
        }

        # Create directories
        for dir_path in structure.values():
            dir_path.mkdir(parents=True, exist_ok=True)

        return structure

    def assemble_presentation_materials(self, structure):
        """Assemble presentation materials"""
        logger.info("Assembling presentation materials...")

        assembled = 0

        # Copy HTML presentation
        html_file = self.presentation_dir / "royal_bayview_agent_presentation.html"
        if html_file.exists():
            shutil.copy2(html_file, structure["presentation"] / "Royal_Bayview_Presentation.html")
            assembled += 1

        # Copy PDF presentation
        pdf_file = self.presentation_dir / "royal_bayview_agent_presentation.pdf"
        if pdf_file.exists():
            shutil.copy2(pdf_file, structure["presentation"] / "Royal_Bayview_Presentation.pdf")
            assembled += 1

        return assembled

    def assemble_media_assets(self, structure):
        """Assemble media assets in organized categories"""
        logger.info("Assembling media assets...")

        assembled = 0

        # Copy organized media categories
        media_categories = ["hero_images", "interior_showcase", "amenities_gallery", "location_context", "videos"]
        for category in media_categories:
            src_dir = self.materials_dir / category
            dst_dir = structure["media"] / category.replace("_", "_").title()

            if src_dir.exists():
                dst_dir.mkdir(exist_ok=True)
                for file_path in src_dir.glob("*"):
                    if file_path.is_file():
                        shutil.copy2(file_path, dst_dir / file_path.name)
                        assembled += 1

        return assembled

    def assemble_documents(self, structure):
        """Assemble supporting documents"""
        logger.info("Assembling documents...")

        assembled = 0

        # Copy documents from materials
        src_docs = self.materials_dir / "documents"
        if src_docs.exists():
            for doc_file in src_docs.glob("*"):
                if doc_file.is_file():
                    shutil.copy2(doc_file, structure["documents"] / doc_file.name)
                    assembled += 1

        # Copy any additional documents from artifacts
        for json_file in self.artifacts_dir.glob("*.json"):
            if "report" in json_file.name.lower():
                shutil.copy2(json_file, structure["documents"] / f"Processing_{json_file.name}")
                assembled += 1

        return assembled

    def assemble_agent_instructions(self, structure):
        """Assemble agent instruction materials"""
        logger.info("Assembling agent instructions...")

        assembled = 0

        # Copy agent instructions file
        agent_instructions_file = Path("agent_instruction.md")
        if agent_instructions_file.exists():
            shutil.copy2(agent_instructions_file, structure["agent_resources"] / "Agent_Instructions.md")
            assembled += 1

        return assembled

    def generate_agent_website(self, structure):
        """Generate agent-centric website for presentations"""
        logger.info("Generating agent-centric website...")

        try:
            # Import the website generator
            import subprocess
            import sys

            # Run the website generator script
            result = subprocess.run([
                sys.executable, "generate_agent_website.py"
            ], capture_output=True, text=True, cwd=Path.cwd())

            if result.returncode == 0:
                logger.info("Website generation completed successfully")

                # Copy the generated website to the package
                website_source = Path("output/agent_website")
                website_target = structure["presentation"] / "agent_website"

                if website_source.exists():
                    # Copy the entire website directory
                    if website_target.exists():
                        shutil.rmtree(website_target)
                    shutil.copytree(website_source, website_target)

                    # Count files
                    website_files = list(website_target.rglob("*"))
                    logger.info(f"Copied {len(website_files)} website files to package")

                    return len(website_files)
                else:
                    logger.warning("Website source directory not found")
                    return 0
            else:
                logger.error(f"Website generation failed: {result.stderr}")
                return 0

        except Exception as e:
            logger.error(f"Error generating agent website: {e}")
            return 0

    def create_marketing_materials(self, structure):
        """Create marketing materials package"""
        logger.info("Creating marketing materials...")

        materials = []

        # Create a marketing summary document
        marketing_content = """# Royal Bayview Marketing Materials

## Key Selling Points
- Premium golf course living in prestigious Thornhill area
- Modern suite designs with high-end finishes
- Full amenity package including fitness center and concierge
- Excellent location with easy access to transportation

## Target Demographics
- Golf enthusiasts and active retirees
- Professionals seeking premium lifestyle
- Families looking for quality education district
- Investors interested in Thornhill real estate

## Competitive Advantages
- Direct golf course views and access
- Boutique building with personalized service
- High-quality construction and finishes
- Prime location in established neighborhood

## Pricing Strategy
- Competitive entry-level pricing
- Value-driven positioning
- Flexible payment options available

## Contact Information
- Sales Office: 416-661-7699
- Email: info@royalbayview.com
- Website: www.royalbayview.com
- Address: 1 Rean Drive, Thornhill, ON

---
*Prepared for Royal Bayview Sales Team*
"""

        marketing_file = structure["marketing_materials"] / "Marketing_Summary.md"
        with open(marketing_file, 'w', encoding='utf-8') as f:
            f.write(marketing_content)
        materials.append(marketing_file)

        return len(materials)

    def create_client_resources(self, structure):
        """Create client resource materials"""
        logger.info("Creating client resources...")

        resources = []

        # Create client questionnaire
        questionnaire_content = """# Royal Bayview Client Discovery Questionnaire

## Personal Information
- Full Name:
- Phone Number:
- Email Address:
- Current Address:

## Lifestyle Preferences
- Are you a golfer? (Yes/No/Interested in learning)
- What activities are important to you? (Fitness, social events, etc.)
- Do you entertain frequently? (Yes/No/Occasionally)

## Housing Requirements
- Preferred suite size: (1 bedroom / 2 bedroom / 3 bedroom)
- Must-have features:
- Nice-to-have features:
- Budget range:

## Timeline
- When are you looking to move?
- Are you currently renting or do you own?
- Any flexibility in timeline?

## Additional Questions
- Any specific concerns or requirements?
- Questions about the building or neighborhood?

## Contact Preferences
- Best way to reach you:
- Preferred communication times:
- Would you like virtual or in-person tours?

---
Thank you for your interest in Royal Bayview!
We will contact you within 24 hours to discuss your requirements.
"""

        questionnaire_file = structure["client_resources"] / "Client_Questionnaire.md"
        with open(questionnaire_file, 'w', encoding='utf-8') as f:
            f.write(questionnaire_content)
        resources.append(questionnaire_file)

        # Create neighborhood guide
        neighborhood_content = """# Thornhill Neighborhood Guide

## Location Highlights
- Prestigious Thornhill neighborhood in North York
- Easy access to Highway 407 and 404
- Close to Bayview Avenue shopping and dining
- Excellent public transportation options

## Education
- Top-rated public schools
- Proximity to York University
- Private school options available

## Shopping & Dining
- Bayview Village Shopping Centre
- Numerous restaurants and cafes
- Grocery stores and specialty shops
- Medical facilities nearby

## Recreation
- Royal Bayview Golf Course
- Multiple parks and green spaces
- Fitness centers and yoga studios
- Community centers with programs

## Transportation
- TTC subway access
- GO Train station nearby
- Major highway access
- Airport accessibility

---
*Royal Bayview - Where Luxury Meets Lifestyle*
"""

        neighborhood_file = structure["client_resources"] / "Neighborhood_Guide.md"
        with open(neighborhood_file, 'w', encoding='utf-8') as f:
            f.write(neighborhood_content)
        resources.append(neighborhood_file)

        return len(resources)

    def create_package_readme(self, structure, stats):
        """Create comprehensive package README"""
        logger.info("Creating package README...")

        readme_content = f"""# Royal Bayview Client Application Package

**Package Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Version**: 1.0
**Total Files**: {stats['total_files']}

## Package Overview

This comprehensive package contains all materials needed for Royal Bayview condo presentations and client consultations. The package is organized for easy navigation and professional delivery.

## Directory Structure

### 📊 Presentation (`presentation/`)
Professional presentation materials for client meetings:
- `Royal_Bayview_Presentation.html` - Interactive web presentation
- `Royal_Bayview_Presentation.pdf` - Print-ready PDF version

### 🖼️ Media (`media/`)
Organized visual assets by category:
- **Hero Images** - Golf course and building exterior shots
- **Interior Showcase** - Suite living spaces and finishes
- **Amenities Gallery** - Building facilities and services
- **Location Context** - Neighborhood and transportation
- **Videos** - Promotional and tour videos

### 📄 Documents (`documents/`)
Supporting documentation and reports:
- Building specifications and floor plans
- Processing reports and analysis summaries
- Legal and disclosure documents

### 📈 Marketing Materials (`marketing_materials/`)
Sales and marketing resources:
- `Marketing_Summary.md` - Key selling points and strategy
- Competitive analysis and positioning
- Target demographic information

### 👥 Client Resources (`client_resources/`)
Tools for client engagement:
- `Client_Questionnaire.md` - Discovery questions for consultations
- `Neighborhood_Guide.md` - Local area information and amenities

### 🎯 Agent Resources (`agent_resources/`)
Professional presentation guidance for real estate agents:
- `Agent_Instructions.md` - Comprehensive presentation guide and talking points
- Key selling strategies and objection handling
- Market intelligence and competitive positioning
- Consultation frameworks and closing strategies

## Usage Guidelines

### For Agent Presentations
1. Review Agent Instructions before client meetings
2. Start with the HTML presentation for interactive client meetings
3. Use organized media folders to customize presentations
4. Reference marketing materials for key selling points
5. Use client questionnaire to guide discovery conversations
6. Follow presentation flow and talking points from Agent Instructions

### For Digital Distribution
- Send HTML presentation link for virtual tours
- Share PDF version for email attachments
- Provide client resources for pre-appointment preparation

### For Print Materials
- Use high-resolution images from media folders
- Print PDF presentation for physical handouts
- Include neighborhood guide in welcome packages

## Package Statistics

- **Presentation Files**: {stats['presentation_files']}
- **Media Assets**: {stats['media_files']}
- **Documents**: {stats['document_files']}
- **Agent Resources**: {stats['agent_files']}
- **Marketing Materials**: {stats['marketing_files']}
- **Client Resources**: {stats['resource_files']}

## Contact Information

**Royal Bayview Sales Office**
- Phone: 416-661-7699
- Email: info@royalbayview.com
- Website: www.royalbayview.com
- Address: 1 Rean Drive, Thornhill, ON

**Sales Team**
- Contact agents directly for private showings
- Virtual tours available upon request
- Financing options and incentives discussed

## Technical Notes

- HTML presentation requires modern web browser
- PDF files are optimized for printing
- Images are in high-resolution format
- All materials are professionally organized and ready for use

## Version History

- **v1.0** (2025-11-16): Initial comprehensive package
  - Complete presentation materials
  - Organized media assets
  - Client engagement resources
  - Professional documentation

---
*Royal Bayview - Your Gateway to Golf Course Living*
*Prepared by AI-Powered Content Processing Pipeline*
"""

        readme_file = self.output_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)

        return readme_file

    def create_zip_archive(self):
        """Create a ZIP archive of the complete package"""
        logger.info("Creating ZIP archive...")

        zip_path = self.output_dir.parent / "Royal_Bayview_Client_Package.zip"

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in self.output_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(self.output_dir.parent)
                    zip_file.write(file_path, arcname)

        return zip_path

    def generate_package_report(self, structure, stats):
        """Generate comprehensive package assembly report"""
        logger.info("Generating package assembly report...")

        report = {
            "assembly_timestamp": datetime.now().isoformat(),
            "package_version": "1.0",
            "output_directory": str(self.output_dir),
            "source_directories": {
                "artifacts": str(self.artifacts_dir),
                "materials": str(self.materials_dir),
                "presentation": str(self.presentation_dir)
            },
            "package_statistics": stats,
            "directory_contents": {},
            "quality_checks": {
                "presentation_complete": stats['presentation_files'] >= 2,
                "media_organized": stats['media_files'] >= 5,
                "documentation_included": stats['document_files'] >= 1,
                "client_resources_created": stats['resource_files'] >= 2
            },
            "recommendations": [
                "Test HTML presentation in target browsers",
                "Verify all media links are working",
                "Customize contact information for specific agents",
                "Add client-specific notes before presentations",
                "Create backup copies of the package"
            ]
        }

        # Count files in each directory
        for name, path in structure.items():
            if path.exists():
                file_count = len(list(path.rglob('*')))
                report["directory_contents"][name] = file_count

        report_file = self.output_dir / "package_assembly_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)

        return report

def count_files_in_structure(structure):
    """Count files in the package structure"""
    stats = {
        "presentation_files": 0,
        "media_files": 0,
        "document_files": 0,
        "agent_files": 0,
        "website_files": 0,
        "marketing_files": 0,
        "resource_files": 0,
        "total_files": 0
    }

    # Count files in each category
    if "presentation" in structure and structure["presentation"].exists():
        stats["presentation_files"] = len(list(structure["presentation"].glob("*")))

    if "media" in structure and structure["media"].exists():
        stats["media_files"] = len(list(structure["media"].rglob("*")))

    if "documents" in structure and structure["documents"].exists():
        stats["document_files"] = len(list(structure["documents"].glob("*")))

    if "marketing_materials" in structure and structure["marketing_materials"].exists():
        stats["marketing_files"] = len(list(structure["marketing_materials"].glob("*")))

    if "client_resources" in structure and structure["client_resources"].exists():
        stats["resource_files"] = len(list(structure["client_resources"].glob("*")))

    if "agent_resources" in structure and structure["agent_resources"].exists():
        stats["agent_files"] = len(list(structure["agent_resources"].glob("*")))

    if "presentation" in structure and structure["presentation"].exists():
        website_dir = structure["presentation"] / "agent_website"
        if website_dir.exists():
            stats["website_files"] = len(list(website_dir.rglob("*")))

    stats["total_files"] = sum(stats.values())

    return stats

def main():
    """Main execution function"""
    try:
        assembler = RoyalBayviewPackageAssembler()

        # Create package structure
        structure = assembler.create_package_structure()

        # Assemble components
        presentation_count = assembler.assemble_presentation_materials(structure)
        media_count = assembler.assemble_media_assets(structure)
        document_count = assembler.assemble_documents(structure)
        agent_count = assembler.assemble_agent_instructions(structure)
        website_count = assembler.generate_agent_website(structure)
        marketing_count = assembler.create_marketing_materials(structure)
        resource_count = assembler.create_client_resources(structure)

        # Get final statistics
        stats = count_files_in_structure(structure)

        # Create README and report
        readme_file = assembler.create_package_readme(structure, stats)
        report = assembler.generate_package_report(structure, stats)

        # Create ZIP archive
        zip_path = assembler.create_zip_archive()

        print("="*80)
        print("ROYAL BAYVIEW APPLICATION PACKAGE ASSEMBLY COMPLETE")
        print("="*80)
        print(f"Output Directory: {assembler.output_dir}")
        print(f"ZIP Archive: {zip_path}")
        print()
        print("Package Contents:")
        print(f"  [DATA] Presentation Files: {stats['presentation_files']}")
        print(f"  [IMG] Media Assets: {stats['media_files']}")
        print(f"  [DOC] Documents: {stats['document_files']}")
        print(f"  [AGENT] Agent Resources: {stats['agent_files']}")
        print(f"  [WEB] Agent Website: {stats['website_files']}")
        print(f"  [MKT] Marketing Materials: {stats['marketing_files']}")
        print(f"  [CLIENT] Client Resources: {stats['resource_files']}")
        print(f"  [TOTAL] Total Files: {stats['total_files']}")
        print()
        print("Key Files Created:")
        print(f"  README: {readme_file.name}")
        print(f"  Report: package_assembly_report.json")
        print(f"  Archive: {zip_path.name} ({zip_path.stat().st_size} bytes)")
        print()
        print("Quality Checks:")
        quality_checks = report["quality_checks"]
        for check, passed in quality_checks.items():
            status = "[PASS]" if passed else "[FAIL]"
            print(f"  {status} {check.replace('_', ' ').title()}")
        print()
        print("Next Steps:")
        print("1. Test HTML presentation in web browser")
        print("2. Verify all media links are working")
        print("3. Customize contact information for agents")
        print("4. Distribute package to sales team")
        print("5. Schedule training on package usage")
        print("="*80)

    except Exception as e:
        logger.error(f"Package assembly failed: {e}")
        print(f"[ERROR] Package assembly failed: {e}")

if __name__ == "__main__":
    main()