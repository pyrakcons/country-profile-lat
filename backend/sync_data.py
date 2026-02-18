import asyncio
import os
import json
import argparse
import pycountry
from modules.data_fetcher import fetch_country_profile

STORAGE_RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage_data", "raw")
os.makedirs(STORAGE_RAW, exist_ok=True)

# List of "popular" countries for daily sync (example list)
POPULAR_COUNTRIES = ["ARE", "USA", "GBR", "IND", "CHN", "DEU", "FRA", "JPN", "CAN", "AUS"]

async def sync_country(country, trigger_ai=False):
    country_code = country.alpha_3
    country_name = country.name
    alpha_2 = country.alpha_2
    
    file_path = os.path.join(STORAGE_RAW, f"{country_code}.json")
    
    print(f"Syncing raw data for {country_name} ({country_code})...")
    try:
        from modules.data_fetcher import fetch_raw_data
        data = await fetch_raw_data(country_name, country_code, alpha_2)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Successfully synced raw data for {country_name}.")
        
        if trigger_ai:
            from sync_ai import generate_for_country
            await generate_for_country(country_code)
            
    except Exception as e:
        print(f"Failed to sync {country_name}: {e}")

async def main():
    parser = argparse.ArgumentParser(description="Sync raw country data to local storage.")
    parser.add_argument("--mode", choices=["daily", "weekly", "single"], default="daily", help="Sync mode: daily (popular), weekly (full), or single.")
    parser.add_argument("--country", help="Country code for single sync mode.")
    parser.add_argument("--ai", action="store_true", help="Trigger AI insight generation immediately after raw sync.")
    args = parser.parse_args()

    countries_to_sync = []
    
    if args.mode == "single":
        if not args.country:
            print("Error: --country is required for single mode.")
            return
        country = pycountry.countries.get(alpha_3=args.country.upper())
        if not country:
            country = pycountry.countries.get(alpha_2=args.country.upper())
        if not country:
            print(f"Error: Country {args.country} not found.")
            return
        countries_to_sync = [country]
    elif args.mode == "daily":
        print("Starting daily sync (popular countries)...")
        for code in POPULAR_COUNTRIES:
            country = pycountry.countries.get(alpha_3=code)
            if country:
                countries_to_sync.append(country)
    elif args.mode == "weekly":
        print("Starting weekly sync (all countries)...")
        countries_to_sync = list(pycountry.countries)

    print(f"Total countries to sync: {len(countries_to_sync)}")
    
    # Process in batches
    batch_size = 5
    for i in range(0, len(countries_to_sync), batch_size):
        batch = countries_to_sync[i:i + batch_size]
        tasks = [sync_country(c, trigger_ai=args.ai) for c in batch]
        await asyncio.gather(*tasks)
        print(f"Progress: {i + len(batch)}/{len(countries_to_sync)}")

if __name__ == "__main__":
    asyncio.run(main())
