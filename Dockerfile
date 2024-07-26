# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the dependencies specified in the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Download the pre-trained model files
RUN pip install transformers sentence-transformers && \
    python -c "from transformers import BertForSequenceClassification; BertForSequenceClassification.from_pretrained('bert-base-uncased').save_pretrained('./smart_model')"

# Download NLTK data resources
RUN python -m nltk.downloader punkt stopwords wordnet

# Copy the rest of the application code into the container
COPY . .

# Expose port 5000 to allow outside access
EXPOSE 5000

# Specify the command to run the application
CMD ["python", "app.py"]
