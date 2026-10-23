# AdaptiveQuote-AI 🤖
 AI-Powered Financial Transaction Risk Assessment & Decision Support System

**AdaptiveQuote-AI** is an end-to-end AI system designed to assess financial transaction risk and support business decision-making.

The project combines **Machine Learning, FastAPI, PostgreSQL, RAG, LLM-based AI Agents, Human-in-the-Loop Feedback, Model Retraining, and Model Versioning** into a single workflow.

Instead of stopping at a machine-learning prediction, the system creates a feedback loop where human decisions can be collected, evaluated, and used to improve future models safely.

---

## 🚀 Key Features

* 🔍 Machine Learning-based transaction risk detection
* 📊 Risk score generation with **LOW / MEDIUM / HIGH** classification
* ⚡ FastAPI REST API for transaction analysis
* 🗄️ PostgreSQL database for transactions, risk assessments, feedback, and model versions
* 🤖 AI Agent powered by **Ollama / Llama**
* 📚 Retrieval-Augmented Generation using **ChromaDB**
* 📖 Policy-aware AI responses using retrieved business rules
* 👤 Human review and feedback workflow
* 🔄 Feedback-driven model retraining
* 🛡️ Evaluation-based model promotion
* 📦 Model versioning and registry
* 📈 Interactive Streamlit dashboard
* 🔗 Complete ML + API + Database + AI workflow

---

## 🏗️ System Architecture

``
                         User
                          │
                          ▼
                Streamlit Dashboard
                          │
                          ▼
                     FastAPI API
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
       ML Risk Engine              PostgreSQL
             │                         │
             ▼                         │
       Risk Assessment ◄───────────────┘
             │
             ▼
          AI Agent
        ┌────┴────┐
        ▼         ▼
       RAG     Risk Tool
        │         │
        ▼         ▼
    ChromaDB   ML Model
        │
        ▼
   Policy Context
        │
        ▼
      AI Analysis
        │
        ▼
    Human Review
        │
        ▼
   Feedback Dataset
        │
        ▼
   Model Retraining
        │
        ▼
    Evaluation Gate
       /       \
      ▼         ▼
  Promote     Reject
     │           │
     ▼           ▼
New Version   Keep Active
    Model         Model
```

---

## 🔄 How It Works

### 1. Transaction Input

A transaction is submitted through the Streamlit dashboard or FastAPI API.

The system stores transaction information such as:

* Transaction amount
* Transaction hour
* Previous transaction amount
* Transaction frequency
* Account age

### 2. Feature Engineering

The ML pipeline creates derived features such as:

```text
amount_change_ratio
```

These features are passed to the trained anomaly detection model.

### 3. Risk Prediction

The ML model generates a probability-based risk score.

The score is converted into:

```text
0–30     → LOW
31–70    → MEDIUM
71–100   → HIGH
```

The system also records the active model version.

### 4. AI Agent Analysis

The AI Agent combines:

* ML risk prediction
* Retrieved policy information
* Transaction context

to provide a business-oriented explanation of the risk assessment.

### 5. Human Review

High-risk or questionable transactions can be reviewed by a human.

The reviewer can provide decisions such as:

```text
Legitimate
Suspicious
Investigate
```

### 6. Feedback & Retraining

Human feedback is added to the training dataset.

The retraining pipeline evaluates the new candidate model against the active model.

A candidate model is promoted only when it satisfies the defined evaluation criteria.

Otherwise, the existing production model remains active.

---

## 🛡️ Safe Model Retraining

The project uses a simple model safety mechanism to prevent an automatically retrained model from replacing a better-performing active model.

```text
Human Feedback
       │
       ▼
Training Dataset
       │
       ▼
Candidate Model
       │
       ▼
Model Evaluation
       │
       ▼
Compare with Active Model
       │
   ┌───┴────┐
   ▼        ▼
Better    Not Better
   │        │
   ▼        ▼
Promote   Reject
```

This demonstrates a basic **MLOps-style model promotion workflow** rather than blindly replacing the production model.

---

## 👤 Human-in-the-Loop

The system supports human validation of AI decisions.

Human feedback is stored in both the application data layer and PostgreSQL database.

This enables the system to maintain a feedback history and prepare reviewed data for future model training.

---

## 🗄️ Database Design

PostgreSQL stores the main application data.

### Main Tables

| Table                | Purpose                                         |
| -------------------- | ----------------------------------------------- |
| `transactions`       | Stores transaction information                  |
| `risk_assessments`   | Stores ML risk predictions                      |
| `agent_interactions` | Stores AI Agent interactions                    |
| `human_feedback`     | Stores reviewer decisions                       |
| `model_versions`     | Stores model evaluation and version information |

---

## 🛠️ Technology Stack

| Category         | Technologies                    |
| ---------------- | ------------------------------- |
| Programming      | Python                          |
| API              | FastAPI                         |
| Database         | PostgreSQL                      |
| ORM              | SQLAlchemy                      |
| Machine Learning | Scikit-learn                    |
| Data Processing  | Pandas                          |
| Model Storage    | Joblib                          |
| AI Agent         | Ollama, Llama                   |
| RAG              | ChromaDB, Sentence Transformers |
| Dashboard        | Streamlit                       |
| API Testing      | Swagger / OpenAPI               |
| Version Control  | Git, GitHub                     |

---

## 📁 Project Structure

```text
AdaptiveQuote-AI/
│
├── app/
│   ├── agent/
│   │   ├── agent.py
│   │   ├── human_review.py
│   │   ├── tools/
│   │   │   ├── feedback_tool.py
│   │   │   ├── policy_tool.py
│   │   │   └── risk_tool.py
│   │   └── data/
│   │
│   ├── ml/
│   │   ├── features.py
│   │   ├── risk_engine.py
│   │   ├── feedback_dataset.py
│   │   ├── retrain_model.py
│   │   ├── review_transactions.py
│   │   └── version_model.py
│   │
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── semantic_search.py
│   │   └── documents/
│   │
│   ├── models/
│   │   └── database_models.py
│   │
│   ├── api.py
│   └── database.py
│
├── dashboard.py
├── create_tables.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sumedhj2004-alt/AdaptiveQuote-AI.git
cd AdaptiveQuote-AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows:

```powershell
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file and configure the required PostgreSQL database connection.

Example:

```env
DATABASE_URL=your_postgresql_connection_string
```

Keep `.env` private and do not commit it to GitHub.

---

## ▶️ Running the Application

### Start FastAPI

```bash
uvicorn app.api:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Start Streamlit Dashboard

Open another terminal:

```bash
streamlit run dashboard.py
```

The dashboard provides:

* Transaction selection
* AI Agent analysis
* Risk analysis
* Human review
* Feedback submission
* Risk assessment history
* Feedback history
* System architecture overview

---

## 🧪 Testing

The project includes testing and validation for:

* Feature engineering
* ML model prediction
* Risk scoring
* FastAPI endpoints
* AI Agent workflow
* Human feedback storage
* Feedback dataset generation
* Model retraining
* Model versioning
* Database operations

The retraining workflow also verifies whether a candidate model improves upon the active model before promotion.

---

## 💼 Business Value

AdaptiveQuote-AI demonstrates how an AI system can be integrated into a real operational workflow.

The project focuses on:

* Automated risk assessment
* AI-assisted decision support
* Policy-aware AI responses
* Human-in-the-loop validation
* Data persistence
* API-based architecture
* Feedback-driven improvement
* Model evaluation
* Safe model deployment practices

This makes the project relevant to **AI/ML Engineering, Data Engineering, Data Science, MLOps, and AI Agent** roles.

---

## 🎯 Project Objective

The primary objective of AdaptiveQuote-AI is to demonstrate the development of a production-style AI application that connects:

**Data → Machine Learning → API → Database → RAG → AI Agent → Human Feedback → Retraining → Model Versioning**

The project emphasizes not only model prediction, but also the engineering workflow required to build a complete AI-enabled application.


🔐 Security

Sensitive information and generated artifacts are excluded from version control using `.gitignore`.

The repository does **not** include:

* `.env` files
* API keys
* Passwords
* Local virtual environments
* Generated ChromaDB databases
* Trained `.pkl` model artifacts
* Python cache files


👨‍💻 Author

Sumedh Satish Jadhav

AI & Data Science Undergraduate

Interested in:

* Data Engineering
* Machine Learning
* Artificial Intelligence
* Data Analytics
* MLOps
* AI Agents
* Business Intelligence


⭐ If you find this project useful, consider giving the repository a star.
