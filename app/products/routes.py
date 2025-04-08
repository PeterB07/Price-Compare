from flask import render_template, jsonify, request, current_app
from app.products import bp
import requests
from datetime import datetime, timedelta
import random
import math

RAPIDAPI_KEY = "fbe1a9d572msha4827e1ae99d357p1d0059jsnb80cced81e6b"

def get_amazon_prices(query):
    url = "https://amazon23.p.rapidapi.com/product-search"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "amazon23.p.rapidapi.com"
    }
    params = {
        "query": query,
        "country": "IN"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('result', [])
    except Exception as e:
        current_app.logger.error(f"Amazon API error: {str(e)}")
        return []

def generate_mock_image_url(query, index):
    # Generate realistic-looking product images using placeholder service
    keywords = query.replace(' ', '+')
    return f"https://source.unsplash.com/featured/600x600/?{keywords}&sig={index}"

def get_flipkart_prices(query):
    # Generate realistic mock data for Flipkart
    mock_data = []
    base_price = random.randint(30000, 80000)
    
    variants = [
        {'suffix': '', 'price_factor': 1.0},
        {'suffix': ' (128GB)', 'price_factor': 1.2},
        {'suffix': ' Pro', 'price_factor': 1.4},
        {'suffix': ' Max', 'price_factor': 1.6}
    ]
    
    for i, variant in enumerate(variants):
        price = int(base_price * variant['price_factor'])
        mock_data.append({
            'name': f"{query}{variant['suffix']} - Flipkart Edition",
            'price': price,
            'image': generate_mock_image_url(query, i),
            'link': 'https://www.flipkart.com',
            'rating': round(random.uniform(4.0, 4.9), 1),
            'reviews_count': random.randint(1000, 5000)
        })
    
    return mock_data

@bp.route('/search', methods=['GET'])
def search():
    return render_template('products/search.html')

@bp.route('/api/search', methods=['GET'])
def api_search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    # Get prices from different stores
    amazon_results = get_amazon_prices(query)
    flipkart_results = get_flipkart_prices(query)

    # Process and combine results
    combined_results = []
    
    # Process Amazon results
    for i, item in enumerate(amazon_results):
        try:
            combined_results.append({
                'title': item.get('title', ''),
                'price': item.get('price', {}).get('current_price', 'N/A'),
                'image': item.get('thumbnail', generate_mock_image_url(query, f"amazon_{i}")),
                'url': item.get('url', ''),
                'store': 'Amazon',
                'rating': item.get('reviews', {}).get('rating', 'N/A'),
                'reviews': item.get('reviews', {}).get('total_reviews', '0')
            })
        except Exception as e:
            current_app.logger.error(f"Error processing Amazon item: {str(e)}")
    
    # Add Flipkart results
    for item in flipkart_results:
        try:
            combined_results.append({
                'title': item.get('name', ''),
                'price': str(item.get('price', 'N/A')),
                'image': item.get('image', ''),
                'url': item.get('link', ''),
                'store': 'Flipkart',
                'rating': str(item.get('rating', 'N/A')),
                'reviews': str(item.get('reviews_count', '0'))
            })
        except Exception as e:
            current_app.logger.error(f"Error processing Flipkart item: {str(e)}")

    return jsonify(combined_results)

def generate_price_trend(base_price, days, volatility=0.02, trend=0.0):
    """Generate realistic price trends with seasonal patterns and random variations"""
    prices = []
    for i in range(days):
        # Add trend
        trend_factor = 1 + (trend * i / days)
        
        # Add seasonal pattern (slight wave pattern)
        seasonal = math.sin(i * 2 * math.pi / 30) * 0.05
        
        # Add random variation
        random_factor = random.uniform(-volatility, volatility)
        
        # Combine factors
        daily_price = base_price * (1 + seasonal + random_factor) * trend_factor
        
        # Ensure price is reasonable
        daily_price = max(base_price * 0.7, min(base_price * 1.3, daily_price))
        
        prices.append(int(daily_price))
    
    return prices

@bp.route('/api/price-history', methods=['GET'])
def price_history():
    days = 90  # Show 3 months of price history
    today = datetime.now()
    
    # Generate dates
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]
    
    # Generate base price
    base_price = 50000
    
    # Generate price trends with different characteristics for each store
    amazon_prices = generate_price_trend(base_price, days, volatility=0.02, trend=-0.1)
    flipkart_prices = generate_price_trend(base_price, days, volatility=0.03, trend=0.05)
    
    return jsonify({
        'dates': dates[::-1],
        'amazon_prices': amazon_prices[::-1],
        'flipkart_prices': flipkart_prices[::-1]
    })