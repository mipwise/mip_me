import mip_me
import utils
import unittest
import os
from math import isclose


class TestLocalExecution(unittest.TestCase):

    def test_1_action_data_ingestion(self):
        # Reads the raw data and places a copy of it inside the 'data/inputs' directory.
        dat = utils.read_data(os.path.join('testing_data', 'tiny_data.json'), mip_me.input_schema)
        utils.check_data(dat, mip_me.input_schema)
        self.assertIsNone(utils.write_data(dat, 'inputs', mip_me.input_schema))

    def test_2_update_food_cost(self):
        dat = utils.read_data('inputs', mip_me.input_schema)
        params = mip_me.input_schema.create_full_parameters_dict(dat)
        total_cost_old = params['Food Cost Multiplier'] * dat.foods['Per Unit Cost'].sum()
        dat_ = mip_me.action_update_food_cost.update_food_cost_solve(dat)
        close_enough = isclose(total_cost_old, dat_.foods['Per Unit Cost'].sum(), rel_tol=1e-2)
        self.assertTrue(close_enough, "food cost update check")
        utils.write_data(dat_, 'inputs', mip_me.input_schema)

    def test_3_main_solve(self):
        dat = utils.read_data('inputs', mip_me.input_schema)
        sln = mip_me.solve(dat)
        self.assertTrue(isclose(sln.buy['Quantity'].sum(), 667, rel_tol=1e-2), "total buy qty check")
        utils.write_data(sln, 'outputs', mip_me.output_schema)

    def test_4_report_builder(self):
        dat = utils.read_data('inputs', mip_me.input_schema)
        sln = utils.read_data('outputs', mip_me.output_schema)
        sln = mip_me.action_report_builder.report_builder_solve(dat, sln)
        self.assertTrue(isclose(sln.nutrition['Quantity'].sum(), 250.37, rel_tol=1e-2), "total nutrition qty check")
        utils.write_data(sln, 'outputs', mip_me.output_schema)


if __name__ == '__main__':
    unittest.main()
