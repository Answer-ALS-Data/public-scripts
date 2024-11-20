# clinical_data_curation.py

import os
import pandas as pd
import numpy as np

def get_filepaths():
    """Prompt user for the clinical data folder path and return it with a trailing backslash."""
    filepath = input(
        "Please put all of the Clinical Data files provided by NeuroBANK into one shared folder, "
        "and then provide the filepath to said folder:\n"
    ).strip()
    if not filepath.endswith("\\"):
        filepath += "\\"
    return filepath

def define_filenames():
    """Define initial and curated filenames."""
    initial_filenames = [
        'v_NB_IATI_AALSDXFX.csv', 'v_NB_IATI_AALSHXFX.csv', 'v_NB_IATI_ALS_CBS.csv',
        'v_NB_IATI_ALS_Gene_Mutations.csv', 'v_NB_IATI_ALSFRS_R.csv', 'v_NB_IATI_ANSASFD.csv',
        'v_NB_IATI_ANSWER_ALS_Medications_Log.csv', 'v_NB_IATI_ANSWER_ALS_MobileApp.csv',
        'v_NB_IATI_Ashworth_Spasticity_Scale.csv', 'v_NB_IATI_Auxiliary_Chemistry.csv',
        'v_NB_IATI_Auxiliary_Chemistry_Labs.csv', 'v_NB_IATI_Cerebrospinal_Fluid.csv',
        'v_NB_IATI_CNS_Lability_Scale.csv', 'v_NB_IATI_Demographics.csv',
        'v_NB_IATI_Diaphragm_Pacing_System_Device.csv', 'v_NB_IATI_DNA_Sample_Collection.csv',
        'v_NB_IATI_Environmental_Questionnaire.csv', 'v_NB_IATI_Family_History_Log.csv',
        'v_NB_IATI_Feeding_Tube_Placement.csv', 'v_NB_IATI_Grip_Strength_Testing.csv',
        'v_NB_IATI_Hand_Held_Dynamometry.csv', 'v_NB_IATI_Medical_History.csv',
        'v_NB_IATI_Mortality.csv', 'v_NB_IATI_NEUROLOG.csv', 'v_NB_IATI_NIV_Log.csv',
        'v_NB_IATI_PBMC_Sample_Collection.csv', 'v_NB_IATI_Permanent_Assisted_Ventilation.csv',
        'v_NB_IATI_Plasma_Sample.csv', 'v_NB_IATI_Reflexes.csv', 'v_NB_IATI_Serum_Sample.csv',
        'v_NB_IATI_subjects.csv', 'v_NB_IATI_Tracheostomy.csv', 'v_NB_IATI_Vital_Capacity.csv',
        'v_NB_IATI_Vital_Signs.csv'
    ]

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

    # Ensure that the number of initial and curated filenames match
    assert len(initial_filenames) == len(curated_filenames), "Filename lists must be of the same length."

    return initial_filenames, curated_filenames

def define_headers():
    """Define the headers for each curated file."""
    headers = [
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'alsdx1', 'alsdx2', 'alsdx3', 'alsdxdt', 'blbclmn', 'blbcumn', 'blbelmn', 'elescrlr', 'lleclmn', 'llecumn', 'lleelmn', 'lueclmn', 'luecumn', 'lueelmn', 'rleclmn', 'rlecumn', 'rleelmn', 'rueclmn', 'ruecumn', 'rueelmn', 'trnkclmn', 'trnkcumn', 'trnkelmn'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'alsdxloc', 'diagdt', 'hxax', 'hxaxnk', 'hxaxtr', 'hxaxtrrp', 'hxblb', 'hxblbsch', 'hxblbsw', 'hxgen', 'hxli', 'hxlil', 'hxlilft', 'hxlill', 'hxlilleg', 'hxlilr', 'hxliu', 'hxliuarm', 'hxliuhnd', 'hxliul', 'hxliur', 'hxot', 'hxotsp', 'onsetdt'],
        ['Participant_ID', 'SubjectUID', 'Child_Name', 'Visit_Name', 'Visit_Date', 'atta', 'attb1', 'attb1tim', 'attb2', 'attb2tim', 'attc1', 'attc2', 'attscr', 'carbeh', 'carbeh01', 'carbeh02', 'carbeh03', 'carbeh04', 'carbeh05', 'carbeh06', 'carbeh07', 'carbeh08', 'carbeh09', 'carbeh10', 'carbeh11', 'carbeh12', 'carbeh13', 'carbeh14', 'carbeh15', 'cbsdn', 'cbsdnsp', 'cbsdt', 'cbstot', 'cbswrite', 'cgcuranx', 'cgcurcry', 'cgcurdep', 'cgcurftg', 'cgqcnst', 'cgqdn', 'cgqdnsp', 'cgqdt', 'cgqrel', 'con1', 'con2', 'con3', 'con4', 'con5', 'con6', 'con7', 'con8', 'conscr', 'ini01', 'ini02', 'ini03', 'ini04', 'ini05', 'ini06', 'ini07', 'ini08', 'ini09', 'ini10', 'ini11', 'ini12', 'ini13', 'ini14', 'ini15', 'ini16', 'ini17', 'ini18', 'ini19', 'ini20', 'iniscr', 'source', 'sourcesp', 'trka', 'trkb', 'trkc', 'trkcor', 'trkerr', 'trkscr'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'ang', 'angnd', 'c9orf72', 'c9orfnd', 'fus', 'fusnd', 'mutot', 'mutotsp', 'prgrnnd', 'progran', 'setx', 'setxnd', 'sod1', 'sod1muta', 'sod1nd', 'tau', 'taund', 'tdp43', 'tdp43nd', 'vapb', 'vapbnd', 'vcp', 'vcpnd'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'alsfdn', 'alsfdnsp', 'alsfrs1', 'alsfrs2', 'alsfrs3', 'alsfrs4', 'alsfrs5', 'alsfrs5a', 'alsfrs5b', 'alsfrs6', 'alsfrs7', 'alsfrs8', 'alsfrs9', 'alsfrsdt', 'alsfrsmd', 'alsfrsr1', 'alsfrsr2', 'alsfrsr3', 'alsfrsrp', 'alsfrssp', 'alsfrst', 'source', 'sourcesp'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'lnadt', 'moptrb', 'otsp', 'sfdt', 'sfsp'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'invdrg', 'med', 'meddose', 'medenddt', 'medfreq', 'medfrqsp', 'medind', 'medrte', 'medrtesp', 'medstdt', 'medu', 'meduotsp'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'madate', 'mobileap'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'asharml', 'asharmr', 'ashdn', 'ashdnsp', 'ashdt', 'ashlegl', 'ashlegr', 'source', 'sourcesp'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'acckrslt', 'acckunit', 'accreuni', 'accrrslt', 'acphouni', 'acphrslt', 'acuarslt', 'acuaunit', 'cknorm', 'crenorm', 'labdn', 'labdt', 'ot1norm', 'ot2norm', 'ot3norm', 'phonorm', 'uanorm', 'uot1rslt', 'uot1test', 'uot1unit', 'uot2rslt', 'uot2test', 'uot2unit', 'uot3rslt', 'uot3test', 'uot3unit'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'acckrslt', 'acckunit', 'accreuni', 'accrrslt', 'acphouni', 'acphrslt', 'acuarslt', 'acuaunit', 'cknorm', 'crenorm', 'labdn', 'labdt', 'ot1norm', 'ot2norm', 'ot3norm', 'phonorm', 'uanorm', 'uot1rslt', 'uot1test', 'uot1unit', 'uot2rslt', 'uot2test', 'uot2unit', 'uot3rslt', 'uot3test', 'uot3unit'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'aliqcnt', 'aliqfzth', 'aliqfztm', 'aliqicth', 'aliqictm', 'aliqth', 'aliqtm', 'aliqvol', 'aliqvolu', 'alqicena', 'alqvolot', 'csfcntth', 'csfcnttm', 'csfcol', 'csfcolth', 'csfcoltm', 'csfdn', 'csfdnsp', 'csfdt', 'csfdur', 'csfspeed', 'possmp', 'possmpsp', 'presmp', 'presmpsp'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'cnslcb', 'cnsldn', 'cnsldnsp', 'cnsldt', 'cnslsq1', 'cnslsq2', 'cnslsq3', 'cnslsq4', 'cnslsq5', 'cnslsq6', 'cnslsq7', 'cnslstot', 'source', 'sourcesp'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'age', 'dob', 'ethnic', 'raceamin', 'raceasn', 'raceblk', 'racenh', 'racewt', 'sex'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'dpsadmin', 'dpsdate', 'dpsdsch', 'dpsrec'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'aliqcnt', 'aliqvol', 'aliqvolu', 'alqvolot', 'dnacnt', 'dnacol', 'dnadn', 'dnadnsp', 'dnadt', 'resource', 'smplnygc'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'adesmock', 'aeock', 'asmkerb', 'bfopo', 'bgclmock', 'ceock', 'city1', 'city2', 'cmock', 'concussrb', 'concusstb', 'cssock', 'driavgtb', 'drinktb', 'edrb', 'etlock', 'exerdd', 'fffock', 'fpsrock', 'headrb', 'hptock', 'hsock', 'imrock', 'leveldd', 'lock', 'lpssock', 'maratb', 'milirb', 'mock', 'msock', 'noytb', 'oasock', 'otsptb', 'ottbx1', 'ottbx2', 'outusrb', 'pcsock', 'pock', 'psock', 'smkavgtb', 'smokerb', 'sportdd', 'srock', 'state1', 'state2', 'teck1', 'teck2', 'teck3', 'tmmock', 'where', 'yrsout', 'yrssmktb', 'yrstb'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'famgen', 'famguid', 'famher', 'famhx1', 'famrel', 'famrelsp', 'fhals', 'fhalz', 'fharth', 'fhasth', 'fhcanc', 'fhcirc', 'fhdem', 'fhdiab', 'fhdown', 'fhftd', 'fhgen', 'fhgnang', 'fhgnc9', 'fhgnfus', 'fhgnot', 'fhgnotsp', 'fhgnprg', 'fhgnsetx', 'fhgnsod1', 'fhgntau', 'fhgntdp', 'fhgnvapb', 'fhgnvcp', 'fhhbp', 'fhhd', 'fhhrt', 'fhlung', 'fhot', 'fhotsp', 'fhpd', 'fhpsy', 'fhpsysp', 'fhstk'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'ftpaccdt', 'ftpadmdt', 'ftpdchdt', 'ftpelctv', 'ftpmeth', 'ftpmthsp', 'ftprecdt', 'ftptyp', 'morabort', 'morasp', 'mordth', 'morhem', 'morinf', 'mornaus', 'morot', 'morotsp', 'moroxygn', 'morpain', 'morper', 'source', 'sourcesp'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'grpdtper', 'grpstat', 'lgrpntck', 'lgrpset', 'lgrpsp', 'lgrpspo', 'lgrpt1', 'lgrpt2', 'rgrpntck', 'rgrpset', 'rgrpsp', 'rgrpspo', 'rgrpt1', 'rgrpt2'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'hhddn', 'hhddnsp', 'hhdldt', 'ladab', 'ladnt', 'ladntsp', 'ladspo', 'ladt1', 'ladt2', 'ladt3', 'leeab', 'leent', 'leentsp', 'leespo', 'leet1', 'leet2', 'leet3', 'lefab', 'lefnt', 'lefntsp', 'lefspo', 'left1', 'left2', 'left3', 'lfdicab', 'lfdicnt', 'lfdicnts', 'lfdicspo', 'lfdict1', 'lfdict2', 'lfdict3', 'lhfab', 'lhfnt', 'lhfntsp', 'lhfspo', 'lhft1', 'lhft2', 'lhft3', 'lkeab', 'lkent', 'lkentsp', 'lkespo', 'lket1', 'lket2', 'lket3', 'lkfab', 'lkfnt', 'lkfntsp', 'lkfspo', 'lkft1', 'lkft2', 'lkft3', 'lsfab', 'lsfnt', 'lsfntsp', 'lsfspo', 'lsft1', 'lsft2', 'lsft3', 'lweab', 'lwent', 'lwentsp', 'lwespo', 'lwet1', 'lwet2', 'lwet3', 'radab', 'radnt', 'radntsp', 'radspo', 'radt1', 'radt2', 'radt3', 'reeab', 'reent', 'reentsp', 'reespo', 'reet1', 'reet2', 'reet3', 'refab', 'refnt', 'refntsp', 'refspo', 'reft1', 'reft2', 'reft3', 'rfdicab', 'rfdicnt', 'rfdicnts', 'rfdicspo', 'rfdict1', 'rfdict2', 'rfdict3', 'rhfab', 'rhfnt', 'rhfntsp', 'rhfspo', 'rhft1', 'rhft2', 'rhft3', 'rkeab', 'rkent', 'rkentsp', 'rkespo', 'rket1', 'rket2', 'rket3', 'rkfab', 'rkfnt', 'rkfntsp', 'rkfspo', 'rkft1', 'rkft2', 'rkft3', 'rsfab', 'rsfnt', 'rsfntsp', 'rsfspo', 'rsft1', 'rsft2', 'rsft3', 'rweab', 'rwent', 'rwentsp', 'rwespo', 'rwet1', 'rwet2', 'rwet3'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'medhx1', 'medhxdsc', 'medhxprs', 'medhxyr'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'aut', 'autdt', 'autobt', 'autpmi', 'auttyp', 'diedcaus', 'dieddt', 'icd10cm', 'source', 'sourcesp'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'd1ag0', 'd1ag1', 'd1ag2', 'd1ag3', 'd1ag4', 'date1', 'diag1', 'diag2', 'diag3', 'diag4', 'diag5', 'diag6', 'diag7', 'diag8', 'diag9', 'hidden1', 'hidden2', 'neuro', 'other'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'nivcont', 'nivstpdt', 'nivstrdt', 'nivusdur', 'nivusg', 'nivusg1', 'nivusrg1', 'nivusrg2'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'smplcol', 'smpldn', 'smpldnsp', 'smpldt', 'tbscol', 'tubshdt'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'pavdt', 'pavyn'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'aliqcnt', 'aliqvol', 'aliqvolu', 'alqfrzna', 'alqfrzth', 'alqfrztm', 'alqiceth', 'alqicetm', 'alqth', 'alqtm', 'alqvolot', 'cntdur', 'plspnk', 'smplclth', 'smplcltm', 'smplctth', 'smplcttm', 'smplspd', 'srplcol', 'srpldn', 'srpldnsp', 'srpldt'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'cfrnd', 'cjjnd', 'cjjscr', 'cpsnd', 'cpsscr', 'crcfrscr', 'lanklnd', 'lanklscr', 'lanklwk', 'lbcpnd', 'lbcpscr', 'lbcpwk', 'lbrchnd', 'lbrchscr', 'lbrchwk', 'lbsnd', 'lbsscr', 'lcadnd', 'lcadscr', 'lcclnnd', 'lcclnscr', 'lffnd', 'lffscr', 'lhsnd', 'lhsscr', 'llclnnd', 'llclnscr', 'lptlrnd1', 'lptlrscr', 'lptlrwk', 'ltrcpnd', 'ltrcpscr', 'ltrcpwk', 'ranklnd', 'ranklscr', 'ranklwk', 'rbcpnd', 'rbcpscr', 'rbcpwk', 'rbrchnd', 'rbrchscr', 'rbrchwk', 'rbsnd', 'rbsscr', 'rcadnd', 'rcadscr', 'rcclnnd', 'rcclnscr', 'rffnd', 'rffscr', 'rflxdt', 'rflxst', 'rhsnd', 'rhsscr', 'rlclnnd', 'rlclnscr', 'rptlrnd', 'rptlrscr', 'rptlrwk', 'rtrcpnd', 'rtrcpscr', 'rtrcpwk'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'aliqcnt', 'aliqvol', 'aliqvolu', 'alqfrzna', 'alqfrzth', 'alqfrztm', 'alqiceth', 'alqicetm', 'alqth', 'alqtm', 'alqvolot', 'cntdur', 'serpnk', 'smplclth', 'smplcltm', 'smplctth', 'smplcttm', 'smplspd', 'srplcol', 'srpldn', 'srpldnsp', 'srpldt'],
        ['Participant_ID', 'SubjectUID', 'subject_group_id'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'admsndt', 'dschgdt', 'rsnothsp', 'trachrsn', 'trchdt', 'trchrcdt'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'fvcl1', 'fvcl2', 'fvcl3', 'fvcnd2', 'fvcnd3', 'fvcndrs2', 'fvcndrs3', 'fvcndsp2', 'fvcndsp3', 'fvcp1', 'fvcp2', 'fvcp3', 'fvcvar', 'source', 'sourcesp', 'svcdn', 'svcdnsp', 'svcdt', 
         'svcl1', 'svcl2', 'svcl3', 'svcnd2', 'svcnd3', 'svcndrs2', 'svcndrs3', 'svcndsp2', 'svcndsp3', 'svcp1', 'svcp2', 'svcp3', 'svcvar', 'vcpos', 'vctyp'],
        ['Participant_ID', 'SubjectUID', 'Form_Name', 'Visit_Name', 'Visit_Date', 'bmi', 'bparm', 'bpdias', 'bppos', 'bpsys', 'height', 'heightu', 'hr', 'rr', 'source', 'sourcesp', 'temp', 'temprt', 'temprtsp', 'tempu', 'vsdn', 'vsdnsp', 'vsdt', 'weight', 'weightu']
    ]
    return headers

def create_full_filepaths(filepath, initial_filenames):
    """Create full file paths for each initial file."""
    return [os.path.join(filepath, filename) for filename in initial_filenames]

def rename_and_move_files(filepath, initial_filenames, curated_filenames):
    """
    Create a 'Clinical' folder, rename files, and move them into the 'Clinical' folder.
    
    Returns the list of new curated file paths.
    """
    clinical_dir = os.path.join(filepath, "Clinical")
    os.makedirs(clinical_dir, exist_ok=True)

    initial_filepaths = create_full_filepaths(filepath, initial_filenames)
    curated_filepaths = [os.path.join(clinical_dir, new_name) for new_name in curated_filenames]

    for src, dest in zip(initial_filepaths, curated_filepaths):
        try:
            os.replace(src, dest)
            print(f"Moved and renamed: {src} -> {dest}")
        except FileNotFoundError:
            print(f"File not found: {src}. Skipping.")
        except Exception as e:
            print(f"Error moving {src} to {dest}: {e}")

    return curated_filepaths

def add_participant_id(curated_filepaths):
    """Add 'Participant_ID' column to each curated CSV file."""
    for file_path in curated_filepaths:
        try:
            df = pd.read_csv(file_path, encoding='unicode_escape')
            if 'Participant_ID' not in df.columns:
                df['Participant_ID'] = "CASE-" + df['SubjectUID'].astype(str)
                df.to_csv(file_path, index=False)
                print(f"Added 'Participant_ID' to {file_path}")
            else:
                print(f"'Participant_ID' already exists in {file_path}. Skipping.")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

def reorder_columns(curated_filepaths, headers):
    """Reorder columns in each CSV file based on the provided headers."""
    for file_path, desired_headers in zip(curated_filepaths, headers):
        try:
            df = pd.read_csv(file_path, encoding='unicode_escape')
            # Check if all desired headers are present in the DataFrame
            missing_columns = set(desired_headers) - set(df.columns)
            if missing_columns:
                print(f"Warning: Missing columns {missing_columns} in {file_path}. They will be filled with NaN.")
                for col in missing_columns:
                    df[col] = np.nan
            df_reordered = df[desired_headers]
            df_reordered.to_csv(file_path, index=False)
            print(f"Reordered columns in {file_path}")
        except Exception as e:
            print(f"Error reordering columns in {file_path}: {e}")

def clean_nan_values(curated_filepaths):
    """Replace '.' with empty strings in each CSV file."""
    for file_path in curated_filepaths:
        try:
            df = pd.read_csv(file_path, encoding='unicode_escape')
            df.replace(to_replace=".", value="", inplace=True)
            df.to_csv(file_path, index=False)
            print(f"Cleaned NaN values in {file_path}")
        except Exception as e:
            print(f"Error cleaning NaN values in {file_path}: {e}")

def update_participant_ids(curated_filepaths):
    """
    Update 'Participant_ID' for control participants.
    Controls are identified in 'subjects.csv' where 'subject_group_id' == 5.
    """
    subjects_file = curated_filepaths[30]  # Assuming 'subjects.csv' is at index 30
    try:
        subjects_df = pd.read_csv(subjects_file, encoding='unicode_escape')
        controls_df = subjects_df[subjects_df['subject_group_id'] == 5]
        ctrl_uid_list = controls_df['SubjectUID'].astype(str).tolist()
        print(f"Identified {len(ctrl_uid_list)} control participants.")

        # Create mapping dictionary: "CASE-uid" -> "CTRL-uid"
        replacement_dict = {f"CASE-{uid}": f"CTRL-{uid}" for uid in ctrl_uid_list}

        # Apply replacement across all files
        for file_path in curated_filepaths:
            try:
                df = pd.read_csv(file_path, encoding='unicode_escape')
                if 'Participant_ID' in df.columns:
                    df['Participant_ID'] = df['Participant_ID'].replace(replacement_dict)
                    df.to_csv(file_path, index=False)
                    print(f"Updated 'Participant_ID' in {file_path}")
            except Exception as e:
                print(f"Error updating 'Participant_ID' in {file_path}: {e}")

    except FileNotFoundError:
        print(f"'subjects.csv' not found at {subjects_file}. Cannot update 'Participant_ID' for controls.")
    except Exception as e:
        print(f"Error processing 'subjects.csv': {e}")

def main():
    """Main function to orchestrate the data curation process."""
    print("Starting Clinical Data Curation Script...")
    
    # Step 1: Get file paths
    filepath = get_filepaths()
    
    # Step 2: Define filenames
    initial_filenames, curated_filenames = define_filenames()
    
    # Step 3: Define headers
    headers = define_headers()
    
    # Step 4: Rename and move files
    curated_filepaths = rename_and_move_files(filepath, initial_filenames, curated_filenames)
    
    # Step 5: Add 'Participant_ID' column
    add_participant_id(curated_filepaths)
    
    # Step 6: Reorder columns
    reorder_columns(curated_filepaths, headers)
    
    # Step 7: Clean NaN values
    clean_nan_values(curated_filepaths)
    
    # Step 8: Update 'Participant_ID' for controls
    update_participant_ids(curated_filepaths)
    
    print("Clinical Data Curation Completed Successfully.")

if __name__ == "__main__":
    main()