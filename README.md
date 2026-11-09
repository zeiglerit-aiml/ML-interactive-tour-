# Interactive ML Landscape

A flat, repo-ready command-line learning tool combining the two LinkedIn ML taxonomies.

## Files

Everything intentionally lives in this one folder:

- `ml_landscape.py` — interactive decision-tree/menu
- `requirements.txt` — Python dependencies
- `README.md` — usage
- `ml_landscape_all.ipynb` — comprehensive notebook version
- `current_algorithm.ipynb` — created/replaced on demand when you select an algorithm

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ml_landscape.py
```

Menu flow:

```text
learning paradigm / major family
  -> model family
    -> algorithm
      -> one-sentence example
      -> small Python snippet
      -> run in terminal OR open in Jupyter
```

The Jupyter option writes the selected lesson to `current_algorithm.ipynb` and launches Jupyter.
When you stop the Jupyter server with Ctrl+C, the terminal menu resumes.

## Other commands

```bash
python ml_landscape.py --list
python ml_landscape.py --build-all-notebook
```

## Reference algorithm checklist\n\nThe 20-algorithm reference image is represented in the catalog. The repository also retains additional algorithms beyond that reference. QDA and hierarchical clustering are included as distinct lessons; PCA is the principal component analysis entry.\n\n## Taxonomy covered

Supervised learning; unsupervised learning; semi-supervised learning; self-supervised learning;
reinforcement learning; artificial neural networks and deep learning; ensemble learning; statistical inference.

Algorithms include Decision Trees, Logistic Regression, SVM, Naive Bayes, KNN, Linear/Polynomial/Ridge/Lasso,
K-Means, Hierarchical Clustering, DBSCAN, Mean Shift, Fuzzy C-Means, PCA, t-SNE, LDA, QDA, Apriori, FP-Growth, ECLAT,
Q-Learning, DQN, A3C, Genetic Algorithms, MLP, RBFNN, CNN, RNN, LSTM, GRU, Transformers,
GANs, Autoencoders, Random Forest, Gradient Boosting, XGBoost, LightGBM, stacking,
confidence intervals, t-tests, and a Bayesian update.

### Taxonomy notes

ANN means **Artificial Neural Network**. “Artificial general networks” is not the standard term.

LDA is shown in the dimensionality-reduction branch because one source map places it there, but Linear
Discriminant Analysis is supervised because it uses labels.

Genetic algorithms are displayed near the reinforcement-learning branch because one map groups them there;
technically evolutionary computation is a separate optimization family.

## Portfolio ownership

Standalone educational ML taxonomy and algorithm exploration tool. Keep its CLI and notebook lesson content independent from production pipeline frameworks.

Account-wide ownership and cleanup decisions are maintained in the [WSP portfolio repository catalog](https://github.com/zeiglerit-aiml/WSP_Integrated_AI_SDLC_GVC_pl/blob/main/REPOSITORY_CATALOG.md).
