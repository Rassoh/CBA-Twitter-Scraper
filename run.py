from src.collect import collect_user_tweets

def main():
    df = collect_user_tweets("CommBank", total=200)
    df.to_csv("data/commbank_recent.csv", index=False)
    print("Saved to data/commbank_recent.csv")
    
    print(f"Save the last {len(df)} tweets from commbank to data/commbank_recent.csv")
    
if __name__ == "__main__":
    main()