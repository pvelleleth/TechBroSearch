from pymongo import MongoClient
import cohere
import os
from typing import List, Dict
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from pymongo.server_api import ServerApi
import certifi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize clients
uri = os.getenv('MONGODB_URI')
# Configure MongoDB client with SSL settings
mongo_client = MongoClient("mongodb+srv://vaibhav:hoya@cluster0.7omrv.mongodb.net/", tlsCAFile=certifi.where())

db = mongo_client['hoyahacks']
co = cohere.Client(os.getenv('COHERE_API_KEY'))

def scrape_url(url: str) -> str:
    """Scrape a URL and return its text content."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"Error fetching {url}: Status {response.status_code}")
            return ""
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'iframe']):
            element.decompose()
        
        # Get text and clean it up
        text = soup.get_text(separator=' ', strip=True)
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def chunk_text(text: str) -> List[str]:
    """Use Cohere to intelligently chunk the text."""
    try:
        response = co.chat(
            message=f"Split this text into meaningful chunks, preserving context. Return only the chunks as a numbered list:\n\n{text}",
            model="command",
            temperature=0.0,
            max_tokens=1000
        )
        
        # Parse the numbered list from the response
        chunks = []
        current_chunk = ""
        
        for line in response.text.split('\n'):
            line = line.strip()
            if line and not line.startswith(('Here', 'I will', 'Let me')):  # Skip introductory text
                # Remove the number at the start if present
                if '. ' in line:
                    line = line.split('. ', 1)[1]
                chunks.append(line)
        
        return chunks if chunks else [text]  # Return original text if chunking fails
    except Exception as e:
        print(f"Error chunking text: {e}")
        return [text]

def process_person(person: Dict) -> Dict:
    """Process a single person's links and create embeddings."""
    try:
        name = person['Name']
        print(f"\nProcessing {name}:")
        
        # Collect all links from the document
        links = []
        i = 1
        while f'Link{i}' in person:
            if person[f'Link{i}']:  # Only add non-empty links
                links.append(person[f'Link{i}'])
            i += 1
        
        print(f"Found {len(links)} links: {links}")
        
        if not links:
            print("No links found in document")
            return None
        
        # Scrape all links
        texts = []
        for link in links:
            print(f"Scraping {link}...")
            text = scrape_url(link)
            if text:
                print(f"Successfully scraped {len(text)} characters")
                # Chunk the text
                chunks = chunk_text(text)
                print(f"Created {len(chunks)} chunks")
                texts.extend(chunks)
            else:
                print(f"Failed to get content from {link}")
        
        if not texts:
            print("No text content extracted from any links")
            return None
        
        # Generate embeddings for each chunk
        try:
            print("Generating embeddings...")
            embedding_response = co.embed(
                texts=texts,
                model="embed-english-v3.0",
                input_type="search_document"
            )
            
            print("Creating summary...")
            # Create a summary of all chunks
            combined_text = " ".join(texts)
            summary_response = co.summarize(
                text=combined_text,
                length='medium',
                format='paragraph',
                model='command',
                temperature=0.3,
                additional_command="Focus on professional background, skills, and expertise."
            )
            
            # Store each chunk with its embedding
            chunks_with_embeddings = []
            for i, (chunk, embedding) in enumerate(zip(texts, embedding_response.embeddings)):
                chunks_with_embeddings.append({
                    "text": chunk,
                    "embedding": embedding
                })
            
            result = {
                "name": name,
                "summary": summary_response.summary,
                "chunks": chunks_with_embeddings,
                "links": links,
                "last_updated": datetime.utcnow()
            }
            print("Successfully processed all data")
            return result
            
        except Exception as e:
            print(f"Error in embedding/summary generation: {str(e)}")
            return None
            
    except Exception as e:
        print(f"Error processing person: {str(e)}")
        return None

def main():
    # Get all people from MongoDB
    people_collection = db['People']
    processed_collection = db['ProcessedPeople']
    
    try:
        # Create index for vector search if it doesn't exist
        processed_collection.create_index([("chunks.embedding", "2dsphere")])
        
        # Get all people from MongoDB
        people = list(people_collection.find())
        print(f"\nFound {len(people)} people to process")
        
        for person in people:
            try:
                print(f"\n{'='*50}")
                print(f"Processing document: {person}")
                
                # Check if we've already processed this person recently
                existing = processed_collection.find_one({"name": person['Name']})
                if existing and (datetime.utcnow() - existing['last_updated']).days < 7:
                    print(f"Skipping {person['Name']} - recently updated")
                    continue
                
                processed = process_person(person)
                if processed:
                    # Use upsert to update if exists or insert if new
                    processed_collection.update_one(
                        {"name": person['Name']},
                        {"$set": processed},
                        upsert=True
                    )
                    print(f"Successfully processed {person['Name']}")
                else:
                    print(f"Failed to process {person['Name']}")
            except Exception as e:
                print(f"Error processing {person.get('Name', 'Unknown')}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main() 