"""
Модуль конвертации JSON-файлов с данными о продажах из raw-директории
в формат Avro и сохранения их в stg-директорию.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Union
from fastavro import writer, parse_schema


def convert_json_to_avro(raw_dir: str, stg_dir: str) -> str:
    """
    Читает JSON-файлы из raw_dir, конвертирует данные в формат Avro и сохраняет в stg_dir.

    Parameters:
        raw_dir (str): Путь к директории, где находятся JSON-файлы.
        stg_dir (str): Путь к директории, куда сохраняются Avro-файлы.

    Returns:
        str: Путь к созданному Avro-файлу.
    """
    date: str = Path(raw_dir).parts[-1]
    input_path = Path(raw_dir)
    output_path = Path(stg_dir)

    output_path.mkdir(parents=True, exist_ok=True)

    schema: Dict[str, Union[str, List[Dict[str, str]]]] = {
        "doc": "Sales data",
        "name": "Sale",
        "namespace": "sales",
        "type": "record",
        "fields": [
            {"name": "client", "type": "string"},
            {"name": "purchase_date", "type": "string"},
            {"name": "product", "type": "string"},
            {"name": "price", "type": "int"},
        ],
    }

    parsed_schema = parse_schema(schema)
    all_records: List[Dict[str, Union[str, int]]] = []

    for filename in input_path.glob("sales_*.json"):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                all_records.extend(data)
            else:
                raise ValueError(f"{filename} does not contain a list of records")

    output_file = output_path / f"sales_{date}.avro"
    with open(output_file, "wb") as out:
        writer(out, parsed_schema, all_records)

    return str(output_file)
