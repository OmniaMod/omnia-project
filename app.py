from pytrends.request import TrendReq
import os
import tweepy
from flask import Flask, jsonify

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
        auth = tweepy.OAuth1UserHandler(
            os.getenv('TWITTER_API_KEY'),
            os.getenv('TWITTER_API_SECRET'),
            os.getenv('TWITTER_ACCESS_TOKEN'),
            os.getenv('TWITTER_ACCESS_SECRET')
        )
        api = tweepy.API(auth)
        trends_result = api.get_place_trends(1)
        trends_data = [
            {"name": trend["name"], "url": trend["url"]}
            for trend in trends_result[0]["trends"]
        ]
        return jsonify({"trends": trends_data})
    except Exception as e:
        print(f"Error fetching trends: {str(e)}")
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
def google_related_queries_debug():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)

        # Define the keyword to analyze (or fetch dynamically)
        keyword = request.args.get('keyword', 'AI')

        # Build payload for the selected keyword
        pytrends.build_payload([keyword])

        # Fetch related queries
        related_queries = pytrends.related_queries()

        # Log the raw related queries data for debugging
        print(f"Related Queries Raw Data: {related_queries}")

        # Check if the data is available for the keyword
        if keyword not in related_queries or not related_queries[keyword]:
            return jsonify({"error": f"No related queries found for keyword: {keyword}"}), 404

        # Return the related queries data
        return jsonify(related_queries[keyword])
    except Exception as e:
        # Log the error for debugging
        print(f"Error in /google-related-queries: {str(e)}")
        return jsonify({"error": str(e)}), 500

