# Cultural Consensus Theory (CCT) - PyMC Implementation

## Objective

This project is about building a basic Cultural Consensus Theory (CCT) model using PyMC. The idea is to look at a small dataset of people’s answers about local plant knowledge, and figure out what the "shared" answers probably are (the consensus), as well as how competent each informant is.

## What’s the Model About?

The theory (Romney et al., 1986) assumes that people who know more tend to agree with the cultural norm more often. So if someone keeps agreeing with the group, they’re probably more knowledgeable.

In this model:

- `D_i` = informant competence (how likely they are to get things right), and we assume it’s between 0.5 and 1.
- `Z_j` = the "correct"/consensus answer for each question (either 0 or 1).
- The probability that person i says “1” on question j is:

p_ij = Z_j * D_i + (1 - Z_j) * (1 - D_i)


If the correct answer is 1, they’ll say 1 with probability equal to their competence. If the correct answer is 0, then they’ll say 0 with that same probability.

## What I Did

- Loaded the data, removed the ID column.
- Set priors: `D ~ Uniform(0.5, 1)` and `Z ~ Bernoulli(0.5)`
- Built the model using PyMC, and ran MCMC with 2000 draws and 4 chains.
- Plotted posterior distributions and checked R-hat values (all around 1.0 so we’re good).

## Key Results

- Some informants had high competence (close to 1), others were around 0.56.
- Most consensus answers were really confident (posterior means near 0 or 1).
- The model’s inferred answers didn’t always match the simple majority vote.

## Majority Vote vs. CCT Model

I also compared the CCT consensus answers with what you'd get from a majority vote. A few questions were different. That makes sense — if less competent people dominate the majority, majority vote can be wrong. The CCT model does better because it weights people by how much they actually know.

## Folder Structure

cct-midterm/
├── code/
│ └── cct.py # PyMC model code
├── data/
│ └── plant_knowledge.csv # The dataset
└── README.md # This file


## Author

Vanessa Wu  
May13, 2025
