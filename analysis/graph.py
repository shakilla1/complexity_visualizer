import matplotlib.pyplot as plt
import io
import base64


def generate_graph(x, y):
    plt.figure()
    plt.plot(x, y)
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")
