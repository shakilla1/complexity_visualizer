from flask import Flask, request, jsonify
import os
import time
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO

app = Flask(__name__)

if not os.path.exists("graphs"):
    os.makedirs("graphs")

@app.route('/')
def home():
    return "Welcome! POST to /graph to generate a complexity graph."

@app.route('/graph', methods=['POST'])
def generate_graph():
    input_size = np.arange(1, 11)
    time_complexity = np.random.randint(1, 100, size=10)
    
    plt.figure()
    plt.plot(input_size, time_complexity, marker='o', linestyle='-', color='b')
    plt.title("Complexity Graph")
    plt.xlabel("Input Size")
    plt.ylabel("Time (ms)")
    
    timestamp = int(time.time())
    filename = f"graphs/graph_{timestamp}.png"
    plt.savefig(filename)
    plt.close()

    buffer = BytesIO()
    plt.figure()
    plt.plot(input_size, time_complexity, marker='o', linestyle='-', color='b')
    plt.title("Complexity Graph")
    plt.xlabel("Input Size")
    plt.ylabel("Time (ms)")
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    
    return jsonify({
        "message": "Graph generated successfully!",
        "file_saved": filename,
        "preview_base64": image_base64
    })

if __name__ == '__main__':
    app.run(debug=True, port=3000)

