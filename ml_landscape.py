#!/usr/bin/env python3
import argparse, json, subprocess, sys, textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CATALOG = {'Supervised Learning': {'description': 'Learn from labeled examples where the desired target is known.', 'example': 'Predict customer churn from historical customers labeled churn/stay.', 'families': {'Classification': {'Decision Tree': ('Use interpretable feature splits to classify an outcome.', 'from sklearn.tree import DecisionTreeClassifier\nX=[[25,1],[45,0],[35,1],[50,0]]; y=[0,1,0,1]\nm=DecisionTreeClassifier(max_depth=2,random_state=42).fit(X,y)\nprint(m.predict([[40,0]]))'), 'Logistic Regression': ('Estimate the probability of a binary outcome such as fraud.', 'from sklearn.linear_model import LogisticRegression\nX=[[.1],[.2],[.8],[.9]]; y=[0,0,1,1]\nm=LogisticRegression().fit(X,y)\nprint(m.predict_proba([[.7]]))'), 'Support Vector Machine': ('Separate classes with a maximum-margin decision boundary.', "from sklearn.svm import SVC\nX=[[1,1],[1,2],[4,4],[4,5]]; y=[0,0,1,1]\nm=SVC(kernel='linear').fit(X,y)\nprint(m.predict([[3.5,4]]))"), 'Naive Bayes': ('Classify using simple probabilistic feature assumptions.', 'from sklearn.naive_bayes import GaussianNB\nX=[[1,20],[2,18],[8,3],[9,2]]; y=[0,0,1,1]\nm=GaussianNB().fit(X,y)\nprint(m.predict([[7,4]]))'), 'Quadratic Discriminant Analysis (QDA)': ('Classify with a separate covariance matrix for each class, allowing quadratic decision boundaries.', 'from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis\nX=[[1,1],[1.5,2],[2,1],[5,5],[5.5,6],[6,5]]; y=[0,0,0,1,1,1]\nm=QuadraticDiscriminantAnalysis().fit(X,y)\nprint(m.predict([[4.5,4.8]])); print(m.predict_proba([[4.5,4.8]]))'), 'k-Nearest Neighbors': ('Classify a sample from the labels of nearby examples.', 'from sklearn.neighbors import KNeighborsClassifier\nX=[[1,1],[1,2],[5,5],[6,5]]; y=[0,0,1,1]\nm=KNeighborsClassifier(3).fit(X,y)\nprint(m.predict([[5,4]]))')}, 'Regression': {'Linear Regression': ('Predict a continuous value with a linear relationship.', 'from sklearn.linear_model import LinearRegression\nX=[[1000],[1500],[2000],[2500]]; y=[200000,280000,360000,440000]\nm=LinearRegression().fit(X,y)\nprint(m.predict([[1800]]))'), 'Polynomial Regression': ('Model a curved continuous relationship.', 'from sklearn.preprocessing import PolynomialFeatures\nfrom sklearn.linear_model import LinearRegression\nX=[[1],[2],[3],[4]]; y=[1,4,9,16]\np=PolynomialFeatures(2); m=LinearRegression().fit(p.fit_transform(X),y)\nprint(m.predict(p.transform([[5]])))'), 'Ridge Regression': ('Shrink coefficients with L2 regularization to reduce overfitting.', 'from sklearn.linear_model import Ridge\nX=[[1,1],[2,2],[3,4],[4,5]]; y=[2,4,7,9]\nm=Ridge(alpha=1).fit(X,y)\nprint(m.predict([[5,6]]))'), 'Lasso Regression': ('Use L1 regularization that can drive weak coefficients to zero.', 'from sklearn.linear_model import Lasso\nX=[[1,0],[2,0],[3,1],[4,1]]; y=[2,4,7,9]\nm=Lasso(alpha=.1).fit(X,y)\nprint(m.coef_,m.predict([[5,1]]))')}}}, 'Unsupervised Learning': {'description': 'Discover useful structure in data that has no target labels.', 'example': 'Group customers into natural behavior segments without predefined segment labels.', 'families': {'Clustering': {'K-Means': ('Partition observations into centroid-based clusters.', "from sklearn.cluster import KMeans\nX=[[1,1],[1,2],[8,8],[9,8]]\nm=KMeans(n_clusters=2,random_state=42,n_init='auto').fit(X)\nprint(m.labels_,m.cluster_centers_)"), 'Hierarchical Clustering': ('Build a nested hierarchy of clusters; inspect the tree or cut it at a chosen number of groups.', 'from sklearn.cluster import AgglomerativeClustering\nX=[[1,1],[1.2,1.1],[5,5],[5.2,5.1],[9,1]]\nm=AgglomerativeClustering(n_clusters=3,linkage=\'ward\').fit(X)\nprint(m.labels_)'), 'DBSCAN': ('Find dense irregular clusters and flag isolated observations as noise.', 'from sklearn.cluster import DBSCAN\nX=[[1,1],[1.1,1.1],[8,8],[8.1,8.1],[20,20]]\nprint(DBSCAN(eps=.5,min_samples=2).fit(X).labels_)'), 'Mean Shift': ('Discover cluster centers by moving candidates toward dense regions.', 'from sklearn.cluster import MeanShift\nX=[[1,1],[1.2,1.1],[8,8],[8.2,8.1]]\nm=MeanShift().fit(X)\nprint(m.labels_,m.cluster_centers_)'), 'Fuzzy C-Means': ('Give each sample partial membership in multiple clusters.', "import numpy as np\nmembership=np.array([[.9,.1],[.6,.4],[.2,.8]])\nprint(membership)\nprint('hard labels:',membership.argmax(1))")}, 'Dimensionality Reduction': {'PCA': ('Compress correlated numeric features into variance-preserving components.', 'from sklearn.decomposition import PCA\nX=[[1,2,3],[2,3,4],[8,9,10],[9,10,11]]\np=PCA(n_components=2).fit(X)\nprint(p.transform(X)); print(p.explained_variance_ratio_)'), 't-SNE': ('Project high-dimensional samples into 2D for local-neighborhood visualization.', 'from sklearn.manifold import TSNE\nfrom sklearn.datasets import load_iris\nX=load_iris().data[:40]\nprint(TSNE(n_components=2,perplexity=5,random_state=42).fit_transform(X)[:5])'), 'LDA': ('Project labeled samples into directions that best separate classes.', 'from sklearn.discriminant_analysis import LinearDiscriminantAnalysis\nfrom sklearn.datasets import load_iris\nX,y=load_iris(return_X_y=True)\nprint(LinearDiscriminantAnalysis(n_components=2).fit_transform(X,y)[:5])')}, 'Pattern Search': {'Apriori': ('Find item combinations that frequently occur together.', "from itertools import combinations\ntx=[{'milk','bread'},{'milk','eggs'},{'milk','bread','eggs'}]\nitems=sorted(set().union(*tx))\nfor p in combinations(items,2): print(p,sum(set(p)<=t for t in tx)/len(tx))"), 'FP-Growth': ('Mine frequent itemsets efficiently with a compressed prefix structure.', "tx=[['a','b'],['a','c'],['a','b','c']]\ncounts={}\nfor row in tx:\n    for item in row: counts[item]=counts.get(item,0)+1\nprint(counts)"), 'ECLAT': ('Mine frequent itemsets by intersecting transaction-ID sets.', "tid={'milk':{1,2,3},'bread':{1,3},'eggs':{2,3}}\npair=tid['milk'] & tid['bread']\nprint(len(pair),pair)")}}}, 'Semi-Supervised Learning': {'description': 'Use a small labeled set together with a much larger unlabeled set.', 'example': 'Train an image classifier using 500 labeled images plus 50,000 unlabeled images.', 'families': {'Pseudo-Labeling': {'Self-Training': ('Use confident model predictions as pseudo-labels for unlabeled samples.', "from sklearn.semi_supervised import SelfTrainingClassifier\nfrom sklearn.svm import SVC\nX=[[1],[2],[3],[8],[9],[10]]; y=[0,0,-1,-1,1,1]\nm=SelfTrainingClassifier(SVC(probability=True,gamma='auto')).fit(X,y)\nprint(m.transduction_)")}, 'Graph-Based': {'Label Spreading': ('Propagate known labels through a similarity graph.', 'from sklearn.semi_supervised import LabelSpreading\nX=[[1],[2],[3],[8],[9],[10]]; y=[0,0,-1,-1,1,1]\nm=LabelSpreading(gamma=.5).fit(X,y)\nprint(m.transduction_)')}}}, 'Self-Supervised Learning': {'description': 'Create supervision from the raw data itself to learn useful representations.', 'example': 'Mask part of a sentence or image and train the model to recover what is missing.', 'families': {'Representation Learning': {'Masked Prediction': ('Hide part of an input and predict it from context.', "import numpy as np\nx=np.array([10.,20.,30.,40.]); idx=2\ncontext=np.delete(x,idx)\nprint('target:',x[idx],'toy prediction:',context.mean())"), 'Contrastive Learning': ('Pull related representations together and push unrelated ones apart.', 'import numpy as np\na=np.array([1.,0.]); pos=np.array([.9,.1]); neg=np.array([-1.,0.])\ncos=lambda x,y:x@y/(np.linalg.norm(x)*np.linalg.norm(y))\nprint(cos(a,pos),cos(a,neg))')}}}, 'Reinforcement Learning': {'description': 'Learn behavior by interacting with an environment and maximizing cumulative reward.', 'example': 'Train an agent to choose actions that maximize long-term reward in a game or control system.', 'families': {'Value-Based': {'Q-Learning': ('Learn a table of state-action values.', 'import numpy as np\nQ=np.zeros((3,2)); s,a,r,s2=0,1,1.,2; alpha,gamma=.1,.9\nQ[s,a]+=alpha*(r+gamma*Q[s2].max()-Q[s,a])\nprint(Q)'), 'Deep Q-Network': ('Approximate Q-values with a neural network.', 'import torch, torch.nn as nn\nq=nn.Sequential(nn.Linear(4,16),nn.ReLU(),nn.Linear(16,2))\nprint(q(torch.tensor([[.1,.2,.3,.4]])).detach().numpy())')}, 'Actor-Critic': {'A3C': ('Use parallel actor-learners to improve a shared policy and value function.', 'import torch.nn as nn\nclass ActorCritic(nn.Module):\n    def __init__(self):\n        super().__init__(); self.body=nn.Sequential(nn.Linear(4,32),nn.ReLU()); self.policy=nn.Linear(32,2); self.value=nn.Linear(32,1)\nprint(ActorCritic())')}, 'Evolutionary': {'Genetic Algorithm': ('Search for high-fitness solutions through selection and mutation.', 'import random\npop=[random.uniform(-5,5) for _ in range(8)]; fitness=lambda x:-(x-2.)**2\nfor _ in range(5):\n    pop=sorted(pop,key=fitness,reverse=True)[:4]; pop += [x+random.gauss(0,.5) for x in pop]\nprint(max(pop,key=fitness))')}}}, 'Artificial Neural Networks → Deep Learning': {'description': 'Use layered differentiable networks; deeper architectures learn hierarchical representations.', 'example': 'Learn complex representations from images, text, audio, time series, or tabular data.', 'families': {'Foundational ANN': {'Multilayer Perceptron': ('Use fully connected hidden layers for nonlinear prediction.', 'from sklearn.neural_network import MLPClassifier\nX=[[0,0],[0,1],[1,0],[1,1]]; y=[0,1,1,0]\nm=MLPClassifier(hidden_layer_sizes=(8,),max_iter=2000,random_state=42).fit(X,y)\nprint(m.predict(X))'), 'RBF Neural Network': ('Use radial-basis activations centered around prototype points.', 'import numpy as np\nx=np.array([1.5,2.]); centers=np.array([[1.,2.],[3.,3.]])\nprint(np.exp(-((centers-x)**2).sum(axis=1)))')}, 'Deep Architectures': {'CNN': ('Learn spatial filters for images and other grid-like data.', 'import torch, torch.nn as nn\nm=nn.Sequential(nn.Conv2d(1,8,3),nn.ReLU(),nn.AdaptiveAvgPool2d(1),nn.Flatten(),nn.Linear(8,2))\nprint(m(torch.randn(1,1,28,28)).shape)'), 'RNN': ('Process sequences while carrying hidden state over time.', 'import torch, torch.nn as nn\nm=nn.RNN(3,5,batch_first=True); out,h=m(torch.randn(2,4,3))\nprint(out.shape,h.shape)'), 'LSTM': ('Use gated memory cells for longer sequential dependencies.', 'import torch, torch.nn as nn\nm=nn.LSTM(3,5,batch_first=True); out,(h,c)=m(torch.randn(2,4,3))\nprint(out.shape,h.shape,c.shape)'), 'GRU': ('Use a streamlined gated recurrent architecture.', 'import torch, torch.nn as nn\nm=nn.GRU(3,5,batch_first=True); out,h=m(torch.randn(2,4,3))\nprint(out.shape,h.shape)'), 'Transformer': ('Use self-attention for long-range context modeling.', 'import torch, torch.nn as nn\nlayer=nn.TransformerEncoderLayer(d_model=8,nhead=2,batch_first=True)\nm=nn.TransformerEncoder(layer,num_layers=1)\nprint(m(torch.randn(2,5,8)).shape)'), 'GAN': ('Train a generator and discriminator adversarially.', 'import torch.nn as nn\nG=nn.Sequential(nn.Linear(8,16),nn.ReLU(),nn.Linear(16,4))\nD=nn.Sequential(nn.Linear(4,16),nn.ReLU(),nn.Linear(16,1),nn.Sigmoid())\nprint(G); print(D)'), 'Autoencoder': ('Compress data into a latent code and reconstruct it.', 'import torch, torch.nn as nn\nae=nn.Sequential(nn.Linear(4,2),nn.ReLU(),nn.Linear(2,4))\nprint(ae(torch.randn(3,4)).shape)')}}}, 'Ensemble Learning': {'description': 'Combine multiple learners to improve accuracy, stability, or generalization.', 'example': 'Combine several models so the ensemble is more reliable than any single learner.', 'families': {'Bagging': {'Random Forest': ('Average many randomized trees to reduce variance.', 'from sklearn.ensemble import RandomForestClassifier\nX=[[1,1],[1,2],[4,4],[5,5]]; y=[0,0,1,1]\nm=RandomForestClassifier(n_estimators=50,random_state=42).fit(X,y)\nprint(m.predict([[4,5]]))')}, 'Boosting': {'Gradient Boosting': ('Add learners sequentially to correct previous residual errors.', 'from sklearn.ensemble import GradientBoostingClassifier\nX=[[1],[2],[3],[8],[9],[10]]; y=[0,0,0,1,1,1]\nm=GradientBoostingClassifier(random_state=42).fit(X,y)\nprint(m.predict([[7]]))'), 'XGBoost': ('Use regularized optimized gradient-boosted trees.', "from xgboost import XGBClassifier\nX=[[1],[2],[3],[8],[9],[10]]; y=[0,0,0,1,1,1]\nm=XGBClassifier(n_estimators=20,max_depth=2,eval_metric='logloss').fit(X,y)\nprint(m.predict([[7]]))"), 'LightGBM': ('Use efficient histogram-based gradient-boosted trees.', 'from lightgbm import LGBMClassifier\nX=[[1],[2],[3],[8],[9],[10]]; y=[0,0,0,1,1,1]\nm=LGBMClassifier(n_estimators=20,verbosity=-1).fit(X,y)\nprint(m.predict([[7]]))')}, 'Stacking': {'Stacking Classifier': ('Train a meta-model on predictions from diverse base models.', "from sklearn.ensemble import StackingClassifier,RandomForestClassifier\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.svm import SVC\nX=[[1],[2],[3],[8],[9],[10]]; y=[0,0,0,1,1,1]\nm=StackingClassifier([('rf',RandomForestClassifier(n_estimators=20,random_state=42)),('svm',SVC(probability=True))],final_estimator=LogisticRegression()).fit(X,y)\nprint(m.predict([[7]]))")}}}, 'Statistical Inference': {'description': 'Estimate uncertainty and draw population-level conclusions from sample data.', 'example': 'Test whether an observed treatment effect is likely larger than ordinary sampling noise.', 'families': {'Estimation': {'Confidence Interval': ('Estimate a plausible range for an unknown population parameter.', 'import numpy as np\nfrom scipy import stats\nx=np.array([10,11,9,12,10,11,13,10]); mean=x.mean(); margin=stats.t.ppf(.975,len(x)-1)*stats.sem(x)\nprint(mean-margin,mean+margin)')}, 'Hypothesis Testing': {'t-Test': ('Compare two means and quantify evidence against a no-difference hypothesis.', 'from scipy.stats import ttest_ind\na=[10,11,9,10,12]; b=[14,13,15,14,16]\nprint(ttest_ind(a,b,equal_var=False))')}, 'Bayesian Inference': {'Bayes Update': ('Update a prior probability using observed evidence.', 'prior=.01; sensitivity=.95; false_positive=.05\nposterior=sensitivity*prior/(sensitivity*prior+false_positive*(1-prior))\nprint(round(posterior,4))')}}}}

def choose(title, options):
    print("\n" + "="*78)
    print(title)
    print("="*78)
    for i, item in enumerate(options, 1):
        print(f"{i:>2}. {item}")
    print(" 0. Back / Exit")
    while True:
        raw = input("\nChoice: ").strip()
        if raw == "0":
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw)-1]
        print("Enter one of the menu numbers.")

def write_current_notebook(path, example, code):
    nb = {
      "cells":[
        {"cell_type":"markdown","metadata":{},"source":[
          "# " + " → ".join(path) + "\n",
          "\n**One-sentence example:** " + example + "\n",
          "\nRun the code below, experiment with it, then return to the CLI when finished.\n"
        ]},
        {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],
          "source":[line+"\n" for line in code.splitlines()]}
      ],
      "metadata":{
        "kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},
        "language_info":{"name":"python","version":"3"}
      },
      "nbformat":4,"nbformat_minor":5
    }
    out = ROOT / "current_algorithm.ipynb"
    out.write_text(json.dumps(nb, indent=2), encoding="utf-8")
    return out

def open_jupyter(nb):
    print("\nLaunching Jupyter for:", nb.name)
    print("When you stop the Jupyter server with Ctrl+C, this CLI resumes.")
    for mode in ("lab","notebook"):
        try:
            rc = subprocess.call([sys.executable,"-m","jupyter",mode,str(nb)], cwd=ROOT)
            return rc
        except FileNotFoundError:
            continue
    print("Jupyter not available. Run: pip install -r requirements.txt")
    return 1

def lesson(path, example, code):
    print("\n" + "─"*78)
    print(" → ".join(path))
    print("─"*78)
    print("Example:", example)
    print("\nPython snippet:\n")
    print(textwrap.indent(code, "    "))
    while True:
        print("\n1. Run snippet in terminal")
        print("2. Create/open this lesson in Jupyter")
        print("3. Create notebook only (do not launch)")
        print("0. Back")
        c = input("Choice: ").strip()
        if c == "1":
            print("\n--- runtime output ---")
            try:
                scope={}
                exec(code, scope, scope)
            except Exception as e:
                print(type(e).__name__ + ":", e)
            print("--- end output ---")
        elif c == "2":
            open_jupyter(write_current_notebook(path, example, code))
        elif c == "3":
            print("Created:", write_current_notebook(path, example, code))
        elif c == "0":
            return
        else:
            print("Enter 0, 1, 2, or 3.")

def interactive():
    while True:
        paradigm = choose("ML LANDSCAPE — choose a learning paradigm / major family", list(CATALOG))
        if paradigm is None:
            return
        p = CATALOG[paradigm]
        print("\n" + p["description"])
        print("Example:", p["example"])
        while True:
            family = choose(paradigm + " — choose a model family", list(p["families"]))
            if family is None:
                break
            algorithms = p["families"][family]
            while True:
                algo = choose(paradigm + " → " + family + " — choose an algorithm", list(algorithms))
                if algo is None:
                    break
                example, code = algorithms[algo]
                lesson([paradigm, family, algo], example, code)

def print_tree():
    for p,pdata in CATALOG.items():
        print(p)
        for f, algos in pdata["families"].items():
            print("  ├─ " + f)
            for a in algos:
                print("  │   └─ " + a)

def build_all_notebook():
    cells=[]
    for p,pdata in CATALOG.items():
        cells.append({"cell_type":"markdown","metadata":{},"source":["# "+p+"\n","\n"+pdata["description"]+"\n","\n**Example:** "+pdata["example"]+"\n"]})
        for f, algos in pdata["families"].items():
            cells.append({"cell_type":"markdown","metadata":{},"source":["## "+f+"\n"]})
            for a,(example,code) in algos.items():
                cells.append({"cell_type":"markdown","metadata":{},"source":["### "+a+"\n","\n"+example+"\n"]})
                cells.append({"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[line+"\n" for line in code.splitlines()]})
    nb={"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3"}},"nbformat":4,"nbformat_minor":5}
    out=ROOT/"ml_landscape_all.ipynb"
    out.write_text(json.dumps(nb,indent=2),encoding="utf-8")
    print("Created:",out)

if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--list",action="store_true",help="Print the whole taxonomy")
    ap.add_argument("--build-all-notebook",action="store_true",help="Create one notebook containing every lesson")
    args=ap.parse_args()
    if args.list:
        print_tree()
    elif args.build_all_notebook:
        build_all_notebook()
    else:
        interactive()
