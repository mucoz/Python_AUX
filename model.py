import os
import re
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.externals import joblib

# Define the keywords or phrases to extract
keywords = ['machine learning', 'natural language processing', 'deep learning']

# Function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

# Function to preprocess the text data
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenize text
    tokens = text.split()
    # Remove stopwords
    stop_words = set(['a', 'an', 'the', 'in', 'on', 'at', 'for', 'of', 'with', 'to', 'and', 'or', 'is', 'are', 'was', 'were', 'has', 'have', 'had', 'been'])
    tokens = [token for token in tokens if token not in stop_words]
    # Stem tokens
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    # Join tokens back into text string
    text = ' '.join(tokens)
    return text

# Function to label the data
def label_data(data_directory):
    data = []
    labels = []
    for filename in os.listdir(data_directory):
        if filename.endswith('.pdf'):
            file_path = os.path.join(data_directory, filename)
            text = extract_text_from_pdf(file_path)
            preprocessed_text = preprocess_text(text)
            data.append(preprocessed_text)
            # Label the data based on whether it contains the keywords or not
            if any(keyword in preprocessed_text for keyword in keywords):
                labels.append(1)
            else:
                labels.append(0)
    return data, labels

# Load the labeled data
data_directory = '/path/to/pdf/files'
data, labels = label_data(data_directory)

# Vectorize the data using TF-IDF
vectorizer = TfidfVectorizer()
vectorized_data = vectorizer.fit_transform(data)

# Split the data into training and testing sets
train_size = int(0.8 * len(labels))
train_data = vectorized_data[:train_size]
train_labels = labels[:train_size]
test_data = vectorized_data[train_size:]
test_labels = labels[train_size:]

# Train an SVM model
model = svm.SVC(kernel='linear')
model.fit(train_data, train_labels)

# Evaluate the model on the test set
test_predictions = model.predict(test_data)
precision = precision_score(test_labels, test_predictions)
recall = recall_score(test_labels, test_predictions)
f1 = f1_score(test_labels, test_predictions)
print('Precision:', precision)
print('Recall:', recall)
print('F1 Score:', f1)

# Save the trained model
model_file_path = '/path/to/model.pkl'
joblib.dump(model, model_file_path)










#################################################


import sys
import os
import re
import PyPDF2
from sklearn.externals import joblib

# Define the keywords or phrases to extract
keywords = ['machine learning', 'natural language processing', 'deep learning']

# Function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

# Function to preprocess the text data
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenize text
    tokens = text.split()
    # Remove stopwords
    stop_words = set(['a', 'an', 'the', 'in', 'on', 'at', 'for', 'of', 'with', 'to', 'and', 'or', 'is', 'are', 'was', 'were', 'has', 'have', 'had', 'been'])
    tokens = [token for token in tokens if token not in stop_words]
    # Stem tokens
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    # Join tokens back into text string
    text = ' '.join(tokens)
    return text

# Load the saved model
model_file_path = '/path/to/model.pkl'
model = joblib.load(model_file_path)

# Get the file path of the PDF file to predict on
pdf_file_path = sys.argv[1]

# Extract text from the PDF file and preprocess it
text = extract_text_from_pdf(pdf_file_path)
preprocessed_text = preprocess_text(text)

# Vectorize the preprocessed text using the same vectorizer used for training
vectorizer = joblib.load('/path/to/vectorizer.pkl')
vectorized_text = vectorizer.transform([preprocessed_text])

# Make a prediction using the trained model
prediction = model.predict(vectorized_text)[0]

# Print the prediction
if prediction == 1:
    print('The PDF file contains at least one of the keywords.')
else:
    print('The PDF file does not contain any of the keywords.')
