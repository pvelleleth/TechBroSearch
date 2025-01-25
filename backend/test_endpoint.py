import requests
import json

def test_search():
    # The URL of your FastAPI endpoint
    url = "http://localhost:8000/search"
    
    # Test queries
    test_queries = [
        {
            "query": "Find software engineers interested in AI",
            "location": "San Francisco"
        },
        
    ]
    
    for query in test_queries:
        print(f"\nTesting query: {query}")
        try:
            # Make the POST request
            response = requests.post(url, json=query)
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                print("\nSuccess! Found profiles:")
                for profile in data['profiles']:
                    print(f"\nName: {profile['name']}")
                    print(f"Bio: {profile['bio']}")
                    print(f"Confidence Score: {profile['confidence_score']}")
                    print(f"Sources: {profile['sources']}")
                    if profile.get('skills'):
                        print(f"Skills: {', '.join(profile['skills'])}")
                    print("-" * 50)
            else:
                print(f"Error: Status code {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"Error making request: {str(e)}")

if __name__ == "__main__":
    test_search() 