import mip_me
import unittest
import inspect
import os
from math import isclose


def _this_directory():
    return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getsourcefile(_this_directory))))


def read_data(input_data_loc, schema):
    """
    Reads data from files and populates an instance of the corresponding schema.

    Parameters
    ----------
    input_data_loc: str
        The location of the data set inside the `data/` directory.
        It can be a directory containing CSV files, a xls/xlsx file, or a json file.
    schema: PanDatFactory
        An instance of the PanDatFactory class of ticdat.
    Returns
    -------
    PanDat
        a PanDat object populated with the tables available in the input_data_loc.
    """
    print(f'Reading data from: {input_data_loc}')
    path = os.path.join(_this_directory(), "data", input_data_loc)
    assert os.path.exists(path), f"bad path {path}"
    if input_data_loc.endswith(".xlsx") or input_data_loc.endswith(".xls"):
        dat = schema.xls.create_pan_dat(path)
    elif input_data_loc.endswith("json"):
        dat = schema.json.create_pan_dat(path)
    else:  # read from cvs files
        dat = schema.csv.create_pan_dat(path)
    return dat


def write_data(sln, output_data_loc, schema):
    """
    Writes data to the specified location.

    Parameters
    ----------
    sln: PanDat
        A PanDat object populated with the data to be written to file/files.
    output_data_loc: str
        A destination inside `data/` to write the data to.
        It can be a directory (to save the data as CSV files), a xls/xlsx file, or a json file.
    schema: PanDatFactory
        An instance of the PanDatFactory class of ticdat compatible with sln.
    Returns
    -------
    None
    """
    print(f'Writing data back to: {output_data_loc}')
    path = os.path.join(_this_directory(), "data", output_data_loc)
    # assert os.path.exists(path), f"bad path {path}"
    if output_data_loc.endswith(".xlsx") or output_data_loc.endswith("xls"):
        schema.xls.write_file(sln, path)
    elif output_data_loc.endswith(".json"):
        schema.json.write_file(sln, path)
    else:  # write to csv files
        schema.csv.write_directory(sln, path)
    return None


class TestLocalExecution(unittest.TestCase):

    def test_1_action_data_ingestion(self):
        # Reads the raw data and places a copy of it inside the 'data/inputs' directory.
        dat = read_data(os.path.join('testing_data', 'tiny_data.json'), mip_me.input_schema)
        self.assertTrue(mip_me.input_schema.good_pan_dat_object(dat), "bad dat check")
        self.assertDictEqual(mip_me.input_schema.find_duplicates(dat), dict(), "duplicate row check")
        self.assertDictEqual(mip_me.input_schema.find_foreign_key_failures(dat), dict(), "foreign key check")
        self.assertDictEqual(mip_me.input_schema.find_data_type_failures(dat), dict(), "data type value check")
        self.assertDictEqual(mip_me.input_schema.find_data_row_failures(dat), dict(), "data row check")
        write_data(dat, 'inputs', mip_me.input_schema)

    def test_2_update_food_cost(self):
        dat = read_data('inputs', mip_me.input_schema)
        params = mip_me.input_schema.create_full_parameters_dict(dat)
        total_cost_old = params['Food Cost Multiplier'] * dat.foods['Per Unit Cost'].sum()
        dat_ = mip_me.action_update_food_cost.update_food_cost_solve(dat)
        close_enough = isclose(total_cost_old, dat_.foods['Per Unit Cost'].sum(), rel_tol=1e-2)
        self.assertTrue(close_enough, "food cost update check")
        write_data(dat_, 'inputs', mip_me.input_schema)

    def test_3_main_solve(self):
        dat = read_data('inputs', mip_me.input_schema)
        sln = mip_me.solve(dat)
        self.assertTrue(isclose(sln.buy['Quantity'].sum(), 667, rel_tol=1e-2), "total buy qty check")
        write_data(sln, 'outputs', mip_me.output_schema)

    def test_4_report_builder(self):
        dat = read_data('inputs', mip_me.input_schema)
        sln = read_data('outputs', mip_me.output_schema)
        sln = mip_me.action_report_builder.report_builder_solve(dat, sln)
        self.assertTrue(isclose(sln.nutrition['Quantity'].sum(), 250.37, rel_tol=1e-2), "total nutrition qty check")
        write_data(sln, 'outputs', mip_me.output_schema)


if __name__ == '__main__':
    unittest.main()
