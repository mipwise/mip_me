"""
Contains the solve code that calls the cure engine.

Created by Aster Santana (Aug, 2021), MipMaster.org.
"""

from mip_start import data_bridge
from mip_start.schemas import input_schema
from mip_start.opt_model_pulp import OptModel


def solve(dat):
    """
    Main solve engine.

    Instantiates classes and calls methods that perform the following tasks:
    - prepare the input data
    - build and solves the optimization model
    - retrieves the solution (if one exists) and populates the output schema.

    :param dat: An object that contains all input tables as attributes (for example, a PanDat object from TicDat).
    :return sln: An object that contains all output tables as attributes (for example, a PanDat object from TicDat).
    """
    params = input_schema.create_full_parameters_dict(dat)
    dat_in = data_bridge.DatIn(dat, params)
    opt_model = OptModel(dat_in, 'diet_problem')
    opt_model.build_base_model()
    if params['Food Cost'] == 'Include delivery cost':
        opt_model.add_complexity_charge_delivery_cost()
    opt_model.optimize()
    dat_out = data_bridge.DatOut(opt_model.sol)
    sln = dat_out.populate_output_schema(dat)
    return sln
