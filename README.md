# Mini Real Estate Analysis Chatbot (React + Django)

This project implements the Sigmavalue Full Stack Developer Assignment.

## Features

- Django backend with a preloaded Excel dataset (`dataset/Sample_data.xlsx`)
- Single endpoint: `POST /api/chat/` that accepts natural-language queries:
  - "Analyze Akurdi"
  - "Compare Ambegaon Budruk and Aundh demand trends"
  - "Show price growth for Akurdi over the last 3 years"
- Backend returns:
  - A natural-language summary (mock LLM-style text)
  - Chart JSON (years + demand/price)
  - Filtered table data
- React frontend:
  - Chat-style interface
  - Displays summary, chart (Chart.js), and filtered table
  - "Download Data" button to download filtered JSON

## Folder Structure

- `backend/` – Django project
- `frontend/` – React app
- `dataset/Sample_data.xlsx` – Excel data

## Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend runs at `http://localhost:8000/` and API base is `http://localhost:8000/api/`.

## Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs at `http://localhost:3000/` and talks to the backend at `http://localhost:8000/api`.

## Example Queries

- `Analyze Akurdi`
- `Compare Ambegaon Budruk and Aundh demand trends`
- `Show price growth for Akurdi over the last 3 years`

## Notes

- Summary text is generated with simple Python logic (mock LLM).
- Chart is powered by Chart.js via `react-chartjs-2`.
- Data processing uses `pandas` and reads the Excel at runtime via `api/data_loader.py`.
