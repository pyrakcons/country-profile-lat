import asyncio
import os
import json
import argparse
import pycountry
from modules.data_fetcher import generate_ai_insights

STORAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage_data")
STORAGE_RAW = os.path.join(STORAGE_DIR, "raw")
STORAGE_INSIGHTS = os.path.join(STORAGE_DIR, "insights")

os.makedirs(STORAGE_INSIGHTS, exist_ok=True)

async def generate_for_country(country_code):
    raw_path = os.path.join(STORAGE_RAW, f"{country_code}.json")
    insights_path = os.path.join(STORAGE_INSIGHTS, f"{country_code}.json")
    
    if not os.path.exists(raw_path):
        print(f"Skipping {country_code}: Raw data not found.")
        return

    print(f"Generating AI insights for {country_code}...")
    try:
        with open(raw_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        
        country_name = raw_data["metadata"]["name"]
        macro_data = raw_data["macro"]
        political_data = raw_data["political"]
        
        insights = await generate_ai_insights(country_name, macro_data, political_data)
        
        with open(insights_path, "w", encoding="utf-8") as f:
            json.dump(insights, f, indent=4)
        print(f"Successfully generated insights for {country_name}.")
    except Exception as e:
        print(f"Failed to generate insights for {country_code}: {e}")

async def main():
    parser = argparse.ArgumentParser(description="Generate AI insights for countries with existing raw data.")
    parser.add_argument("--country", help="Specific country code to process (e.g. ARE). If omitted, processes all in raw folder.")
    parser.add_argument("--force", action="store_true", help="Regenerate even if insights file already exists.")
    args = parser.parse_args()

    codes_to_process = []
    
    if args.country:
        codes_to_process = [args.country.upper()]
    else:
        # Process everything in raw folder
        for filename in os.listdir(STORAGE_RAW):
            if filename.endswith(".json"):
                code = filename.replace(".json", "")
                insights_path = os.path.join(STORAGE_INSIGHTS, f"{code}.json")
                if args.force or not os.path.exists(insights_path):
                    codes_to_process.append(code)

    print(f"Total insights to generate: {len(codes_to_process)}")
    
    # Process in batches
    batch_size = 3
    for i in range(0, len(codes_to_process), batch_size):
        batch = codes_to_process[i:i + batch_size]
        tasks = [generate_for_country(code) for code in batch]
        await asyncio.gather(*tasks)
        print(f"Progress: {i + len(batch)}/{len(codes_to_process)}")

if __name__ == "__main__":
    asyncio.run(main())
