# 🥗 Nutrition Assistant 🥗
*(a RAG-based Q&A chatbot for nutrition facts)*  

<p align="center">
  <img src="assets/cover.png" alt="AI Nutrition Assistant" width="500">
</p>

[Repository: VeraTorka/nutrition-assistant](https://github.com/VeraTorka/nutrition-assistant/tree/main)  
Final submission for [DataTalksClub LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) 2025  

A conversational RAG app that answers nutrition questions from a curated food table (macros, vitamins, minerals, allergens). It retrieves the most relevant rows and generates grounded answers.

[🎥 Watch demo on Loom](https://www.loom.com/share/9f5926a71e664dcb917bdfcab483765c?sid=4f09180d-2f2c-490f-a5d6-b54e1fceddab)


## 🎯 Overview – Problem Description (2 / 2)  
**Problem:**  

People often lack reliable nutrition facts for everyday foods, struggle to estimate macros for portions, and need quick substitutions that respect allergens. Generic chatbots can hallucinate values because they don’t ground answers in a verified dataset.

This problem is relevant for health-conscious users, dietitians, and app developers seeking reliable, explainable food data integrated with conversational AI.

**Solution:** 

Nutrition Assistant is a retrieval-augmented application that answers nutrition questions using a local, curated CSV knowledge base. It retrieves the most relevant food entries and composes concise, evidence-based responses, reducing hallucinations and speeding up decisions.

**Use cases**

- Look up macronutrients (kcal, protein, fat, carbs).
- Check vitamins & minerals (A, B6, B12, C, D, E, calcium, iron, potassium, magnesium, selenium, zinc, iodine).
- Review allergens (tree nuts, peanut, sesame, etc.).
- Ask free-form questions using Flask API.

**Example use cases:**

- "How much protein is in 100g of tofu?"
- "Which fruit has more vitamin C: apple or orange?"
- "Find dairy-free sources of calcium."
- "Compare calories between brown rice and quinoa."

---

## 📚 Dataset Description 

The dataset [`data/data.csv`](data/data.csv) consists of ~435 records, each representing a food item (plant-based, animal-based, snacks, supplements) normalized to 100 g serving.  
Columns include:  
- `food` – food name (e.g., Tofu scramble, Lentil stew, Salmon sandwich).  
- `serving_size_g`, `calories_kcal`, `protein_g`, `fat_g`, `carbohydrates_g`.  
- `vitamin_a_mg`, `vitamin_b6_mg`, `vitamin_b12_mg`, `vitamin_c_mg`, `vitamin_d_mg`, `vitamin_e_mg`.  
- `calcium_mg`, `iron_mg`, `potassium_mg`, `magnesium_mg`, `selenium_mg`, `zinc_mg`, `iodine_mg`.  
- `allergens` – common allergens in the product (e.g., Soy, Gluten, Milk, Egg, Fish, Shellfish).  

**Example row:**

| food | serving_size_g | calories_kcal | protein_g | fat_g | carbohydrates_g | vitamin_c_mg | calcium_mg | iron_mg | potassium_mg | allergens |
|------|----------------|----------------|------------|--------|------------------|----------------|-------------|------------|---------------|-------------|
| Apple | 100 | 52 | 0.3 | 0.2 | 14 | 4.6 | 6 | 0.1 | 107 | — |


The dataset was generated using [ChatGPT](https://chatgpt.com/share/68ee24bc-58a4-8009-919c-8fd5f42ba24e) and curated to realistic nutritional values.

---

## ⚙️ Project Architecture - Retrieval Flow (2 / 2) 

### High-level Flow
```text
User question
      ↓
Flask API
      ↓
Retriever — MinSearch (vector + text index)
      ↓
Relevant food records from CSV
      ↓
LLM (OpenAI gpt-4o-mini) → generates grounded answer
      ↓
Response returned to user
      ↓
Feedback stored in PostgreSQL
      ↓
Monitoring dashboards (Grafana)**
```

- The application uses **MinSearch** for full-text retrieval from the CSV dataset (via `ingest.py` and `rag.py`).  
- The top results are passed to the LLM (OpenAI) which composes an answer grounded in the retrieved context.  
- This combination of a knowledge base + LLM constitutes a full RAG (Retrieval-Augmented Generation) flow.

### Components Overview

| Component | Description |
|------------|-------------|
| **Flask API** | Serves endpoints `/question` and `/feedback`. Enables user interaction and feedback submission. |
| **MinSearch Retriever** | Lightweight local full-text + vector search engine for indexing food data and retrieving top-k relevant rows. |
| **OpenAI LLM** | Generates concise and factually grounded answers using retrieved records as context. |
| **PostgreSQL** | Stores all conversations and user feedback for later analysis. |
| **Grafana** | Optional monitoring layer — visualizes feedback statistics and retrieval quality metrics. |
| **Docker Compose** | Orchestrates the app, PostgreSQL, and Grafana containers for fully reproducible deployment. |

### Key Files

| File | Description |
|------|--------------|
| [`nutrition_assistant/app.py`](nutrition_assistant/app.py) | Main Flask API with endpoints `/question` and `/feedback`. Handles user queries and stores responses. |
| [`nutrition_assistant/ingest.py`](nutrition_assistant/ingest.py) | Loads `data/data.csv`, builds a MinSearch index, and prepares it for retrieval. |
| [`nutrition_assistant/rag.py`](nutrition_assistant/rag.py) | Core logic for Retrieval-Augmented Generation — retrieves relevant rows and queries the LLM. |
| [`nutrition_assistant/db.py`](nutrition_assistant/db.py) | Handles PostgreSQL connections, creates tables, and logs feedback and conversation data. |
| [`docker-compose.yaml`](/docker-compose.yaml) | Defines all containers — app, PostgreSQL, and Grafana — for full local deployment. |
| [`Dockerfile`](/Dockerfile) | Builds the application image with all dependencies. |
| [`data/data.csv`](data/data.csv) | Nutrition knowledge base containing 400+ verified food items with macro/micronutrient data. |
| [`notebooks/`](/notebooks/) | Jupyter notebooks for evaluation and experiments (`rag-test.ipynb`, `evaluation-data-generation.ipynb`). |
| [`test.py`](/test.py) | CLI script to send test queries to the Flask API and validate responses. |

---

## Experiments

For experiments, we use Jupyter notebooks. They are in the [`notebooks`](notebooks/) folder.
To start Jupyter, run:
```bash
cd notebooks
pipenv run jupyter notebook
```

We have the following notebooks:
- [`01-dataset, minsearch, rag.ipynb`](notebooks/01-dataset-minsearch-rag.ipynb): The RAG flow and evaluating the system.
- [`02-eval-data-gen.ipynb`](notebooks/02-eval-data-gen.ipynb): Generating the ground truth dataset for retrieval evaluation.

### 🔎 Retrieval Evaluation (MinSearch) (2 / 2)  

Retrieval evaluation was performed using a ground truth dataset ([`ground-truth-retrieval.csv`](data/ground-truth-retrieval.csv) of 200 queries and LLM-based validation to ensure the correctness of retrieved results: 
- Baseline retrieval: Hit Rate = 0.89, MRR = 0.74  
- Tuned retrieval (with boosting weights): Hit Rate = 0.92, MRR = 0.77  

Boost weights used for fields (food, serving_size_g, etc.) are listed below
The best boosting parameters:

```python
boost = {'food': 3.00,
          'serving_size_g': 0.45,
          'calories_kcal': 0.32,
          'protein_g': 2.86,
          'fat_g': 1.10,
          'carbohydrates_g': 2.11,
          'vitamin_a_mg': 0.91,
          'vitamin_b6_mg': 1.38,
          'vitamin_b12_mg': 2.64,
          'vitamin_c_mg': 2.90,
          'vitamin_d_mg': 1.30,
          'vitamin_e_mg': 0.09,
          'calcium_mg': 0.91,
          'iron_mg': 2.44,
          'potassium_mg': 0.03,
          'magnesium_mg': 2.03,
          'selenium_mg': 2.78,
          'zinc_mg': 1.70,
          'iodine_mg': 1.67,
          'allergens': 0.21
        }
```
The results were consistent across runs, confirming that the tuned retrieval pipeline is both accurate and deterministic (reproducible scores).

### 🤖 RAG Flow Evaluation (LLM-as-a-Judge) (2 / 2)  

Responses were evaluated using an LLM-as-judge metric:  
| Model        | RELEVANT | PARTLY_RELEVANT | NON_RELEVANT |
|--------------|----------|-----------------|-------------|
| gpt-4o-mini  | 163 (81,5%)   | 34 (17%)         | 3 (1.5%) %       |
| gpt-4o       | 161 (80,5%)   | 33 (16,5%)          | 6 (3%) %       |  

Because the difference was minimal (~1 %), gpt-4o-mini was selected for the project.

Several prompt templates were tested — including "direct answer", "chain-of-thought", and "compare foods" variants — and the most concise, grounded prompt was selected based on LLM-judge feedback.

### Evaluation Summary

**Multiple retrieval approaches tested**  
Different MinSearch configurations were compared — with and without boosting.  
**Quantitative and qualitative metrics computed**  
Both numeric metrics (Hit Rate, MRR) and human/LLM-based relevance judgments were used.  
**Best configuration selected and documented**  
The optimized boosting version (Hit Rate = 0.92, MRR = 0.77) was adopted for the final RAG flow.  

---

## 💻 Interface & User Interaction (2/2)

The application offers to interact with the RAG system — via **Flask API endpoints** 

### Flask API

The main entry point is [`app.py`](nutrition_assistant/app.py). It exposes two endpoints:

| Endpoint | Method | Description |
|-----------|---------|--------------|
| `/question` | `POST` | Accepts a user question and returns the grounded answer. |
| `/feedback` | `POST` | Collects user feedback |

**Example 1 - Asking a Question**
```bash
URL=http://localhost:5000
QUESTION="What is the vitamin C content in a 100g apple compared to an orange?"
DATA='{
    "question": "'${QUESTION}'"
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${DATA}" \
    ${URL}/question
```

**Response**
```json
{
  "answer": "In a 100g apple, the vitamin C content is 4.6 mg, while in an orange it is 53.2 mg.",
  "conversation_id": "b9b88e9a-b21f-47b8-b1e3-213f57f62d2e",
  "question": "What is the vitamin C content in a 100g apple compared to an orange?"
}
```

**Example 2 - Sending Feedback**
```bash
ID="b9b88e9a-b21f-47b8-b1e3-213f57f62d2e"
URL=http://localhost:5000
FEEDBACK_DATA='{
    "conversation_id": "'${ID}'",
    "feedback": 1
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${FEEDBACK_DATA}" \
    ${URL}/feedback
```

**Response**
```json
{
  "message": "Feedback received for conversation b9b88e9a-b21f-47b8-b1e3-213f57f62d2e: 1"
}
```
## Ingestion pipeline (2/2)

The ingestion logic is implemented in [`ingest.py`](nutrition_assistant/ingest.py).
The ingestion process is lightweight and re-runs on each container restart, ensuring the index always reflects the latest version of the CSV dataset.

| Component | Description |
|------------|--------------|
| **Source data** | CSV dataset (`data/data.csv`) with food, macronutrient, and micronutrient details. |
| **Process** | The file is automatically loaded and indexed via MinSearch when the app starts. |
| **Indexing** | MinSearch builds a lightweight semantic index in memory for fast retrieval. |
| **Automation** | The ingestion runs automatically when the Flask app starts — no manual steps required. |

**Pipeline entrypoint:**
```python
index = ingest.load_index()
```
---

## 🧭 Monitoring (1/2 — Grafana connected but dashboards not working)

Monitoring in the **Nutrition Assistant** project is partially implemented —  
Grafana is successfully connected but dashboards are not yet functional.

### Current Architecture

| Component | Description |
|------------|--------------|
| **PostgreSQL** | Stores all RAG interactions and user feedback. |
| **Grafana** | Connected via Docker Compose to visualize metrics from PostgreSQL. |
| **Flask API** | Logs every conversation and feedback entry automatically. |

### What Works
✅ Grafana container runs correctly and connects to PostgreSQL.  
✅ PostgreSQL tables `conversations` and `feedback` are populated in real time.  
✅ The `/feedback` endpoint allows users to send evaluations directly from the app.  
✅ Data can be queried manually from PostgreSQL for analysis.  

Example query:
```sql
SELECT COUNT(*) AS total_feedback,
       SUM(CASE WHEN feedback > 0 THEN 1 ELSE 0 END) AS positive,
       SUM(CASE WHEN feedback < 0 THEN 1 ELSE 0 END) AS negative
FROM feedback;
```

### What Doesn’t Work
⚠️ Grafana dashboards do not display visualizations.  
⚠️ Dashboard provisioning files are present but not automatically loaded.  
⚠️ No configured panels for metrics such as latency, cost, or satisfaction.  

In other words, **Grafana is connected but not visualizing** —  
the data pipeline is functional, but the dashboard layer needs setup.

**Future work** includes Grafana dashboards to visualize feedback ratio over time, token usage, and average LLM cost per request.
All data required for these panels are already collected in PostgreSQL.

### Monitoring Summary

| Aspect | Status | Notes |
|--------|---------|-------|
| Data collection | ✅ | Conversations and feedback logged in PostgreSQL |
| Grafana connection | ✅ | Configured and running |
| Dashboards | ⚠️ | Not rendering panels yet |
| Visualization | ❌ | No metrics visible in Grafana UI |

---

## 🐳 Containerization (2/2)

All services (Flask API, PostgreSQL, and Grafana) are containerized and orchestrated via Docker Compose.
Each container is isolated yet networked within the same environment, ensuring easy setup and teardown for reproducibility.

Containerization in the **Nutrition Assistant** project ensures reproducibility, isolated environments,  
and simplified deployment using **Docker** and **Docker Compose**.

### Docker Structure

| Service | Description |
|----------|--------------|
| **app** | Flask-based RAG API service. Handles ingestion, retrieval, and feedback collection. |
| **postgres** | Stores all conversation logs and user feedback for monitoring and evaluation. |

The application image is built using a lightweight Python 3.12 base image and pipenv for dependency management.

---

## 🔁 Reproducibility

The **Nutrition Assistant** project is fully reproducible — any evaluator can clone, configure, and run it locally in minutes without additional setup beyond Docker and an OpenAI API key.

This project was verified on both local Docker and GitHub Codespaces environments, ensuring cross-platform reproducibility

#### Step 1: Clone the Repository

```bash
git clone https://github.com/VeraTorka/nutrition-assistant.git
cd nutrition-assistant
```
This will download the entire project, including all necessary files:
- nutrition_assistant/ — source code
- data/ — dataset (data.csv)
- notebooks/ — evaluation notebooks
- docker-compose.yaml and Dockerfile — for container setup
- .envrc_template — environment configuration sample

#### 🔹 Step 2: Configure Environment Variables

The application requires access to your **OpenAI API key** and PostgreSQL connection details.  
These variables are loaded automatically when using Docker or `direnv`.

1. **Copy the environment template:**
```bash
   cp .envrc_template .envrc
```
2. **Open .envrc and fill in your keys and credentials:**
```bash 
   export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
   export POSTGRES_DB=nutrition
   export POSTGRES_USER=postgres
   export POSTGRES_PASSWORD=postgres
   export GRAFANA_ADMIN_USER=admin
   export GRAFANA_ADMIN_PASSWORD=admin
```
3. **CLoad the environment variables:**
```bash 
    direnv allow
```
or manually:
```bash 
    source .envrc
```

#### Step 3: Install Dependencies (Optional Local Run)

If you want to run the application **locally (without Docker)** — use **Pipenv** to install all dependencies in an isolated environment.

1. **Install Pipenv (if not installed):**
```bash
   pip install pipenv
  ```
2. **Install project dependencies (including dev tools):**
```bash
   pipenv install --dev
  ```
3. **Activate the virtual environment:**
```bash
   pipenv shell
  ```
4. **Run the Flask app locally:**
```bash
   python nutrition_assistant/app.py
  ```
5. **Access the API:**
Open your browser or use curl:
```bash
   http://localhost:5000
  ```

#### Using `requests`

When the application is running, you can use [requests](https://requests.readthedocs.io/en/latest/) to send questions—use [test.py](test.py) for testing it:

```bash
pipenv run python test.py
```

It will pick a random question from the ground truth dataset
and send it to the app.


#### CURL

You can also use `curl` for interacting with the API:

```bash 
URL=http://localhost:5000
QUESTION="What is the vitamin C content in a 100g apple compared to an orange?"
DATA='{
    "question": "'${QUESTION}'"
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${DATA}" \
    ${URL}/question
```
You will see something like the following in the response:

```json 
   {
  "answer": "In a 100g apple, the vitamin C content is 4.6 mg, while in a 100g orange, it is 53.2 mg. Therefore, the orange contains significantly more vitamin C than the apple.",
  "conversation_id": "11cd00f0-8def-45ca-896d-91fad2d76e84",
  "question": "What is the vitamin C content in a 100g apple compared to an orange?"
}
```
Sending feedback:

```bash
ID="11cd00f0-8def-45ca-896d-91fad2d76e84"
URL=http://localhost:5000
FEEDBACK_DATA='{
    "conversation_id": "'${ID}'",
    "feedback": 1
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${FEEDBACK_DATA}" \
    ${URL}/feedback
```
After sending it, you'll receive the acknowledgement:

```json
{
  "message": "Feedback received for conversation d60e2b16-ee87-406f-a589-91dd7a25e11a: 1"
}
```

#### Step 4: Run via Docker (Recommended)

The easiest and most reliable way to reproduce this project is via **Docker Compose**.  
This setup automatically starts all components — Flask API, PostgreSQL, and Grafana.

1. **Build and start containers:**
```bash
   docker compose up --build
```
This command:
- Builds the Docker image for the app (nutrition-assistant-app)
- Starts PostgreSQL and Grafana containers
- Connects them through a shared Docker network

2. **Check that all services are running:**
```bash
   docker ps
```
You should see:
nutrition-assistant-app
nutrition-assistant-postgres
nutrition-assistant-grafana

3. **Access the Running Services**

Once all containers are up, you can access each component using the following URLs and ports:

| Service       | URL / Address              | Description                          |
|----------------|----------------------------|--------------------------------------|
| **Flask API**  | [http://localhost:5000](http://localhost:5000) | RAG-based nutrition assistant (main application) |
| **Grafana**    | [http://localhost:3000](http://localhost:3000) | Optional monitoring dashboard for feedback metrics |
| **PostgreSQL** | `localhost:5432`          | Database storing conversations and feedback logs |

*Tip:*  
If running inside GitHub Codespaces, replace `localhost` with your forwarded port link (e.g., `https://<your-codespace-id>-5000.app.github.dev`).

4. **View logs (optional):**
```bash
   docker logs nutrition-assistant-app
   docker logs nutrition-assistant-postgres
   docker logs nutrition-assistant-grafana
```

5. **Stop the containers:**
```bash
   docker compose down
```
To remove all data volumes as well (Postgres + Grafana data):
```bash
   docker compose down -v
```
--- 

## 🧠 Best Practices and Bonus Points

| Practice | Description | Points |
|-----------|--------------|--------|
| **Hybrid Search** | Combined keyword and semantic (boost-weighted) retrieval using MinSearch | ✅ +1 |
| **Prompt Optimization** | Multiple LLM prompts evaluated to find the most relevant and grounded answer style | ✅ +1 |
| **Reproducible Evaluation** | Consistent retrieval metrics (Hit Rate, MRR) across runs and environments | ✅ +1 |
| **Cloud-ready Deployment** | Fully containerized setup, compatible with Codespaces or any cloud VM | ✅ +2 |
