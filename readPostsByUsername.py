
from apify_client import ApifyClient

# Initialize the ApifyClient with your Apify API token
client = ApifyClient("apify_api_knYA2rQ4ShCsxomYWWHqwfxizBDga11oF9IY")

# Prepare the Actor input
run_input = {
    "handles": ["realswtheory"],
    "tweetsDesired": 3,  # Specify the number of tweets you want
    "proxyConfig": { "useApifyProxy": True },
}

# Run the Actor and wait for it to finish
run = client.actor("quacker/twitter-scraper").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
print("💾 Check your data here: https://console.apify.com/storage/datasets/" + run["defaultDatasetId"])
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print("NEXT POST:")
    print(item['full_text'])
    print("\n\n")

# 📚 Want to learn more 📖? Go to → https://docs.apify.com/api/client/python/docs/quick-start
