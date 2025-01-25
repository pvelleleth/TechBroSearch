from typing import List, Dict, Optional
import cohere
import os
from models.profile import Profile

class ProfileAggregator:
    def __init__(self):
        self.co = cohere.Client(os.getenv('COHERE_API_KEY'))
    
    async def merge_profiles(self, profiles: List[Profile], query: str) -> List[Profile]:
        """Merge profiles from different sources and calculate confidence scores."""
        if not profiles:
            return []
        
        # Group profiles by name (case-insensitive)
        profile_groups: Dict[str, List[Profile]] = {}
        for profile in profiles:
            key = profile.name.lower()
            if key not in profile_groups:
                profile_groups[key] = []
            profile_groups[key].append(profile)
        
        merged_profiles = []
        for profiles_list in profile_groups.values():
            merged = self._merge_profile_group(profiles_list)
            merged.confidence_score = await self._calculate_confidence_score(merged, query)
            merged_profiles.append(merged)
        
        # Sort by confidence score
        merged_profiles.sort(key=lambda x: x.confidence_score, reverse=True)
        return merged_profiles[:5]  # Return top 5 profiles
    
    def _merge_profile_group(self, profiles: List[Profile]) -> Profile:
        """Merge a group of profiles that belong to the same person."""
        if len(profiles) == 1:
            return profiles[0]
        
        # Combine sources and skills
        sources = {}
        skills = set()
        for profile in profiles:
            sources.update(profile.sources)
            skills.update(profile.skills)
        
        # Use the most complete profile as base
        base_profile = max(profiles, key=lambda p: len(p.bio or "") + len(p.skills))
        
        return Profile(
            name=base_profile.name,
            title=base_profile.title,
            bio=base_profile.bio,
            location=base_profile.location,
            confidence_score=0.0,  # Will be calculated later
            sources=sources,
            skills=list(skills)
        )
    
    async def _calculate_confidence_score(self, profile: Profile, query: str) -> float:
        """Calculate confidence score based on profile relevance to query."""
        # Prepare text for semantic similarity
        profile_text = f"{profile.name} {profile.title or ''} {profile.bio or ''} {' '.join(profile.skills)}"
        
        # Get embeddings
        texts = [query, profile_text]
        embeddings = self.co.embed(texts=texts, model="embed-english-v3.0", input_type="search_query").embeddings
        
        # Calculate cosine similarity
        query_embedding = embeddings[0]
        profile_embedding = embeddings[1]
        
        similarity = self._cosine_similarity(query_embedding, profile_embedding)
        
        # Adjust score based on profile completeness
        completeness = sum([
            bool(profile.name) * 0.2,
            bool(profile.title) * 0.2,
            bool(profile.bio) * 0.2,
            bool(profile.skills) * 0.2,
            bool(profile.location) * 0.1,
            (len(profile.sources) / 3) * 0.1  # Normalize by expected number of sources
        ])
        
        return similarity * 0.7 + completeness * 0.3
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        return dot_product / (norm_a * norm_b) 