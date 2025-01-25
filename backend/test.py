from tavily import TavilyClient
import os
import dotenv
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

response = tavily.search("Find me software engineers that work at Google and went to University of Maryland.")
import json

formatted_response = json.dumps(response, indent=4)
print(formatted_response)