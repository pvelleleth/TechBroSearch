
# Product Requirements Document (PRD)  
## **Project Name:** Semantic People Search with Multi-Agent Analysis (Using Cohere LLM and Function Calling)

---

## **1. Overview**  
**Purpose:**  
This application uses **Cohere LLM** with **function calling** capabilities to enable semantic people search. The system allows users to query for individuals (e.g., "Find a data scientist focused on sustainability") and leverages tool-based function calling for APIs (e.g., GitHub, Twitter, AngelList). The backend orchestrates agents that collaborate to identify, analyze, and aggregate information about a person into a unified profile.

---

## **2. Key Features**
1. **Semantic Query Understanding:**  
   - Cohere LLM interprets user queries to identify key attributes like name, profession, location, and interests.
   
2. **Function Calling for API Tool Use:**  
   - The LLM dynamically selects and uses tools (API integrations) to fetch relevant information.

3. **Multi-Agent Analysis:**  
   - Cohere calls functions (APIs/tools) for:
     - Discovering potential matches.
     - Validating and analyzing profiles from different platforms (GitHub, Twitter, etc.).
     - Aggregating information into a comprehensive summary.

4. **Confidence Scoring & Ranking:**  
   - Profiles are ranked based on how closely they match the query.

5. **Frontend-Backend Integration:**  
   - React for the frontend to provide an interactive UI.
   - FastAPI for the backend to manage tool orchestration and API calls.

---

## **3. Functional Requirements**

### **Frontend (React)**
1. **Search Page:**
   - Input field for natural language queries.
   - Submit button to initiate the search.
   - Loading spinner to indicate progress during the search.

2. **Results Page:**
   - Display top 3–5 profiles with:
     - Profile picture (if available).
     - Name, title, and location.
     - Confidence score.
   - Expandable cards for detailed profile analysis.

3. **Error Handling:**
   - User feedback when no matches are found or when errors occur.

---

### **Backend (FastAPI with Cohere LLM)**
1. **Semantic Query Interpretation:**
   - Use Cohere LLM to parse user queries and extract:
     - Name (optional).
     - Keywords (e.g., sustainability, AI, data science).
     - Filters (e.g., location, profession).

2. **Function Calling for API Integration:**
   - **Tool Functions Available to LLM:**
     - **GitHub Tool:** Queries GitHub profiles for repositories, languages, and activity.
     - **Twitter Tool:** Fetches tweets, bio, and engagement metrics.
     - **LinkedIn Tool:** Searches LinkedIn profiles (if accessible).
     - **AngelList Tool:** Finds startup professionals.
     - **Semantic Scholar Tool:** Searches academic papers and authors.

   - **Example Function Call:**
     ```json
     {
       "function": "search_github",
       "parameters": {
         "query": "machine learning sustainability",
         "location": "San Francisco"
       }
     }
     ```

   - **Example API Response:**
     ```json
     {
       "name": "Jane Doe",
       "bio": "AI engineer focusing on sustainability",
       "repos": [
         {"name": "GreenEnergyML", "stars": 150},
         {"name": "ClimateAI", "stars": 300}
       ],
       "languages": ["Python", "TensorFlow"]
     }
     ```

3. **Orchestration of API Calls:**
   - The LLM determines which tools to call based on query interpretation.
   - Handles multiple tools in sequence (e.g., first search GitHub, then analyze Twitter).

4. **Profile Aggregation:**
   - Consolidates data from multiple tools into a unified profile:
     - Name, title, and bio.
     - Skills, repositories, and social media activity.
     - Publications or relevant articles.

5. **Confidence Scoring:**
   - Assigns a score to each profile based on:
     - Keyword relevance.
     - Semantic similarity to the query.
     - Tool-based insights (e.g., GitHub activity, Twitter relevance).

---

## **4. Non-Functional Requirements**
1. **Performance:** Return results within 5 seconds for typical queries.
2. **Scalability:** Support concurrent requests during high traffic (e.g., demo sessions).
3. **Security:** Protect API keys (use environment variables) and avoid storing sensitive data.
4. **Cross-Platform Compatibility:** Ensure frontend compatibility across browsers.

---

## **5. User Flow**

1. **Query Input:**
   - User enters: `"Find a data scientist specializing in climate change in New York."`
   - The LLM interprets the query and decides which tools to use.

2. **Backend Processing:**
   - **Tool 1:** GitHub API fetches profiles with relevant repos.
   - **Tool 2:** Twitter API analyzes public tweets for engagement and topics.
   - **Tool 3:** Semantic Scholar API searches for relevant academic authors.

3. **Profile Aggregation:**
   - Each tool's response is merged into a comprehensive profile summary.

4. **Frontend Display:**
   - Results are shown as ranked profiles with expandable details.

---

## **6. Tool Functions (APIs for LLM Function Calling)**

### **1. GitHub Search Function**
- **Purpose:** Search GitHub profiles for repositories, contributions, and languages.
- **Parameters:**
  - `query` (string): Keywords to search.
  - `location` (optional): Geographical filter.
- **API Call:**
  ```python
  @app.post("/tools/github")
  def search_github(query: str, location: Optional[str]):
      # Call GitHub API and return relevant profiles
  ```

### **2. Twitter Search Function**
- **Purpose:** Search Twitter for bios, tweets, and engagement metrics.
- **Parameters:**
  - `query` (string): Keywords or hashtags.
  - `location` (optional): Geographical filter.
- **API Call:**
  ```python
  @app.post("/tools/twitter")
  def search_twitter(query: str, location: Optional[str]):
      # Call Twitter API and return relevant profiles
  ```

### **3. LinkedIn Search Function**
- **Purpose:** Search LinkedIn profiles based on name, title, and location.
- **Parameters:**
  - `query` (string): Keywords to search.
  - `location` (optional): Geographical filter.
- **API Call:**
  ```python
  @app.post("/tools/linkedin")
  def search_linkedin(query: str, location: Optional[str]):
      # Call LinkedIn API or simulate response
  ```

### **4. Semantic Scholar Search Function**
- **Purpose:** Fetch academic authors and publications.
- **Parameters:**
  - `query` (string): Keywords or author names.
- **API Call:**
  ```python
  @app.post("/tools/semantic_scholar")
  def search_scholar(query: str):
      # Call Semantic Scholar API and return author profiles
  ```

---

## **7. Backend Architecture**

### **Core Components:**
1. **FastAPI Backend:**
   - Handles API endpoints for frontend communication and function calls.
2. **Cohere Integration:**
   - API to process queries and decide which tools to call.
3. **Tool Functions:**
   - GitHub, Twitter, LinkedIn, Semantic Scholar, etc.
4. **Data Aggregator:**
   - Merges responses from multiple tools and calculates confidence scores.

---

## **8. Frontend Architecture**

### **Components:**
1. **SearchBar Component:**
   - Input field and button to trigger the search.
2. **ResultsList Component:**
   - Displays ranked profiles with basic information.
3. **ProfileCard Component:**
   - Expands to show detailed insights about a profile.

---

## **9. Example Payloads**

### **Frontend to Backend Query:**
```json
{
  "query": "Find a machine learning engineer focused on sustainability"
}
```

### **Backend Response:**
```json
[
  {
    "name": "Jane Doe",
    "title": "AI Researcher at GreenTech AI",
    "confidence_score": 92,
    "bio": "Machine learning engineer specializing in renewable energy.",
    "sources": {
      "github": "https://github.com/janedoe",
      "twitter": "https://twitter.com/jane_ai",
      "scholar": "https://scholar.google.com/citations?user=janedoe"
    }
  }
]
```

---

## **10. Timeline**

| **Task**                       | **Time Estimate**   |
|---------------------------------|---------------------|
| FastAPI Backend Setup           | 2 days             |
| Cohere LLM Query Integration    | 2 days             |
| API Tool Functions (GitHub, etc.) | 5 days             |
| React Frontend Development      | 5 days             |
| Profile Aggregation & Scoring   | 3 days             |
| Testing and Bug Fixes           | 3 days             |

---

Let me know if you'd like help setting up any part of this!
