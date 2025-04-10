from flask import Flask, request, jsonify
from flask_cors import CORS
import re

from agents.generation_agent import generate_response_from_openai
from agents.reflection_agent import reflect_on_response
from agents.ranking_agent import rank_content
from agents.evolution_agent import evolve_content
from agents.proximity_agent import find_similar_past_queries
from agents.meta_review_agent import meta_review_analysis
from agents.supervisor import supervise_agents

from utils.db import store_query_result
from utils.web_scraper import scrape_links_from_url
from utils.smart_scraper import smart_keyword_scraper

app = Flask(__name__)
CORS(app)

@app.route('/mindsync/query', methods=['POST'])
def query():
    data = request.get_json()
    user_input = data.get('query', '')

    url_pattern = r'(https?://[^\s]+)'
    found_urls = re.findall(url_pattern, user_input)

    # 1. Direct scraping if URL is present
    if found_urls:
        url = found_urls[0]
        result = scrape_links_from_url(url)
        store_query_result(user_input, result)
        return jsonify({'result': result})

    # 2. Keyword-based smart scraping
    if len(user_input.split()) >= 3 and not found_urls:
        smart_result = smart_keyword_scraper(user_input)
        if smart_result:
            store_query_result(user_input, smart_result)
            return jsonify({'result': smart_result})

    # 3. AI-powered generation pipeline
    initial = generate_response_from_openai(user_input)
    reflected = reflect_on_response(initial)
    ranked = rank_content(reflected)
    evolved = evolve_content(ranked)
    proximity = find_similar_past_queries(user_input)
    meta = meta_review_analysis([initial, reflected, ranked, evolved, proximity])

    final_response = supervise_agents(initial, reflected, ranked, evolved, proximity, meta)
    store_query_result(user_input, final_response)

    return jsonify({'result': final_response})

@app.route('/mindsync/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    result = scrape_links_from_url(url)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
