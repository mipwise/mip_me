__version__ = "0.2.3"
from mip_me.schemas import input_schema, output_schema
from mip_me.action_update_food_cost import update_food_cost_solve
from mip_me.main import solve
from mip_me.action_report_builder import report_builder_solve

actions_config = {
    'Update Food Cost': {
        'schema': 'input',
        'engine': update_food_cost_solve,
        'tooltip': "Update the food cost by the factor entered in the 'Food Cost Multiplier' parameter"},
    'Report Builder': {
        'schema': 'output',
        'engine': report_builder_solve,
        'tooltip': "Reads the output from the main engine and populate the report tables"}
    }

input_tables_config = {
    'hidden_tables': ['parameters'],
    'categories': {
        'Master Tables': ['foods', 'nutrients'],
        'Composition Data': ['foods_nutrients']},
    'order': list(),
    'tables_display_names': {
        'foods_nutrients': 'Foods Composition'},
    'columns_display_names': {
        'foods': {'Per Unit Cost': 'Cost ($/unit)'},
        'nutrients': {'Min Intake': 'Minimum Intake',
                      'Max Intake': 'Maximum Intake'}},
    'hidden_columns': {
        'foods': ['Food ID'],
        'nutrients': ['Nutrient ID'],
        'foods_nutrients': ['Food ID', 'Nutrient ID']}
    }

output_tables_config = {
    'hidden_tables': list(),
    'categories': dict(),
    'order': ['buy', 'nutrition'],
    'tables_display_names': dict(),
    'columns_display_names': dict(),
    'hidden_columns': dict()
    }

parameters_config = {
    'hidden': list(),
    'categories': dict(),
    'order': ['Food Cost', 'Food Portions'],
    'tooltips': {
        'Food Portions': "Whether fractional portions may compose the diet or only whole portions must be used",
        'Food Cost Multiplier': "The factor used by the Update Food Cost action to change food cost"
        }
    }
