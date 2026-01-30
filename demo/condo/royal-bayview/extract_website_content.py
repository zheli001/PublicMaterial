#!/usr/bin/env python3
"""
Royal Bayview Website Content Extractor
Uses Playwright to systematically browse and extract comprehensive content from Tridel's Royal Bayview website.
"""

import asyncio
import json
import os
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
from pathlib import Path
import requests
from playwright.async_api import async_playwright
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RoyalBayviewExtractor:
    def __init__(self, base_url="https://www.tridel.com/royalbayview/", output_dir="output"):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for different content types
        self.media_dir = self.output_dir / "media"
        self.media_dir.mkdir(exist_ok=True)
        self.docs_dir = self.output_dir / "documents"
        self.docs_dir.mkdir(exist_ok=True)

        # Track visited URLs and extracted content
        self.visited_urls = set()
        self.extracted_data = {
            "project_overview": "",
            "location_details": "",
            "amenities": [],
            "suite_features": [],
            "contact_info": {},
            "value_propositions": [],
            "media_assets": {
                "images": [],
                "videos": [],
                "documents": []
            },
            "pricing_floorplans": {
                "suite_types": [],
                "price_ranges": {},
                "availability": ""
            },
            "linked_content": [],
            "last_updated": datetime.now().isoformat(),
            "extraction_completeness": "in_progress"
        }

    async def extract_website_content(self):
        """Main extraction method using Playwright"""
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )

            try:
                # Start with main page
                await self.extract_main_page(context)

                # Extract linked content
                await self.extract_linked_content(context)

                # Extract media assets
                await self.extract_media_assets(context)

                # Extract documents and downloads
                await self.extract_documents(context)

                # Extract pricing and floor plans
                await self.extract_pricing_floorplans(context)

                # Mark extraction as complete
                self.extracted_data["extraction_completeness"] = "completed"

            finally:
                await browser.close()

    async def extract_main_page(self, context):
        """Extract content from the main page"""
        logger.info(f"Extracting main page: {self.base_url}")
        page = await context.new_page()

        try:
            await page.goto(self.base_url, wait_until='networkidle')
            await page.wait_for_timeout(2000)  # Wait for dynamic content

            # Extract project overview
            overview_selectors = [
                'h1', '.hero-title', '.project-title', '.main-title',
                '[class*="title"]', '[class*="headline"]', '.tagline'
            ]

            project_overview = ""
            for selector in overview_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    for element in elements:
                        text = await element.inner_text()
                        if text and len(text.strip()) > 10:
                            project_overview += text.strip() + " "
                except:
                    continue

            self.extracted_data["project_overview"] = project_overview.strip()

            # Extract contact information
            contact_selectors = [
                '.contact', '.phone', '[class*="phone"]', '[class*="contact"]',
                'a[href^="tel:"]', '.sales-info'
            ]

            contact_info = {}
            for selector in contact_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    for element in elements:
                        text = await element.inner_text()
                        if text:
                            # Extract phone numbers
                            phones = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
                            if phones:
                                contact_info["phone"] = phones[0]
                            contact_info["text"] = text.strip()
                except:
                    continue

            self.extracted_data["contact_info"] = contact_info

            # Extract value propositions
            value_props = []
            value_selectors = [
                '.value-prop', '.benefit', '.feature', '[class*="benefit"]',
                '.highlight', '.key-point', 'li', 'p'
            ]

            for selector in value_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    for element in elements:
                        text = await element.inner_text()
                        if text and len(text.strip()) > 20 and len(text.strip()) < 200:
                            value_props.append(text.strip())
                except:
                    continue

            self.extracted_data["value_propositions"] = list(set(value_props))[:10]  # Limit to 10 unique items

            # Get all links for further exploration
            links = await page.query_selector_all('a[href]')
            for link in links:
                href = await link.get_attribute('href')
                if href:
                    full_url = urljoin(self.base_url, href)
                    if self.is_internal_url(full_url):
                        self.extracted_data["linked_content"].append({
                            "url": full_url,
                            "text": await link.inner_text(),
                            "extracted": False
                        })

        except Exception as e:
            logger.error(f"Error extracting main page: {e}")
        finally:
            await page.close()

    async def extract_linked_content(self, context):
        """Extract content from linked pages"""
        logger.info("Extracting linked content...")

        # Define key pages to visit
        key_pages = [
            "/amenities",
            "/neighbourhood",
            "/prices-floorplans",
            "/floorplans",
            "/about",
            "/gallery",
            "/features",
            "/location",
            "/contact"
        ]

        for page_path in key_pages:
            url = urljoin(self.base_url, page_path)
            await self.extract_page_content(context, url)

        # Also visit links found on main page
        for link_info in self.extracted_data["linked_content"]:
            if not link_info["extracted"]:
                await self.extract_page_content(context, link_info["url"])
                link_info["extracted"] = True

    async def extract_page_content(self, context, url):
        """Extract content from a specific page"""
        if url in self.visited_urls:
            return

        logger.info(f"Extracting page: {url}")
        page = await context.new_page()

        try:
            await page.goto(url, wait_until='networkidle')
            await page.wait_for_timeout(1000)
            self.visited_urls.add(url)

            # Extract amenities
            amenity_selectors = [
                '.amenity', '.amenities', '[class*="amenit"]',
                '.feature', '.facility', 'li'
            ]

            for selector in amenity_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    for element in elements:
                        text = await element.inner_text()
                        if text and len(text.strip()) > 5 and text not in self.extracted_data["amenities"]:
                            self.extracted_data["amenities"].append(text.strip())
                except:
                    continue

            # Extract suite features
            if 'floorplan' in url.lower() or 'suite' in url.lower():
                feature_selectors = ['.feature', '.spec', '[class*="spec"]', 'li', 'p']
                for selector in feature_selectors:
                    try:
                        elements = await page.query_selector_all(selector)
                        for element in elements:
                            text = await element.inner_text()
                            if text and len(text.strip()) > 10:
                                self.extracted_data["suite_features"].append(text.strip())
                    except:
                        continue

            # Extract location details
            if 'location' in url.lower() or 'neighbourhood' in url.lower():
                location_text = await page.inner_text('body')
                self.extracted_data["location_details"] = location_text[:2000]  # Limit size

        except Exception as e:
            logger.error(f"Error extracting page {url}: {e}")
        finally:
            await page.close()

    async def extract_media_assets(self, context):
        """Extract images and videos from the website"""
        logger.info("Extracting media assets...")
        page = await context.new_page()

        try:
            await page.goto(self.base_url, wait_until='networkidle')
            await page.wait_for_timeout(2000)

            # Extract images
            images = await page.query_selector_all('img[src]')
            for img in images:
                src = await img.get_attribute('src')
                alt = await img.get_attribute('alt') or ""
                if src:
                    full_src = urljoin(self.base_url, src)
                    if self.is_valid_media_url(full_src):
                        self.extracted_data["media_assets"]["images"].append({
                            "url": full_src,
                            "alt": alt,
                            "category": self.categorize_image(alt, src)
                        })

            # Extract videos
            videos = await page.query_selector_all('video, [class*="video"], iframe[src*="youtube"], iframe[src*="vimeo"]')
            for video in videos:
                if await video.get_attribute('src'):
                    src = await video.get_attribute('src')
                    full_src = urljoin(self.base_url, src)
                    self.extracted_data["media_assets"]["videos"].append({
                        "url": full_src,
                        "type": "video"
                    })

        except Exception as e:
            logger.error(f"Error extracting media assets: {e}")
        finally:
            await page.close()

    async def extract_documents(self, context):
        """Extract PDF documents and downloads"""
        logger.info("Extracting documents...")
        page = await context.new_page()

        try:
            await page.goto(self.base_url, wait_until='networkidle')
            await page.wait_for_timeout(2000)

            # Find PDF links and downloads
            doc_links = await page.query_selector_all('a[href$=".pdf"], a[href*="download"], a[href*="brochure"]')
            for link in doc_links:
                href = await link.get_attribute('href')
                text = await link.inner_text()
                if href:
                    full_href = urljoin(self.base_url, href)
                    self.extracted_data["media_assets"]["documents"].append({
                        "url": full_href,
                        "title": text.strip(),
                        "type": "pdf"
                    })

        except Exception as e:
            logger.error(f"Error extracting documents: {e}")
        finally:
            await page.close()

    async def extract_pricing_floorplans(self, context):
        """Extract pricing and floor plan information"""
        logger.info("Extracting pricing and floor plans...")

        pricing_urls = [
            urljoin(self.base_url, "/prices-floorplans"),
            urljoin(self.base_url, "/floorplans"),
            urljoin(self.base_url, "/pricing")
        ]

        for url in pricing_urls:
            page = await context.new_page()
            try:
                await page.goto(url, wait_until='networkidle')
                await page.wait_for_timeout(2000)

                # Extract pricing information
                pricing_text = await page.inner_text('body')
                price_matches = re.findall(r'\$[\d,]+(?:\.\d{2})?', pricing_text)
                if price_matches:
                    self.extracted_data["pricing_floorplans"]["price_ranges"] = {
                        "found_prices": price_matches[:10]  # Limit to 10
                    }

                # Extract suite types
                suite_selectors = ['.suite-type', '.floorplan', '[class*="suite"]', '.unit-type']
                for selector in suite_selectors:
                    try:
                        elements = await page.query_selector_all(selector)
                        for element in elements:
                            text = await element.inner_text()
                            if text and len(text.strip()) > 5:
                                self.extracted_data["pricing_floorplans"]["suite_types"].append(text.strip())
                    except:
                        continue

            except Exception as e:
                logger.error(f"Error extracting pricing from {url}: {e}")
            finally:
                await page.close()

    def is_internal_url(self, url):
        """Check if URL belongs to the same domain"""
        try:
            parsed_base = urlparse(self.base_url)
            parsed_url = urlparse(url)
            return parsed_url.netloc == parsed_base.netloc
        except:
            return False

    def is_valid_media_url(self, url):
        """Check if URL points to a valid media file"""
        try:
            parsed = urlparse(url)
            path = parsed.path.lower()
            return any(ext in path for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'])
        except:
            return False

    def categorize_image(self, alt, src):
        """Categorize image based on alt text and URL"""
        text = (alt + " " + src).lower()
        if any(keyword in text for keyword in ['exterior', 'building', 'facade']):
            return 'exterior'
        elif any(keyword in text for keyword in ['interior', 'suite', 'living', 'kitchen', 'bedroom']):
            return 'interior'
        elif any(keyword in text for keyword in ['amenity', 'lobby', 'gym', 'pool', 'garden']):
            return 'amenities'
        elif any(keyword in text for keyword in ['location', 'neighborhood', 'map', 'golf']):
            return 'location'
        else:
            return 'general'

    def save_results(self):
        """Save extracted data to JSON file"""
        output_file = self.output_dir / "website_content_extraction.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.extracted_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Results saved to {output_file}")

        # Also save a human-readable summary
        summary_file = self.output_dir / "extraction_summary.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("# Royal Bayview Website Content Extraction Summary\n\n")
            f.write(f"**Extraction Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Website URL**: {self.base_url}\n\n")
            f.write(f"**Status**: {self.extracted_data['extraction_completeness']}\n\n")

            f.write("## Project Overview\n")
            f.write(self.extracted_data['project_overview'] or "No overview extracted\n\n")

            f.write("## Key Amenities\n")
            for amenity in self.extracted_data['amenities'][:10]:
                f.write(f"- {amenity}\n")
            f.write("\n")

            f.write("## Contact Information\n")
            contact = self.extracted_data['contact_info']
            if contact:
                f.write(f"- Phone: {contact.get('phone', 'Not found')}\n")
                f.write(f"- Details: {contact.get('text', '')}\n")
            f.write("\n")

            f.write("## Media Assets Found\n")
            f.write(f"- Images: {len(self.extracted_data['media_assets']['images'])}\n")
            f.write(f"- Videos: {len(self.extracted_data['media_assets']['videos'])}\n")
            f.write(f"- Documents: {len(self.extracted_data['media_assets']['documents'])}\n\n")

            f.write("## Value Propositions\n")
            for prop in self.extracted_data['value_propositions'][:5]:
                f.write(f"- {prop}\n")
            f.write("\n")

        logger.info(f"Summary saved to {summary_file}")

async def main():
    """Main execution function"""
    extractor = RoyalBayviewExtractor()
    logger.info("Starting Royal Bayview website content extraction...")

    try:
        await extractor.extract_website_content()
        extractor.save_results()
        logger.info("Website content extraction completed successfully!")
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())