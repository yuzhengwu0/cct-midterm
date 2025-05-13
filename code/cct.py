# ---------- Step 1: Import packages and load data ----------
import pandas as pd
import numpy as np
import pymc as pm
import aesara.tensor as at
import arviz as az

def load_data(filepath='data/plant_knowledge.csv'):
    df = pd.read_csv(filepath)
    data = df.iloc[:, 1:].values  # Remove the first column (Informant ID)
    return data

X = load_data()
N, M = X.shape  # N = number of informants, M = number of questions/items

# ---------- Step 2: Build the model ----------
with pm.Model() as model:
    # Prior for each informant's competence (between 0.5 and 1)
    D = pm.Uniform('D', lower=0.5, upper=1.0, shape=N)

    # Prior for each question's consensus answer (0 or 1)
    Z = pm.Bernoulli('Z', p=0.5, shape=M)

    # Broadcast D and Z to match shapes (N, M)
    D_broadcast = D[:, None]
    Z_broadcast = Z[None, :]

    # Calculate probability of each informant giving a "1" response
    p = Z_broadcast * D_broadcast + (1 - Z_broadcast) * (1 - D_broadcast)

    # Likelihood: observed data follows a Bernoulli distribution with calculated probabilities
    X_obs = pm.Bernoulli('X_obs', p=p, observed=X)

    # ---------- Step 3: Sampling ----------
    trace = pm.sample(2000, tune=1000, chains=4, target_accept=0.9, return_inferencedata=True)

# ---------- Step 4: Analyze results ----------
# Print summary statistics for competence and consensus answers
print(az.summary(trace, var_names=['D', 'Z']))

# Plot posterior distributions
az.plot_posterior(trace, var_names=["D"])
az.plot_posterior(trace, var_names=["Z"])

# ---------- Step 5: Postprocessing ----------
# Get mean of posterior samples
D_means = trace.posterior['D'].mean(dim=("chain", "draw")).values
Z_means = trace.posterior['Z'].mean(dim=("chain", "draw")).values

# Get most likely consensus answers (1 if > 0.5)
Z_consensus = (Z_means > 0.5).astype(int)

# Calculate naive majority vote per item
majority_vote = (X.mean(axis=0) > 0.5).astype(int)

# Print comparison
print("\nConsensus answers from model:\n", Z_consensus)
print("\nMajority vote answers:\n", majority_vote)
print("\nDifference (1 = different):\n", Z_consensus != majority_vote)
