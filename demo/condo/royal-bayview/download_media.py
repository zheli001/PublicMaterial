#!/usr/bin/env python3
"""
Royal Bayview Media Downloader
Downloads and organizes media files from the cataloged URLs.
Filters to keep only relevant Royal Bayview project content.
"""

import os
import json
import requests
from pathlib import Path
from urllib.parse import urlparse, unquote, urljoin
import logging
from datetime import datetime
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RoyalBayviewMediaDownloader:
    def __init__(self, json_file="output/website_content_extraction.json", output_dir="output"):
        self.json_file = Path(json_file)
        self.output_dir = Path(output_dir)
        self.media_dir = self.output_dir / "media"
        self.images_dir = self.media_dir / "images"
        self.videos_dir = self.media_dir / "videos"
        self.documents_dir = self.media_dir / "documents"
        self.pages_dir = self.media_dir / "pages"

        # Create directories
        for dir_path in [self.images_dir, self.videos_dir, self.documents_dir, self.pages_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Track downloaded files to avoid duplicates
        self.downloaded_files = set()

    def load_media_data(self):
        """Load media assets from the extraction JSON"""
        with open(self.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('media_assets', {})

    def is_relevant_image(self, url, alt, category):
        """Filter to keep only relevant Royal Bayview images"""
        # Skip generic Tridel logos and UI elements
        irrelevant_terms = [
            'tridel-logo', 'scroll-to-top', 'logo', 'icon',
            'microsite', 'general'
        ]

        url_lower = url.lower()
        alt_lower = (alt or '').lower()

        # Skip if URL or alt contains irrelevant terms
        for term in irrelevant_terms:
            if term in url_lower or term in alt_lower:
                return False

        # Keep images that are Royal Bayview specific
        relevant_terms = [
            'royal', 'bayview', 'suite', 'living', 'dining',
            'lobby', 'amenity', 'golf', 'course', 'aerial',
            'interior', 'exterior', 'location'
        ]

        for term in relevant_terms:
            if term in url_lower or term in alt_lower:
                return True

        return False

    def is_relevant_video(self, url):
        """Filter to keep only relevant Royal Bayview videos"""
        # For now, keep all videos as they're likely project-specific
        return 'royal' in url.lower() or 'bayview' in url.lower() or 'vimeo' in url.lower()

    def is_relevant_document(self, url, title):
        """Filter to keep only relevant Royal Bayview documents"""
        text = (url + ' ' + (title or '')).lower()
        return 'royal' in text or 'bayview' in text or 'pdf' in url.lower()

    def download_file(self, url, filename, folder):
        """Download a file from URL to specified folder"""
        if filename in self.downloaded_files:
            logger.info(f"Skipping duplicate: {filename}")
            return False

        try:
            logger.info(f"Downloading: {url}")
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()

            filepath = folder / filename
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            self.downloaded_files.add(filename)
            logger.info(f"Downloaded: {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to download {url}: {e}")
            return False

    def generate_filename(self, url, prefix="", extension=""):
        """Generate a clean filename from URL with proper extension handling"""
        parsed = urlparse(url)

        # Handle Contentful URLs with query parameters
        query_params = {}
        if parsed.query:
            for param in parsed.query.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    query_params[key] = value

        # Extract filename from URL path
        path = unquote(parsed.path)
        base_name = Path(path).stem

        # Determine extension
        if not extension:
            # Check for format in query parameters (Contentful)
            if 'fm' in query_params:
                extension = query_params['fm'].lower()
                # Map common formats
                if extension == 'jpg':
                    extension = 'jpg'
                elif extension in ['jpeg', 'png', 'gif', 'webp', 'svg']:
                    extension = extension
                else:
                    extension = 'jpg'  # default
            # Check URL path for extension
            elif '.' in path:
                extension = Path(path).suffix[1:].lower()
            else:
                extension = 'jpg'  # default

        # Clean filename and add prefix if provided
        clean_name = "".join(c for c in base_name if c.isalnum() or c in (' ', '-', '_')).rstrip()

        if prefix:
            clean_name = f"{prefix}_{clean_name}"

        return f"{clean_name}.{extension}"
        clean_name = "".join(c for c in base_name if c.isalnum() or c in (' ', '-', '_')).rstrip()

        if prefix:
            clean_name = f"{prefix}_{clean_name}"

        return f"{clean_name}.{extension}"

    def download_images(self, images_data):
        """Download relevant images"""
        logger.info("Downloading images...")
        downloaded = 0

        for i, img in enumerate(images_data):
            url = img.get('url', '')
            alt = img.get('alt', '')
            category = img.get('category', 'general')

            if self.is_relevant_image(url, alt, category):
                # Generate meaningful filename
                prefix = f"rb_{category}_{i+1:02d}"
                filename = self.generate_filename(url, prefix)

                if self.download_file(url, filename, self.images_dir):
                    downloaded += 1
            else:
                logger.info(f"Skipping irrelevant image: {alt}")

        return downloaded

    def download_videos(self, videos_data):
        """Download videos"""
        logger.info("Downloading videos...")
        downloaded = 0

        for i, video in enumerate(videos_data):
            url = video.get('url', '')

            if self.is_relevant_video(url):
                # For Vimeo videos, we might need to handle differently
                # For now, just try to download directly
                filename = f"rb_video_{i+1:02d}.mp4"
                if self.download_file(url, filename, self.videos_dir):
                    downloaded += 1

        return downloaded

    def download_documents(self, documents_data):
        """Download documents"""
        logger.info("Downloading documents...")
        downloaded = 0

        for i, doc in enumerate(documents_data):
            url = doc.get('url', '')
            title = doc.get('title', '')

            if self.is_relevant_document(url, title):
                filename = self.generate_filename(url, f"rb_doc_{i+1:02d}", "pdf")
                if self.download_file(url, filename, self.documents_dir):
                    downloaded += 1

        return downloaded

    def download_html_pages(self):
        """Download key HTML pages as complete web pages with local link resolution"""
        logger.info("Downloading key HTML pages with local link resolution...")

        # Key pages to download based on navigation
        key_pages = {
            "overview": "https://www.tridel.com/royalbayview/",
            "amenities": "https://www.tridel.com/royalbayview/amenities",
            "prices-floorplans": "https://www.tridel.com/royalbayview/prices-floorplans",
            "neighbourhood": "https://www.tridel.com/royalbayview/neighbourhood",
            "gallery": "https://www.tridel.com/royalbayview/gallery",
            "news": "https://www.tridel.com/royalbayview/news",
            "presentation-centre": "https://www.tridel.com/royalbayview/presentation-centre"
        }

        downloaded = 0
        for page_name, url in key_pages.items():
            try:
                logger.info(f"Downloading and processing HTML page: {page_name}")
                response = requests.get(url, timeout=30)
                response.raise_for_status()

                # Parse HTML and resolve links
                soup = BeautifulSoup(response.text, 'html.parser')
                base_url = url.rstrip('/')

                # Create subdirectory for this page's assets
                page_assets_dir = self.pages_dir / f"{page_name}_assets"
                page_assets_dir.mkdir(exist_ok=True)

                # Process different types of links
                assets_downloaded = self._resolve_and_download_assets(soup, base_url, page_assets_dir, page_name)

                # Update HTML links to point to local assets
                self._update_html_links(soup, page_assets_dir, page_name)

                # Save the modified HTML
                filename = f"rb_{page_name}.html"
                filepath = self.pages_dir / filename

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(soup))

                self.downloaded_files.add(filename)
                downloaded += 1
                logger.info(f"Saved HTML page with {assets_downloaded} local assets: {filepath}")

            except Exception as e:
                logger.error(f"Failed to download HTML page {page_name}: {e}")

        return downloaded

    def _resolve_and_download_assets(self, soup, base_url, assets_dir, page_name):
        """Download and resolve linked assets (images, CSS, JS)"""
        assets_downloaded = 0

        # Process images
        for img in soup.find_all('img', src=True):
            assets_downloaded += self._download_asset(img, 'src', base_url, assets_dir, page_name, 'images')

        # Process CSS links
        for link in soup.find_all('link', rel='stylesheet', href=True):
            assets_downloaded += self._download_asset(link, 'href', base_url, assets_dir, page_name, 'css')

        # Process JavaScript
        for script in soup.find_all('script', src=True):
            assets_downloaded += self._download_asset(script, 'src', base_url, assets_dir, page_name, 'js')

        # Process other linked resources
        for link in soup.find_all('link', href=True):
            if link.get('rel') not in ['stylesheet', 'canonical', 'icon', 'shortcut icon']:
                assets_downloaded += self._download_asset(link, 'href', base_url, assets_dir, page_name, 'assets')

        return assets_downloaded

    def _download_asset(self, element, attr, base_url, assets_dir, page_name, asset_type):
        """Download a single asset and return 1 if successful"""
        try:
            url = element[attr]
            if not url or url.startswith('data:') or url.startswith('#'):
                return 0

            # Convert relative URLs to absolute
            absolute_url = urljoin(base_url + '/', url)

            # Skip external domains (keep only tridel.com and related)
            parsed_url = urlparse(absolute_url)
            if not (parsed_url.netloc.endswith('tridel.com') or 'ctfassets.net' in parsed_url.netloc):
                return 0

            # Generate local filename
            url_path = unquote(parsed_url.path)
            filename = os.path.basename(url_path)
            if not filename:
                filename = f"{asset_type}_{hash(absolute_url) % 10000}.{self._get_extension_from_url(absolute_url)}"

            # Create asset type subdirectory
            asset_dir = assets_dir / asset_type
            asset_dir.mkdir(exist_ok=True)

            local_path = asset_dir / filename

            # Download the asset
            response = requests.get(absolute_url, timeout=30)
            response.raise_for_status()

            with open(local_path, 'wb') as f:
                f.write(response.content)

            # Update the element to point to local path
            relative_path = f"{page_name}_assets/{asset_type}/{filename}"
            element[attr] = relative_path

            self.downloaded_files.add(relative_path)
            return 1

        except Exception as e:
            logger.debug(f"Failed to download asset {url}: {e}")
            return 0

    def _get_extension_from_url(self, url):
        """Extract file extension from URL"""
        parsed = urlparse(url)
        path = unquote(parsed.path)
        if '.' in path:
            return path.split('.')[-1].lower()
        # Try to infer from query parameters (Contentful style)
        query = parsed.query
        if 'fm=' in query:
            format_param = query.split('fm=')[1].split('&')[0]
            return format_param.lower()
        return 'bin'

    def _update_html_links(self, soup, assets_dir, page_name):
        """Update any remaining links in HTML to point to local resources"""
        # Update any internal links to point to local HTML files
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('/royalbayview/'):
                # Convert to local HTML file reference
                page_part = href.split('/royalbayview/')[1].split('/')[0]
                if page_part in ['amenities', 'prices-floorplans', 'neighbourhood', 'gallery', 'news', 'presentation-centre']:
                    a['href'] = f"rb_{page_part}.html"
                elif href == '/royalbayview/' or href == '/royalbayview':
                    a['href'] = 'rb_overview.html'

    def download_videos_improved(self, videos_data):
        """Download videos with improved handling"""
        logger.info("Downloading videos with improved handling...")
        downloaded = 0

        for i, video in enumerate(videos_data):
            url = video.get('url', '')

            if self.is_relevant_video(url):
                try:
                    # For Vimeo videos, try to get the direct video URL
                    if 'vimeo.com' in url:
                        # Extract video ID from Vimeo URL
                        video_id = None
                        if 'player.vimeo.com/video/' in url:
                            video_id = url.split('player.vimeo.com/video/')[1].split('?')[0].split('/')[0]

                        if video_id:
                            # Try to get video info from Vimeo API (this might not work without auth)
                            # For now, just save the embed URL as reference
                            filename = f"rb_vimeo_video_{video_id}_embed.html"
                            embed_html = f"""
                            <!DOCTYPE html>
                            <html>
                            <head><title>Royal Bayview Video {video_id}</title></head>
                            <body>
                                <h2>Royal Bayview Video</h2>
                                <p>Original Vimeo URL: {url}</p>
                                <iframe src="{url}" width="640" height="360" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>
                            </body>
                            </html>
                            """

                            filepath = self.videos_dir / filename
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(embed_html)

                            self.downloaded_files.add(filename)
                            downloaded += 1
                            logger.info(f"Saved Vimeo embed: {filepath}")
                        else:
                            logger.warning(f"Could not extract video ID from: {url}")
                    else:
                        # For other video URLs, try direct download
                        filename = f"rb_video_{i+1:02d}.mp4"
                        if self.download_file(url, filename, self.videos_dir):
                            downloaded += 1

                except Exception as e:
                    logger.error(f"Error processing video {url}: {e}")

        return downloaded

    def create_inventory(self):
        """Create an inventory of all downloaded files"""
        logger.info("Creating inventory of downloaded files...")

        inventory = {
            "download_date": datetime.now().isoformat(),
            "total_files": len(self.downloaded_files),
            "images": [],
            "videos": [],
            "documents": [],
            "pages": []
        }

        # Inventory images
        for img_file in sorted(self.images_dir.glob("*")):
            if img_file.is_file():
                inventory["images"].append({
                    "filename": img_file.name,
                    "path": str(img_file),
                    "size": img_file.stat().st_size
                })

        # Inventory videos
        for vid_file in sorted(self.videos_dir.glob("*")):
            if vid_file.is_file():
                inventory["videos"].append({
                    "filename": vid_file.name,
                    "path": str(vid_file),
                    "size": vid_file.stat().st_size
                })

        # Inventory documents
        for doc_file in sorted(self.documents_dir.glob("*")):
            if doc_file.is_file():
                inventory["documents"].append({
                    "filename": doc_file.name,
                    "path": str(doc_file),
                    "size": doc_file.stat().st_size
                })

        # Inventory pages
        for page_file in sorted(self.pages_dir.glob("*")):
            if page_file.is_file():
                inventory["pages"].append({
                    "filename": page_file.name,
                    "path": str(page_file),
                    "size": page_file.stat().st_size
                })

        # Save inventory to JSON
        inventory_path = self.media_dir / "inventory.json"
        with open(inventory_path, 'w', encoding='utf-8') as f:
            json.dump(inventory, f, indent=2, ensure_ascii=False)

        logger.info(f"Inventory created with {inventory['total_files']} files")
        return inventory
        for vid_file in sorted(self.videos_dir.glob("*")):
            if vid_file.is_file():
                inventory["videos"].append({
                    "filename": vid_file.name,
                    "size_kb": round(vid_file.stat().st_size / 1024, 1),
                    "path": str(vid_file.relative_to(self.output_dir))
                })

        # Inventory documents
        for doc_file in sorted(self.documents_dir.glob("*")):
            if doc_file.is_file():
                inventory["documents"].append({
                    "filename": doc_file.name,
                    "size_kb": round(doc_file.stat().st_size / 1024, 1),
                    "path": str(doc_file.relative_to(self.output_dir))
                })

        # Save inventory
        inventory_file = self.media_dir / "media_inventory.json"
        with open(inventory_file, 'w', encoding='utf-8') as f:
            json.dump(inventory, f, indent=2, ensure_ascii=False)

        logger.info(f"Media inventory saved to {inventory_file}")
        return inventory

    def download_all_media(self):
        """Main method to download all media"""
        logger.info("Starting Royal Bayview media download...")

        # Load media data
        media_data = self.load_media_data()

        # Download each type
        images_downloaded = self.download_images(media_data.get('images', []))
        videos_downloaded = self.download_videos_improved(media_data.get('videos', []))
        documents_downloaded = self.download_documents(media_data.get('documents', []))
        pages_downloaded = self.download_html_pages()

        # Create inventory
        inventory = self.create_inventory()

        # Summary
        total_downloaded = images_downloaded + videos_downloaded + documents_downloaded + pages_downloaded

        logger.info("Media download completed!")
        logger.info(f"Images downloaded: {images_downloaded}")
        logger.info(f"Videos downloaded: {videos_downloaded}")
        logger.info(f"Documents downloaded: {documents_downloaded}")
        logger.info(f"HTML pages downloaded: {pages_downloaded}")
        logger.info(f"Total files: {total_downloaded}")

        return {
            "images": images_downloaded,
            "videos": videos_downloaded,
            "documents": documents_downloaded,
            "pages": pages_downloaded,
            "total": total_downloaded,
            "inventory": inventory
        }

def main():
    """Main execution function"""
    downloader = RoyalBayviewMediaDownloader()
    results = downloader.download_all_media()

    # Print summary
    print("\n" + "="*50)
    print("ROYAL BAYVIEW MEDIA DOWNLOAD SUMMARY")
    print("="*50)
    print(f"Images downloaded: {results['images']}")
    print(f"Videos downloaded: {results['videos']}")
    print(f"Documents downloaded: {results['documents']}")
    print(f"HTML pages downloaded: {results['pages']}")
    print(f"Total files: {results['total']}")
    print(f"Files saved to: {downloader.media_dir}")
    print("="*50)

if __name__ == "__main__":
    main()