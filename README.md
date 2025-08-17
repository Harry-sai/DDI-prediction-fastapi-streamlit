# Drug-Drug Interaction (DDI) Prediction using Machine Learning

## Project Overview

This project predicts **Drug-Drug Interactions (DDIs)** using **Machine Learning** and provides a **full-stack deployment** pipeline with **FastAPI** (backend API) and **Streamlit** (user interface).

Drug-Drug Interactions are critical in pharmacology, as they can cause severe adverse effects when two or more drugs are taken together. This project leverages **drug embeddings** and **classification models** to predict the **type of interaction** between two drugs.

---

## Dataset

* Source: **Mendeley: DrugBank-Extracted DDI dataset**
* Preprocessed & label-encoded version used.
* Key Columns:

  * `drug1_name` → Name of the first drug
  * `drug2_name` → Name of the second drug
  * `drug1id_num`, `drug2id_num` → Numeric IDs for drugs
  * `merged DDI type index` → Target variable (interaction type, multi-class classification)

---

## Approach

### 1. Exploratory Data Analysis (EDA)

* Distribution of interaction types
* Most frequent drugs in interactions
* Network graph of drugs & their interaction types
* Outlier checks

### 2. Preprocessing

* Label Encoding for drugs & interaction types
* **Word2Vec embeddings** trained on drug sequences → each drug represented as a dense vector
* Final feature representation = **concatenation of drug1 & drug2 embeddings**

### 3. Model Training

* Models tried:

  * **Random Forest**
  * **XGBoost** (best performing)
* GroupKFold to avoid drug leakage across train/test splits
* Hyperparameter tuning with **Optuna**

### 4. Hyperparameter Tuning (Optuna)

* Parameters tuned: `max_depth`, `learning_rate`, `subsample`, `colsample_bytree`, `min_child_weight`, `reg_lambda`, `reg_alpha`
* Early stopping used to avoid overfitting

---

## Results

| Model           | Accuracy   |
| --------------- | ---------- |
| Random Forest   | \~38%      |
| XGBoost (tuned) | **86.05%** |

* Training Accuracy: \~99%
* Validation Accuracy: \~86%
* Model generalizes well with tuned parameters

---

## Deployment

### 🔹 FastAPI Backend

The model is served through **FastAPI** with REST endpoints:

* `GET /` → Home page (welcome message)
* `GET /about` → Project information
* `POST /Drug_interaction` → Takes `drug1` and `drug2` as input, returns predicted interaction type

**Example request:**
```Running Uvicorn
uvicorn drug:app --reload
```
Then open Browse with the Url and search the endpoint or directly go to docs if don't want to open it through streamlit

**Example response:**

```json
{
  "interaction_type_index": 3,
  "interaction_type_label": "Synergistic Effect"
}
```

### Streamlit Frontend

A **Streamlit UI** was built for non-technical users:

* `Home` – Welcome page with project intro
* `About` – Explains dataset, approach, and results
* `Drug Interaction` – User can input two drug names → get **predicted interaction type + index**

Run using:

```bash/powershell
streamlit run app.py
```

---

## Future Improvements

* Use **pretrained embeddings** (BioWordVec, PubChem2Vec)
* Explore **deep learning** models (Graph Neural Networks, Transformers)
* Integrate **molecular structure data (SMILES)**
* Add visualization of drug interaction networks in Streamlit

---

## Tech Stack

* **Python** (pandas, numpy, matplotlib, seaborn)
* **scikit-learn** (Random Forest, preprocessing)
* **XGBoost** (classification)
* **Optuna** (hyperparameter tuning)
* **gensim** (Word2Vec embeddings)
* **FastAPI** (backend API)
* **Streamlit** (user interface)

