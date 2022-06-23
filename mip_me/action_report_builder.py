
def report_builder_solve(dat, sln):
    """Sample output action that populates the nutrition table (which could have been populated in the main solve)."""
    buy_df = sln.buy[['Food ID', 'Quantity']]
    nutrients_df = dat.nutrients[['Nutrient ID', 'Nutrient Name']]
    foods_nutrients_df = dat.foods_nutrients[['Food ID', 'Nutrient ID', 'Quantity']]
    foods_nutrients_df = foods_nutrients_df.rename(columns={'Quantity': 'Quantity per Food'})
    # merge buy and foods nutrients to get total nutrients of the diet
    nutrition_df = buy_df.merge(foods_nutrients_df, on='Food ID', how='left')
    nutrition_df['Quantity'] = nutrition_df['Quantity'] * nutrition_df['Quantity per Food']
    nutrition_df = nutrition_df[['Nutrient ID', 'Quantity']].groupby('Nutrient ID').agg('sum').reset_index()
    # merge nutrition with nutrients to get nutrient's names
    nutrition_df = nutrition_df.merge(nutrients_df, on='Nutrient ID', how='left')
    nutrition_df = nutrition_df.round({'Quantity': 2})
    nutrition_df = nutrition_df.astype({'Nutrient ID': str, 'Nutrient Name': str, 'Quantity': 'Float64'})
    sln.nutrition = nutrition_df[['Nutrient ID', 'Nutrient Name', 'Quantity']]
    return sln
