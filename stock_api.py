from flask import Flask, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/stock/<symbol>')
def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol + ".NS")  # NSE India
        data = stock.history(period="1d")
        if not data.empty:
            price = data["Close"].iloc[-1]
            return jsonify({"symbol": symbol, "price": round(price, 2)})
        else:
            return jsonify({"error": "No data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
