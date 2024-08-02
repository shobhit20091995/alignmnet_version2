# Combined Flask Application

This project merges two separate Flask applications into one, with different API endpoints for evaluating SMART criteria and analyzing similarity scores. The project uses transformers, NLTK, and sentence-transformers libraries.

## API Endpoints

1. **http://localhost:5000/evaluate_smat_criteria**: Planner version and Evaluate Feasibility / SMART criteria.
2. **http://localhost:5000/analyze**: Analyze Similarity/Alignment scores.

## Requirements

- Docker
- Python 3.9

## Setup Instructions

1. **Build the Docker image:**

    ```sh
    docker build -t combined-app .
    ```

2. **Run the Docker container:**

    ```sh
    docker run -p 5000:5000 combined-app
    ```

## Endpoints Usage

### /evaluate_smat_criteria  -- PLANNER VERSION

**Request:**

- **Method:** POST
- **Content-Type:** application/json
- **Body:**
    ```json
Input file -- step_1_ProjectRequirements.json   AND step_2_ProjectScopeStatement.json

### /evaluate_smat_criteria  -- FEASIBILITY SMAT

**Request:**

- **Method:** POST
- **Content-Type:** application/json
- **Body:**
    ```json
Input file -- Input_fesibility_smat.json

### /analyze --  ALIGNMENT

**Request:**

- **Method:** POST
- **Content-Type:** application/json
- **Body:**
    ```json

Input file -- Input_alignment_master.json

## Dependencies

All dependencies are listed in the `requirements.txt` file. The main dependencies are:

- Flask==2.3.2
- nltk
- sentence-transformers
- pandas
- transformers==4.29.2
- torch==2.0.1
- numpy<2

## Notes

- Ensure Docker is installed and running on your system.
- The application will be available at `http://localhost:5000` after running the Docker container.
