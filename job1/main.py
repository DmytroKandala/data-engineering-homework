# main.py — Flask-сервер для первой джобы (загрузка данных из API)

from flask import Flask, request, jsonify, typing as flask_typing
from sales_api import fetch_sales_data, save_sales_data
from typing import Dict, Any

app = Flask(__name__)

@app.route("/", methods=["POST"])
def run_job() -> flask_typing.ResponseReturnValue:
    try:
        data: Dict[str, Any] = request.get_json()
        date: str | None = data.get("date")
        raw_dir: str = data.get("raw_dir", ".")

        if not date:
            return jsonify({
                "status": "error",
                "message": "Missing 'date' in request"
            }), 400

        sales_data = fetch_sales_data(date)
        saved_path = save_sales_data(date, raw_dir, sales_data)

        return jsonify({
            "status": "success",
            "message": f"Sales data for {date} saved to {saved_path}"
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
