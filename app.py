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


@app.route("/entityquery/<entity>", methods=["POST"])
def entityquery(entity):
    details = request.data
    decoded = json.loads(details)
    testing = eval(decoded)
    G1 = nx.DiGraph()
    for i in range(len(testing)):
        G1.add_node(testing[i]["fentity"], name=testing[i]["fentity"])
        G1.add_node(testing[i]["sentity"], name=testing[i]["sentity"])
        G1.add_edge(
            testing[i]["fentity"],
            testing[i]["sentity"],
            start=testing[i]["fentity"],
            end=testing[i]["fentity"],
            relation=testing[i]["fentity"]
            + " "
            + testing[i]["relationship"]
            + " "
            + testing[i]["sentity"],
        )
    ed = G1.edges(entity)
    G2 = G1.edge_subgraph(ed)
    n = G2.number_of_nodes()
    if n == 0:
        n = 1
    print(n)
    pos = nx.spring_layout(G2, k=(8 / math.sqrt(n)))
    nx.draw(G2, pos, node_shape="s", node_size=1000)
    node_labels = nx.get_node_attributes(G2, "name")
    edge_labels = nx.get_edge_attributes(G2, "relation")
    nx.draw_networkx_labels(G2, pos, labels=node_labels)
    nx.draw_networkx_edge_labels(G2, pos, edge_labels=edge_labels)
    img = BytesIO()  # file-like object for the image
    plt.savefig(img)  # save the image to the stream
    img.seek(0)  # writing moved the cursor to the end of the file, reset
    plt.clf()  # clear pyplot
    return send_file(img, mimetype="image/png")


@app.route("/addrelationship", methods=["POST"])
def addrelationship():
    details = request.data
    decoded = json.loads(details)
    testing = eval(decoded)
    G = nx.DiGraph()
    print("TESTING", len(testing))
    for i in range(len(testing)):
        G.add_node(testing[i]["fentity"], name=testing[i]["fentity"])
        G.add_node(testing[i]["sentity"], name=testing[i]["sentity"])
        # G.add_edge(testing[i]['fentity'], testing[i]['sentity'], start=testing[i]['fentity'], end=testing[i]['fentity'],relation=testing[i]['fentity']+' '+testing[i]['relationship']+' '+testing[i]['sentity'])
        G.add_edge(testing[i]["fentity"], testing[i]["sentity"])
    n = G.number_of_nodes()
    if n == 0:
        n = 1
    pos = nx.spring_layout(G, k=(8 / math.sqrt(n)))
    # pos = hierarchy_pos(G)
    nx.draw(G, pos, node_shape="s", node_size=1000)
    node_labels = nx.get_node_attributes(G, "name")
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    edge_labels = nx.get_edge_attributes(G, "relation")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    img = BytesIO()  # file-like object for the image
    plt.savefig(img)  # save the image to the stream
    img.seek(0)  # writing moved the cursor to the end of the file, reset
    plt.clf()  # clear pyplot
    return send_file(img, mimetype="image/png")


def hierarchy_pos(G, root=None, width=1, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723
    Licensed under Creative Commons Attribution-Share Alike

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    """
    if not nx.is_tree(G):
        raise TypeError("cannot use hierarchy_pos on a graph that is not a tree")

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(
                iter(nx.topological_sort(G))
            )  # allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(
        G, root, width=1, vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None
    ):
        """
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        """

        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            print(len(children))
            print("1st width", width)
            width = 1
            dx = width / len(children)
            print("DX", dx)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                print("CHIDL", child)
                nextx += dx
                print("2nd WIDTH", width)
                pos = _hierarchy_pos(
                    G,
                    child,
                    width=dx,
                    vert_gap=vert_gap,
                    vert_loc=vert_loc - vert_gap,
                    xcenter=nextx,
                    pos=pos,
                    parent=root,
                )

        return pos

    print("3rd Width:", width)
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


# driver function
if __name__ == "__main__":
    app.run(debug=True)
