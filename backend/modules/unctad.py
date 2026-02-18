import httpx
import json
import subprocess
import tempfile
import os
import asyncio

class UnctadClient:
    # We'll use World Bank FDI indicators as a reliable source for UNCTAD-style data
    INWARD_FDI = "BX.KLT.DINV.CD.WD"
    OUTWARD_FDI = "BM.KLT.DINV.CD.WD"

    async def fetch_fdi_data(self, country_code: str):
        indicators = [self.INWARD_FDI, self.OUTWARD_FDI]
        combined_data = []
        
        async with httpx.AsyncClient() as client:
            tasks = []
            for ind in indicators:
                url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{ind}"
                params = {"format": "json", "per_page": 100, "mrnev": 5}
                tasks.append(client.get(url, params=params))
            
            responses = await asyncio.gather(*tasks)
            for response in responses:
                if response.status_code == 200:
                    # Remove BOM and handle potential parsing issues
                    content = response.text.lstrip('\ufeff')
                    try:
                        raw_json = json.loads(content)
                        if isinstance(raw_json, list) and len(raw_json) > 1:
                            combined_data.extend(raw_json[1])
                    except json.JSONDecodeError:
                        continue
        
        if combined_data:
            return self.process_with_jq(combined_data)
        return []

    def process_with_jq(self, data):
        """
        Demonstrates using 'jq' to transform and filter JSON data as requested by the user.
        """
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(data, f)
            temp_path = f.name

        try:
            # Use jq to group by indicator and take only the latest value for each
            # This is a bit complex for demonstration
            jq_filter = 'group_by(.indicator.id) | map({indicator: .[0].indicator.value, values: map({year: .date, value: .value})})'
            result = subprocess.run(['jq', jq_filter, temp_path], capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"error": "jq failed", "details": result.stderr}
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

unctad_client = UnctadClient()
