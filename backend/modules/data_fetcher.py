import asyncio
import json
import pycountry
from modules.world_bank import world_bank_client
from modules.wikipedia import wikipedia_client
from modules.unctad import unctad_client
from modules.llm_engine import llm_engine

async def fetch_raw_data(country_name: str, country_code: str, alpha_2: str):
    """Fetches raw data from APIs (World Bank, Wikipedia, UNCTAD)."""
    macro_task = world_bank_client.get_macro_stats(country_code)
    wiki_summary_task = wikipedia_client.get_summary(country_name)
    political_task = wikipedia_client.get_political_landscape(country_name)
    fdi_task = unctad_client.fetch_fdi_data(country_code)

    macro_data, wiki_summary, political_landscape, fdi_data = await asyncio.gather(
        macro_task, wiki_summary_task, political_task, fdi_task
    )

    return {
        "metadata": {
            "name": country_name,
            "code": country_code,
            "flag": f"https://flagcdn.com/w320/{alpha_2.lower()}.png"
        },
        "wiki": wiki_summary,
        "macro": macro_data,
        "fdi": fdi_data,
        "political": political_landscape
    }

async def generate_ai_insights(country_name, macro_data, political_landscape):
    """Generates AI insights using LLM based on provided raw data."""
    llm_insights_raw = await llm_engine.summarize_country_data(
        country_name, macro_data, political_landscape
    )
    
    llm_insights = {
        "investment_climate_summary": "Insights pending...",
        "political_summary": "Insights pending...",
        "key_takeaways": ["Data available in sections below."]
    }

    try:
        if isinstance(llm_insights_raw, str):
            cleaned_insight = llm_insights_raw
            if "```json" in cleaned_insight:
                cleaned_insight = cleaned_insight.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned_insight:
                 cleaned_insight = cleaned_insight.split("```")[1].split("```")[0].strip()
            
            parsed = json.loads(cleaned_insight)
            if isinstance(parsed, dict):
                llm_insights.update(parsed)
        elif isinstance(llm_insights_raw, dict) and "error" not in llm_insights_raw:
             llm_insights.update(llm_insights_raw)
    except Exception as e:
        print(f"LLM Parsing Error: {e}")
        llm_insights["raw"] = str(llm_insights_raw)
    
    return llm_insights

async def fetch_country_profile(country_name: str, country_code: str, alpha_2: str):
    """Legacy wrapper that does both (used by cold start in main.py)."""
    raw_data = await fetch_raw_data(country_name, country_code, alpha_2)
    insights = await generate_ai_insights(country_name, raw_data["macro"], raw_data["political"])
    raw_data["insights"] = insights
    return raw_data
