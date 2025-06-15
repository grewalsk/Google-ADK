from fastapi import FastAPI


from .tools.newsanalysttools import get_news_articles

app = FastAPI()

@app.get("/news")
async def get_news():
    news_articles = get_news_articles()
    return news_articles