from google.adk.agents import LlmAgent

NewsCollectorAgent = LlmAgent(
    name = "NewsArticleCollector",
    model = "gemini-2.0-flash",
    description = "Takes data from the observed events in the ticker and collects news articles related to the event.",
    instruction = "",
    tools = [],
)