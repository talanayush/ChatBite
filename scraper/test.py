import pandas as pd
import glob
import os

def combine_csv_files(folder_path=".", output_file="Nugget_final_dataset.csv"):
    # Get all CSV files in the current folder
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

    combined_df = pd.DataFrame()

    for file in csv_files:
        # Exclude the output file if it already exists to avoid re-reading it
        if os.path.basename(file) == output_file:
            continue
        try:
            df = pd.read_csv(file)
            df["source_file"] = os.path.basename(file)  # optional
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    # Save inside the current folder
    output_path = os.path.join(folder_path, output_file)
    combined_df.to_csv(output_path, index=False)
    print(f"✅ Combined {len(csv_files)} files into {output_path}")

if __name__ == "__main__":
    combine_csv_files()
