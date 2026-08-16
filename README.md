# AI Study Helper

AI Study Helper is a Django document question-answering application. Upload a PDF, DOCX, or TXT file, ask a question in plain English, and receive a concise answer grounded in the relevant passages.

> **Upload. Ask. Understand.**

## Features

- Supports PDF, DOCX, and TXT uploads up to 15 MB
- Retrieves passages most relevant to each question
- Uses Groq for concise, document-grounded answers
- Shows supporting source passages for verification
- Keeps document and question history in the database
- Includes a responsive technical white-and-grey interface
- Continues to show source passages without an AI key

## How it works

1. A document is uploaded and its text is extracted.
2. The text is divided into overlapping passages.
3. The app ranks passages against the user's question.
4. Only the best matching passages are sent to the AI model.
5. The generated answer and sources are saved with the document.

This retrieval-first flow keeps the model focused on the uploaded document and reduces unsupported answers.

## Technology

| Area | Tools |
| --- | --- |
| Backend | Python, Django |
| AI | Groq, OpenAI-compatible Python SDK |
| Document parsing | pypdf, python-docx |
| Database | SQLite locally, PostgreSQL on Render |
| Production server | Gunicorn, WhiteNoise |
| Frontend | Django templates and custom CSS |

## Run locally

### Prerequisites

- Python 3.11 or newer
- A Groq API key (optional, but needed for AI-written answers)

### Setup

```powershell
git clone https://github.com/sparshmajotra/AI_study_helper-.git
cd "AI_study_helper-"

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a local secrets file:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and add a newly generated Groq key:

```env
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=openai/gpt-oss-120b
```

Run migrations and start the application:

```powershell
python manage.py migrate
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000).

> Keep `.env` private. It is excluded from Git and must never be committed.

## Test the project

```powershell
python manage.py check
python manage.py test
```

## Deploy to Render

The repository includes a `render.yaml` Blueprint that provisions a Django web service and PostgreSQL database.

1. In Render, choose **New → Blueprint** and connect this repository.
2. Select the `master` branch and deploy the Blueprint.
3. Open the `ai-study-helper` web service after both resources are ready.
4. In **Environment**, provide a value for `GROQ_API_KEY`.
5. Save with **Save, rebuild, and deploy**.
6. Open the generated `onrender.com` URL when deployment completes.

The Blueprint supplies the production database URL, generates a Django secret key, runs migrations, collects static files, and starts Gunicorn.

### Storage note

PostgreSQL stores the extracted text, documents, questions, and answers. Free Render web services use an ephemeral filesystem, so original uploaded files can be removed after a restart or redeploy. A persistent disk for the `media` directory is available on paid Render web services if retaining source files is required.

## Project structure

```text
config/                 Django settings and URL configuration
knowledge/              Upload, extraction, retrieval, and Q&A logic
templates/knowledge/    Django templates
static/knowledge/       Application stylesheet
build.sh                Render build command
render.yaml             Render Blueprint configuration
.env.example            Safe environment-variable template
```

## Security notes

- Store API keys only in `.env` locally or Render environment variables in production.
- Use `DJANGO_DEBUG=false` in production.
- Render generates the production `DJANGO_SECRET_KEY` through the Blueprint.
- Rotate any API key that has been accidentally shared.

## Author

Built by **Sparsh Majotra**.

## License

No license has been selected yet. Add one before distributing or reusing this project publicly.
