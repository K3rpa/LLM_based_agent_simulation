import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from typing import List

client = OpenAI(
    api_key="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"
)

def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def get_embedding(text: str) -> List[float]:
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Embedding error: {e}")
        return []

def calculate_similarity(emb1: List[float], emb2: List[float]) -> float:
    if not emb1 or not emb2:
        return 0.0
    emb1 = np.array(emb1).reshape(1, -1)
    emb2 = np.array(emb2).reshape(1, -1)
    return cosine_similarity(emb1, emb2)[0][0]

# Static data loaded once
system_role = load_file("systemrole.txt")

with open("short_term_memory.json", "r", encoding="utf-8") as f:
    short_memory = json.load(f)

with open("long_term_memory.json", "r", encoding="utf-8") as f:
    long_memory = json.load(f)

with open("memory_accuracy_questions_with_answers.json", "r", encoding="utf-8") as f:
    question_set = json.load(f)

with open("causal_reasoning_questions.json", "r", encoding="utf-8") as f:
    question_set_c = json.load(f)

short_text = "\n".join([f"[Tick {m['tick']}] {m['event']}" for m in short_memory.values()])
long_text = "\n".join([f"[Tick {m['tick']}] {m['event']}" for m in long_memory.values()])
memory_context = f"Short-Term Memory:\n{short_text}\n\nLong-Term Memory:\n{long_text}"

smoothie = SmoothingFunction().method4
all_results = []

for run in range(20):
    print(f"\n========== Simulation {run + 1} started ==========")
    bleu_scores = []
    similarity_scores = []

    for item in question_set:
        qid = item["id"]
        question = item["question"]
        gold_answer = item["answer"]

        prompt = (
            f"Use the following memory to answer the question.\n"
            f"{memory_context}\n\n"
            f"Question: {question}\n"
            f"Only provide a brief answer without any explanation."
        )

        messages = [
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            predicted = response.choices[0].message.content.strip()
        except Exception as e:
            predicted = "ERROR"

        ref = [gold_answer.lower().split()]
        cand = predicted.lower().split()
        score = sentence_bleu(ref, cand, smoothing_function=smoothie)
        bleu_scores.append(score)

    average_score_m = sum(bleu_scores) / len(bleu_scores)

    for item in question_set_c:
        qid = item["id"]
        question = item["question"]
        correct_answers = item["correct_answers"]

        prompt = (
            f"Use the following memory to answer the question.\n"
            f"{memory_context}\n\n"
            f"Question: {question}\n"
            f"Only provide a brief answer without any explanation."
        )

        messages = [
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            predicted = response.choices[0].message.content.strip()
        except Exception as e:
            predicted = "ERROR"

        pred_embedding = get_embedding(predicted)
        sims = [calculate_similarity(pred_embedding, get_embedding(ans)) for ans in correct_answers]
        max_sim = max(sims) if sims else 0.0

        verdict = max_sim
        if max_sim < 0.75 and predicted != "ERROR":
            god_prompt = (
                f"The agent answered: \"{predicted}\" in response to the question: \"{question}\"\n"
                f"Does this answer sound reasonable in general causal logic? Reply only with 1 for yes, 0 for no."
            )
            god_messages = [
                {"role": "system", "content": "You are the god and judge of all reasoning."},
                {"role": "user", "content": god_prompt}
            ]
            try:
                god_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=god_messages
                )
                god_verdict = god_response.choices[0].message.content.strip()
                if "1" in god_verdict:
                    verdict = 0.75
            except Exception as e:
                print(f"God error: {e}")

        similarity_scores.append(verdict)

    average_score_s = sum(similarity_scores) / len(similarity_scores)
    final_score = average_score_m * 0.8 + average_score_s * 0.2

    all_results.append({
        "bleu": round(average_score_m, 4),
        "similarity": round(average_score_s, 4),
        "final_score": round(final_score, 4)
    })

average_bleu = sum(r["bleu"] for r in all_results) / 20
average_similarity = sum(r["similarity"] for r in all_results) / 20
average_final = sum(r["final_score"] for r in all_results) / 20

all_results.append({
    "average_bleu": round(average_bleu, 4),
    "average_similarity": round(average_similarity, 4),
    "average_final_score": round(average_final, 4)
})

with open("result20.txt", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)

print("20 runs completed. Results saved to result2.txt.")
