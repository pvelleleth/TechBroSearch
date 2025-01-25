import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from crawl4ai import Crawler
import cohere
import os
from typing import List, Dict
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Initialize clients
mongo_client = AsyncIOMotorClient(os.getenv('MONGODB_URI'))
db = mongo_client['People']  # Replace with your database name
co = cohere.Client(os.getenv('COHERE_API_KEY'))
crawler = Crawler()

async def scrape_url(url: str) -> str:
    """Scrape a URL and return its text content."""
    try:
        # Use crawl4ai to get the page content
        response = await crawler.get(url)
        if not response or not response.text:
            return ""
        
        # Parse with BeautifulSoup to get clean text
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it up
        text = soup.get_text(separator=' ', strip=True)
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text[:10000]  # Limit text length to avoid token limits
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

async def process_person(person: Dict) -> Dict:
    """Process a single person's links and create embeddings."""
    name = person['name']
    links = person.get('links', [])
    
    # Scrape all links
    texts = []
    for link in links:
        text = await scrape_url(link)
        if text:
            texts.append(text)
    
    if not texts:
        return None
    
    # Combine all texts and create a summary
    combined_text = " ".join(texts)
    
    # Use Cohere to generate a summary
    summary_response = co.summarize(
        text=combined_text,
        length='medium',
        format='paragraph',
        model='command',
        temperature=0.3,
        additional_command="Focus on professional background, skills, and expertise."
    )
    summary = summary_response.summary
    
    # Generate embeddings for the summary
    embedding_response = co.embed(
        texts=[summary],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    
    return {
        "name": name,
        "summary": summary,
        "embedding": embedding_response.embeddings[0],
        "links": links,
        "last_updated": datetime.utcnow()
    }

async def main():
    # Get all people from MongoDB
    people_collection = db['People']
    processed_collection = db['ProcessedPeople']
    
    # Create index for vector search if it doesn't exist
    await processed_collection.create_index([("embedding", "2dsphere")])
    
    cursor = people_collection.find({})
    async for person in cursor:
        print(f"Processing {person['name']}...")
        
        # Check if we've already processed this person recently
        existing = await processed_collection.find_one({"name": person['name']})
        if existing and (datetime.utcnow() - existing['last_updated']).days < 7:
            print(f"Skipping {person['name']} - recently updated")
            continue
        
        processed = await process_person(person)
        if processed:
            # Use upsert to update if exists or insert if new
            await processed_collection.update_one(
                {"name": person['name']},
                {"$set": processed},
                upsert=True
            )
            print(f"Successfully processed {person['name']}")
        else:
            print(f"Failed to process {person['name']}")

if __name__ == "__main__":
    asyncio.run(main()) 