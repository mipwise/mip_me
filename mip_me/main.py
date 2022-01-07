from mip_me import output_schema

import gurobipy as gp
import pandas as pd


def solve(dat):
    # Prepare optimization parameters
    I = set(dat.foods['Food ID'])
    J = set(dat.nutrients['Nutrient ID'])
    nl = dict(zip(dat.nutrients['Nutrient ID'], dat.nutrients['Min Intake']))
    nu = dict(zip(dat.nutrients['Nutrient ID'], dat.nutrients['Max Intake']))
    nq = dict(zip(zip(dat.foods_nutrients['Food ID'], dat.foods_nutrients['Nutrient ID']),
                  dat.foods_nutrients['Quantity']))
    c = dict(zip(dat.foods['Food ID'], dat.foods['Per Unit Cost']))

    # Build optimization model
    mdl = gp.Model("diet_problem")
    x = mdl.addVars(I, vtype=gp.GRB.CONTINUOUS, name='x')
    mdl.addConstrs((sum(nq[i, j] * x[i] for i in I) >= nl[j] for j in J), name='min_nutrients')
    mdl.addConstrs((sum(nq[i, j] * x[i] for i in I) <= nu[j] for j in J), name='max_nutrients')
    mdl.setObjective(sum(c[i] * x[i] for i in I), sense=gp.GRB.MINIMIZE)

    # Optimize and retrieve the solution
    mdl.optimize()
    if mdl.status == gp.GRB.OPTIMAL:
        x_sol = [(key, var.X) for key, var in x.items()]
    else:
        x_sol = None
        print(f'Model is not optimal. Status: {mdl.status}')

    # Populate output schema
    sln = output_schema.PanDat()
    if x_sol:
        x_df = pd.DataFrame(x_sol, columns=['Food ID', 'Quantity'])
        # populate buy table
        buy_df = x_df.merge(dat.foods[['Food ID', 'Food Name']], on='Food ID', how='left')
        buy_df = buy_df.round({'Quantity': 2})
        buy_df = buy_df.astype({'Food ID': str, 'Food Name': str, 'Quantity': 'Float64'})
        sln.buy = buy_df[['Food ID', 'Food Name', 'Quantity']]
    return sln
