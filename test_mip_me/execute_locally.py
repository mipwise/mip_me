import mip_me
import inspect
import os


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


if __name__ == "__main__":
    _input_data_loc = {
        1: "testing_data.xlsx",  # Loads data from the 'data/test_data_1.xlsx' workbook.
        2: "testing_data_2",  # Loads data from csv files in the 'data/test_data_2' directory.
        3: "inputs"}[1]  # Loads data from csv files in the 'data/inputs' directory.
    engine = {
        1: 'Action Data Ingestion',
        2: 'Update Food Cost',
        3: 'Main Solve',
        4: 'Report Builder'}[3]
    if engine == 'Action Data Ingestion':
        # Pools the data from '_input_data' and place it in the 'data/inputs' directory.
        dat = read_data(_input_data_loc, mip_me.input_schema)
        write_data(dat, 'inputs', mip_me.input_schema)
    elif engine == 'Update Food Cost':
        dat = read_data(_input_data_loc, mip_me.input_schema)
        dat = mip_me.action_update_food_cost.update_food_cost_solve(dat)
        write_data(dat, 'inputs', mip_me.input_schema)
    elif engine == 'Main Solve':
        dat = read_data(_input_data_loc, mip_me.input_schema)
        _sln = mip_me.solve(dat)
        write_data(_sln, 'outputs', mip_me.output_schema)
    elif engine == 'Report Builder':
        dat = read_data(_input_data_loc, mip_me.input_schema)
        _sln = read_data('outputs', mip_me.output_schema)
        _sln = mip_me.action_report_builder.report_builder_solve(dat, _sln)
        write_data(_sln, 'outputs', mip_me.output_schema)
    else:
        raise ValueError('Bad engine')
