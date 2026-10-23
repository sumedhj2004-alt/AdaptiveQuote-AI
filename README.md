Perfect. Paste this \*\*complete README\*\* into Notepad. It is written around the actual features you built—no exaggerated claims.



\# AdaptiveQuote AI



\### AI-Powered Transaction Risk Assessment, RAG Policy Intelligence \& Human Feedback System



AdaptiveQuote AI is an end-to-end intelligent transaction risk platform that combines \*\*Machine Learning, FastAPI, PostgreSQL, RAG, Ollama, human feedback, automated retraining, model versioning, and an interactive Streamlit dashboard\*\*.



The system analyzes transaction behavior, generates a risk score, provides an AI-powered explanation using business policy context, and continuously collects human feedback for future model improvement.



\---



\## 🚀 Key Features



\* \*\*ML-Based Risk Detection\*\*



&#x20; \* Calculates transaction risk scores from transaction behavior.

&#x20; \* Classifies transactions as `LOW`, `MEDIUM`, or `HIGH` risk.



\* \*\*AI Agent\*\*



&#x20; \* Uses Ollama/Llama for natural-language transaction analysis.

&#x20; \* Explains risk results and recommends whether human review is required.



\* \*\*RAG-Based Policy Intelligence\*\*



&#x20; \* Uses ChromaDB for policy document retrieval.

&#x20; \* Provides policy context to the AI Agent before generating recommendations.



\* \*\*Human Review \& Feedback\*\*



&#x20; \* Allows reviewers to mark transactions as legitimate, suspicious, or investigate.

&#x20; \* Stores human feedback in PostgreSQL and CSV.



\* \*\*Self-Learning Pipeline\*\*



&#x20; \* Combines historical and live human feedback.

&#x20; \* Builds a training dataset for future model retraining.



\* \*\*Safe Model Retraining\*\*



&#x20; \* Trains a candidate model using human feedback.

&#x20; \* Compares candidate performance against the active model.

&#x20; \* Rejects weaker models automatically.



\* \*\*Model Versioning\*\*



&#x20; \* Tracks model versions used for risk assessments.

&#x20; \* Stores model versions with risk assessment records.

&#x20; \* Maintains historical model versions.



\* \*\*PostgreSQL Database\*\*



&#x20; \* Stores transactions, risk assessments, AI interactions, human feedback, and model versions.



\* \*\*Streamlit Dashboard\*\*



&#x20; \* Risk analysis interface.

&#x20; \* AI Agent interaction.

&#x20; \* Human feedback submission.

&#x20; \* Recent risk assessments.

&#x20; \* Feedback history.

&#x20; \* System architecture view.



\---



\## 🏗️ System Architecture



```text

&#x20;                   User

&#x20;                     │

&#x20;                     ▼

&#x20;            Streamlit Dashboard

&#x20;                     │

&#x20;                     ▼

&#x20;                FastAPI API

&#x20;                /          \\

&#x20;               ▼            ▼

&#x20;        PostgreSQL       ML Risk Engine

&#x20;                             │

&#x20;                             ▼

&#x20;                        Risk Score

&#x20;                             │

&#x20;                             ▼

&#x20;                      AI Agent (Ollama)

&#x20;                        /          \\

&#x20;                       ▼            ▼

&#x20;                RAG / ChromaDB   Policy Context

&#x20;                       │

&#x20;                       ▼

&#x20;                 Human Review

&#x20;                       │

&#x20;                       ▼

&#x20;                Feedback Dataset

&#x20;                       │

&#x20;                       ▼

&#x20;               Automated Retraining

&#x20;                       │

&#x20;                       ▼

&#x20;                Candidate Evaluation

&#x20;                       │

&#x20;                ┌──────┴──────┐

&#x20;                ▼             ▼

&#x20;             Promote        Reject

&#x20;                │             │

&#x20;                └──────┬──────┘

&#x20;                       ▼

&#x20;                 Model Versioning

```



\---



\## 🧠 Machine Learning Pipeline



The risk engine uses transaction-level behavioral features including:



\* Transaction amount

\* Transaction hour

\* Previous transaction amount

\* Transaction frequency

\* Account age

\* Amount change ratio



The model produces:



```text

Risk Score → Risk Level → Model Version

```



Risk classification:



```text

0–30    → LOW

31–70   → MEDIUM

71–100  → HIGH

```



\---



\## 🔄 Human Feedback Learning Loop



The platform supports a continuous feedback workflow:



```text

Transaction

&#x20;    ↓

ML Risk Prediction

&#x20;    ↓

AI Agent Analysis

&#x20;    ↓

Human Review

&#x20;    ↓

Human Feedback

&#x20;    ↓

Training Dataset

&#x20;    ↓

Candidate Model

&#x20;    ↓

Performance Evaluation

&#x20;    ↓

Safety Gate

&#x20;    ↓

Model Promotion / Rejection

```



The model is \*\*not automatically replaced simply because retraining completed\*\*.



A candidate model must demonstrate improved performance before it can replace the active model.



\---



\## 🛡️ Model Safety Mechanism



The retraining pipeline compares the candidate model against the currently active model.



The system evaluates:



\* Accuracy

\* Precision

\* Recall

\* F1 Score

\* Confusion Matrix



The suspicious-class F1 score is used as the primary improvement criterion.



If the candidate performs worse, it is rejected.



Example from the final system test:



```text

Candidate Model

Accuracy: 0.80

Suspicious F1: 0.00



Active Model

Accuracy: 1.00

Suspicious F1: 1.00



Result:

Candidate rejected

Active model preserved

```



This prevents a weaker retrained model from automatically replacing the production model.



\---



\## 🗄️ Database



PostgreSQL stores the major system entities:



\### Transactions



Stores transaction-level behavioral information.



\### Risk Assessments



Stores:



\* Risk score

\* Risk level

\* Transaction ID

\* Model version

\* Timestamp



\### Agent Interactions



Stores:



\* User input

\* AI Agent response

\* Transaction reference

\* Timestamp



\### Human Feedback



Stores:



\* Human decision

\* Corrected risk information

\* Reviewer feedback

\* Risk assessment reference

\* Timestamp



\### Model Versions



Stores model evaluation and version information.



\---



\## 📊 Dashboard



The Streamlit dashboard provides:



\* Transaction analysis

\* ML risk scoring

\* AI Agent analysis

\* Human review submission

\* Recent risk assessments

\* Human feedback history

\* Database-backed project metrics

\* System architecture visualization



\---



\## 🛠️ Technology Stack



| Category          | Technology                 |

| ----------------- | -------------------------- |

| Programming       | Python                     |

| API               | FastAPI                    |

| Database          | PostgreSQL                 |

| ORM               | SQLAlchemy                 |

| Machine Learning  | Scikit-learn               |

| Data Processing   | Pandas                     |

| Model Persistence | Joblib                     |

| Generative AI     | Ollama / Llama             |

| RAG               | ChromaDB                   |

| Embeddings        | Sentence Transformers      |

| Dashboard         | Streamlit                  |

| API Testing       | Swagger / FastAPI Docs     |

| Environment       | Python Virtual Environment |



\---



\## 📁 Project Structure



```text

AdaptiveQuote-AI/

│

├── app/

│   ├── agent/

│   │   ├── agent.py

│   │   ├── human\_review.py

│   │   ├── tools/

│   │   │   ├── feedback\_tool.py

│   │   │   ├── policy\_tool.py

│   │   │   └── risk\_tool.py

│   │   └── data/

│   │

│   ├── ml/

│   │   ├── risk\_engine.py

│   │   ├── features.py

│   │   ├── feedback\_dataset.py

│   │   ├── retrain\_model.py

│   │   ├── version\_model.py

│   │   ├── review\_transactions.py

│   │   ├── data/

│   │   ├── models/

│   │   └── versions/

│   │

│   ├── rag/

│   │   ├── ingest.py

│   │   ├── semantic\_search.py

│   │   ├── documents/

│   │   └── chroma\_db/

│   │

│   ├── models/

│   │   └── database\_models.py

│   │

│   ├── api.py

│   ├── database.py

│   └── \_\_init\_\_.py

│

├── dashboard.py

├── README.md

└── .env

```



\---



\## ⚙️ Installation



Clone the repository:



```bash

git clone <your-github-repository-url>

cd AdaptiveQuote-AI

```



Create a virtual environment:



```bash

python -m venv .venv

```



Activate it on Windows:



```powershell

.venv\\Scripts\\activate

```



Install dependencies:



```bash

pip install -r requirements.txt

```



\---



\## 🔐 Environment Variables



Create a `.env` file and configure the PostgreSQL connection.



Example:



```env

DATABASE\_URL=postgresql://postgres:YOUR\_PASSWORD@localhost:5432/adaptivequote

```



Keep credentials private and \*\*never commit `.env` to GitHub\*\*.



\---



\## ▶️ Running the Application



\### Start FastAPI



```powershell

uvicorn app.api:app --reload

```



API documentation:



```text

http://127.0.0.1:8000/docs

```



\### Start Streamlit Dashboard



Open another terminal:



```powershell

streamlit run dashboard.py

```



The dashboard will open in the browser.



\---



\## 🔌 Main API Workflow



\### Risk Assessment



```text

POST /risk

```



Receives transaction information and returns:



\* Transaction ID

\* Risk Assessment ID

\* Risk Score

\* Risk Level

\* Model Version



\### AI Agent



```text

POST /agent

```



Uses:



\* Transaction information

\* ML Risk Tool

\* RAG Policy Context

\* Ollama AI



to generate an explainable risk assessment and human-review recommendation.



\### Health Check



```text

GET /health

```



Used to verify API availability.



\---



\## 🧪 Testing Performed



The system was tested end-to-end for:



\* API health

\* Transaction creation

\* Risk prediction

\* Risk assessment persistence

\* Model version tracking

\* AI Agent analysis

\* RAG policy integration

\* Human feedback submission

\* PostgreSQL feedback storage

\* Feedback dataset generation

\* Candidate model retraining

\* Candidate vs active model comparison

\* Safe model rejection

\* Streamlit dashboard integration



\---



\## 🎯 Project Objective



The goal of AdaptiveQuote AI is to demonstrate how an intelligent transaction-risk platform can combine:



\*\*Machine Learning + Generative AI + RAG + Human-in-the-Loop Learning + Data Engineering\*\*



into a single production-oriented workflow.



The project focuses not only on making predictions, but also on:



\* Explainability

\* Policy-aware AI decisions

\* Human oversight

\* Feedback-driven learning

\* Model governance

\* Safe model deployment



\---



\## 👨‍💻 Author



\*\*Sumedh Satish Jadhav\*\*



AI \& Data Science Undergraduate



Skills demonstrated:



`Python` • `SQL` • `Machine Learning` • `FastAPI` • `PostgreSQL` • `RAG` • `ChromaDB` • `Ollama` • `Streamlit` • `Data Engineering` • `Model Versioning`









