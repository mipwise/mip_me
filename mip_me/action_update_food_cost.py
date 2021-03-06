from mip_me import input_schema


def update_food_cost_solve(dat):
    """Sample input action that simply multiplies the food cost by the Food Cost Multiplier parameter."""
    params = input_schema.create_full_parameters_dict(dat)
    dat_ = input_schema.copy_pan_dat(dat)
    foods = dat_.foods
    foods['Per Unit Cost'] = params['Food Cost Multiplier'] * foods['Per Unit Cost']
    foods = foods.round({'Per Unit Cost': 2})
    dat_.foods = foods
    return dat_


