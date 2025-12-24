# Log Classification System

An end-to-end AI-powered log classification system that automatically categorizes log messages using multiple classification methods: regex patterns, BERT-based machine learning, and Large Language Models (LLMs).

## Features

- **Multi-Method Classification**: Combines regex, BERT, and LLM classifiers for robust log categorization
- **Web Interface**: User-friendly frontend for uploading CSV files and viewing results
- **API Backend**: FastAPI server for programmatic access
- **Flexible Processing**: Handles different log sources with specialized classifiers
- **Batch Processing**: Classify entire CSV files at once

## Project Structure

```
Log Classification System/
├── classify.py              # Main classification logic
├── server.py                # FastAPI backend server
├── processor_regex.py       # Regex-based classifier
├── processor_bert.py        # BERT-based ML classifier
├── processor_llm.py         # LLM-based classifier (for LegacyCRM)
├── test.csv                 # Sample test data
├── output.csv               # Classification results
├── Front_End/
│   ├── app.html            # Web interface
│   ├── app.js              # Frontend JavaScript
│   └── app.css             # Frontend styling
├── Models/
│   └── log_classifier.joblib  # Trained BERT model
└── Training/
    ├── log_classification.ipynb  # Training notebook
    └── dataset/
        └── synthetic_logs.csv    # Training data
```

## Installation

1. **Install Dependencies**:
   Make sure you have Python installed on your system. Install the required Python libraries by running the following command:

   ```bash
   pip install -r requirements.txt
   ```

2. For LLM classification, create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

## Usage

### Running the Server

Start the FastAPI server:
```bash
uvicorn server:app --reload
```

The server will run at `http://localhost:8000`

### Web Interface

1. Open `Front_End/app.html` in your browser
2. Upload a CSV file with columns: `source` and `log_message`
3. Click "Classify Logs" to process the file
4. Download the classified results

### API Usage

Send a POST request to `/classify/` with a CSV file containing `source` and `log_message` columns:

```bash
curl -X POST "http://localhost:8000/classify/" -F "file=@your_file.csv"
```

## Classification Methods

1. **Regex Classifier**: Uses predefined patterns for common log types (User Action, System Notification)
2. **BERT Classifier**: Machine learning model using sentence transformers for complex logs
3. **LLM Classifier**: Uses Groq API for LegacyCRM logs (Workflow Error, Deprecation Warning)

The system automatically selects the appropriate classifier based on the log source and content.

## Training

To retrain the BERT model:

1. Open `Training/log_classification.ipynb`
2. Run the notebook cells to train on the synthetic dataset
3. The trained model will be saved to `Models/log_classifier.joblib`

## Sample Data

The `test.csv` file contains sample log entries for testing. The `Training/dataset/synthetic_logs.csv` contains the training data with labeled examples.

## Dependencies

- fastapi: Web framework
- uvicorn: ASGI server
- pandas: Data processing
- sentence-transformers: BERT embeddings
- joblib: Model serialization
- groq: LLM API client
- python-dotenv: Environment variables

## License
This project is open-source. Feel free to use and modify as needed.

Some concepts and best practices used in this project were learned from online learning resources, including the Codebasics YouTube channel.
