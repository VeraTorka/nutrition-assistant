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