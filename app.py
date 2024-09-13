# Using flask to make an api
# import necessary libraries and functions
from flask import (
    Flask,
    request,
    send_file,
    json,
    render_template,
    send_from_directory,
)
from flask_cors import CORS
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import random
import math
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# Download necessary NLTK data (if you haven't already)
nltk.download('vader_lexicon')

# Run in background
matplotlib.use("agg")

# creating a Flask app
app = Flask(__name__, template_folder="./", static_folder="./")
CORS(app)


# Render homepage
@app.route("/")
def home():
    return render_template("index.html")


# Route to serve static files
@app.route("/<path:filename>")
def serve_static_files(filename):
    return send_from_directory(app.static_folder, filename)


@app.route("/sentimentanalysis", methods=["POST"])
def entityquery():
    details = request.data
    decoded = json.loads(details)
    testing = eval(decoded)
    print(testing)
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(testing)

    # Determine sentiment category based on compound score
    if sentiment_scores['compound'] >= 0.05:
        sentiment = 'Positive'
    elif sentiment_scores['compound'] <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    return sentiment
    # return sentiment, sentiment_scores


# @app.route("/addrelationship", methods=["POST"])
# def addrelationship():
#     details = request.data
#     decoded = json.loads(details)
#     testing = eval(decoded)
#     G = nx.DiGraph()
#     print("TESTING", len(testing))
#     for i in range(len(testing)):
#         G.add_node(testing[i]["fentity"], name=testing[i]["fentity"])
#         G.add_node(testing[i]["sentity"], name=testing[i]["sentity"])
#         # G.add_edge(testing[i]['fentity'], testing[i]['sentity'], start=testing[i]['fentity'], end=testing[i]['fentity'],relation=testing[i]['fentity']+' '+testing[i]['relationship']+' '+testing[i]['sentity'])
#         G.add_edge(testing[i]["fentity"], testing[i]["sentity"])
#     n = G.number_of_nodes()
#     if n == 0:
#         n = 1
#     pos = nx.spring_layout(G, k=(8 / math.sqrt(n)))
#     # pos = hierarchy_pos(G)
#     nx.draw(G, pos, node_shape="s", node_size=1000)
#     node_labels = nx.get_node_attributes(G, "name")
#     nx.draw_networkx_labels(G, pos, labels=node_labels)
#     edge_labels = nx.get_edge_attributes(G, "relation")
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
#     img = BytesIO()  # file-like object for the image
#     plt.savefig(img)  # save the image to the stream
#     img.seek(0)  # writing moved the cursor to the end of the file, reset
#     plt.clf()  # clear pyplot
#     return send_file(img, mimetype="image/png")




# driver function
if __name__ == "__main__":
    app.run(debug=True)
