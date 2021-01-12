import os
import time
import json
from pathlib import Path

from requests_oauthlib import OAuth1Session

def get_env():
    return (
        os.environ["API_KEY"], 
        os.environ["API_SECRET_KEY"], 
        os.environ["ACCESS_TOKEN"], 
        os.environ["ACCESS_TOKEN_SECRET"])

def login(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET):
    return OAuth1Session(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

def search(twitter, params, max_id=None, kwags=None):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    if max_id is not None:
        params["max_id"] = max_id
    if kwags is not None:
        params.update(kwags)
    print(params)
    res = twitter.get(url, params=params)
    return json.loads(res.text)

def data_save(data, dir, idx):
    path = dir / f"{str(idx).zfill(5)}.json"
    with open(str(path), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path

def call_loop(params, api, dir, slp_time=15):
    max_id_str = None
    idx = 0

    while True:
        print(f"Pooling Start: {str(idx).zfill(5)}")
        params.update({"max_id": max_id_str})
        data = api(**params)
        path = data_save(data, dir, idx)
        if "search_metadata" in data.keys():
            _max_id_str = data["statuses"][-1]["id_str"]
            print(_max_id_str)
            if max_id_str == _max_id_str:
                print("Fin")
                break
            max_id_str = _max_id_str
            print(f"Save as {str(path)}")
            print(f"Sleep {slp_time}sec")
            time.sleep(slp_time)
            idx += 1
        else:
            print("Fin")
            break

def main():
    API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = get_env()
    twitter = login(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    query = {"q": "#3分バーチャル劇場9ステ", "lang": "ja", "count": 100, "tweet_mode": "extended"}
    params = {"twitter": twitter, "params": query}

    dir = Path.cwd() / "#3分バーチャル劇場9ステ"
    call_loop(params, search, dir, slp_time=3)

if __name__ == "__main__":
    main()
