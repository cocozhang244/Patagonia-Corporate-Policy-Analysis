#!/usr/bin/env python3
"""
Patagonia ESG Analysis - Master Execution Script
Author: Analysis Team
Date: November 13, 2025
Purpose: Run complete end-to-end analysis pipeline
"""

import os
import sys
import subprocess
from datetime import datetime
import time


def print_header(text):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")


def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print_header(f"STEP: {description}")
    print(f"Executing: {script_name}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            text=True,
            check=True
        )

        elapsed = time.time() - start_time
        print(f"\n✓ {script_name} completed successfully in {elapsed:.2f} seconds")
        return True

    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start_time
        print(f"\n❌ ERROR in {script_name} after {elapsed:.2f} seconds")
        print(f"Error: {e}")
        return False
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ UNEXPECTED ERROR in {script_name} after {elapsed:.2f} seconds")
        print(f"Error: {e}")
        return False


def check_prerequisites():
    """Check that all required files exist"""
    print_header("CHECKING PREREQUISITES")

    required_scripts = [
        'extract_text_with_pages.py',
        'analyze_esg_content.py',
        'visualize_findings.py'
    ]

    all_present = True
    for script in required_scripts:
        if os.path.exists(script):
            print(f"  ✓ Found: {script}")
        else:
            print(f"  ❌ Missing: {script}")
            all_present = False

    if not all_present:
        print("\n❌ Some required scripts are missing!")
        return False

    print("\n✓ All required scripts found")
    return True


def main():
    """Execute full analysis pipeline"""

    print("="*80)
    print(" "*20 + "PATAGONIA ESG ANALYSIS")
    print(" "*15 + "Complete Analysis Pipeline")
    print("="*80)
    print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    overall_start = time.time()

    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)

    # Pipeline steps
    steps = [
        ('extract_text_with_pages.py', 'Text Extraction with Page Tracking'),
        ('analyze_esg_content.py', 'ESG Content Analysis & Data Extraction'),
        ('visualize_findings.py', 'Visualization Generation')
    ]

    results = {}

    # Execute each step
    for script, description in steps:
        success = run_script(script, description)
        results[script] = success

        if not success:
            print_header("PIPELINE FAILED")
            print(f"Failed at step: {description}")
            print(f"Script: {script}")
            print("\nPlease review the error messages above and fix any issues.")
            sys.exit(1)

        # Brief pause between steps
        time.sleep(1)

    # All steps completed successfully
    overall_elapsed = time.time() - overall_start

    print_header("ANALYSIS PIPELINE COMPLETE")
    print("✓ All steps executed successfully!\n")

    print("Execution Summary:")
    for script, success in results.items():
        status = "✓ SUCCESS" if success else "❌ FAILED"
        print(f"  {status}: {script}")

    print(f"\nTotal execution time: {overall_elapsed:.2f} seconds ({overall_elapsed/60:.2f} minutes)")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n" + "="*80)
    print("OUTPUT DIRECTORIES")
    print("="*80)
    print("\n1. extracted_data/")
    print("   - Individual JSON files for each document")
    print("   - Individual TXT files for each document")
    print("   - MASTER_PAGE_INDEX.csv and .xlsx")
    print("   - extraction_log.json")

    print("\n2. analysis_output/")
    print("   - targets_goals_extracted.csv")
    print("   - language_tone_analysis.csv")
    print("   - initiatives_extracted.csv")
    print("   - geographic_references.csv")
    print("   - impact_areas_extracted.csv")
    print("   - MASTER_FINDINGS_SUMMARY.json")

    print("\n3. visualizations/")
    print("   - language_tone_analysis.png")
    print("   - targets_goals_analysis.png")
    print("   - geographic_distribution.png")
    print("   - impact_areas_analysis.png")
    print("   - initiatives_analysis.png")
    print("   - EXECUTIVE_DASHBOARD.png")

    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("\n1. Review extracted data in extracted_data/ directory")
    print("2. Examine analysis results in analysis_output/ directory")
    print("3. View visualizations in visualizations/ directory")
    print("4. Cross-reference page numbers for quality checks")
    print("5. Perform manual validation of key findings")
    print("6. Review ANALYTICAL_FRAMEWORK.md for interpretation guidance")

    print("\n" + "="*80)


if __name__ == "__main__":
    main()
