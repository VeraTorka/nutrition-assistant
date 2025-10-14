# 🥗 Nutrition Assistant 🥗
### (a RAG-based Q&A chatbot)
A conversational RAG app that answers nutrition questions from a curated food table (macros, vitamins, minerals, allergens). It retrieves the most relevant rows and generates grounded answers.

## Overview (Problem description)
People often lack reliable nutrition facts for everyday foods, struggle to estimate macros for portions, and need quick substitutions that respect allergens. Generic chatbots can hallucinate values because they don’t ground answers in a verified dataset.

Nutrition Assistant is a retrieval-augmented application that answers nutrition questions using a local, curated CSV knowledge base. It retrieves the most relevant food entries and composes concise, evidence-based responses, reducing hallucinations and speeding up decisions.

Use cases

Look up macronutrients (kcal, protein, fat, carbs).
Check vitamins & minerals (A, B6, B12, C, D, E, calcium, iron, potassium, magnesium, selenium, zinc, iodine).
Review allergens (tree nuts, peanut, sesame, etc.).
Ask free-form questions in a Streamlit UI.

## Dataset generation
https://chatgpt.com/share/68ee24bc-58a4-8009-919c-8fd5f42ba24e

