"""
Flask-сервер для второй джобы:
Конвертация JSON-файлов из raw-директории в Avro-формат и сохранение в stg-директорию.
"""

from flask import Flask, request, jsonify
from typing import Any, Dict
from convert_to_avro import convert_json_to_avro

app = Flask(__name__)


@app.route("/convert", methods=["POST"])
def convert() -> Any:
    try:
        req_data: Dict[str, Any] = request.get_json()
        raw_dir: str | None = req_data.get("raw_dir")
        stg_dir: str | None = req_data.get("stg_dir")

        if not raw_dir or not stg_dir:
            return jsonify({
                "status": "error",
                "message": "Missing raw_dir or stg_dir"
            }), 400

        convert_json_to_avro(raw_dir, stg_dir)

        return jsonify({
            "status": "success",
            "message": f"Converted files from {raw_dir} to {stg_dir}"
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
