# 🥗 Nutrition Assistant 🥗
### (a RAG-based Q&A chatbot)
A conversational RAG app that answers nutrition questions from a curated food table (macros, vitamins, minerals, allergens). It retrieves the most relevant rows and generates grounded answers.

This project was implemented for 
[LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) -
a free course about LLMs and RAG.

To see a demo of the project check this video:

## Overview (Problem description)
People often lack reliable nutrition facts for everyday foods, struggle to estimate macros for portions, and need quick substitutions that respect allergens. Generic chatbots can hallucinate values because they don’t ground answers in a verified dataset.

Nutrition Assistant is a retrieval-augmented application that answers nutrition questions using a local, curated CSV knowledge base. It retrieves the most relevant food entries and composes concise, evidence-based responses, reducing hallucinations and speeding up decisions.

**Use cases**

- Look up macronutrients (kcal, protein, fat, carbs).
- Check vitamins & minerals (A, B6, B12, C, D, E, calcium, iron, potassium, magnesium, selenium, zinc, iodine).
- Review allergens (tree nuts, peanut, sesame, etc.).
- Ask free-form questions in a Streamlit UI.

## Dataset Description

The dataset used in this project contains information about **various food items**, including both plant-based and animal-based meals, snacks, and supplements. Each record represents one specific food item with detailed nutritional and micronutrient information.
- **food:** The name of the food item (e.g., *Tofu scramble, Lentil stew, Salmon sandwich*).  
- **serving_size_g:** Standard serving size in grams (all values normalized to 100 g).  
- **calories_kcal:** Energy value per 100 g, measured in kilocalories.  
- **protein_g:** Amount of protein (in grams) per 100 g.  
- **fat_g:** Amount of total fat (in grams) per 100 g.  
- **carbohydrates_g:** Total carbohydrates (in grams) per 100 g.  
- **vitamin_a_mg – vitamin_e_mg:** Concentrations of selected vitamins (A, B6, B12, C, D, E) in milligrams.  
- **calcium_mg, iron_mg, potassium_mg, magnesium_mg, selenium_mg, zinc_mg, iodine_mg:** Key minerals and trace elements (mg per 100 g).  
- **allergens:** Common allergens present in the product (e.g., *Soy, Gluten, Milk, Egg, Fish, Shellfish*).  


The dataset was generated using [ChatGPT](https://chatgpt.com/share/68ee24bc-58a4-8009-919c-8fd5f42ba24e) and contains 435 records. 

## Technologies

- Python 3.12
- Docker and Docker Compose for containerization
- [Minsearch](https://github.com/alexeygrigorev/minsearch) for full-text search
- Flask as the API interface (see [Background](#background) for more information on Flask)
- Grafana for monitoring and PostgreSQL as the backend for it
- OpenAI as an LLM

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


## Retrieval evaluation
The basic approach - using `minsearch` without any boosting - gave the following metrics:
- Hit rate: 89%
- MRR: 74%

The improved version (with tuned boosting):
- Hit rate: 92%
- MRR: 77%

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


