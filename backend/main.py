from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pycountry
from modules.world_bank import world_bank_client
from modules.wikipedia import wikipedia_client
from modules.unctad import unctad_client
from modules.llm_engine import llm_engine
import json

app = FastAPI(title="Country Profile API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

COMMON_MAPPING = {
    "UAE": "ARE",
    "USA": "USA",
    "UK": "GBR",
    "INDIA": "IND",
    "EMIRATES": "ARE"
}

def get_country_info(query: str):
    query = query.strip().upper()
    
    # 1. Check common mapping
    if query in COMMON_MAPPING:
        country = pycountry.countries.get(alpha_3=COMMON_MAPPING[query])
        if country:
            return country

    try:
        # 2. Try exact alpha_3 match
        if len(query) == 3:
            country = pycountry.countries.get(alpha_3=query)
            if country:
                return country
        
        # 3. Try exact alpha_2 match
        if len(query) == 2:
            country = pycountry.countries.get(alpha_2=query)
            if country:
                return country
        
        # 4. Fallback to fuzzy search
        results = pycountry.countries.search_fuzzy(query)
        if results:
            return results[0]
    except Exception:
        # If fuzzy search fails, try one last time by name prefix
        try:
            for c in pycountry.countries:
                if query in c.name.upper():
                    return c
        except:
            return None
    return None

import os
from modules.data_fetcher import fetch_country_profile

STORAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage_data")
STORAGE_RAW = os.path.join(STORAGE_DIR, "raw")
STORAGE_INSIGHTS = os.path.join(STORAGE_DIR, "insights")

@app.get("/")
async def root():
    return {"message": "Country Profile API is running"}

@app.get("/api/country/{query}")
async def get_country_profile(query: str):
    country = get_country_info(query)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    country_code = country.alpha_3
    country_name = country.name
    alpha_2 = country.alpha_2
    
    raw_path = os.path.join(STORAGE_RAW, f"{country_code}.json")
    insights_path = os.path.join(STORAGE_INSIGHTS, f"{country_code}.json")
    
    # Try to load raw data
    data = None
    if os.path.exists(raw_path):
        print(f"Loading raw data for {country_name}...")
        with open(raw_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        # Cold start: fetch raw data
        print(f"Cold start: fetching raw data for {country_name}...")
        try:
            from modules.data_fetcher import fetch_raw_data
            data = await fetch_raw_data(country_name, country_code, alpha_2)
            os.makedirs(STORAGE_RAW, exist_ok=True)
            with open(raw_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching raw data: {str(e)}")

    # Try to load insights
    insights = {
        "investment_climate_summary": "AI Insights pending...",
        "political_summary": "Insights pending...",
        "key_takeaways": ["Insights will be generated in the next sync."]
    }
    
    if os.path.exists(insights_path):
        print(f"Loading AI insights for {country_name}...")
        try:
            with open(insights_path, "r", encoding="utf-8") as f:
                insights = json.load(f)
        except Exception as e:
            print(f"Error loading insights: {e}")
    else:
        # If no insights yet, we could trigger a background job or just return pending
        # For now, we return pending as requested by the pipeline design
        pass

    data["insights"] = insights
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
