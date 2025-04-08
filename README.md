# Price-Compare - Electronics Price Comparison

A modern web application that compares electronics prices across different e-commerce platforms and tracks price history.

## Features

- Real-time price comparison between Amazon and Flipkart
- Interactive price history graphs
- Product search and filtering
- Category-based browsing
- Responsive design for all devices

## Tech Stack

- Flask (Python web framework)
- SQLAlchemy (Database ORM)
- Chart.js (Interactive graphs)
- Bootstrap 5 (UI Framework)
- RapidAPI Integration

## Setup

1. Clone the repository:
```bash
git clone https://github.com/PeterB07/droperia.git
cd droperia
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with:
```
SECRET_KEY=your-secret-key
FLASK_APP=run.py
FLASK_DEBUG=1
```

5. Initialize the database:
```bash
flask db upgrade
```

6. Run the application:
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## API Integration

The application uses RapidAPI to fetch real-time product data. You'll need to set up your RapidAPI key in the configuration.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
