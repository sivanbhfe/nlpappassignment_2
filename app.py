# Using flask to make an api
# import necessary libraries and functions
from io import BytesIO

from flask import (
    Flask,
    request,
    send_file,
    json,
    render_template,
    send_from_directory,
)
from flask_cors import CORS
import matplotlib
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK datasets
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

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
def sentimentanalysis():
    details = request.data
    decoded = json.loads(details)
    rawtext = eval(decoded)
    inputtext = preprocess_text(rawtext) # Get the input content pre-processed
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(inputtext)

    # Determine sentiment category based on compound score
    if sentiment_scores['compound'] >= 0.05:
        sentiment = 'Positive'
    elif sentiment_scores['compound'] <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    return sentiment

@app.route("/sentimentscoreandvisual",methods=["POST"])
def sentimentscoreandvisual():
    details = request.data
    decoded = json.loads(details)
    rawtext1 = eval(decoded)
    inputtext1 = preprocess_text(rawtext1) # Get the input content pre-processed
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(inputtext1)
    plt.figure(figsize=(4, 4))
    plt.bar(sentiment_scores.keys(), sentiment_scores.values(), color='lightblue',width = 0.1)
    plt.xlabel('Sentiment')
    plt.ylabel('Scores')
    plt.title('Actual scores from Sentiment Analyzer for reference:',fontsize = 8)
    for i, v in enumerate(sentiment_scores.values()):
        plt.text(i,v+0.02,str(v),ha='center')
    img = BytesIO()  # file-like object for the image
    plt.savefig(img)  # save the image to the stream
    img.seek(0)  # writing moved the cursor to the end of the file, reset
    plt.clf()  # clear pyplot
    return send_file(img, mimetype="image/png")


# Text preprocessing function
def preprocess_text(text):
      # Convert to lowercase
      text = text.lower()

      # Tokenize text
      tokens = word_tokenize(text)

      # Remove punctuation
      tokens = [word for word in tokens if word.isalnum()]

      return ' '.join(tokens)


# driver function
if __name__ == "__main__":
    app.run(debug=True)
