from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cohere
from tavily import TavilyClient
import os
import asyncio
from typing import List

from models.profile import SearchQuery, SearchResponse, Profile
from tools.github_tool import GitHubTool
from tools.twitter_tool import TwitterTool
from services.profile_aggregator import ProfileAggregator

# Initialize clients
co = cohere.Client(os.getenv('COHERE_API_KEY'))
tavily = TavilyClient(os.getenv('TAVILY_API_KEY'))

# Initialize tools and services
github_tool = GitHubTool()
twitter_tool = TwitterTool()
profile_aggregator = ProfileAggregator()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/search", response_model=SearchResponse)
async def search_profiles(query: SearchQuery):
    try:
        # Use Cohere to understand the query
        response = co.chat(
            message=f"Analyze this search query and extract key terms for finding relevant profiles: {query.query}",
            model="command",
            temperature=0.0
        )
        search_terms = response.text
        
        # Search profiles using different tools
        tasks = [
            github_tool.search_users(search_terms, query.location),
            twitter_tool.search_users(search_terms, query.location)
        ]
        tool_results = await asyncio.gather(*tasks)
        
        # Get detailed profiles for each result
        profiles: List[Profile] = []
        for tool_index, results in enumerate(tool_results):
            tool_tasks = []
            for result in results:
                if tool_index == 0:  # GitHub
                    tool_tasks.append(github_tool.get_user_details(result["login"]))
                else:  # Twitter
                    tool_tasks.append(twitter_tool.get_user_details(result["username"]))
            
            tool_profiles = await asyncio.gather(*tool_tasks)
            profiles.extend([p for p in tool_profiles if p is not None])
        
        # Merge and rank profiles
        merged_profiles = await profile_aggregator.merge_profiles(profiles, query.query)
        
        return SearchResponse(profiles=merged_profiles)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}