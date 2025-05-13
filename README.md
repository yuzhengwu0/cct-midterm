# Cultural Consensus Theory (CCT) Model

## Objective

Implement a basic Cultural Consensus Theory (CCT) model using PyMC to analyze a small dataset concerning local plant knowledge. The goal is to estimate the consensus answers to the questions and the competence level of each informant.

## Model Description

This model is based on Romney, Weller & Batchelder (1986), which assumes that the probability of agreement between informants is proportional to their competence. Informants are modeled with latent competence values between 0.5 and 1. Each question has a latent consensus answer (0 or 1).

Priors:
- Competence `D_i ~ Uniform(0.5, 1)`
- Consensus answer `Z_j ~ Bernoulli(0.5)`

The probability of each informant’s answer is defined as:

