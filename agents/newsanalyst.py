from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from pydantic import BaseModel 

from tools.newsanalysttools import get_news_articles, scrape_and_assess_news_impact
from tools.keyword import extract_keywords

class NewsOutput(BaseModel):
    source: str
    article_title: str
    source_url: str
    published_at: str
    scraped_content: str

NEWS_ANALYST_INSTRUCTIONS = """
**Persona:**
You are a fast and efficient News Collector for a quantitative analysis firm. Your role is to systematically retrieve and document recent news articles relevant to a specific market event. You are meticulous, unbiased, and focused on data gathering, not interpretation.

**Objective:**
Given a market topic, your mission is to find relevant news articles and process them one by one, extracting the core text and metadata, and formatting this information perfectly into the `NewsOutput` schema.

**Core Workflow (Strictly follow this order):**
1.  **Extract Keywords:** When given a market topic, your first action is to use the `extract_keywords` tool to identify the essential search terms.
2.  **Fetch News Articles:** Use the `get_news_articles` tool with the extracted keywords to retrieve a list of recent, relevant news article URLs.
3.  **Process a Single URL:** From the list of URLs you retrieved, select the most relevant one to process.
    - **A) Scrape Content:** Use the `scrape_and_assess_news_impact` tool on that single URL. Its primary function for you is to scrape the full text of the article.
    - **B) Extract and Format:** From the scraped content and the initial article data, meticulously extract the required information to populate the `NewsOutput` schema: `source`, `article_title`, `source_url`, `published_at`, and the full `scraped_content`.
4.  **Output Structured Data:** Return the fully populated `NewsOutput` object. Your task for this cycle is now complete.

**Rules & Constraints:**
- **Mandatory Tool Sequence:** You MUST use the tools in this exact order: `extract_keywords` -> `get_news_articles` -> `scrape_and_assess_news_impact`.
- **One Article Per Cycle:** You are designed to process and return data for only one article at a time. Your final output for a successful run is a single `NewsOutput` object.
- **Focus on Extraction, Not Analysis:** Your job is to collect and structure data, not to analyze or assess market impact. Do not provide summaries, opinions, or any information not explicitly part of the `NewsOutput` schema.
- **Data Integrity:** Ensure the `NewsOutput` object is populated accurately from the source data. The `scraped_content` field should contain the full text of the article you processed.
"""

keywordTool = FunctionTool(
    func = extract_keywords,
    description = "Extracts keywords from the prompt that is then passed to the information sources to use as information."
)

newsTool = FunctionTool(
    func = get_news_articles,
    description = "Searches for recent news articles related to a specific market question. Only use this tool to gather raw, unfiltered news articles."
)

scrapeTool = FunctionTool(
    func = scrape_and_assess_news_impact,
    description = "Scrapes the full text from article URLs, then analyzes the article content to create a summary and assess the likely impact on a specific question about a Polymarket market. Use this AFTER fetching news articles with the get_news_articles tool."
)




NewsCollectorAgent = LlmAgent(
    name = "SocialMediaAnalyst",
    model = "gemini-1.5-flash",
    description = "Takes data from the observed events in the ticker and collects news articles related to the event.",
    instruction = NEWS_ANALYST_INSTRUCTIONS,
    tools = [keywordTool, newsTool, scrapeTool],
    output_schema = NewsOutput
    output_key = "news_output"
)




#systemInstructions: only for 2.0 later models.


#multishot vs zeroshot

# Essential parts of a prompt:

##Objective, what you want the model to achieve. Be specific about your mission or goal. 
## Step by step instructions on how to perform the task at hand.  
##Can combine with persona.

##Instructions, step by step on how the prompt should accomplish its goals. 

# Optional parts of a prompt:


##Persona: Role/ vision ykwim. 
##Constraints: on what the model can or cannot do.
##Tone 
##Context: obvious
##Few shot
##Reasoning steps, formatting response in a format. 
## Recap, recapping key instructions. -> Constraints + response format. 
##Safeguards against prompt injection. 


