import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
import re
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("earth911_scraper.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_user_agent():
    """Return a common user agent string"""
    return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'

def make_request(url, max_attempts=3):
    """Make an HTTP request with retries"""
    headers = {
        'User-Agent': create_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    }
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()  # Raise exception for 4xx/5xx responses
            return response
        except Exception as e:
            logger.error(f"Error on attempt {attempt+1}/{max_attempts}: {e}")
            if attempt == max_attempts - 1:
                raise
            time.sleep(2)

def extract_facilities(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    facilities = []
    
    location_cards = soup.find_all('li', class_='result-item')
    logger.info(f"Found {len(location_cards)} result items")
    
    for card in location_cards:
        try:
            name_elem = card.select_one('h2.title a')
            name = name_elem.text.strip() if name_elem else "N/A"
            
            address_parts = []
            address_elems = card.select('div.contact p')
            for elem in address_elems:
                if elem.text.strip():
                    address_parts.append(elem.text.strip())
            address = ', '.join(address_parts) if address_parts else "N/A"
            
            materials_elem = card.select_one('p.result-materials')
            materials = []
            if materials_elem:
                for material in materials_elem.select('span.material'):
                    if material.text.strip() and not "more" in material.text:
                        materials.append(material.text.strip())
            
            materials_text = ", ".join(materials) if materials else "N/A"
            
            updated = "N/A"
            
            facility = {
                "Business Name": name,
                "Last Updated": updated,
                "Address": address,
                "Materials Accepted": materials_text
            }
            
            facilities.append(facility)
            logger.info(f"Added facility: {name}")
            
        except Exception as e:
            logger.error(f"Error extracting facility data: {e}")
    
    return facilities

def main():
    material = "Electronics"
    zipcode = "10001"
    radius = "100"
    
    logger.info(f"Searching for {material} recycling centers near {zipcode} within {radius} miles...")
    
    base_url = f"https://search.earth911.com/?what={material}&where={zipcode}&radius={radius}"
    
    try:
        response = make_request(base_url)
        logger.info("Successfully retrieved first page")
    except Exception as e:
        logger.error(f"Failed to retrieve search results: {e}")
        return
    
    all_facilities = extract_facilities(response.text)
    
    max_pages = 20  # Safety limit
    current_page = 1
    
    while current_page < max_pages:
        soup = BeautifulSoup(response.text, 'html.parser')
        next_page_link = soup.select_one('a.next')
        
        if not next_page_link:
            logger.info("No more pages available")
            break
        
        next_page_url = f"https://search.earth911.com{next_page_link['href']}" if next_page_link else None
        
        if not next_page_url:
            logger.info("No more pages to process")
            break
        
        current_page += 1
        logger.info(f"Getting page {current_page}: {next_page_url}")
        
        try:
            time.sleep(2)  # Be nice to their server
            response = make_request(next_page_url)
            
            facilities = extract_facilities(response.text)
            all_facilities.extend(facilities)
            
            logger.info(f"Retrieved page {current_page}, now have {len(all_facilities)} total facilities")
            
        except Exception as e:
            logger.error(f"Error retrieving page {current_page}: {e}")
            break
    
    if all_facilities:
        cleaned_facilities = []
        for facility in all_facilities:
            cleaned_facility = {}
            for key, value in facility.items():
                if isinstance(value, str):
                    cleaned_value = value.replace('ï»¿', '').strip()
                    cleaned_facility[key] = cleaned_value
                else:
                    cleaned_facility[key] = value
            cleaned_facilities.append(cleaned_facility)
        
        df = pd.DataFrame(cleaned_facilities)
        df.to_csv("earth911_data_clean.csv", index=False, encoding='utf-8')
        
        logger.info(f"Success! Scraped {len(all_facilities)} facilities across {current_page} pages")
        logger.info(f"Data saved to earth911_data_clean.csv")
    else:
        logger.error("No facilities found!")

if __name__ == "__main__":
    main()