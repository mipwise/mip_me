from mip_me import input_schema
from mip_me.action_update_food_cost import update_food_cost_solve
input_path = "test_mip_me/data/inputs"
output_path = "test_mip_me/data/inputs/testing_data.xlsx"
dat = input_schema.csv.create_pan_dat(input_path)
dat = update_food_cost_solve(dat)
input_schema.xls.write_file(dat, output_path)
