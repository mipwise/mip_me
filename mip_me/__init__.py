__version__ = "0.1.10"
from mip_me.schemas import input_schema, output_schema
from mip_me.action_update_food_cost import update_food_cost_solve
from mip_me.main import solve
from mip_me.action_report_builder import report_builder_solve

actions_config = {
    'Update Food Cost': {
        'schema': 'input',
        'engine': update_food_cost_solve,
        'tool_tip': "Update the food cost by the factor entered in the 'Food Cost Multiplier' parameter"},
    'Report Builder': {
        'schema': 'output',
        'engine': report_builder_solve,
        'tool_tip': "Reads the output from the main engine and populate the report tables"}
    }

input_tables_config = {
    'hidden': ['parameters'],
    'categories': {
        'Master Tables': ['foods', 'nutrients'],
        'Composition Data': ['foods_nutrients']},
    'order': [],
    'tables_display_names': {
        'foods_nutrients': 'Foods Composition'},
    'columns_display_names': {
        'foods': {'Per Unit Cost': 'Cost ($/unit)',
                  'Fixed Cost': 'Fixed Cost ($)'},
        'nutrients': {'Min Intake': 'Minimum Intake',
                      'Max Intake': 'Maximum Intake'}}
    }

output_tables_config = {
    'hidden': [],
    'categories': {},
    'order': ['buy', 'nutrition'],
    'tables_display_names': {},
    'columns_display_names': {}
    }

parameters_config = {
    'hidden': [],
    'categories': {},
    'order': ['Food Cost', 'Food Portions'],
    'tool_tips': {
        'Food Portions': "Whether fractional portions may compose the diet or only whole portions must be used",
        'Food Cost Multiplier': "The factor used by the Update Food Cost action to change food cost"
        }
    }

app_config = {
    'input_tables_config': input_tables_config,
    'parameters_config': parameters_config,
    'output_tables_config': output_tables_config,
    'actions_config': actions_config
}
