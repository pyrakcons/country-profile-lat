import httpx
from bs4 import BeautifulSoup

class WikipediaClient:
    BASE_URL = "https://en.wikipedia.org/api/rest_v1/page/summary"
    
    async def get_summary(self, country_name: str):
        url = f"{self.BASE_URL}/{country_name.replace(' ', '_')}"
        headers = {"User-Agent": "CountryProfileApp/1.0 (contact: admin@example.com)"}
        async with httpx.AsyncClient(headers=headers) as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
            return None

    async def get_political_landscape(self, country_name: str):
        # 1. Fetch summary for general context
        summary_data = await self.get_summary(country_name)
        context_text = summary_data.get('extract', '') if summary_data else ""
        
        # 2. Fetching the main page to parse the infobox
        url = f"https://en.wikipedia.org/wiki/{country_name.replace(' ', '_')}"
        headers = {"User-Agent": "CountryProfileApp/1.0 (contact: admin@example.com)"}
        async with httpx.AsyncClient(headers=headers) as client:
            response = await client.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                infobox = soup.find('table', {'class': 'infobox'})
                if not infobox:
                    return {"context": context_text, "raw_info": "Infobox missing"}
                
                political_data = {"context": context_text}
                rows = infobox.find_all('tr')
                for row in rows:
                    th = row.find('th')
                    td = row.find('td')
                    if th and td:
                        key = th.get_text(strip=True)
                        if any(x in key.lower() for x in ['government', 'president', 'prime minister', 'monarch', 'legislature']):
                            political_data[key] = td.get_text(strip=True)
                
                return political_data
            return {"context": context_text}

wikipedia_client = WikipediaClient()
