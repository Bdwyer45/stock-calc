from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Stock Calculator API is running! Use /calculate with ticker, amount, and date."

@app.route('/calculate', methods=["POST"])
def calculate():
    ticker = request.form.get("symbol")
    amount = float(request.form.get("amount"))
    date_str = request.form.get("date")

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
