import nltk
nltk.download('stopwords') # download the stopwords corpus
nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token not in stop_words and token.isalpha()]
    return filtered_tokens

text = ""
print(result)