
def update_food_cost_solve(dat):
    """Increases food cost by 20%"""
    foods = dat.foods.copy()
    foods['Per Unit Cost'] = 1.2 * foods['Per Unit Cost']
    foods = foods.round({'Per Unit Cost': 2})
    dat.foods = foods
    return dat
