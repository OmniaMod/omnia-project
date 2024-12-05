from pytrends.request import TrendReq
import os
import tweepy
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "OMNIA is live and pulling insights from the zeitgeist!",
        "routes": {
            "/get-twitter-trends": "Fetches Twitter trends"
        }
    })

@app.route('/get-twitter-trends', methods=['GET'])
def get_twitter_trends():
    try:
        # Use OAuthHandler for Tweepy v3.10.0
        auth = tweepy.OAuthHandler(
            os.getenv('TWITTER_API_KEY'),
            os.getenv('TWITTER_API_SECRET')
        )
        auth.set_access_token(
            os.getenv('TWITTER_ACCESS_TOKEN'),
            os.getenv('TWITTER_ACCESS_SECRET')
        )
        api = tweepy.API(auth)

        # Fetch trends for a specific location (WOEID = 1 for Worldwide)
        trends_result = api.trends_place(1)  # WOEID 1 = Worldwide
        trends_data = [
            {"name": trend["name"], "url": trend["url"]}
            for trend in trends_result[0]["trends"]
        ]
        return jsonify({"trends": trends_data})
    except Exception as e:
        print(f"Error in /get-twitter-trends: {str(e)}")
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
from bs4 import BeautifulSoup
import requests

@app.route('/scrape-twitter-trends', methods=['GET'])
def scrape_twitter_trends():
    try:
        url = "https://twitter-trending.com/"  # Example site for trends
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract trends (adjust based on target site's structure)
        trends = [trend.text for trend in soup.select('.trend-item h2')]
        return jsonify({"trends": trends})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/google-interest-over-time', methods=['GET'])
def google_interest_over_time():
    try:
        # Initialize pytrends
        pytrends = TrendReq(hl='en-US', tz=360)

        # Define keywords to analyze
        keywords = ["AI", "Crypto", "Web3"]  # Replace or expand with other topics

        # Build payload for the selected timeframe
        pytrends.build_payload(keywords, cat=0, timeframe='now 7-d')

        # Fetch interest over time
        interest_over_time = pytrends.interest_over_time()

        # Return results as JSON
        return jsonify(interest_over_time.reset_index().to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/google-related-queries', methods=['GET'])
def google_related_queries():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)

        # Get the keyword from query parameters (default to 'AI')
        keyword = request.args.get('keyword', 'AI')

        # Build payload for the selected keyword
        pytrends.build_payload([keyword])

        # Fetch related queries
        related_queries = pytrends.related_queries()

        # Debug the structure of the related queries
        print(f"Related Queries Raw Data: {related_queries}")

        # Check if related queries exist and return a safe structure
        if not related_queries or keyword not in related_queries:
            return jsonify({"error": f"No related queries found for keyword: {keyword}"}), 404

        keyword_data = related_queries.get(keyword, {})
        return jsonify(keyword_data or {"error": f"No related queries found for keyword: {keyword}"})
    except Exception as e:
        # Log and return errors
        print(f"Error in /google-related-queries: {str(e)}")
        return jsonify({"error": str(e)}), 500
