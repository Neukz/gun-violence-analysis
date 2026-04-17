import pandas as pd

def get_state_populations_2015():
    print("Fetching 2015 census data...")
    # Official US Census dataset for 2010-2019 population estimates
    url = "https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/national/totals/nst-est2019-alldata.csv"
    
    # Read the data using pandas
    df = pd.read_csv(url)
    
    # SUMLEV 40 filters the data to include ONLY the 50 states and D.C./Puerto Rico
    states_df = df[df['SUMLEV'] == 40].copy()
    
    # Select the state name and ONLY the target year 2015
    columns_to_keep = [
        'NAME', 
        'POPESTIMATE2015'
    ]
    states_df = states_df[columns_to_keep]
    
    # Rename columns for a cleaner dataframe
    states_df.rename(columns={
        'NAME': 'state',
        'POPESTIMATE2015': 'population'
    }, inplace=True)
    
    # Sort alphabetically by state and reset the index
    states_df.sort_values(by='state', inplace=True)
    states_df.reset_index(drop=True, inplace=True)
    
    return states_df

if __name__ == "__main__":
    # Fetch the dataframe
    df = get_state_populations_2015()
    
    # Print the first few rows to the console
    print("\nFirst 5 states:\n", df.head())
    
    # Save the dataframe locally as a CSV file
    output_filename = "US_State_Populations_2015.csv"
    df.to_csv(output_filename, index=False)
    print(f"\nData successfully saved to {output_filename}")