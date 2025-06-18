import pandas as pd
import os
from datetime import datetime

def merge_all_results(
    results_folder="results",
    ground_truth_file=os.path.join("datasets", "last_visit_with_img_exist_subcol_v2.csv")
):
    """
    Merges all results_*.xlsx files with the ground truth.
    Ground truth is in datasets/, output is saved in results/.
    """

    # Step 1: Find all results_*.xlsx files
    result_files = sorted([
        os.path.join(results_folder, f)
        for f in os.listdir(results_folder)
        if f.startswith("results_") and f.endswith(".xlsx")
    ])

    if not result_files:
        print("No results_*.xlsx files found.")
        return

    # Step 2: Read ground truth CSV
    ground_truth_df = pd.read_csv(ground_truth_file)

    # Step 3: Initialize empty DataFrame for all results
    combined_results = pd.DataFrame()

    # Step 4: Loop through each results_*.xlsx file
    for file in result_files:
        df = pd.read_excel(file)

        # Extract ran_id, tracking, eye from image_name (e.g. 123-xyz-left.jpg)
        parts = df['image_name'].str.replace('.jpg', '', regex=False).str.split('-', expand=True)
        df[['ran_id', 'tracking', 'eye']] = parts
        df['ran_id'] = df['ran_id'].astype(int)

        # Add to combined_results
        combined_results = pd.concat([combined_results, df], ignore_index=True)

    # Step 5: Remove duplicates (keep the latest one for each image)
    combined_results.drop_duplicates(subset=['ran_id', 'tracking', 'eye'], keep='last', inplace=True)

    # Step 6: Merge with ground truth
    merged_df = pd.merge(
        ground_truth_df,
        combined_results,
        how='left',
        on=['ran_id', 'tracking', 'eye']
    )

    # Step 7: Sort if eye_no is available
    if 'eye_no' in merged_df.columns:
        merged_df = merged_df.sort_values(by=['ran_id', 'eye_no'])
    else:
        merged_df = merged_df.sort_values(by=['ran_id'])

    merged_df.reset_index(drop=True, inplace=True)

    # Step 8: Save the merged output to results/ with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = os.path.join(results_folder, f"merged_output_{timestamp}.xlsx")
    merged_df.to_excel(output_filename, index=False)

    print(f"Merged file saved: {output_filename}")


if __name__ == "__main__":
    merge_all_results()
