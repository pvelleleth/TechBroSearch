from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cohere
from tavily import TavilyClient
import os
from motor.motor_asyncio import AsyncIOMotorClient
from models.profile import SearchQuery, SearchResponse, Profile

# Initialize clients
co = cohere.Client(os.getenv('COHERE_API_KEY'))
tavily = TavilyClient(os.getenv('TAVILY_API_KEY'))
mongo_client = AsyncIOMotorClient(os.getenv('MONGODB_URI'))
db = mongo_client['hoyahacks']  # Replace with your database name

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
        
        # Find the most similar profiles using dot product similarity
        pipeline = [
            {
                "$addFields": {
                    "similarity": {
                        "$reduce": {
                            "input": {"$range": [0, {"$size": "$embedding"}]},
                            "initialValue": 0,
                            "in": {
                                "$add": [
                                    "$$value",
                                    {"$multiply": [
                                        {"$arrayElemAt": ["$embedding", "$$this"]},
                                        {"$arrayElemAt": [query_embedding, "$$this"]}
                                    ]}
                                ]
                            }
                        }
                    }
                }
            },
            {"$sort": {"similarity": -1}},
            {"$limit": 5}
        ]
        
        cursor = processed_collection.aggregate(pipeline)
        
        # Convert MongoDB results to Profile objects
        profiles = []
        async for doc in cursor:
            profile = Profile(
                name=doc['name'],
                bio=doc['summary'],
                confidence_score=float(doc['similarity']),  # Convert from Decimal128
                sources={"links": doc['links']},
                skills=[]  # You might want to extract skills from the summary
            )
            profiles.append(profile)
        
        return SearchResponse(profiles=profiles)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

