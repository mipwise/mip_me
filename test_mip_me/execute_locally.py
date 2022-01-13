from mip_me import input_schema, output_schema
from mip_me import build_report_solve

input_path = "data/inputs"
output_path = "data/outputs"
dat = input_schema.csv.create_pan_dat(input_path)
sln = output_schema.csv.create_pan_dat(output_path)
sln = build_report_solve(dat, sln)
output_schema.csv.write_directory(sln, output_path)
