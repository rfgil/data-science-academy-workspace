# Data Dictionary 

| Variable     | Description | |
|--------------|-----------| |
| **admission_id** | Unique identifier of an encounter | |
| **patient_id** | Unique identifier of a patient | |
| **race** | Patient race | |
| **gender** | Patient gender | |
| **age** | Patient age grouped in 10-year intervals | |
| **weight** | Patient weight (lb) | |
| **admission_type_code** | Admission type identifier | 1: Emergency<br>2: Urgent<br>3: Elective<br>4: Newborn<br>5: Not Available<br>6: NULL<br>7: Trauma Center<br>8: Not Mapped |
| **discharge_disposition_code** | discharge_disposition_code | 1: Discharged to home<br>2: Discharged/transferred to another short term hospital<br>3: Discharged/transferred to SNF<br>4: Discharged/transferred to ICF<br>5: Discharged/transferred to another type of inpatient care institution<br>6: Discharged/transferred to home with home health service<br>7: Left AMA<br>8: Discharged/transferred to home under care of Home IV provider<br>9: Admitted as an inpatient to this hospital<br>10: Neonate discharged to another hospital for neonatal aftercare<br>11: Expired<br>12: Still patient or expected to return for outpatient services<br>13: Hospice / home<br>14: Hospice / medical facility<br>15: Discharged/transferred within this institution to Medicare approved swing bed<br>16: Discharged/transferred/referred another institution for outpatient services<br>17: Discharged/transferred/referred to this institution for outpatient services<br>18: NULL<br>19: ""Expired at home. Medicaid only:  hospice.""<br>20: ""Expired in a medical facility. Medicaid only:  hospice.""<br>21: ""Expired:  place unknown. Medicaid only:  hospice.""<br>22: Discharged/transferred to another rehab fac including rehab units of a hospital .<br>23: Discharged/transferred to a long term care hospital.<br>24: Discharged/transferred to a nursing facility certified under Medicaid but not certified under Medicare.<br>25: Not Mapped<br>26: Unknown/Invalid<br>30: Discharged/transferred to another Type of Health Care Institution not Defined Elsewhere<br>27: Discharged/transferred to a federal health care facility.<br>28: Discharged/transferred/referred to a psychiatric hospital of psychiatric distinct part unit of a hospital<br>29: Discharged/transferred to a Critical Access Hospital (CAH).<br> |
| **admission_source_code** | Admission source identifier | 1: Physician Referral<br>2: Clinic Referral<br>3: HMO Referral<br>4: Transfer from a hospital<br>5: Transfer from a Skilled Nursing Facility (SNF)<br>6: Transfer from another health care facility<br>7: Emergency Room<br>8: Court/Law Enforcement<br>9: Not Available<br>10: Transfer from critial access hospital<br>11: Normal Delivery<br>12: Premature Delivery<br>13: Sick Baby<br>14: Extramural Birth<br>15: Not Available<br>17: NULL<br>18: Transfer From Another Home Health Agency<br>19: Readmission to Same Home Health Agency<br>20: Not Mapped<br>21: Unknown/Invalid<br>22: Transfer from hospital inpt/same fac reslt in a sep claim<br>23: Born inside this hospital<br>24: Born outside this hospital<br>25: Transfer from Ambulatory Surgery Center<br>26: Transfer from Hospice |
| **time_in_hospital** | Number of days between admission and discharge | |
| **payer_code** | Payer identifier | |
| **medical_specialty** | Physician speciality | |
| **has_prosthesis** | Indicates if patient has any prothesis. | |
| **complete_vaccination_status** | The patient vaccination status. | |
| **num_lab_procedures** | Number of lab tests performed during the encounter | |
| **num_procedures** | Number of procedures (other than lab tests) performed during the encounter | |
| **num_medications** | Number of distinct generic names administered during the encounter | |
| **number_outpatient** | Number of outpatient visits of the patient in the year preceding the encounter | |
| **number_emergency** | Number of emergency visits of the patient in the year preceding the encounter | |
| **number_inpatient** | Number of inpatient visits of the patient in the year preceding the encounter | |
| **diag_1** | The primary diagnosis (coded as first three digits of ICD9) | |
| **diag_2** | Secondary diagnosis (coded as first three digits of ICD9) | |
| **diag_3** | Additional secondary diagnosis (coded as first three digits of ICD9) | |
| **number_diagnoses** | Number of diagnoses entered to the system | |
| **blood_type** | Patient blood type | |
| **hemoglobin_level** | Encounter initial patient hemoglobin level (g/dl) | |
| **blood_transfusion** | Indicates if pacient required blood transfusion during encounter | Yes: blood transfusion was performed during the encounter<br>No: no blood transfusion was performed during the encounter |
| **max_glu_serum** | Indicates the range of the glucose serum result or if the test was not taken. | >200: result greater than 200 but less than 300<br>>300: result greater than 300<br>norm: normal level<br>none: test was not performed |
| **A1Cresult** | Indicates the range of the A1c test result or if the test was not taken. | >8: the result was greater than 8%<br>>7: the result was greater than 7% but less than 8%<br>norm: the result was less than 7%<br>none: test was not performed |
| **diuretics** | Indicate whether diuretics were prescribed. | Yes: a diuretic was prescribed during the encounter<br>No: no diuretic was prescribed during the encounter |
| **insulin** | Indicate whether insulin was prescribed. | Yes: insulin was prescribed during the encounter<br>No: insulin was not prescribed during the encounter |
| **change** | Indicates if there was a change in diabetic medications (either dosage or generic name). | Ch: there was a change in diabetic medication<br>No: there was no change in diabetic medication |
| **diabetesMed** | Indicates if there was any diabetic medication prescribed. | Yes: diabetic medication was prescribed during the encounter<br>No: no diabetic medication was not prescribed during the encounter |
| **readmitted** | Patient readmitted within 30 days of discharge. | Yes: if the patient was readmitted<br>No: no record of readmission. |


