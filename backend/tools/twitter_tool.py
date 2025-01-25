from typing import Optional, List, Dict
import os
import tweepy
from models.profile import Profile

class TwitterTool:
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )
    
    async def search_users(self, query: str, location: Optional[str] = None) -> List[Dict]:
        search_query = query
        if location:
            search_query += f" near:{location}"
        
        try:
            # Search for users
            users = self.client.search_users(query=search_query, max_results=5)
            return [user.data for user in users[0]] if users[0] else []
        except Exception as e:
            print(f"Twitter search error: {e}")
            return []
    
    async def get_user_details(self, username: str) -> Optional[Profile]:
        try:
            # Get user profile
            user = self.client.get_user(username=username, user_fields=["description", "location", "url"])
            if not user.data:
                return None
            
            user_data = user.data
            
            # Get recent tweets to analyze common topics
            tweets = self.client.get_users_tweets(
                user_data.id, 
                max_results=10,
                tweet_fields=["context_annotations"]
            )
            
            # Extract topics from tweets
            topics = set()
            if tweets.data:
                for tweet in tweets.data:
                    if hasattr(tweet, "context_annotations"):
                        for annotation in tweet.context_annotations:
                            if "domain" in annotation:
                                topics.add(annotation["domain"]["name"])
            
            return Profile(
                name=user_data.name,
                bio=user_data.description,
                location=user_data.location,
                confidence_score=0.0,  # Will be calculated later
                sources={"twitter": f"https://twitter.com/{user_data.username}"},
                skills=list(topics)  # Use topics as skills
            )
        except Exception as e:
            print(f"Twitter user details error: {e}")
            return None 