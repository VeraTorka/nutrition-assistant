# 🥗 Nutrition Assistant 🥗
*(a RAG-based Q&A chatbot for nutrition facts)*  

[Repository: VeraTorka/nutrition-assistant](https://github.com/VeraTorka/nutrition-assistant/tree/main)  
Final submission for [DataTalksClub LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) 2025  

A conversational RAG app that answers nutrition questions from a curated food table (macros, vitamins, minerals, allergens). It retrieves the most relevant rows and generates grounded answers.

To see a demo of the project check this video:

## 🎯 Overview – Problem Description (2 / 2)  
**Problem:**  
People often lack reliable nutrition facts for everyday foods, struggle to estimate macros for portions, and need quick substitutions that respect allergens. Generic chatbots can hallucinate values because they don’t ground answers in a verified dataset.

**Solution:** 
Nutrition Assistant is a retrieval-augmented application that answers nutrition questions using a local, curated CSV knowledge base. It retrieves the most relevant food entries and composes concise, evidence-based responses, reducing hallucinations and speeding up decisions.

**Use cases**
- Look up macronutrients (kcal, protein, fat, carbs).
- Check vitamins & minerals (A, B6, B12, C, D, E, calcium, iron, potassium, magnesium, selenium, zinc, iodine).
- Review allergens (tree nuts, peanut, sesame, etc.).
- Ask free-form questions in a Streamlit UI.

---

## 📚 Dataset Description 

The dataset `data/data.csv` consists of ~435 records, each representing a food item (plant-based, animal-based, snacks, supplements) normalized to 100 g serving.  
Columns include:  
- `food` – food name (e.g., Tofu scramble, Lentil stew, Salmon sandwich).  
- `serving_size_g`, `calories_kcal`, `protein_g`, `fat_g`, `carbohydrates_g`.  
- `vitamin_a_mg`, `vitamin_b6_mg`, `vitamin_b12_mg`, `vitamin_c_mg`, `vitamin_d_mg`, `vitamin_e_mg`.  
- `calcium_mg`, `iron_mg`, `potassium_mg`, `magnesium_mg`, `selenium_mg`, `zinc_mg`, `iodine_mg`.  
- `allergens` – common allergens in the product (e.g., Soy, Gluten, Milk, Egg, Fish, Shellfish).  

The dataset was generated using [ChatGPT](https://chatgpt.com/share/68ee24bc-58a4-8009-919c-8fd5f42ba24e) and curated to realistic nutritional values.

---

## ⚙️ Retrieval Flow (2 / 2)  
Architecture: 
User Query → Retrieval Engine (MinSearch) → Top-k Results → LLM (OpenAI) → Grounded Answer

- The application uses **MinSearch** for full-text retrieval from the CSV dataset (via `ingest.py` and `rag.py`).  
- The top results are passed to the LLM (OpenAI) which composes an answer grounded in the retrieved context.  
- This combination of a knowledge base + LLM constitutes a full RAG (Retrieval-Augmented Generation) flow.

---

## Experiments (check links)

For experiments, we use Jupyter notebooks.
They are in the [`notebooks`](notebooks/) folder.

To start Jupyter, run:

```bash
cd notebooks
pipenv run jupyter notebook
```

We have the following notebooks:

- [`01-dataset, minsearch, rag.ipynb`](notebooks/rag-test.ipynb): The RAG flow and evaluating the system.
- [`02-eval-data-gen.ipynb`](notebooks/evaluation-data-generation.ipynb): Generating the ground truth dataset for retrieval evaluation.

---

## 🔎 Retrieval Evaluation (2 / 2)  
Evaluation is based on a ground truth dataset (`ground-truth-retrieval.csv`) and metrics:  
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

Multiple approaches were compared and the best one selected.

---

## 🤖 LLM Evaluation (2 / 2)  
Responses were evaluated using an LLM-as-judge metric:  
| Model        | RELEVANT | PARTLY_RELEVANT | NON_RELEVANT |
|--------------|----------|-----------------|-------------|
| gpt-4o-mini  | 81.5 %   | 17.0 %          | 1.5 %       |
| gpt-4o       | 80.5 %   | 16.5 %          | 3.0 %       |  
Because the difference was minimal (~1 %), gpt-4o-mini was selected for the project.

---



## Preparation

Since we use OpenAI, you need to provide the API key:

1. Install `direnv`. If you use Ubuntu, run `sudo apt install direnv` and then `direnv hook bash >> ~/.bashrc`.
2. Copy `.envrc_template` into `.envrc` and insert your key there.
3. For OpenAI, it's recommended to create a new project and use a separate key.
4. Run `direnv allow` to load the key into your environment.

For dependency management, we use pipenv, so you need to install it:

```bash
pip install pipenv
```

Once installed, you can install the app dependencies:

```bash
pipenv install --dev
```

## Running the application

## Interface

We use Flask for serving the application as an API.

Refer to the ["Using the Application" section](#using-the-application)
for examples on how to interact with the application.

## Ingestion

The ingestion script is in [`ingest.py`](nutrition_assistant/ingest.py).

Since we use an in-memory database, `minsearch`, as our
knowledge base, we run the ingestion script at the startup
of the application.

It's executed inside [`rag.py`](nutrition_assistant/rag.py)
when we import it.





### RAG flow evaluation

We used the LLM-as-a-Judge metric to evaluate the quality
of our RAG flow.

For `gpt-4o-mini`, in a sample with 200 records, we had:

- 163 (81,5%) `RELEVANT`
- 34 (17%) `PARTLY_RELEVANT`
- 3 (1.5%) `NON_RELEVANT`

We also tested `gpt-4o`:

- 161 (80,5%) `RELEVANT`
- 33 (16,5%) `PARTLY_RELEVANT`
- 6 (3%) `NON_RELEVANT`

The difference is minimal - 1%, so we opted for `gpt-4o-mini`.

### Using `requests`

When the application is running, you can use
[requests](https://requests.readthedocs.io/en/latest/)
to send questions—use [test.py](test.py) for testing it:

```bash
pipenv run python test.py
```

It will pick a random question from the ground truth dataset
and send it to the app.


### CURL

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
  "conversation_id": "d60e2b16-ee87-406f-a589-91dd7a25e11a",
  "question": "What is the vitamin C content in a 100g apple compared to an orange?"
}
```
Sending feedback:

```bash
ID="d60e2b16-ee87-406f-a589-91dd7a25e11a"
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

## Background

Here we provide background on some tech not used in the
course and links for further reading.

### Flask

We use Flask for creating the API interface for our application.
It's a web application framework for Python: we can easily
create an endpoint for asking questions and use web clients
(like `curl` or `requests`) for communicating with it.

In our case, we can send questions to `http://localhost:5000/question`.

For more information, visit the [official Flask documentation](https://flask.palletsprojects.com/).


