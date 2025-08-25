import pandas as pd 
from src.client import paginate

TWEET_FIELDS = [
    "id", "text", "created_at","public_metrics","entities","context_annotations",
    "conversation_id","referenced_tweets","lang", "source"
]
USER_FIELDS = ["username", "id", "verified", "created_at", "public_metrics"]

def collect_user_tweets(username="CommBank", max_results=100, total=500):
    params = {
        "query" : f"from:{username} -is:retweet",
        "tweet.fields" : ",".join(TWEET_FIELDS),
        "max_results" : max_results,
        "user.fields" : ",".join(USER_FIELDS),
        "expansions" : "author_id",
    }
    rows, users = [], {}
    for page in paginate("tweets/search/recent", params, limit=total):
        users_page = {u["id"]: u for u in page.get("includes", {}).get("users", [])}
        users.update(users_page)
        for t in page.get("data", []):
            a = users_page.get(t["author_id"], {})
            row = {**t, **{f"user_{k}": v for k, v in a.items()}}
            rows.append({
                "tweet_id": row.get("id"),
                "text": row.get("text"),
                "created_at": row.get("created_at"),
                "likes": row.get("public_metrics", {}).get("like_count"),
                "retweets": row.get("public_metrics", {}).get("retweet_count"),
                "replies": row.get("public_metrics", {}).get("reply_count"),
                "quotes": row.get("public_metrics", {}).get("quote_count"),
                "source": row.get("source"),
                "lang": row.get("lang"),
                "author_username": row.get("username"),
                "author_verified": row.get("verified"),
            })
    return pd.DataFrame(rows)