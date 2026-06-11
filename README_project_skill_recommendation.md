# Market-Driven Skill Recommendation System for Developers

## Introduction
This project builds a **market-driven skill recommendation system** for developers using data from the **Stack Overflow Developer Survey**. The goal is to recommend the next skills a developer should learn based on their current skill set and real-world patterns observed in professional developer profiles.

The project combines two complementary ideas:
- **Association Rule Mining with FP-Growth** to capture explicit co-occurrence patterns among skills.
- **Graph Embedding (Node2Vec-style biased random walk + Word2Vec)** to capture latent structural relationships among skills in a co-occurrence graph.

The system compares four recommenders:
1. **Popularity baseline**
2. **FP-Growth only**
3. **Node2Vec only**
4. **Hybrid (FP-Growth + embedding)**

The evaluation is framed as **future skill prediction**:
- Input: skills a developer already has
- Ground truth: skills the developer wants to work with but does not yet have

In the final implementation, the project shows that different recommenders optimize different goals:
- **Popularity** is strongest on pure relevance metrics.
- **FP-Growth only** is the strongest learned and interpretable recommender.
- **Node2Vec only** provides very broad exploration but weak direct relevance.
- **Hybrid** acts as a coverage-oriented compromise between explicit rule-based relevance and embedding-based exploration.

---

## Dataset: How to Download the Stack Overflow CSV

The official survey landing page is:
- https://survey.stackoverflow.co/

Official 2025 survey results page:
- https://survey.stackoverflow.co/2025/

Official 2025 methodology page:
- https://survey.stackoverflow.co/2025/methodology

The survey index page also provides a **Download Full Data Set (CSV)** link for each year:
- https://survey.stackoverflow.co/

### Recommended steps
1. Open the official survey index page.
2. Choose the year you want to use, preferably **2025**.
3. Click **Download Full Data Set (CSV)**.
4. Extract the downloaded archive.
5. Place the CSV file in your project data folder.

### Why this dataset is used
This dataset is suitable because it includes:
- skills developers **have worked with**
- skills developers **want to work with**
- professional status and employment fields
- experience-related fields
- multiple technology categories such as language, database, framework, platform, AI tools, and development environments

This makes it suitable for constructing both:
- a transaction-based representation for FP-Growth
- a graph-based representation for Node2Vec-style embedding

---

## Getting Started

### Recommended environment
- OS: Windows 10/11
- Editor: Visual Studio Code
- Python: **3.10 or 3.11 recommended**
- Jupyter support enabled in VS Code

---

## Local Setup in VS Code

### 1. Create a project folder
Put the notebooks, downloaded CSV file, and related outputs inside one project directory.

Example layout:
```text
project_root/
├─ data/
│  ├─ survey_results_public.csv
│  ├─ survey_results_schema.csv
│  └─ research_outputs/
├─ colab_preprocessing_pipeline_improved.ipynb
├─ local_training_research_enhanced_improved.ipynb
├─ final_research_paper.docx
└─ README_project_skill_recommendation.md
```

### 2. Create a virtual environment
Open terminal in VS Code at the project root.

#### On Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### On Windows CMD
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

### 3. Install required packages
```bash
pip install --upgrade pip
pip install pandas numpy matplotlib seaborn scikit-learn jupyter ipykernel mlxtend networkx gensim openpyxl
```

If your implementation uses a separate node2vec package, install it only if needed. In this project, the primary implementation is **Node2Vec-style custom random walk + Word2Vec**, so the external `node2vec` package is not required for the main logic.

### 4. Register the environment as a Jupyter kernel
```bash
python -m ipykernel install --user --name skill-rec-venv --display-name "Python (skill-rec-venv)"
```

### 5. Select the interpreter in VS Code
In VS Code:
1. Press `Ctrl + Shift + P`
2. Search for **Python: Select Interpreter**
3. Choose the interpreter from `.venv`
4. Open each notebook and select the same Jupyter kernel

### 6. Recommended VS Code extensions
- Python
- Jupyter
- Pylance

---

## How to Run the Project

### Step 1: Prepare the dataset
- Download the official Stack Overflow CSV.
- Place the raw CSV in your local `data/` folder.
- Make sure the notebook path variables match your folder layout.

### Step 2: Run the preprocessing notebook
Open:
- `colab_preprocessing_pipeline_improved.ipynb`

Run cells in order.

This notebook will:
- load the raw survey
- filter the population
- create skill lists
- create target skills
- build vocabulary
- split the dataset
- export all artifacts needed for modeling

Typical artifacts produced:
- `cleaned_model_population.csv`
- `skill_vocabulary_final.csv`
- `train_users.csv`
- `valid_users.csv`
- `test_users.csv`
- `fpgrowth_train_matrix.csv`
- `graph_edges_train.csv`

### Step 3: Run the training notebook
Open:
- `local_training_research_enhanced_improved.ipynb`

Run cells in order.

This notebook will:
- load preprocessing artifacts
- train the four recommenders
- evaluate them on validation and test sets
- run hybrid ablation
- run stability analysis
- export CSV outputs and charts

### Step 4: Inspect generated outputs
Check the `research_outputs/` folder or the configured output directory.

---

## Algorithms Used

### 1. Popularity Baseline
A simple recommender that ranks skills by their global frequency in the training data and recommends the most common skills the user does not already have.

Why it is used:
- serves as a strong baseline
- tests whether personalization actually adds value

### 2. FP-Growth
Used to discover **frequent skill combinations** and generate **association rules**.

Core statistics used:
- **Support**: how often a skill or itemset appears
- **Confidence**: how often the consequent appears when the antecedent appears
- **Lift**: how strongly the antecedent and consequent are associated beyond chance

Why it is used:
- highly interpretable
- suitable for transactional skill data
- good for capturing explicit ecosystems of technologies

### 3. Node2Vec-style Graph Embedding
The project constructs a **skill co-occurrence graph**:
- node = skill
- edge = co-occurrence of skills among users

Then it performs:
- biased random walks inspired by Node2Vec
- Word2Vec training on the random-walk corpus

Why it is used:
- captures latent structural relationships among skills
- allows recommendation beyond direct frequent co-occurrence

### 4. Hybrid Recommendation
Combines:
- rule-based candidates from FP-Growth
- embedding-based candidates from the graph model

Default fusion idea:
- normalize scores from both components
- combine them using weights `alpha` and `beta`
- apply a popularity-aware penalty to avoid overly generic skills dominating recommendations

Why it is used:
- balances interpretability and exploration
- aims to reduce over-reliance on popularity alone

---

## Why These Formulations Are Used

### Future skill prediction target
The project defines:
- `have_skills` = current skills
- `want_skills` = desired future skills
- `target_skills = want_skills - have_skills`

Why it is used:
- the recommender should predict what the user wants to learn next, not what they already know
- this makes evaluation more realistic for skill recommendation

### Evaluation metrics
The project uses both relevance-oriented and exploration-oriented metrics.

#### Relevance
- **Recall@K**: how many true future skills are recovered in the top-K list
- **HitRate@K**: whether at least one true future skill appears in the top-K list

#### Exploration / breadth
- **Catalog Coverage**: how much of the skill dictionary is actually recommended
- **Novelty**: whether recommended skills are less globally common
- **Diversity**: whether recommendations span varied categories
- **Average Support**: the average popularity of recommended skills

Why this combination is used:
- relevance alone favors popularity-heavy systems
- exploration alone can overvalue noisy recommendations
- together they show the trade-off between accuracy and breadth

---

## Main Findings from the Project

Based on the final outputs:
- **Popularity** is the strongest model on pure relevance metrics.
- **FP-Growth only** is the strongest learned and interpretable recommender.
- **Node2Vec only** explores the widest part of the catalog but is weakest on direct relevance.
- **Hybrid** does not dominate all baselines on Recall or HitRate, but provides a strong trade-off by greatly improving catalog coverage and novelty while remaining more grounded than pure embedding recommendation.

This means the project does **not** simply conclude that hybrid is always best. Instead, it shows that different recommenders serve different goals:
- direct relevance
- interpretability
- exploration and broader skill discovery

---

## References for Dataset and Methodology Context
- Stack Overflow Annual Developer Survey index: https://survey.stackoverflow.co/ citeturn201224search3
- Stack Overflow Developer Survey 2025: https://survey.stackoverflow.co/2025/ citeturn201224search0
- Stack Overflow Developer Survey 2025 Methodology: https://survey.stackoverflow.co/2025/methodology citeturn201224search6

