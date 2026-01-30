#!/usr/bin/env python3
"""
Royal Bayview Agent Presentation Materials Organizer
Clean up, modify and reorganize media files for agent presentation use.
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RoyalBayviewMediaOrganizer:
    def __init__(self, media_dir="output/media", artifacts_dir="output/artifacts", output_dir="output/agent_materials"):
        self.media_dir = Path(media_dir)
        self.artifacts_dir = Path(artifacts_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load media organization proposal
        self.organization_proposal = self._load_organization_proposal()

    def _load_organization_proposal(self):
        """Load the media organization proposal"""
        proposal_file = self.artifacts_dir / "media_organization_proposal.json"
        if proposal_file.exists():
            with open(proposal_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Default organization if proposal doesn't exist
            return {
                "presentation_images": {
                    "hero_images": ["golf_course_aerial.jpg", "building_exterior.jpg"],
                    "interior_showcase": ["suite_living_room.jpg", "suite_bedroom.jpg", "suite_kitchen.jpg"],
                    "amenities_gallery": ["lobby.jpg", "gym.jpg", "concierge.jpg"],
                    "location_context": ["neighborhood_map.jpg", "transportation.jpg"]
                },
                "thumbnails": "Create 300x200px thumbnails for gallery views",
                "high_res": "Keep original high-resolution images for printing",
                "videos": "Organize promotional videos for client presentations",
                "documents": "Clean PDF documents for distribution"
            }

    def analyze_current_media(self):
        """Analyze current media file organization"""
        logger.info("Analyzing current media organization...")

        analysis = {
            "total_files": 0,
            "by_type": {"images": 0, "videos": 0, "documents": 0, "pages": 0},
            "file_sizes": {},
            "duplicates": [],
            "issues": []
        }

        # Scan each media subdirectory
        for category in ["images", "videos", "documents", "pages"]:
            category_dir = self.media_dir / category
            if category_dir.exists():
                files = list(category_dir.glob("*"))
                analysis["by_type"][category] = len([f for f in files if f.is_file()])

                for file_path in files:
                    if file_path.is_file():
                        analysis["total_files"] += 1
                        size = file_path.stat().st_size
                        analysis["file_sizes"][str(file_path)] = size

                        # Check for potential duplicates (same name, different extensions)
                        name_without_ext = file_path.stem
                        if any(f for f in files if f != file_path and f.stem == name_without_ext):
                            analysis["duplicates"].append(str(file_path))

        # Check for issues
        if analysis["by_type"]["images"] == 0:
            analysis["issues"].append("No images found")
        if analysis["by_type"]["documents"] == 0:
            analysis["issues"].append("No documents found")

        return analysis

    def create_presentation_structure(self):
        """Create the organized presentation structure"""
        logger.info("Creating presentation structure...")

        structure = {
            "hero_images": self.output_dir / "hero_images",
            "interior_showcase": self.output_dir / "interior_showcase",
            "amenities_gallery": self.output_dir / "amenities_gallery",
            "location_context": self.output_dir / "location_context",
            "thumbnails": self.output_dir / "thumbnails",
            "videos": self.output_dir / "videos",
            "documents": self.output_dir / "documents",
            "presentation_assets": self.output_dir / "presentation_assets"
        }

        # Create directories
        for dir_path in structure.values():
            dir_path.mkdir(parents=True, exist_ok=True)

        return structure

    def organize_images_by_category(self, structure):
        """Organize images into presentation categories"""
        logger.info("Organizing images by category...")

        images_dir = self.media_dir / "images"
        if not images_dir.exists():
            logger.warning("Images directory not found")
            return 0

        organized = 0

        # Get all image files
        image_files = list(images_dir.glob("*"))
        image_files = [f for f in image_files if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']]

        for img_file in image_files:
            filename = img_file.name.lower()

            # Categorize based on filename content
            if any(keyword in filename for keyword in ['golf', 'course', 'aerial', 'exterior']):
                # Hero/location images
                shutil.copy2(img_file, structure["hero_images"] / img_file.name)
                organized += 1
            elif any(keyword in filename for keyword in ['interior', 'suite', 'living', 'bedroom', 'kitchen', 'bathroom']):
                # Interior showcase
                shutil.copy2(img_file, structure["interior_showcase"] / img_file.name)
                organized += 1
            elif any(keyword in filename for keyword in ['lobby', 'amenities', 'gym', 'pool', 'concierge']):
                # Amenities gallery
                shutil.copy2(img_file, structure["amenities_gallery"] / img_file.name)
                organized += 1
            elif any(keyword in filename for keyword in ['location', 'neighborhood', 'map', 'transportation']):
                # Location context
                shutil.copy2(img_file, structure["location_context"] / img_file.name)
                organized += 1
            else:
                # Default to hero images
                shutil.copy2(img_file, structure["hero_images"] / img_file.name)
                organized += 1

        return organized

    def organize_videos_and_documents(self, structure):
        """Organize videos and documents"""
        logger.info("Organizing videos and documents...")

        organized = 0

        # Copy videos
        videos_dir = self.media_dir / "videos"
        if videos_dir.exists():
            for video_file in videos_dir.glob("*"):
                if video_file.is_file():
                    shutil.copy2(video_file, structure["videos"] / video_file.name)
                    organized += 1

        # Copy documents
        documents_dir = self.media_dir / "documents"
        if documents_dir.exists():
            for doc_file in documents_dir.glob("*"):
                if doc_file.is_file():
                    shutil.copy2(doc_file, structure["documents"] / doc_file.name)
                    organized += 1

        return organized

    def create_thumbnails_placeholder(self, structure):
        """Create thumbnail placeholder information"""
        logger.info("Creating thumbnail organization info...")

        thumbnail_info = {
            "thumbnail_specs": {
                "size": "300x200px",
                "format": "JPEG",
                "quality": "85%",
                "purpose": "Gallery views and quick loading"
            },
            "source_images": list(structure["hero_images"].glob("*.jpg")),
            "recommendation": "Use image processing library (PIL/Pillow) to create thumbnails"
        }

        thumbnail_file = structure["thumbnails"] / "thumbnail_requirements.json"
        with open(thumbnail_file, 'w', encoding='utf-8') as f:
            json.dump(thumbnail_info, f, indent=2, default=str)

        return thumbnail_info

    def create_presentation_readme(self, structure, analysis):
        """Create a README for the organized materials"""
        logger.info("Creating presentation README...")

        readme_content = f"""# Royal Bayview Agent Presentation Materials

**Organized on**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Files**: {analysis['total_files']}
**Images**: {analysis['by_type']['images']}
**Videos**: {analysis['by_type']['videos']}
**Documents**: {analysis['by_type']['documents']}

## Directory Structure

### 📸 Hero Images (`hero_images/`)
High-impact images for presentation openings:
- Golf course aerial views
- Building exterior shots
- Key selling point visuals

### 🏠 Interior Showcase (`interior_showcase/`)
Suite interior photography:
- Living room, bedroom, kitchen views
- Quality finish examples
- Space utilization shots

### 🏢 Amenities Gallery (`amenities_gallery/`)
Building amenity photography:
- Lobby and common areas
- Fitness facilities
- Concierge and service areas

### 📍 Location Context (`location_context/`)
Location and neighborhood imagery:
- Maps and transportation
- Surrounding area highlights
- Lifestyle context images

### 🎬 Videos (`videos/`)
Promotional and informational videos:
- Property tours
- Neighborhood introductions
- Developer testimonials

### 📄 Documents (`documents/`)
Supporting documentation:
- Floor plans and specifications
- Building information
- Legal and disclosure documents

### 🖼️ Thumbnails (`thumbnails/`)
Optimized images for quick loading:
- 300x200px gallery thumbnails
- Web-optimized formats
- Fast presentation loading

## Usage Guidelines

### For Digital Presentations
1. Start with hero images for impact
2. Use interior showcase for suite visualization
3. Show amenities gallery to demonstrate value
4. Include location context for lifestyle appeal

### For Print Materials
- Use high-resolution images from original folders
- Ensure 300 DPI minimum for professional printing
- Consider color correction for different media

### File Naming Convention
- Descriptive names (e.g., `golf_course_aerial.jpg`)
- Consistent formatting
- Professional presentation

## Technical Notes

- All images are in original high-resolution format
- Videos are in original format (may need conversion for web use)
- Documents are preserved in original PDF format
- Thumbnails need to be generated separately for web optimization

## Next Steps

1. Review organized materials in each category
2. Generate thumbnails for web presentations
3. Test presentation flow with organized assets
4. Customize file names if needed for specific presentations
5. Create backup copies of organized materials

---
*Prepared for Royal Bayview real estate agents*
*Contact: 416-661-7699*
"""

        readme_file = self.output_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)

        return readme_file

    def generate_organization_report(self, analysis, structure, organized_images, organized_other):
        """Generate a comprehensive organization report"""
        logger.info("Generating organization report...")

        report = {
            "organization_timestamp": datetime.now().isoformat(),
            "source_media_dir": str(self.media_dir),
            "output_dir": str(self.output_dir),
            "original_analysis": analysis,
            "organization_results": {
                "images_organized": organized_images,
                "videos_documents_organized": organized_other,
                "total_organized": organized_images + organized_other
            },
            "directory_structure": {name: str(path) for name, path in structure.items()},
            "thumbnails_info": "Requirements documented in thumbnails/thumbnail_requirements.json",
            "recommendations": [
                "Review organized images in each category",
                "Generate thumbnails for web presentations",
                "Test presentation flow with new organization",
                "Create backup copies of organized materials",
                "Customize filenames for specific agent needs"
            ]
        }

        report_file = self.output_dir / "organization_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)

        return report

def main():
    """Main execution function"""
    try:
        organizer = RoyalBayviewMediaOrganizer()

        # Analyze current media
        analysis = organizer.analyze_current_media()

        # Create presentation structure
        structure = organizer.create_presentation_structure()

        # Organize images
        organized_images = organizer.organize_images_by_category(structure)

        # Organize videos and documents
        organized_other = organizer.organize_videos_and_documents(structure)

        # Create thumbnails info
        thumbnail_info = organizer.create_thumbnails_placeholder(structure)

        # Create README
        readme_file = organizer.create_presentation_readme(structure, analysis)

        # Generate report
        report = organizer.generate_organization_report(analysis, structure, organized_images, organized_other)

        print("="*70)
        print("ROYAL BAYVIEW MEDIA ORGANIZATION COMPLETE")
        print("="*70)
        print(f"Output Directory: {organizer.output_dir}")
        print(f"Images Organized: {organized_images}")
        print(f"Videos/Documents: {organized_other}")
        print(f"Total Organized: {organized_images + organized_other}")
        print()
        print("Created Directories:")
        for name, path in structure.items():
            file_count = len(list(path.glob("*"))) if path.exists() else 0
            print(f"  {name}: {file_count} files")
        print()
        print("Key Files:")
        print(f"  README: {readme_file.name}")
        print(f"  Report: organization_report.json")
        print()
        if analysis["issues"]:
            print("Issues Found:")
            for issue in analysis["issues"]:
                print(f"  - {issue}")
        print()
        print("Next Steps:")
        print("1. Review organized materials in each category")
        print("2. Generate thumbnails for web presentations")
        print("3. Test with the HTML presentation file")
        print("4. Proceed to final package assembly")
        print("="*70)

    except Exception as e:
        logger.error(f"Organization failed: {e}")
        print(f"❌ Organization failed: {e}")

if __name__ == "__main__":
    main()