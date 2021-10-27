![Unit tests (python versions)](https://github.com/SABS-R3-Epidemiology/seirmo/workflows/Unit%20tests%20(python%20versions)/badge.svg)
![Unit tests (OS versions)](https://github.com/SABS-R3-Epidemiology/seirmo/workflows/Unit%20tests%20(OS%20versions)/badge.svg)
[![codecov](https://codecov.io/gh/SABS-R3-Epidemiology/seirmo/branch/main/graph/badge.svg?token=D1P3CMQTDP)](https://codecov.io/gh/SABS-R3-Epidemiology/seirmo)
[![Documentation Status](https://readthedocs.org/projects/seirmo/badge/?version=latest)](https://seirmo.readthedocs.io/en/latest/?badge=latest)

## Table of contents
* [General info](#general-info)
* [Deterministic Model](#deterministic-model)
* [Setup](#set-up)

## General Info
This program models the outbreak of an infectious disease with the SEIR model. The SEIR model is a compartmental model with four compartments: susceptible (S), exposed (but not yet infectious) (E), infectious (I), and recovered (R). Each individual is in one compartment at a time, and different rates quantify the movement of an individual from one compartment to another. 



Two submodels are defined in the program: a deterministic SEIR model and a stochastic SEIR model. Both are non-spatial and are time dependant. 


## Deterministic Model
The deterministic model supposes that the population is homogeneous and that small fluctuations in compartments do not impact the general solution. The deterministic model solves this set of ODEs: 

<img src="https://render.githubusercontent.com/render/math?math=\frac{dS(t)}{dt} = - \beta S(t) I(t) ">
<img src="https://render.githubusercontent.com/render/math?math=\frac{dE(t)}{dt} = \beta S(t) I(t) - \kappa E(t) ">
<img src="https://render.githubusercontent.com/render/math?math=\frac{dI(t)}{dt} = \kappa E(t) - \gamma I(t)">
<img src="https://render.githubusercontent.com/render/math?math=\frac{dR(t)}{dt} = \gamma I(t)">


## Set up
