import pandas as pd
import numpy as np


df=pd.read_csv('../data/data_unclean.csv', sep=';')

df=df.drop_duplicates(subset='food')

df = df.replace({np.nan: "no", None: "no"})

df.insert(0, 'id', df.index)

df.to_csv('../data/data.csv', index=False)

df=pd.read_csv('../data/data.csv')

get_ipython().system(' wget https://raw.githubusercontent.com/alexeygrigorev/minsearch/refs/heads/main/minsearch.py')

df.columns


documents=df.to_dict(orient='records')


documents



import minsearch


index = minsearch.Index(
    text_fields=["food", "allergens"],
    keyword_fields=["id"],
)

index.fit(documents)


# In[14]:


query = "How many calories in duck"


# In[15]:


index.search(query)


# ### LLM answer

# In[16]:


import os


# In[17]:


from openai import OpenAI
client = OpenAI()


# In[18]:


response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{"role": "user", "content":query}]
)
response.choices[0].message.content


# ## RAG Flow

# In[19]:


def search(query):
    boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,

    )

    return results


# ### Prompt evaluation

# In[20]:


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


# In[21]:


def llm(prompt, model='gpt-4o-mini'):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# In[22]:


def rag(query, model='gpt-4o-mini'):
    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt, model=model)
    return answer


# In[23]:


question = "What is the vitamin C content in a 100g apple compared to an orange?"
answer = rag(question)
print(answer)


# ## Retrieval evaluation

# In[24]:


df_question = pd.read_csv('../data/ground-truth-retrieval.csv')


# In[25]:


df_question.head()


# In[26]:


ground_truth = df_question.to_dict(orient='records')


# In[27]:


ground_truth[0]


# In[28]:


def hit_rate(relevance_total):
    cnt = 0

    for line in relevance_total:
        if True in line:
            cnt = cnt + 1

    return cnt / len(relevance_total)

def mrr(relevance_total):
    total_score = 0.0

    for line in relevance_total:
        for rank in range(len(line)):
            if line[rank] == True:
                total_score = total_score + 1 / (rank + 1)

    return total_score / len(relevance_total)


# In[29]:


def minsearch_search(query):
    boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results


# In[30]:


def evaluate(ground_truth, search_function):
    relevance_total = []

    for q in tqdm(ground_truth):
        doc_id = q['id']
        results = search_function(q)
        relevance = [d['id'] == doc_id for d in results]
        relevance_total.append(relevance)

    return {
        'hit_rate': hit_rate(relevance_total),
        'mrr': mrr(relevance_total),
    }


# In[31]:


from tqdm.auto import tqdm


# In[32]:


evaluate(ground_truth, lambda q: minsearch_search(q['question']))


# ## Parameter optimization

# In[33]:


df_validation = df_question[:100]
df_test = df_question[100:]


# In[34]:


import random

def simple_optimize(param_ranges, objective_function, n_iterations=10):
    best_params = None
    best_score = float('-inf') 

    for _ in range(n_iterations):
        current_params = {}
        for param, (min_val, max_val) in param_ranges.items():
            if isinstance(min_val, int) and isinstance(max_val, int):
                current_params[param] = random.randint(min_val, max_val)
            else:
                current_params[param] = random.uniform(min_val, max_val)


        current_score = objective_function(current_params)

        if current_score > best_score:  
            best_score = current_score
            best_params = current_params

    return best_params, best_score


# In[35]:


gt_val = df_validation.to_dict(orient='records')


# In[36]:


def minsearch_search(query, boost=None):
    if boost is None:
        boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results


# In[37]:


param_ranges = {
    'food': (0.0, 3.0),
    'serving_size_g': (0.0, 3.0),
    'calories_kcal': (0.0, 3.0),
    'protein_g': (0.0, 3.0),
    'fat_g': (0.0, 3.0),
    'carbohydrates_g': (0.0, 3.0),
    'vitamin_a_mg': (0.0, 3.0),
    'vitamin_b6_mg': (0.0, 3.0),
    'vitamin_b12_mg': (0.0, 3.0),
    'vitamin_c_mg': (0.0, 3.0),
    'vitamin_d_mg': (0.0, 3.0),
    'vitamin_e_mg': (0.0, 3.0),
    'calcium_mg': (0.0, 3.0),
    'iron_mg': (0.0, 3.0),
    'potassium_mg': (0.0, 3.0),
    'magnesium_mg': (0.0, 3.0),
    'selenium_mg': (0.0, 3.0),
    'zinc_mg': (0.0, 3.0),
    'iodine_mg': (0.0, 3.0),
    'allergens' : (0.0, 3.0)
}

def objective(boost_params):
    def search_function(q):
        return minsearch_search(q['question'], boost_params)

    results = evaluate(gt_val, search_function)
    return results['mrr']


# In[38]:


simple_optimize(param_ranges, objective, n_iterations=20)


# In[39]:


def minsearch_improved(query):
    boost = {
          'food': 3.00,
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

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results

evaluate(ground_truth, lambda q: minsearch_improved(q['question']))


# ## RAG evaluation (LLM-as-a-Judge)

# In[40]:


prompt2_template = """
You are an expert evaluator for a RAG system.
Your task is to analyze the relevance of the generated answer to the given question.
Based on the relevance of the generated answer, you will classify it
as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

Here is the data for evaluation:

Question: {question}
Generated Answer: {answer_llm}

Please analyze the content and context of the generated answer in relation to the question
and provide your evaluation in parsable JSON without using code blocks:

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
  "Explanation": "[Provide a brief explanation for your evaluation]"
}}
""".strip()


# In[41]:


len(ground_truth)


# In[42]:


record = ground_truth[0]
question = record['question']
answer_llm=rag(question)


# In[43]:


print(answer_llm)


# In[44]:


prompt = prompt2_template.format(question=question, answer_llm=answer_llm)
print(prompt)


# In[45]:


import json


# In[46]:


df_sample = df_question.sample(n=200, random_state=1)


# In[47]:


sample = df_sample.to_dict(orient='records')


# In[ ]:


evaluations = []

for record in tqdm(sample):
    question = record['question']
    answer_llm = rag(question) 

    prompt = prompt2_template.format(
        question=question,
        answer_llm=answer_llm
    )

    evaluation = llm(prompt)
    evaluation = json.loads(evaluation)

    evaluations.append((record, answer_llm, evaluation))


# In[ ]:


df_eval.relevance.value_counts()


# In[87]:


df_eval.relevance.value_counts(normalize=True)


# In[81]:


df_eval.to_csv('../data/rag-eval-gpt-4o-mini.csv', index=False)


# In[82]:


df_eval[df_eval.relevance == 'NON_RELEVANT']


# In[83]:


evaluations_gpt4o = []

for record in tqdm(sample):
    question = record['question']
    answer_llm = rag(question, model='gpt-4o') 

    prompt = prompt2_template.format(
        question=question,
        answer_llm=answer_llm
    )

    evaluation = llm(prompt)
    evaluation = json.loads(evaluation)

    evaluations_gpt4o.append((record, answer_llm, evaluation))


# In[ ]:


df_eval = pd.DataFrame(evaluations_gpt4o, columns=['record', 'answer', 'evaluation'])

df_eval['id'] = df_eval.record.apply(lambda d: d['id'])
df_eval['question'] = df_eval.record.apply(lambda d: d['question'])

df_eval['relevance'] = df_eval.evaluation.apply(lambda d: d['Relevance'])
df_eval['explanation'] = df_eval.evaluation.apply(lambda d: d['Explanation'])

del df_eval['record']
del df_eval['evaluation']


# In[ ]:


df_eval.relevance.value_counts()


# In[ ]:


df_eval.relevance.value_counts()


# In[ ]:


df_eval.relevance.value_counts(normalize=True)


# In[ ]:


df_eval.to_csv('../data/rag-eval-gpt-4o.csv', index=False)

