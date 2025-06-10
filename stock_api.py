from flask import Flask, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/stock/<symbol>')
def get_stock_info(symbol):
    try:
        stock = yf.Ticker(symbol + ".NS")
        data = stock.history(period="2d")  # Get 2 days of data

        if len(data) >= 2:
            prev_close = data["Close"].iloc[-2]
            current_price = data["Close"].iloc[-1]
            pl = current_price - prev_close
            pl_percent = (pl / prev_close) * 100

            return jsonify({
                "symbol": symbol.upper(),
                "price": round(current_price, 2),
                "previous_close": round(prev_close, 2),
                "pl": round(pl, 2),
                "pl_percent": round(pl_percent, 2)
            })
        else:
            return jsonify({"error": "Not enough data"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
