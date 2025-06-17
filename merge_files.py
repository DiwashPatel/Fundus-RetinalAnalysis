def merge_two_files(results_file, ground_truth_file = "last_visit_with_img_exist_subcol_v2.csv"):
    """
    Merges the Results file with Ground truth file. 
    Just pass the name of the results_file. 
    For eg:
    results.xlsx
    """

    import pandas as pd
    from datetime import datetime
    import os


    # Load files
    ground_truth_df = pd.read_csv(ground_truth_file)     # First table (CSV)
    results_df = pd.read_excel(results_file)            # ChatGPT results with image_name

    # Extract ran_id, tracking, eye from image_name
    results_df[['ran_id', 'tracking', 'eye']] = results_df['image_name'].str.replace('.jpg', '').str.split('-', expand=True)

    # Convert ran_id to integer to match ground truth
    results_df['ran_id'] = results_df['ran_id'].astype(int)

    # Merge both files on ran_id, tracking, eye
    merged_df = pd.merge(
    ground_truth_df,
    results_df,
    how='left',
    on=['ran_id', 'tracking', 'eye']
    )

    # Optional: Sort to keep left/right eye order consistent
    merged_df = merged_df.sort_values(by=['ran_id', 'eye_no']).reset_index(drop=True)

    # Create timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Save merged result with timestamp in filename
    output_filename = f'merged_output_{timestamp}.xlsx'
    merged_df.to_excel(output_filename, index=False)

    print(f"Merged file saved as: {output_filename}")

if __name__ == "__main__":
    merge_two_files("results_1.xlsx")