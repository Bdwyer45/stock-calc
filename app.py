from flask import Flask, request, jsonify
import yfinance as yf
from datetime import datetime

app = Flask(__name__)

@app.route('/calculate')
def calculate():
    ticker = request.args.get("ticker")
    amount = float(request.args.get("amount"))
    date_str = request.args.get("date")

    stock = yf.Ticker(ticker)
    hist = stock.history(start=date_str)
    if hist.empty:
        return jsonify({"error": "Invalid date or ticker"}), 400

    price_then = hist.iloc[0]['Open']
    price_now = hist.iloc[-1]['Close']
    shares = amount / price_then
    value_now = shares * price_now
    dividends = stock.dividends[date_str:].sum() * shares
    total = value_now + dividends

    return jsonify({
        "price_then": round(price_then, 2),
        "price_now": round(price_now, 2),
        "shares": round(shares, 2),
        "total_with_dividends": round(total, 2),
        "total_profit_with_dividends": round(total - amount, 2),
        "percent_return_with_dividends": round((total - amount) / amount * 100, 2)
    })
