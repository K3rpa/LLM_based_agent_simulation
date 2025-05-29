# 🧠 Memory Architecture for Generative Agents Using LLM

**Author:** Boxi Chen  
**Affiliation:** California State University, Chico  
**Contact:** bchen1@csuchico.edu

## 📘 Overview

This project implements a simulation framework for **LLM-based generative agents** with **structured memory architectures**, designed to evaluate how different memory types (episodic, semantic, and procedural) impact an agent’s behavior over a 14-day virtual environment.

The goal is to equip LLM-powered agents with **human-like memory recall**, **planning**, and **causal reasoning**, addressing one of the key weaknesses of LLMs — **lack of persistent memory**.

## 🧠 Core Concepts

The system uses a **three-layer memory architecture**:
- `sensory_memory.json`: short-term sensory inputs (FIFO)
- `short_term_memory.json`: filtered significant events
- `long_term_memory.json`: deeply relevant, identity-aligned experiences

Supported memory types:
- **Episodic Memory:** Personal experiences and events
- **Semantic Memory:** General facts and knowledge
- **Procedural Memory:** Routines and behavioral patterns

Each memory type is tested independently.


## 🧪 Simulation Process

- Runs for **14 simulated days**, with each hour = 1 tick (336 ticks total)
- At each tick:
  - Agent executes a main event from the daily plan
  - `event.py` injects subevents if main event match
  - Events are stored in sensory memory → filtered → promoted to long/short-term memory
- Planning is influenced by memories and updated dynamically
- Periodic memory-based plan reflection occurs every 12 ticks

## 📊 Evaluation Metrics

The agent is evaluated on:
- **Memory Accuracy:** 30 factual recall questions scored with BLEU
- **Causal Reasoning:** 10 questions scored using cosine similarity + LLM validation
- **Total Score:** 0.8 × Memory Accuracy + 0.2 × Causal Reasoning

> Results indicate **episodic memory** performs best in long-term recall.

## 📌 Key Files

| File | Description |
|------|-------------|
| `main.py` | Launches the full simulation |
| `memory.py` | Initializes agent with specified memory type |
| `plan.py` | Manages daily and weekly plans |
| `event.py` | Handles event injection and matching |
| `systemrole.txt` | Defines agent’s personality |
| `fixed_subevent.json` | Stores environment up coming for events |
| `*_memory.json` | Track and log different types of agent memory |
| `*_results.json` | Output of BLEU and similarity scoring |
| `graph.ipynb` | Jupyter notebook to visualize results |

## 📈 Sample Result

Example question:
    Q: Who are your teammates in your algorithm class?
    A: Brian, David, and Jasmine.
    Reference: Tom, Brian, Chris, and Alex
    BLEU Score: 0.0098
Even partial matches receive low BLEU scores, showing the challenge of memory precision.

## 🔮 Future Work

- Introduce **abstraction** and **summarization** of memories
- Scale to **semester-long simulations**
- Expand to **multi-agent environments** for social memory
- Evaluate **human-likeness** of behaviors with GPT judges

## 📄 Citation

If you use this project, please cite:

> Boxi Chen. *Memory Architecture for Generative Agents Using LLM*. California State University, Chico. CSCI-693, Spring 2025.

## 🤝 Acknowledgments

This project is inspired by foundational work in cognitive science, generative agents, and memory-augmented AI systems, including:

- M. A. Conway and C. W. Pleydell-Pearce, *The construction of autobiographical memories in the self-memory system*, Psychological Review, 2000. [[1]](https://doi.org/10.1037/0033-295X.107.2.261)
- J. S. Park et al., *Generative agents: Interactive simulacra of human behavior*, ACM UIST, 2023. [[2]](https://doi.org/10.1145/3586183.3606763)
- R. M. Jones et al., *Automated intelligent pilots for combat flight simulation*, AI Magazine, 1999. [[3]](https://doi.org/10.1609/aimag.v20i1.1455)
- O. Khattab et al., *Demonstrate-Search-Predict: Composing retrieval and language models for knowledge-intensive NLP*, arXiv:2212.14024, 2023. [[4]](https://arxiv.org/abs/2212.14024)
- R. Krishna et al., *Socially situated artificial intelligence enables learning from human interaction*, PNAS, 2022. [[5]](https://doi.org/10.1073/pnas.2115730119)
- W. H. Kruskal and W. A. Wallis, *Use of ranks in one-criterion variance analysis*, JASA, 1952. [[6]](https://doi.org/10.1080/01621459.1952.10483441)
- Tutor2u Psychology, *Episodic, Procedural and Semantic Memory*, March 2021. [[7]](https://www.tutor2u.net/psychology/reference/episodic-procedural-and-semantic-memory)


