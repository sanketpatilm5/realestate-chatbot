# Real Estate Analysis Chatbot  
**Full Stack Developer Assignment – Sigmavalue**

🚀 **Live Frontend:** https://realestate-chatbot-lovat.vercel.app  
🔗 **Backend API:** https://realestate-chatbot-fdpo.onrender.com/api/

---

## 📖 Project Overview
This chatbot helps analyze real estate market trends based on area queries using Excel dataset inputs.  
It provides:
- AI-style summary
- Interactive chart
- Filtered table
- Location comparison
- Data download functionality

---

## 🏗️ Tech Stack

| Layer | Technology |
|------|------------|
| Frontend | React, Bootstrap, Chart.js |
| Backend | Django REST Framework |
| Data Processing | Pandas |
| Deployment | Render (Backend), Vercel (Frontend) |
| Optional | OpenAI API Integration (mocked summary) |

---

## 🚀 Features

- 🔍 Query area analysis (`Analyze Akurdi`)
- 🔁 Compare two locations (`Compare Wakad and Aundh demand trends`)
- 📊 View price/demand trends across years
- 📃 Display filtered data tables
- 📥 Download JSON data
- 🧠 Natural language understanding

---

## 📂 Project Structure

```
real-estate-chatbot/
├── backend/
│   ├── api/
│   ├── config/
│   ├── requirements.txt
│   └── data_loader.py
├── frontend/
│   ├── src/
│   ├── .env
│   └── package.json
└── README.md
```

---

## 🧪 Example API Use

### 🔹 Single Query
```json
POST /api/chat/
{
  "query": "Analyze Akurdi"
}
```

### 🔹 Comparison
```json
POST /api/chat/
{
  "query": "Compare Wakad and Aundh demand trends"
}
```

---

## 🛠️ Run Locally

### 1️⃣ Clone & navigate
```bash
git clone <your-repo-url>
cd real-estate-chatbot
```

### 2️⃣ Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3️⃣ Frontend Setup
```bash
cd ../frontend
npm install
npm start
```

---

## 🌍 Deployment

| Component | Platform | Status |
|-----------|----------|--------|
| Frontend | Vercel | ✔ Live |
| Backend | Render | ✔ Live |

Changes pushed to GitHub redeploy automatically.

---


## 👤 Author

**Sanket Vasant Patil**  
📧 Contact: sanketpatil.m5@gmail.com 
🧑‍💻 Aspiring Full Stack Developer

---

## 📌 Notes
- Excel dataset: `Sample_data.xlsx`
- Mock summary used (easy upgrade to LLM)
- Production-ready deployment setup

---


