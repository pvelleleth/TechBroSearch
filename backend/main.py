from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cohere
from tavily import TavilyClient
import os
from pymongo import MongoClient
from models.profile import SearchQuery, SearchResponse, Profile
import certifi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize clients
co = cohere.Client(os.getenv('COHERE_API_KEY'))
tavily = TavilyClient(os.getenv('TAVILY_API_KEY'))
mongo_client = MongoClient("mongodb+srv://vaibhav:hoya@cluster0.7omrv.mongodb.net/", tlsCAFile=certifi.where())
db = mongo_client['hoyahacks']

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/search", response_model=SearchResponse)
async def search_profiles(query: SearchQuery):
    try:
        # Get embedding for the search query
        query_embedding = co.embed(
            texts=[query.query],
            model="embed-english-v3.0",
            input_type="search_query"
        ).embeddings[0]
        
        # Perform vector search in MongoDB
        processed_collection = db['ProcessedPeople']
        
        # Find the most similar chunks using dot product similarity
        pipeline = [
            # Unwind the chunks array to search through individual chunks
            {"$unwind": "$chunks"},
            {
                "$addFields": {
                    "similarity": {
                        "$reduce": {
                            "input": {"$range": [0, {"$size": "$chunks.embedding"}]},
                            "initialValue": 0,
                            "in": {
                                "$add": [
                                    "$$value",
                                    {"$multiply": [
                                        {"$arrayElemAt": ["$chunks.embedding", "$$this"]},
                                        {"$arrayElemAt": [query_embedding, "$$this"]}
                                    ]}
                                ]
                            }
                        }
                    }
                }
            },
            # Sort by similarity
            {"$sort": {"similarity": -1}},
            # Group back by person to get their most relevant chunks
            {
                "$group": {
                    "_id": "$name",
                    "name": {"$first": "$name"},
                    "summary": {"$first": "$summary"},
                    "links": {"$first": "$links"},
                    "max_similarity": {"$max": "$similarity"},
                    "relevant_chunks": {
                        "$push": {
                            "text": "$chunks.text",
                            "similarity": "$similarity"
                        }
                    }
                }
            },
            # Sort by the person's maximum chunk similarity
            {"$sort": {"max_similarity": -1}},
            # Limit to top 5 people
            {"$limit": 5}
        ]
        
        # Execute pipeline and get results
        results = list(processed_collection.aggregate(pipeline))
        
        # Convert MongoDB results to Profile objects
        profiles = []
        for doc in results:
            # Take the top 3 most relevant chunks for each person
            top_chunks = sorted(doc['relevant_chunks'], 
                              key=lambda x: x['similarity'], 
                              reverse=True)[:3]
            
            # Combine chunks into a contextual bio
            chunk_texts = [chunk['text'] for chunk in top_chunks]
            
            # Combine the person's summary with relevant chunks for context
            context = f"Summary: {doc['summary']}\n\nRelevant Experience: {' '.join(chunk_texts)}"
            
            # Use Cohere to create a coherent bio that's relevant to the search query
            bio_response = co.chat(
                message=f"""Based on the following information about a person, create a concise professional bio that's relevant to the search query: '{query.query}'\n\nPerson's Information:\n{context}""",
                model="command",
                temperature=0.3,
                max_tokens=300
            )
            
            profile = Profile(
                name=doc['name'],
                bio=bio_response.text,
                confidence_score=float(doc['max_similarity']),
                sources={"links": ', '.join(doc['links'])},
                skills=[]  # You might want to extract skills from the bio
            )
            profiles.append(profile)
        
        return SearchResponse(profiles=profiles)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

