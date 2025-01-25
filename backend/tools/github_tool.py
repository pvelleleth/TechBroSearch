from typing import Optional, List, Dict
import os
import aiohttp
from models.profile import Profile

class GitHubTool:
    def __init__(self):
        self.api_key = os.getenv('GITHUB_API_KEY')
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.api_key}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    async def search_users(self, query: str, location: Optional[str] = None) -> List[Dict]:
        search_query = f"{query}"
        if location:
            search_query += f" location:{location}"
            
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/search/users",
                headers=self.headers,
                params={"q": search_query}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["items"][:5]  # Return top 5 results
                return []
    
    async def get_user_details(self, username: str) -> Optional[Profile]:
        async with aiohttp.ClientSession() as session:
            # Get user profile
            async with session.get(
                f"{self.base_url}/users/{username}",
                headers=self.headers
            ) as response:
                if response.status != 200:
                    return None
                user_data = await response.json()
            
            # Get user's repositories
            async with session.get(
                f"{self.base_url}/users/{username}/repos",
                headers=self.headers,
                params={"sort": "stars", "per_page": 5}
            ) as response:
                repos = await response.json() if response.status == 200 else []
            
            # Extract skills from repos
            skills = set()
            for repo in repos:
                if repo.get("language"):
                    skills.add(repo["language"])
            
            return Profile(
                name=user_data.get("name", username),
                title=user_data.get("company"),
                bio=user_data.get("bio"),
                location=user_data.get("location"),
                confidence_score=0.0,  # Will be calculated later
                sources={"github": user_data["html_url"]},
                skills=list(skills)
            ) 