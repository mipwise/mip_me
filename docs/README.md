# Diet Problem
This directory contains documentation about the Diet Problem, which is the 
problem we use along the [Mip Go](https://www.mipwise.com/mip-go) program.

The *Diet Problem*, also known as *Stigler diet*, is a classic 
optimization problem widely used to illustrate a use case
of linear programming. You can find much more details on Wikipedia: 
[Stigler Diet](https://en.wikipedia.org/wiki/Stigler_diet)

Here is a short statement of the problem:

*Given a set of foods and a set of nutrients, the goal is to 
make a selection of food and the respective quantity to compose 
the least expensive diet that meets min and max recommended 
intake of nutrients.*

## Input schema
We can organize the input data for the Diet Problem in three
tables, `foods`, `nutrients`, and `foods_nutrients`.

Here is a sample data with three foods and two nutrients only:

* `foods`

| Food ID | Food Name  | Per Unit Cost |
|:-------:|:----------:|:-------------:|
|   f1    |   Grapes   |      3.5      |
|   f2    |   Melon    |      5.6      |
|   f3    | Watermelon |      2.3      |

* `nutrients`

| Nutrient ID | Nutrient Name | Min Intake | Max Intake |
|:-----------:|:-------------:|:----------:|:----------:|
|     n1      |   Calories    |   2000.0   |   4000.0   |
|     n2      | Carbohydrates |   250.0    |   450.0    |

* `foods_nutrients`

| Food ID | Nutrient ID | Quantity |
|:-------:|:-----------:|:--------:|
|   f1    |     n1      |   0.69   |
|   f2    |     n1      |   0.28   |
|   f3    |     n1      |   0.3    |
|   f1    |     n2      |  0.181   |
|   f2    |     n2      |  0.0658  |
|   f3    |     n2      |  0.0755  |

## Formulation and models
A formulation of the Diet Problem is in the 
[diet_problem.ipynb](diet_problem.ipynb) Jupyter Notebook.

The model is implemented in solving engine in [main.py](../mip_me/main.py).