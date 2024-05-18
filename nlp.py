import spacy
from textblob import TextBlob
import rake_nltk
import nltk

# Ensure that the necessary NLTK data is downloaded
nltk.download('stopwords')
nltk.download('punkt')

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def process_text(text):
    doc = nlp(text)
    
    # Tokenization
    tokens = [token.text for token in doc]
    
    # Part-of-Speech Tagging
    pos_tags = [(token.text, token.pos_) for token in doc]
    
    # Named Entity Recognition (NER)
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    
    # Sentiment Analysis
    sentiment = TextBlob(text).sentiment
    
    # Keyword Extraction
    rake_nltk_var = rake_nltk.Rake()
    rake_nltk_var.extract_keywords_from_text(text)
    keywords = rake_nltk_var.get_ranked_phrases()
    
    return {
        "tokens": tokens,
        "pos_tags": pos_tags,
        "entities": entities,
        "sentiment": sentiment,
        "keywords": keywords
    }