import pandas as pd
import os

# List all CSV files in the data folder
data_folder = 'data/'
csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

# Process each file
processed_dfs = []

for csv_file in csv_files:
    print(f"Processing {csv_file}...")
    
    # Load the CSV
    df = pd.read_csv(os.path.join(data_folder, csv_file))
    
    # Filter for pink morsel only (case-insensitive)
    df = df[df['product'].str.lower() == 'pink morsel']
    
    # Convert price from string (e.g., "$3.00") to float
    df['price'] = df['price'].str.replace('$', '').astype(float)
    
    # Create sales column (quantity * price)
    df['sales'] = df['quantity'] * df['price']
    
    # Keep only the required columns
    df = df[['sales', 'date', 'region']]
    
    processed_dfs.append(df)

# Combine all dataframes into one
final_df = pd.concat(processed_dfs, ignore_index=True)

# Save to output file
final_df.to_csv('output.csv', index=False)

print("✓ Data processing complete!")
print(f"Total rows processed: {len(final_df)}")
print("\nFirst few rows of output:")
print(final_df.head())