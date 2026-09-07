#!/usr/bin/env python3
"""
generate_failsafe.py - Build offline alert dataset from ALeRCE
If live API fails, creates synthetic data so the workshop still works.
"""

import pandas as pd
import numpy as np
from alerce.core import Alerce
import os
import sys
import time

def fetch_objects(alerce, class_name, prob_min, max_items=5):
    """Fetch objects of a given class with probability above prob_min."""
    try:
        result = alerce.query_objects(
            classifier='lc_classifier',
            class_name=class_name,
            prob=prob_min,
            page_size=max_items,
            order_by='firstmjd',
            order_mode='DESC'
        )
        items = result.get('items', [])
        if items:
            return pd.DataFrame(items)
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"  [ERROR] query failed: {e}")
        return pd.DataFrame()

def build_synthetic_fallback():
    """Generate a small synthetic dataset if real API fails."""
    print("[WARN] Using synthetic dataset (no internet / API down)")
    np.random.seed(42)
    oids = ['ZTF_sn_001', 'ZTF_sn_002', 'ZTF_agn_003', 'ZTF_agn_004', 'ZTF_cv_005']
    types = ['SNe Ia', 'SNe Ia', 'AGN', 'AGN', 'CV']
    rows = []
    for oid, typ in zip(oids, types):
        # Simulate light curve points
        n_points = 20
        mjd_base = 60000 + np.random.randint(0, 50)
        for i in range(n_points):
            mjd = mjd_base + i * 0.5 + np.random.randn() * 0.05
            mag = 18 + np.random.randn() * 0.5
            if typ == 'AGN':
                mag += np.sin(i/3) * 0.3  # stochastic
            filt = 'g' if i % 2 == 0 else 'r'
            rows.append({
                'oid': oid,
                'meanra': 150 + np.random.rand() * 10,
                'meandec': 30 + np.random.rand() * 10,
                'firstmjd': mjd_base,
                'lastmjd': mjd_base + n_points * 0.5,
                'class_name': typ,
                'probability': 0.8 if typ == 'SNe Ia' else 0.2,
                'mjd': mjd,
                'mag': mag,
                'mag_err': 0.05,
                'filter': filt,
                'object_type': typ,
            })
    df = pd.DataFrame(rows)
    # Keep only required columns for the notebook
    keep_cols = ['oid', 'meanra', 'meandec', 'firstmjd', 'lastmjd', 'class_name', 'probability', 'mjd', 'mag', 'mag_err', 'filter', 'object_type']
    return df[keep_cols]

def main():
    print("="*60)
    print("TDMMA Workshop - Failsafe Data Generator")
    print("="*60)
    
    # Initialize ALeRCE client
    alerce = Alerce()
    
    # Fetch SNe Ia (genuine, short baseline)
    print("\n[1] Fetching SNe Ia (prob ≥ 0.75)...")
    df_sn = fetch_objects(alerce, 'SNIa', 0.75, max_items=3)
    if not df_sn.empty:
        df_sn['object_type'] = 'SNe Ia'
        print(f"    → Found {len(df_sn)} SNe Ia")
    else:
        print("    → No SNe Ia fetched")
    
    # Fetch AGNs (impostors, long baseline)
    print("\n[2] Fetching AGNs (prob ≥ 0.85)...")
    df_agn = fetch_objects(alerce, 'AGN', 0.85, max_items=5)
    if not df_agn.empty:
        df_agn['object_type'] = 'AGN'
        print(f"    → Found {len(df_agn)} AGNs")
    else:
        print("    → No AGNs fetched")
    
    # Combine if we have real data
    if not df_sn.empty or not df_agn.empty:
        df_combined = pd.concat([df_sn, df_agn], ignore_index=True)
        # Ensure all needed columns exist (fill missing with defaults)
        for col in ['mjd', 'mag', 'mag_err', 'filter']:
            if col not in df_combined.columns:
                df_combined[col] = np.nan
        # Create a fake lightcurve for each object (just for demo)
        # We'll expand later in notebook, but for now keep the summary
        print(f"\n[3] Combining {len(df_combined)} objects...")
        # Save the summary table (will be used as the candidate list)
        output_path = 'data/reference_alerts.parquet'
        os.makedirs('data', exist_ok=True)
        df_combined.to_parquet(output_path, index=False)
        print(f"    ✓ Saved {len(df_combined)} records to {output_path}")
        print("\nObjects summary:")
        print(df_combined[['oid', 'class_name', 'object_type']].to_string(index=False))
    else:
        print("\n[!] No real data fetched. Using synthetic fallback.")
        df_synth = build_synthetic_fallback()
        output_path = 'data/reference_alerts.parquet'
        os.makedirs('data', exist_ok=True)
        df_synth.to_parquet(output_path, index=False)
        print(f"    ✓ Synthetic dataset saved ({len(df_synth)} records)")
        print("\nSynthetic objects:")
        print(df_synth[['oid', 'object_type']].drop_duplicates().to_string(index=False))
    
    print("\n" + "="*60)
    print("Done! Now set USE_LIVE_API = False in your notebook.")
    print("="*60)

if __name__ == "__main__":
    main()
