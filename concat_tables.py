import pandas as pd
import os
from datetime import datetime

def merge_on_ranid_tracking(
    results_folder="results",
    ground_truth_file=os.path.join("datasets", 'Sample with available VCDR.xlsx')
):
    """
    Merges all results_*.xlsx/.csv files with the ground truth,
    matching only on ran_id and tracking (not eye).
    Drops ground truth rows with no matching prediction.
    """
    # Step 1: Find all results_*.xlsx/.csv files
    result_files = sorted([
        os.path.join(results_folder, f)
        for f in os.listdir(results_folder)
        if f.startswith("results_") and (f.endswith(".xlsx") or f.endswith(".csv"))
    ])

    if not result_files:
        print("No results_*.xlsx or .csv files found.")
        return

    # Step 2: Read ground truth
    if ground_truth_file.endswith('.xlsx'):
        ground_truth_df = pd.read_excel(ground_truth_file)
    else:
        ground_truth_df = pd.read_csv(ground_truth_file)

    # Step 3: Combine all prediction results
    combined_results = pd.DataFrame()
    for file in result_files:
        if file.endswith('.xlsx'):
            df = pd.read_excel(file)
        elif file.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            continue

        # Extract ran_id and tracking from image_name (e.g. 123-xyz-left.jpg)
        parts = df['image_name'].str.replace('.jpg', '', regex=False).str.split('-', expand=True)
        df[['ran_id', 'tracking']] = parts[[0, 1]]
        df['ran_id'] = df['ran_id'].astype(int)
        combined_results = pd.concat([combined_results, df], ignore_index=True)

    # Step 4: Remove duplicates (keep the latest one for each ran_id+tracking)
    combined_results.drop_duplicates(subset=['ran_id', 'tracking'], keep='last', inplace=True)

    # Step 5: Merge with ground truth on ran_id and tracking only (inner join)
    merged_df = pd.merge(
        ground_truth_df,
        combined_results,
        how='inner',  # Only keep rows present in both
        on=['ran_id', 'tracking'],
        suffixes=('_truth', '_pred')
    )

    # Step 6: Sort and save
    merged_df = merged_df.sort_values(by=['ran_id', 'tracking']).reset_index(drop=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = os.path.join(results_folder, f"merged_on_ranid_tracking_{timestamp}.xlsx")
    merged_df.to_excel(output_filename, index=False)
    print(f"Merged file saved: {output_filename}")

if __name__ == "__main__":
    merge_on_ranid_tracking()