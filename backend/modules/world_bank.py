import httpx
import asyncio

class WorldBankClient:
    BASE_URL = "https://api.worldbank.org/v2"
    
    INDICATORS = {
        "gdp": "NY.GDP.MKTP.CD",
        "gdp_growth": "NY.GDP.MKTP.KD.ZG",
        "inflation": "FP.CPI.TOTL.ZG",
        "unemployment": "SL.UEM.TOTL.ZS",
        "debt_gdp": "GC.DOD.TOTL.GD.ZS"
    }

    async def fetch_indicator(self, country_code: str, indicator: str, limit: int = 5):
        indicator_id = self.INDICATORS.get(indicator)
        if not indicator_id:
            return None
        
        url = f"{self.BASE_URL}/country/{country_code}/indicator/{indicator_id}"
        params = {
            "format": "json",
            "per_page": 5
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if len(data) > 1 and data[1]:
                    return data[1]
            return []

    async def get_macro_stats(self, country_code: str):
        tasks = {name: self.fetch_indicator(country_code, name) for name in self.INDICATORS}
        results = await asyncio.gather(*tasks.values())
        return dict(zip(tasks.keys(), results))

world_bank_client = WorldBankClient()
