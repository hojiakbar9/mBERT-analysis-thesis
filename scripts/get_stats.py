import pandas as pd
import argparse

def main(compilation_file, mapping_file, output_file):
    df_compilation = pd.read_csv(compilation_file)
    filtered_ids = df_compilation[df_compilation['compile'] == 1]['id']
    df_mapping = pd.read_csv(mapping_file)
    filtered_mapping = df_mapping[df_mapping['id'].isin(filtered_ids)]

    mut_operator_counts = filtered_mapping['mut_operator'].value_counts()

    table = mut_operator_counts.reset_index()
    table.columns = ['Operator', 'Count']

    print("Mutation Operator Table (with Counts):")
    print(table)

    table.to_csv(output_file, index=False)
    print(f"\nThe table has been saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count mutation operators based on compilation results")
    parser.add_argument("compilation_file", type=str, help="Path to the compilation CSV file")
    parser.add_argument("mapping_file", type=str, help="Path to the mapping CSV file")
    parser.add_argument("output_file", type=str, help="Path to save the output CSV file")

    args = parser.parse_args()

    main(args.compilation_file, args.mapping_file, args.output_file)
