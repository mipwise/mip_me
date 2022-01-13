from mip_me import input_schema, output_schema
from mip_me import update_food_cost_solve
from mip_me import solve
from mip_me import report_builder_solve

import os
import inspect


def _this_directory():
    return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getsourcefile(_this_directory))))


def read_xls_data(schema, data):
    path = os.path.join(_this_directory(), "data", data)
    assert os.path.exists(path), f"bad path {path}"
    print(f'Reading data from: {data}')
    return schema.xls.create_pan_dat(path)


def read_csv_data(schema, data):
    path = os.path.join(_this_directory(), "data", data)
    assert os.path.exists(path), f"bad path {path}"
    print(f'Reading data from: {data}')
    return schema.csv.create_pan_dat(path)


def write_csv_data(dat_sln, schema, solution_dir):
    path = os.path.join(_this_directory(), "data", solution_dir)
    assert os.path.exists(path), f"bad path {path}"
    print(f'Writing data back to: {solution_dir}')
    return schema.csv.write_directory(dat_sln, path)


engine = {0: 'Data Ingestion',
          1: 'Action Update Food Cost',
          2: 'Main Solve',
          3: 'Action Report Builder'}[3]

if engine == 'Data Ingestion':
    dat = read_xls_data(input_schema, 'testing_data.xlsx')
    write_csv_data(dat, input_schema, 'inputs')
elif engine == 'Action Update Food Cost':
    dat = read_csv_data(input_schema, 'inputs')
    dat = update_food_cost_solve(dat)
    write_csv_data(dat, input_schema, 'inputs')
elif engine == 'Main Solve':
    dat = read_csv_data(input_schema, 'inputs')
    sln = solve(dat)
    write_csv_data(sln, output_schema, 'outputs')
elif engine == 'Action Report Builder':
    dat = read_csv_data(input_schema, 'inputs')
    sln = read_csv_data(output_schema, 'outputs')
    sln = report_builder_solve(dat, sln)
    write_csv_data(sln, output_schema, 'outputs')
else:
    raise ValueError('Bad engine')


