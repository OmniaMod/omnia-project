from flask import Flask, jsonify, request
from playwright.async_api import async_playwright
from pytrends.request import TrendReq
import asyncio

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "OMNIA is live and pulling insights from the zeitgeist!",
        "routes": {
            "/scrape-twitter-trends": "Scrapes Twitter trends from Trends24",
            "/google-trending-searches": "Fetches trending searches from Google Trends",
            "/google-interest-over-time": "Fetches interest over time for specific keywords",
            "/google-related-queries": "Fetches related queries for a keyword"
        }
    })

@app.route('/scrape-twitter-trends', methods=['GET'])
async def scrape_twitter_trends():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto("https://trends24.in/")

            # Wait for trends to load
            await page.wait_for_selector("ol.trend-card li a")

            # Extract trends
            trends = await page.eval_on_selector_all(
                "ol.trend-card li a",
                "elements => elements.map(el => el.innerText)"
            )

            await browser.close()

            if not trends:
                return jsonify({"error": "No trends found on the site"}), 404

            return jsonify({"trends": trends})
    except Exception as e:
        print(f"Error in /scrape-twitter-trends: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/google-trending-searches', methods=['GET'])
def google_trending_searches():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        trending_searches = pytrends.trending_searches(pn='united_states')  # Replace 'united_states' with desired region

        # Convert the trending searches to a list
        trends = trending_searches[0].tolist()

        if not trends:
            return jsonify({"error": "No trends found"}), 404

        return jsonify({"trends": trends})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/google-interest-over-time', methods=['GET'])
def google_interest_over_time():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)

        # Define keywords to analyze
        keywords = request.args.getlist('keywords') or ["AI", "Crypto", "Web3"]

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

        # Debug the full structure of the related queries
        print(f"Related Queries Full Data: {related_queries}")

        # Check if the data for the keyword exists
        if not related_queries or keyword not in related_queries:
            return jsonify({"error": f"No related queries found for keyword: {keyword}"}), 404

        # Safely extract and return the related queries
        keyword_data = related_queries.get(keyword)
        return jsonify(keyword_data)
    except Exception as e:
        print(f"Error in /google-related-queries: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
