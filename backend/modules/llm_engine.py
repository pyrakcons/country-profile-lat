import ollama
import asyncio

class LLMEngine:
    def __init__(self, model="llama3.1:8b"):
        self.model = model

    async def summarize_country_data(self, country_name, macro_data, political_data):
        prompt = f"""
        Summarize the following data for {country_name} into a professional "Investment Climate" and "Political Landscape" overview.
        Focus on key strengths, risks, and trends.
        
        Macroeconomic Data:
        {macro_data}
        
        Political Data:
        {political_data}
        
        Provide the output in JSON format with fields: 
        - "investment_climate_summary": a string containing a professional 2-3 sentence paragraph.
        - "political_summary": a string containing a professional 2-3 sentence paragraph.
        - "political_landscape": an object with categories:
            - "government_type": string
            - "current_leaders": list of strings
            - "major_parties": list of strings
            - "stability": string (High/Medium/Low with brief reason)
            - "upcoming_elections": string
            - "recent_conflicts": string
        - "key_takeaways": a list of strings.

        IMPORTANT: Provide ONLY valid JSON. Do not include any comments (like //), conversational filler, or Markdown bolding outside the JSON block.
        """
        
        try:
            # ollama.chat is synchronous, so we offload it to a thread to avoid blocking the event loop
            response = await asyncio.to_thread(
                ollama.chat, 
                model=self.model, 
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['message']['content']
        except Exception as e:
            return {"error": str(e)}

llm_engine = LLMEngine()
