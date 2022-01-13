from mip_me import input_schema, output_schema
from mip_me import build_report_solve

import os
import inspect


def _this_directory():
    return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getsourcefile(_this_directory))))


def read_data(data_set, schema):
    print(f'Reading data from: {data_set}')
    path = os.path.join(_this_directory(), "data", data_set)
    assert os.path.exists(path), f"bad path {path}"
    # Assuming that data is archived as a collection of csv files, one file for each table
    return schema.csv.create_pan_dat(path)


def write_data(sln, schema, solution_dir):
    print(f'Writing data to: {solution_dir}')
    path = os.path.join(_this_directory(), "data", solution_dir)
    assert os.path.exists(path), f"bad path {path}"
    print(f'Writing data back to: {solution_dir}')
    return schema.csv.write_directory(sln, path)


input_path = "data/inputs"
output_path = "data/outputs"
dat = input_schema.csv.create_pan_dat(input_path)
sln = output_schema.csv.create_pan_dat(output_path)
sln = build_report_solve(dat, sln)
output_schema.csv.write_directory(sln, output_path)

_data_set = {1: "test_data_kaggle",
             2: "test_data_ticdat",
             3: "inputs"}[3]
engine = {1: 'Main Solve',
          2: 'Action Data Ingestion',
          3: 'Action Update Food Cost',
          4: 'Action Report Builder'}[3]
if engine == 'Main Solve':
    dat = read_data("inputs", mip_start.input_schema)
    _sln = mip_start.solve(dat)
    write_data(_sln, mip_start.output_schema, 'outputs')
elif engine == 'Action Update Food Cost':
    solve = mip_start.app_config['actions_config']['Update Food Cost']['engine']
    dat = read_data(_data_set, mip_start.input_schema)
    _sln = solve(dat)
    write_data(_sln, mip_start.input_schema, 'inputs')
elif engine == 'Action Report Builder':
    solve = mip_start.app_config['actions_config']['Report Builder']['engine']
    dat = read_data(_data_set, mip_start.input_schema)
    _sln = read_data('outputs', mip_start.output_schema)
    _sln = solve(dat, _sln)
    write_data(_sln, mip_start.output_schema, 'outputs')
else:
    raise ValueError('Bad engine')


