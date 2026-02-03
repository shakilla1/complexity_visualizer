#!/usr/bin/python3
from flask import Flask, request, jsonify
from sqlalchemy import text

from analysis.analyzer import run_analysis
from analysis.graph import generate_graph
from database.connection import engine

app = Flask(__name__)


@app.route("/analyze", methods=["GET"])
def analyze():
    algo = request.args.get("algo")
    n = int(request.args.get("n", 0))
    steps = int(request.args.get("steps", 1))

    result = run_analysis(algo, n, steps)
    graph = generate_graph(range(steps), result["timings"])

    return jsonify({
        "algo": algo,
        "items": n,
        "steps": steps,
        "start_time": result["start_time"],
        "end_time": result["end_time"],
        "total_time_ms": result["total_time_ms"],
        "time_complexity": "O(n^2)",
        "graph_base64": graph
    })


@app.route("/save_analysis", methods=["POST"])
def save_analysis():
    data = request.get_json()

    query = text("""
        INSERT INTO algo_analysis
        (algo, items, steps, start_time, end_time,
         total_time_ms, time_complexity, graph_base64)
        VALUES
        (:algo, :items, :steps, :start_time, :end_time,
         :total_time_ms, :time_complexity, :graph_base64)
    """)

    with engine.connect() as conn:
        result = conn.execute(query, data)
        conn.commit()
        analysis_id = result.lastrowid

    return jsonify({
        "status": "success",
        "id": analysis_id
    }), 201


@app.route("/retrieve_analysis", methods=["GET"])
def retrieve_analysis():
    analysis_id = request.args.get("id")

    query = text(
        "SELECT * FROM algo_analysis WHERE id = :id"
    )

    with engine.connect() as conn:
        row = conn.execute(
            query, {"id": analysis_id}
        ).fetchone()

    if not row:
        return jsonify({"error": "Not found"}), 404

    return jsonify(dict(row))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
