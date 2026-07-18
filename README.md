# AI Study Helper

AI Study Helper is a Django web application that lets you upload a document and ask clear, natural-language questions about it. It finds the most relevant parts of your document, then uses Groq AI to create a short, easy-to-read answer grounded in those passages.

> Upload a file. Ask a question. Understand the answer.

## Features

- Upload **PDF**, **DOCX**, and **TXT** documents (up to 15 MB)
- Ask questions about one uploaded document at a time
- Retrieve the most relevant document passages before answering
- Generate concise answers in simple language with Groq
- View the supporting source passages for each answer
- Keep recent documents and question history in a local SQLite database
- Responsive, technical white-and-grey interface
- Works without an AI key: relevant source passages remain available

## How it works

1. The document text is extracted when the file is uploaded.
2. The app breaks the text into manageable passages.
3. For each question, it selects the passages most related to the question.
4. Groq receives only those passages and is instructed to answer using them alone.
5. The answer and its source passages are saved with the document.

This retrieval-first approach keeps answers tied to the uploaded file instead of relying on general AI knowledge.

## Tech stack

- **Backend:** Python and Django
- **Database:** SQLite
- **AI provider:** Groq (OpenAI-compatible API)
- **Document parsing:** `pypdf` and `python-docx`
- **Frontend:** Django templates and custom CSS

## Quick start

### 1. Clone the repository

```powershell
git clone https://github.com/sparshmajotra/AI_study_helper-.git
cd "AI_study_helper-"
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Add your Groq API key

Create your local environment file:

```powershell
Copy-Item .env.example .env
```

Open `.env` and add a newly generated Groq key:

```env
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.3-70b-versatile
```

Never commit `.env` or share its contents. The project’s `.gitignore` already excludes it.

### 5. Prepare the database and run the app

```powershell
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Using the application

1. Upload a PDF, DOCX, or TXT file.
2. Enter a focused question, such as *“What are the main conclusions?”*
3. Read the concise answer.
4. Expand **View source passages** when you want to check where the answer came from.

If you see a message saying that an AI-generated summary is unavailable, confirm that `.env` exists beside `manage.py`, contains a valid `GROQ_API_KEY`, and restart the Django server.

## Project structure

```text
config/                 Django configuration and environment settings
knowledge/              Upload, retrieval, question-answering, and data models
templates/knowledge/    User interface templates
static/knowledge/       Application styles
.env.example            Safe environment-variable template
requirements.txt        Python dependencies
```

## Running tests

```powershell
python manage.py test
```

## Deploy on Render

This repository includes `render.yaml` and `build.sh` for Render deployment.

1. In Render, select **New → Blueprint** and connect this GitHub repository.
2. Render detects `render.yaml`; create the `ai-study-helper` web service and database.
3. In the web service’s **Environment** page, add `GROQ_API_KEY` with a newly generated Groq key. Do not add it to GitHub.
4. Create a persistent disk mounted at `/opt/render/project/src/media` if you want uploaded source files kept between deployments.
5. Deploy. Render generates `DJANGO_SECRET_KEY`, configures the build command, and runs migrations automatically.

For manual setup, use `bash build.sh` as the build command and `gunicorn config.wsgi:application` as the start command. Set `DJANGO_DEBUG=false`; Render supplies `RENDER_EXTERNAL_HOSTNAME` automatically, which this project allows as a Django host.

## Notes for deployment

Before deploying, set `DJANGO_DEBUG=false`, use a strong `DJANGO_SECRET_KEY`, configure `DJANGO_ALLOWED_HOSTS`, and replace SQLite with a production database when needed. Store API keys in your hosting platform’s secret manager rather than in source files.

## License

This project is currently provided without a license. Add one before distributing or reusing it publicly.
