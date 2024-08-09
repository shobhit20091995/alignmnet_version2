# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 11:41:14 2024

@author: HP
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 01:43:24 2024

@author: HP
"""

import os
import boto3    
from botocore.exceptions import ClientError
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import torch.nn.functional as F
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from dotenv import load_dotenv
from flask import Flask, request, jsonify, abort


# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize the Flask application
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Fetch AWS credentials from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Check if credentials are correctly retrieved
if not aws_access_key_id or not aws_secret_access_key:
    raise ValueError("AWS credentials are not set in the environment variables.")

# Initialize the boto3 S3 client with environment variables
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='ap-southeast-2'
)

# Get the current working directory
current_directory = os.path.dirname(os.path.abspath(__file__))


# Define your bucket name and the path to the model files
bucket_name = 'intalign'
model_folder = 'smart_model/'  # Update this path based on your S3 bucket structure

local_model_dir = os.path.join(current_directory, 'smart_model')

# Create local directory if it does not exist
os.makedirs(local_model_dir, exist_ok=True)

print(f"The local model directory has been created at: {local_model_dir}")


def download_model_from_s3():
    try:
        # Check if the bucket exists
        s3.head_bucket(Bucket=bucket_name)
        print(f'Bucket "{bucket_name}" exists and is accessible.')

        # List all objects in the specified folder
        objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=model_folder)

        files_to_download = []

        # Check for missing files
        if 'Contents' in objects:
            for obj in objects['Contents']:
                key = obj['Key']
                file_name = os.path.relpath(key, model_folder)
                local_file_path = os.path.join(local_model_dir, file_name)
                
                if not os.path.exists(local_file_path):
                    files_to_download.append((key, local_file_path))

        # Download each missing file from the S3 bucket to the local directory
        if files_to_download:
            for key, local_file_path in files_to_download:
                local_dir = os.path.dirname(local_file_path)
                os.makedirs(local_dir, exist_ok=True)

                try:
                    s3.download_file(bucket_name, key, local_file_path)
                    print(f'Successfully downloaded {key}')
                except Exception as e:
                    print(f'Error downloading {key}: {e}')
        else:
            print('All files are already present locally.')

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchBucket':
            print(f'The bucket "{bucket_name}" does not exist.')
        else:
            print(f'Client error: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')

# Download the model from S3 when the application starts
download_model_from_s3()

# Load the tokenizer and model for SMART criteria
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained(local_model_dir, ignore_mismatched_sizes=True)

# Load the dataset from the uploaded Excel file
file_path = 'Updated_SMAT_Table.xlsx'
df = pd.read_excel(file_path)

# Normalize the titles in the dataframe for comparison
df['Title_normalized'] = df['Title'].str.lower().str.replace(' ', '').str.replace('-', '').str.replace('_', '')

# Function to preprocess text
def preprocess_text(text):
    text = re.sub(r'#\S+', '', text)  # Remove hashtags
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

# Load the model for similarity scoring
similarity_model = SentenceTransformer('all-MiniLM-L6-v2')

# Utility functions
def get_goal_scores(goal_title):
    normalized_title = goal_title.lower().replace(' ', '').replace('-', '').replace('_', '')
    goal_scores = df[df['Title_normalized'] == normalized_title]
    if goal_scores.empty:
        return None
    return {
        "specific": float(goal_scores['specific'].values[0]),
        "measurable": float(goal_scores['measurable'].values[0]),
        "achievable": float(goal_scores['achievable'].values[0]),
        "time_bound": float(goal_scores['time_bound'].values[0])
    }

def get_smart_scores(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    outputs = model(**inputs)
    logits = outputs.logits
    probs = torch.sigmoid(logits)
    return probs.detach().numpy()[0]

def evaluate_smart_criteria(title, text):
    scores = get_smart_scores(text)
    criteria = {
        "specific": float(scores[0]),
        "measurable": float(scores[1]),
        "achievable": float(scores[2]),
        "time_bound": float(scores[3])
    }

    goal_scores = get_goal_scores(title)
    if not goal_scores:
        return {
            "title": title,
            "text": text,
            "criteria_scores": {},
            "average_score": 0
        }

    selected_scores = {k: v for k, v in criteria.items() if goal_scores[k] != 0}
    average_score = float(sum(selected_scores.values()) / len(selected_scores)) if selected_scores else 0

    result = {
        "title": title,
        "text": text,
        "criteria_scores": selected_scores,
        "average_score": average_score
    }
    return result

@app.route('/evaluate_smat_criteria', methods=['POST'])
def evaluate_smart_criteria_api():
    request_data = request.get_json()
    artifact_name = request_data.get('artifactName')
    elements = request_data.get('elements', {})

    evaluation_results = []
    total_average_score = 0
    count_of_scores = 0

    def evaluate_nested_elements(main_title, elements):
        for key, value in elements.items():
            full_key = f"{main_title} - {key}"
            if isinstance(value, str):
                evaluation_result = evaluate_smart_criteria(main_title, value)
                evaluation_result["nested_key"] = key
                if evaluation_result["average_score"] > 0:
                    nonlocal total_average_score, count_of_scores
                    total_average_score += evaluation_result["average_score"]
                    count_of_scores += 1
                evaluation_results.append(evaluation_result)
            elif isinstance(value, dict):
                evaluate_nested_elements(full_key, value)

    for key, value in elements.items():
        if isinstance(value, str):
            evaluation_result = evaluate_smart_criteria(key, value)
            if evaluation_result["average_score"] > 0:
                total_average_score += evaluation_result["average_score"]
                count_of_scores += 1
            evaluation_results.append(evaluation_result)
        elif isinstance(value, dict):
            evaluate_nested_elements(key, value)

    overall_average_score = total_average_score / count_of_scores if count_of_scores else 0

    return jsonify({
        "evaluation_results": evaluation_results,
        "overall_average_score": overall_average_score
    })

# Initialize the Sentence-BERT model
alignment_model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to calculate similarity using Sentence-BERT
def calculate_similarity_sbert(a, b):
    embeddings1 = alignment_model.encode(a, convert_to_tensor=True)
    embeddings2 = alignment_model.encode(b, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embeddings1, embeddings2)
    return similarity.item()

# Function to check alignment within each artifact using Sentence-BERT
def check_alignment_sbert(artifact):
    alignment_results = {}
    section_averages = {}
    for section, content in artifact.items():
        if section == "artifactName":
            continue
        try:
            # Check for missing 'Master' or 'Slaves'
            if "Master" not in content:
                raise KeyError(f"Missing 'Master' in section: {section}")
            if "Slaves" not in content:
                raise KeyError(f"Missing 'Slaves' in section: {section}")

            master_content = content["Master"]
            slaves_content = content["Slaves"]

            for master_key, master_value in master_content.items():
                similarities = []
                for slave in slaves_content:
                    for slave_key, slave_value in slave.items():
                        similarity = calculate_similarity_sbert(master_value, slave_value)
                        similarities.append((slave_key, slave_value, similarity, master_value))
                alignment_results[(section, master_key)] = similarities
                total_similarity = sum(similarity for _, _, similarity, _ in similarities)
                average_similarity = total_similarity / len(similarities) if similarities else 0
                section_averages[section] = section_averages.get(section, []) + [average_similarity]

        except KeyError as e:
            # Return a dictionary with an error message
            return {
                "error": {
                    "message": str(e),
                    "type": "not found error",
                    "code": 404
                }
            }

    overall_averages = {section: sum(averages) / len(averages) for section, averages in section_averages.items()}
    return {"results": alignment_results, "averages": overall_averages}

@app.route('/analyze', methods=['POST'])
def check_alignment():
    input_data = request.json
    results = []
    for artifact in input_data["artifacts"]:
        artifact_name = artifact["artifactName"]
        response = check_alignment_sbert(artifact)

        # Check if there was an error
        if "error" in response:
            return jsonify(response["error"]), 404

        alignment_results = response["results"]
        overall_averages = response["averages"]

        artifact_result = {
            "artifactName": artifact_name,
            "alignmentResults": [],
            "overallAverages": overall_averages
        }
        for (section, master_key), similarities in alignment_results.items():
            artifact_result["alignmentResults"].append({
                "section": section,
                "masterKey": master_key,
                "averageSimilarity": sum(similarity for _, _, similarity, _ in similarities) / len(similarities),
                "similarities": [
                    {
                        "slaveKey": slave_key,
                        "slaveValue": slave_value,
                        "similarity": similarity,
                        "masterValue": master_value
                    } for slave_key, slave_value, similarity, master_value in similarities
                ]
            })
        results.append(artifact_result)
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
