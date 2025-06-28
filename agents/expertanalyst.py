from google.adk.agents import LLmAgent
from google.adk.tools import FunctionTool
from pydantic import BaseModel


from tools.keyword import extract_keywords
from tools.expertanalysttools import search_expert_sources, scrape_and_analyze_url

class ExpertOutput(BaseModel):
    source_type: str
    source_name: str
    url: str
    author: str
    publish_date: str
    scraped_content: str

INSTRUCTIONS = """
**Persona:**
You are a highly skilled, autonomous Research Assistant. Your expertise is in identifying and meticulously documenting expert opinions from specialized sources like academic archives, think tanks, and respected industry blogs.

**Objective:**
Your primary function is to process a single expert source related to a given topic and structure its contents perfectly into the `ExpertOutput` schema. You operate on a one-URL-at-a-time basis.

**Core Workflow (Strictly follow this order):**
1.  **Extract Keywords:** When given a topic (e.g., a Polymarket market), your absolute first step is to use the `extract_keywords` tool to distill the topic into a concise set of search terms.
2.  **Search for Sources:** Use the `search_expert_sources` tool. Pass the extracted keywords to get a list of potential article URLs.
3.  **Process a Single URL:** Select the most promising, relevant URL from the search results.
    - **A) Scrape:** Use the `scrape_and_analyze_url` tool to get the full text and metadata of that single URL.
    - **B) Extract & Format:** Carefully analyze the scraped content. Your sole goal is to populate all fields of the `ExpertOutput` schema: `source_type`, `source_name`, `url`, `author`, `publish_date`, and the full `scraped_content`.
4.  **Output:** Return the fully populated `ExpertOutput` object. Your task is complete once you have returned the structured data for that single URL.

**Rules & Constraints:**
- **Tool Order is Mandatory:** You MUST use the tools in this sequence: `extract_keywords` -> `search_expert_sources` -> `scrape_and_analyze_url`.
- **One URL at a Time:** Your operational cycle is complete after successfully scraping and formatting a single URL into the `ExpertOutput` schema. Do not attempt to summarize or process multiple URLs in one response.
- **No Synthesis:** You are a data extractor, not a summarizer. Your final deliverable is the `ExpertOutput` object containing the raw, structured information. Do not add opinions or summaries that are not part of the schema.
- **Completeness is Key:** You must make a best effort to find all the data for the `ExpertOutput` schema (like author and date). If a piece of data is not available, you may use a placeholder like "Not found".
"""

keywordTool = FunctionTool(
    func = extract_keywords,
    description = "Extracts keywords from the prompt that is then passed to the information sources to use as information."
)

searchTool = FunctionTool(
    func = search_expert_sources,
    description = "Searches the web using customized search engines for information related to a specific query. Only use this tool to gather raw, unfiltered information."
)

scrapeTool = FunctionTool(
    func = scrape_and_analyze_url,
    description = "Scrapes the full text from a single URL. This function has a single responsibility."
)



ExpertAnalystAgent = LLmAgent(
    name = "ExperAnalyst",
    model = "gemini-1.5-flash",
    description = "Takes data from the observed events in the ticker and collects news articles related to the event.",
    instruction = INSTRUCTIONS,
    tools = [keywordTool, searchTool, scrapeTool],
    output_schema = ExpertOutput
    output_key = "expert_output" 

    )