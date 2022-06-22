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
        The location of the data set inside the `data/` directory. It can be a directory containing CSV files or an
        Excel file.
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
    if input_data_loc.endswith("xlsx"):
        return schema.xls.create_pan_dat(path)
    return schema.csv.create_pan_dat(path)


def write_data(sln, output_data_loc, schema):
    """
    Writes data as CSV files to the specified location.

    Parameters
    ----------
    sln: PanDat
        A PanDat object populated with the data to be written to CSV files.
    output_data_loc: str
        A subdirectory of `data/` to write the data to.
    schema: PanDatFactory
        An instance of the PanDatFactory class of ticdat compatible with sln.
    Returns
    -------
    None
    """
    print(f'Writing data back to: {output_data_loc}')
    path = os.path.join(_this_directory(), "data", output_data_loc)
    assert os.path.exists(path), f"bad path {path}"
    if output_data_loc.endswith("xlsx"):
        schema.xls.write_file(sln, path)
    schema.csv.write_directory(sln, path)
    return None


class TestMipMe(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dat = read_data("testing_data.xlsx", mip_me.input_schema)

    def test_action_data_ingestion(self):
        # Pools the data from '_input_data' and place it in the 'data/inputs' directory.
        dat = self.dat
        self.assertTrue(mip_me.input_schema.good_pan_dat_object(dat), "bad dat check")
        self.assertDictEqual(mip_me.input_schema.find_duplicates(dat), dict(), "duplicate row check")
        self.assertDictEqual(mip_me.input_schema.find_foreign_key_failures(dat), dict(), "foreign key check")
        self.assertDictEqual(mip_me.input_schema.find_data_type_failures(dat), dict(), "data type value check")
        self.assertDictEqual(mip_me.input_schema.find_data_row_failures(dat), dict(), "data row check")
        write_data(dat, 'inputs', mip_me.input_schema)

    def test_update_food_cost(self):
        dat = read_data('inputs', mip_me.input_schema)
        params = mip_me.input_schema.create_full_parameters_dict(dat)
        total_cost_old = params['Food Cost Multiplier'] * dat.foods['Per Unit Cost'].sum()
        dat_ = mip_me.action_update_food_cost.update_food_cost_solve(dat)
        self.assertTrue(isclose(total_cost_old, dat_.foods['Per Unit Cost'].sum(), rel_tol=1e-2),
                        "food cost update check")
        write_data(dat_, 'inputs', mip_me.input_schema)

    def test_main_solve_testing_data(self):
        dat = self.dat
        sln = mip_me.solve(dat)
        df = sln.buy
        quantities_dict = {'f1': 0.0, 'f2': 0.0, 'f3': 667}
        self.assertDictEqual(quantities_dict, dict(zip(df['Food ID'], df['Quantity'])), "buy quantity check")
        write_data(sln, 'outputs', mip_me.output_schema)

    def test_report_builder(self):
        dat = self.dat
        sln = read_data('outputs', mip_me.output_schema)
        sln = mip_me.action_report_builder.report_builder_solve(dat, sln)
        self.assertTrue(isclose(sln.nutrition['Quantity'].sum(), 250.37, rel_tol=1e-2),
                        "total nutrition quantity check")
        write_data(sln, 'outputs', mip_me.output_schema)


if __name__ == '__main__':
    unittest.main()
