from mip_me import output_schema
from mip_me import input_schema

import pulp
import pandas as pd


def solve(dat):
    """Main solve engine that prepares the data, builds and solve the optimization model, and populates the buy table
    from the output of the optimization."""
    params = input_schema.create_full_parameters_dict(dat)
    # Prepare optimization parameters
    I = set(dat.foods['Food ID'])
    J = set(dat.nutrients['Nutrient ID'])
    nl = dict(zip(dat.nutrients['Nutrient ID'], dat.nutrients['Min Intake']))
    nu = dict(zip(dat.nutrients['Nutrient ID'], dat.nutrients['Max Intake']))
    nq = dict(zip(zip(dat.foods_nutrients['Food ID'], dat.foods_nutrients['Nutrient ID']),
                  dat.foods_nutrients['Quantity']))
    c = dict(zip(dat.foods['Food ID'], dat.foods['Per Unit Cost']))

    # Build optimization model
    mdl = pulp.LpProblem("diet_problem", sense=pulp.LpMinimize)
    if params['Food Portions'] == 'Ensure whole portions':
        x = pulp.LpVariable.dicts(indices=I, cat=pulp.LpInteger, lowBound=0.0, name='x')
    else:
        x = pulp.LpVariable.dicts(indices=I, cat=pulp.LpContinuous, lowBound=0.0, name='x')
    yu = pulp.LpVariable.dicts(indices=J, cat=pulp.LpContinuous, lowBound=0.0, name='yu')
    yl = pulp.LpVariable.dicts(indices=J, cat=pulp.LpContinuous, lowBound=0.0, name='yl')
    for j in J:
        if nl[j] == nl[j]:
            mdl.addConstraint(pulp.lpSum(nq.get((i, j), 0) * x[i] for i in I) >= nl[j] - yl[j], name=f'C1_{j}')
        if nu[j] == nu[j]:
            mdl.addConstraint(pulp.lpSum(nq.get((i, j), 0) * x[i] for i in I) <= nu[j] + yu[j], name=f'C2_{j}')
        if params['Feasibility'] == 'Flexible':
            yl[j].upBound = nl[j]
        else:
            yl[j].upBound = 0.0
            yu[j].upBound = 0.0
    mdl.setObjective(pulp.lpSum(c[i] * x[i] for i in I)
                     + params['Violation Penalty'] * pulp.lpSum(yu[j] for j in J)
                     + params['Violation Penalty'] * pulp.lpSum(yl[j] for j in J))

    # Optimize and retrieve the solution
    mdl.solve()
    status = mdl.solve(pulp.PULP_CBC_CMD(timeLimit=params['Time Limit'], gapRel=params['MIP Gap']))
    status = pulp.LpStatus[status]
    if status == 'Optimal':
        x_sol = [(key, var.value()) for key, var in x.items()]
        print(f'Optimal solution found!')
    else:
        x_sol = None
        print(f'Model is not optimal. Status: {status}')

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
