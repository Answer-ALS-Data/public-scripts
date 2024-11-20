# clinical_package_validation.py

import os
import pandas as pd

def get_clinical_folder():
    """Prompt user for the Clinical folder path and return it."""
    folder_path = input(
        "Please provide the filepath to the 'Clinical' folder containing the curated CSV files:\n"
    ).strip()
    return folder_path

def define_curated_filenames():
    """Define curated filenames."""
    curated_filenames = [
        'AALSDXFX.csv', 'AALSHXFX.csv', 'ALS_CBS.csv', 'ALS_Gene_Mutations.csv',
        'ALSFRS_R.csv', 'ANSASFD.csv', 'ANSWER_ALS_Medications_Log.csv',
        'ANSWER_ALS_MobileApp.csv', 'Ashworth_Spasticity_Scale.csv',
        'Auxiliary_Chemistry.csv', 'Auxiliary_Chemistry_Labs.csv',
        'Cerebrospinal_Fluid.csv', 'CNS_Lability_Scale.csv', 'Demographics.csv',
        'Diaphragm_Pacing_System_Device.csv', 'DNA_Sample_Collection.csv',
        'Environmental_Questionnaire.csv', 'Family_History_Log.csv',
        'Feeding_Tube_Placement.csv', 'Grip_Strength_Testing.csv',
        'Hand_Held_Dynamometry.csv', 'Medical_History.csv', 'Mortality.csv',
        'NEUROLOG.csv', 'NIV_Log.csv', 'PBMC_Sample_Collection.csv',
        'Permanent_Assisted_Ventilation.csv', 'Plasma_Sample.csv', 'Reflexes.csv',
        'Serum_Sample.csv', 'subjects.csv', 'Tracheostomy.csv',
        'Vital_Capacity.csv', 'Vital_Signs.csv'
    ]
    return curated_filenames

def create_full_filepaths(clinical_folder, curated_filenames):
    """Create full file paths for each curated file."""
    return [os.path.join(clinical_folder, filename) for filename in curated_filenames]

def load_subjects(subjects_filepath):
    """Load subjects.csv and return a mapping of SubjectUID to group ('CASE' or 'CTRL')."""
    try:
        subjects_df = pd.read_csv(subjects_filepath, encoding='unicode_escape')
        # Assuming 'subject_group_id' == 5 indicates control
        subjects_df['Group'] = subjects_df['subject_group_id'].apply(lambda x: 'CTRL' if x == 5 else 'CASE')
        uid_to_group = subjects_df.set_index('SubjectUID')['Group'].to_dict()
        print(f"Loaded subjects.csv with {len(uid_to_group)} participants.")
        return uid_to_group
    except FileNotFoundError:
        print(f"Error: 'subjects.csv' not found at {subjects_filepath}.")
        return {}
    except Exception as e:
        print(f"Error loading 'subjects.csv': {e}")
        return {}

def validate_participant_ids(file_path, uid_to_group):
    """Validate Participant_ID prefixes based on SubjectUID."""
    try:
        df = pd.read_csv(file_path, encoding='unicode_escape', dtype=str)
        if 'Participant_ID' not in df.columns or 'SubjectUID' not in df.columns:
            print(f"[WARNING] 'Participant_ID' or 'SubjectUID' column missing in {os.path.basename(file_path)}. Skipping Participant_ID validation.")
            return True
        
        # Drop rows where SubjectUID is NaN
        df = df.dropna(subset=['SubjectUID'])
        
        # Initialize lists to collect mismatches
        mismatches = []
        
        for idx, row in df.iterrows():
            subject_uid = row['SubjectUID']
            participant_id = row['Participant_ID']
            expected_group = uid_to_group.get(subject_uid, None)
            
            if expected_group is None:
                mismatches.append((subject_uid, participant_id, "Unknown SubjectUID"))
                continue
            
            expected_prefix = f"{expected_group}-"
            if not participant_id.startswith(expected_prefix):
                mismatches.append((subject_uid, participant_id, f"Expected prefix '{expected_prefix}'"))
        
        if not mismatches:
            print(f"[PASS] All Participant_ID prefixes are correct in {os.path.basename(file_path)}.")
            return True
        else:
            print(f"[FAIL] Participant_ID prefix mismatches found in {os.path.basename(file_path)}:")
            for uid, pid, issue in mismatches:
                print(f"  SubjectUID: {uid}, Participant_ID: {pid} - {issue}")
            return False
    except Exception as e:
        print(f"[ERROR] Failed to validate Participant_ID in {os.path.basename(file_path)}: {e}")
        return False

def main():
    """Main function to validate Participant_ID prefixes in clinical data."""
    print("Starting Clinical Data Validation Script...\n")
    
    # Step 1: Get Clinical folder path
    clinical_folder = get_clinical_folder()
    if not os.path.isdir(clinical_folder):
        print(f"Error: The folder '{clinical_folder}' does not exist.")
        return
    
    # Step 2: Define curated filenames
    curated_filenames = define_curated_filenames()
    
    # Step 3: Create full file paths
    curated_filepaths = create_full_filepaths(clinical_folder, curated_filenames)
    
    # Step 4: Load subjects.csv to get SubjectUID to Group mapping
    subjects_filepath = os.path.join(clinical_folder, 'subjects.csv')
    uid_to_group = load_subjects(subjects_filepath)
    if not uid_to_group:
        print("Error: Unable to proceed without SubjectUID to Group mapping.")
        return
    
    # Initialize counters
    total_files = len(curated_filepaths)
    participant_id_pass = 0
    participant_id_fail = 0
    
    # Step 5: Validate each curated file
    for file_path in curated_filepaths:
        filename = os.path.basename(file_path)
        print(f"\nValidating file: {filename}")
        
        # Skip subjects.csv itself
        if filename.lower() == 'subjects.csv':
            print("Skipping validation for 'subjects.csv'.")
            continue
        
        pid_valid = validate_participant_ids(file_path, uid_to_group)
        if pid_valid:
            participant_id_pass += 1
        else:
            participant_id_fail += 1
    
    # Step 6: Summarize results
    print("\n=== Validation Summary ===")
    print(f"Total Files Validated: {total_files - 1}")  # Excluding subjects.csv
    print(f"Participant_ID Validation Passed: {participant_id_pass}")
    print(f"Participant_ID Validation Failed: {participant_id_fail}")
    print("==========================\n")
    
    if participant_id_fail == 0:
        print("All Participant_ID prefixes are correct!")
    else:
        print("Some Participant_ID prefixes are incorrect. Please review the issues above.")

if __name__ == "__main__":
    main()
