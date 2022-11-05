import mip_me
import utils
import unittest
import os
from math import isclose


class TestMipMe(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dat = utils.read_data(os.path.join('testing_data', 'tiny_data.json'), mip_me.input_schema)

    def test_1_action_data_ingestion(self):
        """Ensures the input data matches the defined input schema and has no integrity issues."""
        dat = self.dat
        utils.check_data(dat, mip_me.input_schema)

    def test_2_update_food_cost(self):
        dat = self.dat
        params = mip_me.input_schema.create_full_parameters_dict(dat)
        total_cost_old = params['Food Cost Multiplier'] * dat.foods['Per Unit Cost'].sum()
        dat_ = mip_me.action_update_food_cost.update_food_cost_solve(dat)
        close_enough = isclose(total_cost_old, dat_.foods['Per Unit Cost'].sum(), rel_tol=1e-2)
        self.assertTrue(close_enough, "food cost update check")

    def test_3_main_solve(self):
        dat = self.dat
        sln = mip_me.solve(dat)
        self.assertTrue(isclose(sln.buy['Quantity'].sum(), 667, rel_tol=1e-2), "total buy qty check - continuous")
        sln = mip_me.action_report_builder.report_builder_solve(self.dat, sln)
        self.assertTrue(isclose(sln.nutrition['Quantity'].sum(), 250.37, rel_tol=1e-2), "total nutrition qty check")

    def test_4_main_solve_with_fractional_portions(self):
        dat = mip_me.input_schema.copy_pan_dat(self.dat)
        dat.parameters.loc[dat.parameters['Name'] == 'Food Portions', 'Value'] = 'Portions can be fractional'
        sln = mip_me.solve(dat)
        self.assertTrue(isclose(sln.buy['Quantity'].sum(), 667, rel_tol=1e-2), "total buy qty check - integer")

    def test_5_main_solve_with_infeasible_model(self):
        dat = mip_me.input_schema.copy_pan_dat(self.dat)
        dat.parameters.loc[dat.parameters['Name'] == 'Feasibility', 'Value'] = 'Strict'
        dat.nutrients['Max Intake'] = dat.nutrients['Min Intake'] - 1
        sln = mip_me.solve(dat)
        self.assertEqual(len(sln.buy), 0, "check empty output for infeasible model")


if __name__ == '__main__':
    unittest.main()
