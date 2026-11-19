#coding=utf-8


if __package__:
    from . import file_paths as paths
else:
    import file_paths as paths


import pandas as pd


#Last search
Last_fn=paths.PREVIOUS_RESULTS
last_df = pd.read_excel(Last_fn)


#New search
New_fn =paths.CURRENT_RESULTS
new_df = pd.read_excel(New_fn)


print(f"\nPrevious file row count: {len(last_df)}")
print(f"Current file row count: {len(new_df)}")

if 'url' in last_df.columns and 'url' in new_df.columns:
    print("\nRemoving previously seen URLs...")
    # Collect all URLs from the previous file.
    old_urls = set(last_df['url'].dropna().astype(str))

    # Select rows whose URLs do not appear in the previous file.
    new_data = new_df[~new_df['url'].astype(str).isin(old_urls)].copy()

    # Continue existing paper numbers, or treat an unnumbered baseline as 1..N.
    if 'index' in last_df.columns and not last_df.empty:
        previous_indices = pd.to_numeric(last_df['index'], errors='raise')
        if previous_indices.isna().any() or (previous_indices % 1 != 0).any():
            raise ValueError("The previous index column must contain whole numbers.")
        next_index = int(previous_indices.max()) + 1
    else:
        next_index = len(last_df) + 1

    # Replace any current-search index with the continuing paper numbers.
    if 'index' in new_data.columns:
        new_data = new_data.drop(columns=['index'])
    new_data.insert(0, 'index', range(next_index, next_index + len(new_data)))

    print(f"Added row count: {len(new_data)}")

    # Save the added rows.
    output_file = paths.UPDATED_ONLY_RESULTS
    new_data.to_excel(output_file, index=False)
    print(f"\nAdded rows saved to: {output_file}")

    # Display the first few added rows.
    print("\nPreview of added rows:")
    print(new_data.head(10))



# Summary statistics
print("\n" + "="*50)
print(f"Summary:")
print(f"  Previous data: {len(last_df)} rows")
print(f"  Current data: {len(new_df)} rows")
print(f"  Added: {len(new_data)} rows")
print(f"  Previously seen: {len(new_df) - len(new_data)} rows (filtered out)")
print("="*50)
