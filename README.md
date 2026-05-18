# AI Data Analyst Assistant

This project is a Streamlit web app that lets you upload a CSV file, inspect the dataset, generate AI insights with Groq, and ask questions about the data.

Live Denmo: https://ai-data-analyst-assistant-evvjnmmbs7gzvk9i7dygkh.streamlit.app/

## Features

- Upload CSV datasets
- View dataset preview, shape, types, missing values, and numeric statistics
- Generate AI-based analysis using Groq
- Ask custom questions about the uploaded dataset
- Show a basic numeric column distribution chart

## Project Files

- `app2.py` - main Streamlit application
- `requirements.txt` - Python dependencies
- `.gitattributes` - files that should not be pushed to GitHub

## Run Locally

1. Create and activate a virtual environment
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a Streamlit secrets file at `.streamlit/secrets.toml`

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

4. Start the app:

```bash
streamlit run app2.py
```

## Deploy On Streamlit Community Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Choose your repository
4. Set the main file path to `app2.py`
5. In app settings, add a secret named `GROQ_API_KEY`
6. Deploy

## Important

Do not hardcode API keys in the source code or push them to GitHub.

