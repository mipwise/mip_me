from mip_me import input_schema
from mip_me.action_update_food_cost import update_food_cost_solve
path = "test_mip_me/data/inputs"
dat = input_schema.csv.create_pan_dat(path)
print('Before:\n', dat.foods)
dat = update_food_cost_solve(dat)
print('After:\n', dat.foods)
