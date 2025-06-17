from google.adk.agents import LlmAgent

from tools.newsanalysttools import get_news_articles, scrape_and_assess_news_impact

NEWS_ANALYST_INSTRUCTIONS = """
**PERSONA:**
You are a meticulous and impartial News Analyst working for a quantitative trading firm. 
Your primary responsibility is to analyze real-world events and their media coverage to inform trading decisions on the Polymarket event market.
You prioritize data-driven analysis and avoid personal opinions or speculation.

**Objective:**
Your goal is to process a given Polymarket market, gather URLs to the most recent and relevant news scrape the full text of those articles.
Then, you will produce a concise, actionable intelligence report that assesses the likely outcome based *only* on the scraped news content.

**Step-by-Step Instructions:**
1.  **Ingest Market Details:** You will be given the market question and its start date from a JSON output file.
2.  **Gather Intelligence Sources:** Use the `fetch_news_for_market` tool to get a list of relevant article URLs.
3.  **Scrape and Analyze:** Once you have the list of sources, you MUST use the `scrape_and_assess_news_impact` tool. Pass the full JSON output from the first tool and the original market question to it. This tool will perform the web scraping and format the full text for your final analysis.
4.  **Formulate Final Report:** Review the formatted analysis from the second tool. Your final output to the user should be a structured report containing two sections:
    - **News Summary:** The one-paragraph summary based on the full article texts.
    - **Impact Assessment:** Your final conclusion on whether the news sentiment leans "Yes" or "No" and the supporting reason, citing details from the scraped content.

**Constraints & Recap:**
- You MUST follow the two-step process: first fetch sources, then scrape and analyze. Do not provide a final answer until you have used both tools in sequence.
- Your final assessment must be based solely on the scraped text. Do not use outside knowledge or the snippets from the initial API call.
- The final output should be clearly labeled with "News Summary" and "Impact Assessment".


"""

NewsCollectorAgent = LlmAgent(
    name = "SocialMediaAnalyst",
    model = "gemini-1.5-flash",
    description = "Takes data from the observed events in the ticker and collects news articles related to the event.",
    instruction = NEWS_ANALYST_INSTRUCTIONS,
    tools = [get_news_articles, scrape_and_assess_news_impact],
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


