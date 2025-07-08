#!/usr/bin/env python3
"""
Plot accuracy by mutation depth across multiple repair_results SQLite databases.
"""

import argparse
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(
        description="Plot accuracy by mutation depth across models"
    )
    parser.add_argument(
        "--cases-db",
        required=True,
        help="SQLite DB with 'cases' table (columns 'id', 'mutation_depth')",
    )
    parser.add_argument(
        "--result-dbs",
        required=True,
        nargs='+',
        help="One or more repair_results SQLite DBs to analyze",
    )
    args = parser.parse_args()

    # Load and prepare cases data
    conn = sqlite3.connect(args.cases_db)
    df_cases = pd.read_sql("SELECT id, mutation_depth FROM cases", conn)
    conn.close()
    df_cases['mutation_depth'] = pd.to_numeric(
        df_cases['mutation_depth'], errors='coerce'
    )
    df_cases = df_cases.dropna(subset=['mutation_depth'])
    df_cases['mutation_depth'] = df_cases['mutation_depth'].astype(int)
    all_depths = sorted(df_cases['mutation_depth'].unique())

    # Collect fix counts by mutation depth
    records = []
    for db_path in args.result_dbs:
        model = os.path.basename(db_path)
        model = (
            model.removeprefix('repair_results_')
                 .removesuffix('_targets.db')
                 .split('_')[1]
        )
        conn = sqlite3.connect(db_path)
        df_res = pd.read_sql("SELECT case_id, fix FROM repair_results", conn)
        conn.close()

        df_ok = df_res[df_res['fix'] == 1].merge(
            df_cases[['id', 'mutation_depth']],
            left_on='case_id',
            right_on='id',
        )
        counts = df_ok['mutation_depth'].value_counts().to_dict()

        for depth in all_depths:
            records.append({
                'model': model,
                'mutation_depth': depth,
                'accuracy': counts.get(depth, 0),
            })

    df_md = pd.DataFrame(records)

    # Plotting
    plt.figure(figsize=(10, 6))
    for model in sorted(df_md['model'].unique()):
        df_m = df_md[df_md['model'] == model]
        plt.plot(
            df_m['mutation_depth'],
            df_m['accuracy'],
            marker='x',
            label=model,
        )

    plt.xlabel('Mutation Depth')
    plt.ylabel('Accuracy')
    plt.title('Accuracy by Mutation Depth Across Models')
    plt.legend(title='Model', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(all_depths, rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()