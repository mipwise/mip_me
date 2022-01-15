"""
This module is dedicated to the app configuration.
Things such as display names (for tables and its columns), table categories and sorting, parameters categories
and sorting, and actions, are all defined in this script.
"""

from mip_me import update_food_cost_solve
from mip_me import report_builder_solve

input_tables_config = {
    'hidden': [],
    'categories': {},
    'order': [],
    'tables_display_names': {},
    'columns_display_names': {}
    }

parameters_config = {
    'hidden': [],
    'categories': {},
    'order': [],
    'tool_tips': {}
    }

output_tables_config = {
    'hidden': [],
    'categories': {},
    'order': [],
    'tables_display_names': {},
    'columns_display_names': {}
    }

# input_tables_config = {
#     'hidden': ['parameters'],
#     'categories': {
#         'Master Tables': ['foods', 'nutrients'],
#         'Composition Data': ['foods_nutrients']},
#     'order': [],  # already specified in the categories
#     'tables_display_names': {
#         'foods_nutrients': 'Foods Composition'},
#     'columns_display_names': {
#         'foods': {'Per Unit Cost': 'Cost ($/unit)',
#                   'Fixed Cost': 'Fixed Cost ($)'},
#         'nutrients': {'Min Intake': 'Minimum Intake',
#                       'Max Intake': 'Maximum Intake'}}
#     }
#
# parameters_config = {
#     'hidden': [],
#     'categories': {},
#     'order': ['Food Cost', 'Food Portions'],  # other already specified in the'How do You Like Your Boss categorie
#     'tool_tips': {
#         'Food Cost': "Whether the total cost of the diet should include delivery cost or only per unit cost",
#         'Food Portions': "Whether fractional portions may compose the diet or only whole portions must be used"
#         }
#     }
#
# output_tables_config = {
#     'hidden': [],
#     'categories': {},
#     'order': ['nutrition', 'buy'],
#     'tables_display_names': {},
#     'columns_display_names': {}
#     }
#
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

app_config = {
    'input_tables_config': input_tables_config,
    'parameters_config': parameters_config,
    'output_tables_config': output_tables_config,
    'actions_config': actions_config
}
