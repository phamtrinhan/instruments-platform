import uuid

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


# Flask app configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/stocks_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Stock model
class Stock(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    symbol = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

# API route to list all stocks
@app.route('/api/v1/stocks', methods=['GET'])
def list_stocks():
    try:
        # Query all stocks from the database
        stocks = Stock.query.all()

        # Convert the results to a list of dictionaries
        stock_list = [
            {
                'id': stock.id,
                'symbol': stock.symbol,
                'name': stock.name,
                'price': stock.price
            }
            for stock in stocks
        ]

        # Return the list as JSON
        return jsonify(stock_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API route to create a new stock
@app.route('/api/v1/stocks', methods=['POST'])
def create_stock():
    # Parse JSON data from the request
    data = request.get_json()

    # If the input is a list, process multiple stocks
    if isinstance(data, list):
        created_stocks = []
        errors = []

        for stock_data in data:
            symbol = stock_data.get('symbol')
            name = stock_data.get('name')
            price = stock_data.get('price')

            if not symbol or not name or price is None:
                errors.append({'error': 'Missing required fields: symbol, name, or price', 'data': stock_data})
                continue

            existing_stock = Stock.query.filter_by(symbol=symbol).first()
            if existing_stock:
                errors.append({'error': f'Stock with symbol {symbol} already exists.', 'data': stock_data})
                continue

            new_stock = Stock(symbol=symbol, name=name, price=price)
            db.session.add(new_stock)
            created_stocks.append(new_stock)

        db.session.commit()

        return jsonify({
            'created': [
                {
                    'id': stock.id,
                    'symbol': stock.symbol,
                    'name': stock.name,
                    'price': stock.price
                } for stock in created_stocks
            ],
            'errors': errors
        }), 201

    # Validate required fields for single stock
    symbol = data.get('symbol')
    name = data.get('name')
    price = data.get('price')

    if not symbol or not name or price is None:
        return jsonify({'error': 'Missing required fields: symbol, name, or price'}), 400

    # Check for duplicate symbol
    existing_stock = Stock.query.filter_by(symbol=symbol).first()
    if existing_stock:
        return jsonify({'error': f'Stock with symbol {symbol} already exists.'}), 400

    # Create and save the new stock
    new_stock = Stock(symbol=symbol, name=name, price=price)
    db.session.add(new_stock)
    db.session.commit()

    # Return the created stock details
    return jsonify({
        'id': new_stock.id,
        'symbol': new_stock.symbol,
        'name': new_stock.name,
        'price': new_stock.price
    }), 201

# API route to delete a stock by ID
@app.route('/api/v1/stocks/<id>', methods=['GET'])
def get_stock(id):
    try:
        # Find the stock by ID
        stock = Stock.query.get_or_404(id)
        # Return a success message
        return jsonify({
            'id': stock.id,
            'symbol': stock.symbol,
            'name': stock.name,
            'price': stock.price
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# API route to delete a stock by ID
@app.route('/api/v1/stocks/<id>', methods=['DELETE'])
def delete_stock(id):
    try:
        # Find the stock by ID
        stock = Stock.query.get_or_404(id)

        # Delete the stock
        db.session.delete(stock)
        db.session.commit()

        # Return a success message
        return jsonify({'message': f'Stock with ID {id} has been deleted.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API route to search stocks by name prefix
@app.route('/api/v1/stocks/search', methods=['GET'])
def search_stocks():
    query = request.args.get('q', '').strip().lower()  # Get the search query from URL params
    if not query:
        return jsonify({"error": "Query parameter 'q' is required."}), 400

    try:
        # Filter stocks containing the given query
        results = Stock.query.filter(
            db.or_(
                Stock.name.ilike(f'{query}%'),
                Stock.symbol.ilike(f'{query}%')
            )
        ).all()
        # Convert results to a list of names
        suggestions = [
            {
                'id': stock.id,
                'symbol': stock.symbol,
                'name': stock.name,
                'price': stock.price
            }
            for stock in results
        ]

        return jsonify(suggestions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Main function for initializing the database and running the app
def main():
    print("Hello, World!")

if __name__ == '__main__':
    # Ensure all database tables are created
    with app.app_context():
        db.create_all()

    # Run the Flask application
    app.run(port=8001, debug=True)
