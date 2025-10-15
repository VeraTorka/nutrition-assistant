import os
import ingest
from openai import OpenAI

client = OpenAI()
index = ingest.load_index()



def search(query):
    boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,

    )

    return results


prompt_template = """
You are a precise and reliable nutrition assistant.
Answer the QUESTION based on the CONTEXT from our exercises database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}
CONTEXT: {context}
""".strip()

entry_template = """
food: {food}
serving_size_g: {serving_size_g}
calories_kcal: {calories_kcal}
protein_g: {protein_g}
fat_g: {fat_g}
carbohydrates_g: {carbohydrates_g}
vitamin_a_mg: {vitamin_a_mg}
vitamin_b6_mg: {vitamin_b6_mg}
vitamin_b12_mg: {vitamin_b12_mg}
vitamin_c_mg: {vitamin_c_mg}
vitamin_d_mg: {vitamin_d_mg}
vitamin_e_mg: {vitamin_e_mg}
calcium_mg: {calcium_mg}
iron_mg: {iron_mg}
potassium_mg: {potassium_mg}
magnesium_mg: {magnesium_mg}
selenium_mg: {selenium_mg}
zinc_mg: {zinc_mg}
iodine_mg: {iodine_mg}
allergens: {allergens}
""".strip()


def build_prompt(query, search_results):
    context = ""

    for doc in search_results:
        context = context + entry_template.format(**doc) + "\n\n"

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt


def llm(prompt, model='gpt-4o-mini'):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def rag(query, model='gpt-4o-mini'):
    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt, model=model)
    return answer