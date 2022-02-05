import os
import sys
import numpy as np
import pandas as pd

from sklearn.base import TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

#from .utils import variables_mapping

class PreProcessingTransformer(TransformerMixin):
    """
    Applies the preprocessing logic to all columns.
    Sets all variables' dtype and transform the raw input into valid categories.
    The unknown/unexpected values are converted into None
    """

    def __init__(self):
        self.known_categories = variables_mapping()
        self.known_categories.pop('readmitted', None) # Remove the readmitted key


    def transform(self, X, *_):
        X_clean = X.copy()
        X_clean = X_clean.replace({None: np.nan})
        for column in self.known_categories.keys():
            #type_ = 'object' if self.known_categories[column]['type'] == 'category' else self.known_categories[column]['type']
            X_clean[column] = (X[column]
                               .apply(lambda value: self.known_categories[column]['mapping'](value))
                               .astype(self.known_categories[column]['type'])
                              )

        return X_clean

    def fit(self, *_):
        return self


class DropColumnsTransformer(TransformerMixin):
    """
    Removes columns that won't be used by the predictive model
    """

    def transform(self, X, *_):
        X_ = X.copy()

        # Drop training rows that have a given 'discharge_disposition_code' ??

        return X_.drop([
            'admission_id',
            'patient_id',
            'weight',
            'max_glu_serum',
            'insulin' #change, diabetesMed
        ],
            axis = 1
        )

    def fit(self, *_):
        return self


class CustomImputer(TransformerMixin):

    def __init__(self):
        self.dict_ = {}

    def transform(self, X, *_):
        X_ = X.copy()
        for column in self.dict_.keys():
            X_[column] = self.dict_[column].transform(X[[column]])

        return X_


    def fit(self, X, *_):
        for numeric_column in X.select_dtypes(include=["Int64", "float64", "int64"]).columns:
            self.dict_[numeric_column] = SimpleImputer(strategy='mean')
            self.dict_[numeric_column].fit(X[[numeric_column]])


        return self
        #for category_column in X.select_dtypes(include=["object"]):
        #    self.dict_[category_column] = SimpleImputer(strategy='most_frequent')
        #    self.dict_[category_column].fit(X[[category_column]])


def get_mapping_or_nan(value, mapping):
    try:
        return mapping[value]
    except:
        if value != "nan": print('Unexpected value "' + str(value) + '"')
        return np.nan


def any_to_num(value):
    ''' Tries to converts the argument into into a float, if the conversion fails returns the argument itself
    '''
    try:
        return float(value)
    except:
        return value


def variables_mapping():
    d_ = {}

    # admission_id - nothing to do here

    # patient_id - nothing to do here


    # race
    d_['race'] = {}
    d_['race']['dict'] = {
        'caucasian': 'white',
        'euro': 'white',
        'black': 'black',
        'other': 'other',
        'white': 'white',
        'africanamerican': 'black',
        'afro american': 'black',
        'african american': 'black',
        'european': 'white',
        'asian': 'asian',
        'hispanic': 'hispanic',
        'latino': 'hispanic',
        '?': 'unknown',
    }
    d_['race']['type'] = pd.CategoricalDtype(set(d_['race']['dict'].values()))
    d_['race']['mapping'] = lambda value: d_['race']['dict'].get(str(value).lower(), 'unknown')


    # gender
    d_['gender'] = {}
    d_['gender']['dict'] = {
        'female': 'female',
        'male': 'male',
        'unknown/invalid': 'unknown'
    }
    d_['gender']['type'] = pd.CategoricalDtype(set(d_['gender']['dict'].values()))
    d_['gender']['mapping'] = lambda value: d_['gender']['dict'].get(str(value).lower(), 'unknown')


    # age
    d_['age'] = {}
    d_['age']['dict'] = {
        '[0-10)': 0,
        '[10-20)': 10,
        '[20-30)': 20,
        '[30-40)': 30,
        '[40-50)': 40,
        '[50-60)': 50,
        '[60-70)': 60,
        '[70-80)': 70,
        '[80-90)': 80,
        '[90-100)': 90
    }
    d_['age']['type'] = "Int64"
    d_['age']['mapping'] = lambda value: d_['age']['dict'].get(str(value).lower(), np.nan)


    # weight
    d_['weight'] = {}
    d_['weight']['dict'] = {
        '>200': 200,
        #'?': np.nan,
        '[0-25)': 0,
        '[100-125)': 100,
        '[125-150)': 125,
        '[150-175)': 150,
        '[175-200)': 175,
        '[25-50)': 25,
        '[50-75)': 50,
        '[75-100)': 75
    }
    d_['weight']['type'] = "Int64"
    d_['weight']['mapping'] = lambda value: d_['weight']['dict'].get(str(value).lower(), np.nan)


    # admission_type_code
    d_['admission_type_code'] = {}
    d_['admission_type_code']['dict'] = {
        1: 'Emergency', # Urgent
        2: 'Urgent', # Isn't urgent the same as emergency?? Assuming, urgent is the same as emergency
        3: 'Elective',
        4: 'Newborn',
        #5: 'unknown', # 'Not Available',
        #6: 'unknown', # 'NULL'
        7: 'Trauma Center',
        #8: 'unknown' # 'Not Mapped'
        '?': 'unknown'
    }
    d_['admission_type_code']['type'] = pd.CategoricalDtype(set(d_['admission_type_code']['dict'].values()))
    d_['admission_type_code']['mapping'] = lambda value: 'unknown' if np.nan_to_num(value) == 0 else d_['admission_type_code']['dict'].get(int(value), 'unknown')


    # discharge_disposition_code
    d_['discharge_disposition_code'] = {}
    d_['discharge_disposition_code']['dict'] = {
        1: 'Discharged to home',
        2: 'Discharged/transferred to another short term hospital',
        3: 'Discharged/transferred to SNF',
        4: 'Discharged/transferred to ICF',
        5: 'Discharged/transferred to another type of inpatient care institution',
        6: 'Discharged/transferred to home with home health service',
        7: 'Left AMA',
        8: 'Discharged/transferred to home under care of Home IV provider',
        9: 'Admitted as an inpatient to this hospital',
        10: 'Neonate discharged to another hospital for neonatal aftercare',
        11: 'Expired',
        12: 'Still patient or expected to return for outpatient services',
        13: 'Hospice / home',
        14: 'Hospice / medical facility',
        15: 'Discharged/transferred within this institution to Medicare approved swing bed',
        16: 'Discharged/transferred/referred another institution for outpatient services',
        17: 'Discharged/transferred/referred to this institution for outpatient services',
        #18: np.nan, #'NULL',
        19: 'Expired at home. Medicaid only: hospice',
        20: 'Expired in a medical facility. Medicaid only: hospice',
        21: 'Expired: place unknown. Medicaid only: hospice',
        22: 'Discharged/transferred to another rehab fac including rehab units of a hospital',
        23: 'Discharged/transferred to a long term care hospital',
        24: 'Discharged/transferred to a nursing facility certified under Medicaid but not certified under Medicare',
        #25: np.nan, #'Not Mapped',
        #26: np.nan, #'Unknown/Invalid',
        30: 'Discharged/transferred to another Type of Health Care Institution not Defined Elsewhere',
        27: 'Discharged/transferred to a federal health care facility',
        28: 'Discharged/transferred/referred to a psychiatric hospital of psychiatric distinct part unit of a hospital',
        29: 'Discharged/transferred to a Critical Access Hospital (CAH)',
        '?': 'unknown'
    }
    d_['discharge_disposition_code']['type'] = pd.CategoricalDtype(set(d_['discharge_disposition_code']['dict'].values()))
    d_['discharge_disposition_code']['mapping'] = lambda value: 'unknown' if np.nan_to_num(value) == 0 else d_['discharge_disposition_code']['dict'].get(int(value), 'unknown')


    # admission_source_code
    d_['admission_source_code'] = {}
    d_['admission_source_code']['dict'] = {
        1: 'Physician Referral',
        2: 'Clinic Referral',
        3: 'HMO Referral',
        4: 'Transfer from a hospital',
        5: 'Transfer from a Skilled Nursing Facility (SNF)',
        6: 'Transfer from another health care facility',
        7: 'Emergency Room',
        8: 'Court/Law Enforcement',
        #9: np.nan, #'Not Available',
        10: 'Transfer from critial access hospital',
        11: 'Normal Delivery',
        12: 'Premature Delivery',
        13: 'Sick Baby',
        14: 'Extramural Birth',
        #15: np.nan, # 'Not Available',
        #17: np.nan, # 'NULL',
        18: 'Transfer From Another Home Health Agency',
        19: 'Readmission to Same Home Health Agency',
        #20: np.nan, # 'Not Mapped',
        #21: np.nan, #'Unknown/Invalid',
        22: 'Transfer from hospital inpt/same fac reslt in a sep claim',
        23: 'Born inside this hospital',
        24: 'Born outside this hospital',
        25: 'Transfer from Ambulatory Surgery Center',
        26: 'Transfer from Hospice',
        '?': 'unknown'
    }
    d_['admission_source_code']['type'] = pd.CategoricalDtype(set(d_['admission_source_code']['dict'].values()))
    d_['admission_source_code']['mapping'] = lambda value: 'unknown' if np.nan_to_num(value) == 0 else d_['admission_source_code']['dict'].get(int(value), 'unknown')

    # time_in_hospital - nothing to do here


    # payer_code
    d_['payer_code'] = {}
    d_['payer_code']['dict'] = {
        #'?': np.nan,
        'bc': 'BC',
        'ch': 'CH',
        'cm': 'CM',
        'cp': 'CP',
        'dm': 'DM',
        'fr': 'FR',
        'hm': 'HM',
        'mc': 'MC',
        'md': 'MD',
        'mp': 'MP',
        'og': 'OG',
        'ot': 'OT',
        'po': 'PO',
        'si': 'SI',
        'sp': 'SP',
        'un': 'UN',
        'wc': 'WC',
        '?': 'unknown',
    }
    d_['payer_code']['type'] = pd.CategoricalDtype(set(d_['payer_code']['dict'].values()))
    d_['payer_code']['mapping'] = lambda value: d_['payer_code']['dict'].get(str(value).lower(), 'unknown')



    # medical_specialty
    d_['medical_specialty'] = {}
    d_['medical_specialty']['dict'] = {
        #'?': np.nan,

        # Anesthesiology
        'anesthesiology': 'Anesthesiology',
        'anesthesiology-pediatric': 'Anesthesiology',

        # Cardiology
        'cardiology': 'Cardiology',
        'cardiology-pediatric': 'Cardiology',

        # Endocrinology
        'endocrinology': 'Endocrinology',
        'endocrinology-metabolism': 'Endocrinology',

        # Hematology
        'hematology': 'Hematology',
        'hematology/oncology': 'Hematology',

        # Gynecology/Obstetrics
        'obstetrics': 'Gynecology/Obstetrics',
        'obsterics&gynecology-gynecologicOnco': 'Gynecology/Obstetrics',
        'obstetricsandgynecology': 'Gynecology/Obstetrics',
        'obsterics&gynecology-gynecologiconco': 'Gynecology/Obstetrics',
        'gynecology': 'Gynecology/Obstetrics',

        # Orthopedics
        'orthopedics': 'Orthopedics',
        'orthopedics-reconstructive': 'Orthopedics',

        # Pediatrics
        'pediatrics': 'Pediatrics',
        'pediatrics-criticalcare': 'Pediatrics',
        'pediatrics-hematology-oncology': 'Pediatrics',
        'pediatrics-pulmonology': 'Pediatrics',
        'pediatrics-endocrinology': 'Pediatrics',
        'pediatrics-emergencymedicine': 'Pediatrics',
        'pediatrics-neurology': 'Pediatrics',
        'pediatrics-allergyandimmunology': 'Pediatrics',

        # PhysicalMedicine
        'physicalmedicineandrehabilitation': 'PhysicalMedicine',
        'physiciannotfound': 'PhysicalMedicine',

        # Psychiatry
        'psychiatry': 'Psychiatry',
        'psychiatry-child/adolescent': 'Psychiatry',
        'psychology': 'Psychiatry',
        'psychiatry-addictive': 'Psychiatry',

        # Radiology
        'radiologist': 'Radiology',
        'radiology': 'Radiology',

        # Surgery
        'surgeon': 'Surgery',
        'surgery-cardiovascular': 'Surgery',
        'surgery-cardiovascular/thoracic': 'Surgery',
        'surgery-colon&rectal': 'Surgery',
        'surgery-general': 'Surgery',
        'surgery-maxillofacial': 'Surgery',
        'surgery-neuro': 'Surgery',
        'surgery-pediatric': 'Surgery',
        'surgery-plastic': 'Surgery',
        'surgery-thoracic': 'Surgery',
        'surgery-vascular': 'Surgery',
        'surgicalspecialty': 'Surgery',

        # Others
        'allergyandimmunology': 'Others', # 10 or less occurrences
        'dcpteam': 'Others',              # 10 or less occurrences - ??
        'dentistry': 'Others',            # 10 or less occurrences
        'dermatology': 'Others',          # 1 occurrence
        'neurophysiology': 'Others',      # 1 occurrence
        'outreachservices': 'Others',     # 10 or less occurrences - ??
        'perinatology': 'Others',         # 1 occurrence
        'proctology': 'Others',           # 1 occurrence
        'resident': 'Others',             # 1 occurrence - ??
        'speech': 'Others',               # 1 occurrence
        'sportsmedicine': 'Others',       # 1 occurrence
        'hospitalist': 'Others',          # 44 occurrences - ??
        'osteopath': 'Others',            # 29 occurrences
        'rheumatology': 'Others',         # 14 occurrences
        'otolaryngology': 'Others',       # 26 occurrences
        'pathology': 'Others',            # 16 occurrences

        # Ungrouped specialties
        'emergency/trauma': 'Emergency/Trauma',
        'family/generalpractice': 'Family/GeneralPractice',
        'gastroenterology': 'Gastroenterology',
        'infectiousdiseases': 'InfectiousDiseases',
        'internalmedicine': 'InternalMedicine',
        'nephrology': 'Nephrology',
        'neurology': 'Neurology',
        'oncology': 'Oncology',
        'ophthalmology': 'Ophthalmology',
        'podiatry': 'Podiatry',
        'pulmonology': 'Pulmonology',
        'urology': 'Urology'
    }
    d_['medical_specialty']['type'] = pd.CategoricalDtype(set(d_['medical_specialty']['dict'].values()))
    d_['medical_specialty']['mapping'] = lambda value: d_['medical_specialty']['dict'].get(str(value).lower(), 'Others')

    # has_prosthesis - nothing to do here


    # complete_vaccination_status
    d_['complete_vaccination_status'] = {}
    d_['complete_vaccination_status']['dict'] = {
        'none': 'none',
        'incomplete': 'incomplete',
        'complete': 'complete'
    }
    d_['complete_vaccination_status']['type'] = pd.CategoricalDtype(['none', 'incomplete', 'complete'], ordered=True)
    d_['complete_vaccination_status']['mapping'] = lambda value: d_['complete_vaccination_status']['dict'].get(str(value).lower(), 'complete') # Impute the complete status, since it is the most common


    # num_lab_procedures
    d_['num_lab_procedures'] = {}
    d_['num_lab_procedures']['type'] = "Int64"
    d_['num_lab_procedures']['mapping'] = lambda value: value

    # num_procedures - nothing to do here


    # num_medications
    d_['num_medications'] = {}
    d_['num_medications']['type'] = "Int64"
    d_['num_medications']['mapping'] = lambda value: value

    # number_outpatient - nothing to do here

    # number_emergency - nothing to do here

    # number_inpatient - nothing to do here


    # diag_1, diag_2, diag_3
    def icd9_group(icd9_code):
        ''' Converts a given ICD9 code into its group. Returns None if there is no match
        '''
        if icd9_code is None or icd9_code == '?': return 'unknown' # np.nan

        value_ = any_to_num(str(icd9_code).lower())
        if type(value_) is str:
            if value_.startswith('v') or value_.startswith('e'): return 'external causes of injury'
        else:
            code = np.nan_to_num(value_)
            if code == 0: return 'unknown' #np.nan
            if code >= 1 and code <= 139: return 'infectious and parasitic diseases'
            if code >= 140 and code <= 239: return 'neoplasms'
            if code >= 240 and code <= 279: return 'endocrine, nutritional and metabolic diseases, and immunity disorders'
            if code >= 280 and code <= 289: return 'diseases of the blood and blood-forming organs'
            if code >= 290 and code <= 319: return 'mental disorders'
            if code >= 320 and code <= 389: return 'diseases of the nervous system and sense organs'
            if code >= 390 and code <= 459: return 'diseases of the circulatory system'
            if code >= 460 and code <= 519: return 'diseases of the respiratory system'
            if code >= 520 and code <= 579: return 'diseases of the digestive system'
            if code >= 580 and code <= 629: return 'diseases of the genitourinary system'
            if code >= 630 and code <= 679: return 'complications of pregnancy, childbirth, and the puerperium'
            if code >= 680 and code <= 709: return 'diseases of the skin and subcutaneous tissue'
            if code >= 710 and code <= 739: return 'diseases of the musculoskeletal system and connective tissue'
            if code >= 740 and code <= 759: return 'congenital anomalies'
            if code >= 760 and code <= 779: return 'certain conditions originating in the perinatal period'
            if code >= 780 and code <= 799: return 'symptoms, signs, and ill-defined conditions'
            if code >= 800 and code <= 999: return 'injury and poisoning'

        print('Invalid ICD9 code ' + icd9_code)
        return 'unknown' #np.nan

    diag_type = pd.CategoricalDtype([
        'unknown',
        'external causes of injury',
        'infectious and parasitic diseases',
        'neoplasms',
        'endocrine, nutritional and metabolic diseases, and immunity disorders',
        'diseases of the blood and blood-forming organs',
        'mental disorders',
        'diseases of the nervous system and sense organs',
        'diseases of the circulatory system',
        'diseases of the respiratory system',
        'diseases of the digestive system',
        'diseases of the genitourinary system',
        'complications of pregnancy, childbirth, and the puerperium',
        'diseases of the skin and subcutaneous tissue',
        'diseases of the musculoskeletal system and connective tissue',
        'congenital anomalies',
        'certain conditions originating in the perinatal period',
        'symptoms, signs, and ill-defined conditions',
        'injury and poisoning'
    ])

    d_['diag_1'] = {}
    d_['diag_1']['type'] = diag_type
    d_['diag_1']['mapping'] = lambda value: icd9_group(value)

    d_['diag_2'] = {}
    d_['diag_2']['type'] = diag_type
    d_['diag_2']['mapping'] = lambda value: icd9_group(value)

    d_['diag_3'] = {}
    d_['diag_3']['type'] = diag_type
    d_['diag_3']['mapping'] = lambda value: icd9_group(value)


    # number_diagnoses - nothing to do here


    # blood_type
    d_['blood_type'] = {}
    d_['blood_type']['dict'] = {
        'a+': 'A+',
        'a-': 'A-',
        'ab+': 'AB+',
        'ab-': 'AB-',
        'b+': 'B+',
        'b-': 'B-',
        'o+': 'O+',
        'o-': 'O-',
    }
    d_['blood_type']['type'] = pd.CategoricalDtype(set(d_['blood_type']['dict'].values()))
    d_['blood_type']['mapping'] = lambda value: d_['blood_type']['dict'].get(str(value).lower(), 'O+') # Impute the 'O+' since it is the most common

    # hemoglobin_level - nothing to do here

    # blood_transfusion - nothing to do here


    # max_glu_serum
    d_['max_glu_serum'] = {}
    d_['max_glu_serum']['dict'] = {
        '>200': 200,
        '>300': 300,
        'norm': 85, # https://my.clevelandclinic.org/health/diagnostics/12363-blood-glucose-test
        'none': np.nan
    }
    d_['max_glu_serum']['type'] = "Int64" #"category"
    d_['max_glu_serum']['mapping'] = lambda value: d_['max_glu_serum']['dict'].get(str(value).lower(), np.nan)


    # A1Cresult
    d_['A1Cresult'] = {}
    d_['A1Cresult']['dict'] = {
        '>7': 7,
        '>8': 8,
        'norm': 5, # https://www.cdc.gov/diabetes/managing/managing-blood-sugar/a1c.html
        'none': np.nan
    }
    d_['A1Cresult']['type'] = "Int64"
    d_['A1Cresult']['mapping'] = lambda value: d_['A1Cresult']['dict'].get(str(value).lower(), np.nan)


    # diuretics
    d_['diuretics'] = {}
    d_['diuretics']['dict'] = {
        'yes': True,
        'no': False
    }
    d_['diuretics']['type'] = "bool"
    d_['diuretics']['mapping'] = lambda value: d_['diuretics']['dict'].get(str(value).lower(), False) # False is the most common, by far


    # insulin
    d_['insulin'] = {}
    d_['insulin']['dict'] = {
        'yes': True,
        'no': False
    }
    d_['insulin']['type'] = "bool"
    d_['insulin']['mapping'] = lambda value: d_['insulin']['dict'].get(str(value).lower(), True) # True is the most common occurrence


    # change
    d_['change'] = {}
    d_['change']['dict'] = {
        'ch': True,
        'no': False
    }
    d_['change']['type'] = "bool"
    d_['change']['mapping'] = lambda value: d_['change']['dict'].get(str(value).lower(), False) # False is the most common occurrence


    # diabetesMed
    d_['diabetesMed'] = {}
    d_['diabetesMed']['dict'] = {
        'yes': True,
        'no': False
    }
    d_['diabetesMed']['type'] = "bool"
    d_['diabetesMed']['mapping'] = lambda value: d_['diabetesMed']['dict'].get(str(value).lower(), True) # True is the most common occurrence


    # readmitted
    d_['readmitted'] = {}
    d_['readmitted']['dict'] = {
        'yes': True,
        'no': False
    }
    d_['readmitted']['type'] = "bool"
    d_['readmitted']['mapping'] = lambda value: d_['readmitted']['dict'].get(str(value).lower(), np.nan)

    return d_
