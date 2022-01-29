# Email from your head of engineering

Dear new employee 

Welcome to the team, and congratulations on passing the gruelling interview process! We’re glad to have you as the newest member of our team here at Lisbon Data Science’s Awkward Problem Solutions™. As I’m sure you know from the interview process, we are a consultancy that tackles the hard data science problems no one else will touch. 

We have been tasked to deal with a sensitive and important issue, whose ramifications might have severe consequences. The Hazel and Bazel Hospital, in Los Angeles, California, has contacted us regarding **suspicion of malpractice** and is currently under investigation by the Fair Medical Practices Bureau. Situations have come to light where **patients have been wrongfully medically discharged**, resulting in severe health consequences for the patient. **Our main objective is to identify patients who are likely to return to the hospital in less than 30 days**, for which the hospital might be liable for wrongful discharge before due time. 

The reasons for this are still unknown, and investigation into this matter is required. It is **unknown if this is a demographic-specific issue or specific to any of the medical specialities/services**. Additionally, they want us to create and deploy a REST API endpoint for patient discharge verification. This will be integrated directly into the hospital’s system to be triggered every time the medical dismissal information for a patient is filled in in their system. You will be responsible for setting this system up and running it for a year. 
 
Due to the sensitivity of this issue, you’ll be working directly with Dr Agnes Crumplebottom, the Hazel and Bazel Hospital medical director. Dr Crumplebottom will be your only point of contact during this project. Due to the sensitive nature of the project, information might be limited. 

As you may imagine, this project is a huge deal for our consultancy, we’re counting on you to deliver on this one. Naturally, if you have any questions you can ask me, but I’m counting on you to lead and execute from start to finish. You can find Dr Crumplebottom email attached below. 

Yours, 
Aveline
VP of Data Science 
Awkward Problem Solutions™.


# Email from Dr Agnes Crumplebottom

Aveline 

I can’t stress enough how important the matter we have at hand is. I’m under enormous pressure from the board to initiate a thorough investigation, and some funders are threatening to withdraw funding which is vital for the renovation of my office. You have guaranteed the confidentiality of our communications so I’ll speak frankly to you. If the money we are spending with your firm is an indication of your secrecy, this might be better than confessing to the Pope.

I’ll cut to the chase and talk frankly to you. The situation appears to be dire. We’ve received private, but trustworthy, information that the Fair Medical Practices Bureau is currently investigating our hospital and that a class-action lawsuit is currently in the works. Apparently, according to these “officers”, we’ve been providing subpar treatment to our patients. As you know, **our Hospital focuses on diabetes**, a pervasive and lucrative epidemic. Funny that when confined, **people still tend to overeat**. But I digress. We offer premium quality services, tailored to diabetic patients so that they receive the best care for their unique condition. Of course, we don’t promise a cure, as that would be counter-intuitive for our interests, but our care practices are both extensive and in-depth, insurance allowing.

The main suspicion is our number of returning patients after a very short time after discharge. To me, this is a sign that we provide such good care that they just want more. But some hold other opinions. The board has forced me to procure an external party to investigate and present an objective report. I am trusting you, and your firm, with this task. You promised me the best of your people, and I’m counting on it. 

I have discussed this matter extensively with our head of IT, which will be expecting a service to be integrated into our own internal system for medical discharge approval, so all we need is a REST API that our own code can call. We won’t be sending you any requests from recent events, as naturally, we wouldn’t know the outcome. 

Regarding data, we are providing you with our patient information since 2012. The head of IT has provided you with a field description in [this link](data_dictionary.md). The [training dataset](../data/train_data.csv) has approximately 81,411 observations, I expect this should be enough.

Regarding the analysis, **we want you to search for evidence that any of our services may be discriminating on gender, ethnicity or age regarding who they chose to dismiss from our care**. We are particularly interested in knowing **if any of our specialities or admission sources are responsible for the unexpected patient discharge rate**. Additionally, some questions regarding our **care for uninsured patients** have been brought up. I denied these offensive insinuations but the board is of the unanimous opinion that this is a matter to be considered. 

As you may imagine these are sensitive topics, with many jobs, one of them my own, on the line. We, therefore, need you to propose what metrics would suggest that anything unacceptable is being observed. **Some training and changes of staff and/or policy may impact the data over time**.

The report will be read both by me and by the members of our board. I expect this report to be well straight-forward and structured. I’m paying you enough for it. After the analysis is completed and your report has been understood, we will run a proof of concept with your company for the use of your API in integration with our hospital patient record management system. It is imperative that we succeed in ending these insinuations that we do not provide the necessary medical care to as many patients as possible. If during the investigation it is observed that we are failing to provide care to a patient that needs it, the consequences for us and for your company will be dire. **Nevertheless, we don't have the monetary, personal and infrastructural resources to retain all patients indefinitely**. We expect that your API should be able to signal potential wrongful discharges with all of these requirements. 

From your last email, I understand you’ve hired a specialist to deal with this project. I’m very much looking forward to working with them, and am of course available to answer their questions as they occur. But please be mindful that my time is limited. And more important than yours. 

Best regards 
Agnes Crumplebottom, MD PhD 
Medical director
Hazel and Bazel Hospital 


### Email from Dr Agnes Crumplebottom (Jan 25th)

Greetings,

It’s good to know who will be handling this mess. Your email was very thorough, if not extensive. At least you seem to have a solid understanding of our data and challenges. I’ve attempted to answer the main questions. Please find my answers below.

> Given the data at hand, what output/label do you expect? Do you want the verification model to state whether a patient should be discharged? Or do you want the model to classify the patient as a possible wrong discharge?

As I’ve stated in my previous mail and in the data dictionary, **the goal is to predict if a person is likely to be readmitted within 30 days**. For the patients that would be readmitted in 30 days, we would like to identify them and keep them in our facilities further. This means that patients classified as readmitted = “Yes” should stay longer and patients classified as readmitted = “No” show no indication that they require further assistance and can be safely discharged.

> How should we assess model performance? Which minimum values should be considered for the patient readmission classification and for the bias between specialties?

This is a very technical question and, as the expert, it should be up to you to make the ultimate decision based on our business requirements: we cannot fail to provide care to a patient that needs it. This means we would like to minimize the number of wrong discharges that would lead patients to return in less than 30 days.

But we are not made of money so this should not be the only criteria. **As a rule of thumb, consider that at least 50% of the patients identified for readmission should actually be sick**.

**The wrongful discharge rate, or readmission rate, should not vary more than 10 percentage points between sub-groups, and less than 5 percentage points between medical specialties.**

> Information on **patient insurance** status is unclear. Could you provide more information on this?

The record of a **patient's insurance status should be able to be inferred from their Payer identifier information**. With the SP (self-pay) code you will be able to identify the uninsured patients, with the remaining codes referring to different insurance providers.

> I understand you are concerned about imbalances regarding medical specialties. However, by looking at the data we find 71 specialties, many of which have a very low amount of data points. 

I trust your expertise to deal with this imbalance in the way you see fit, **including defining a minimum number of observations, and justify it in your report.**  

> Regarding the dataset, I would like to clarify a few issues:
> -  do the null values in the num_medications and num_lab_procedures variables indicate a zero/lack of medications/lab procedures or a real absence of data?
> - do the "None" values in the complete_vaccination_status variable indicate a lack of information or lack of vaccines?
> - finally, we have a lot of value equal to "?". Should these be considered as missing values? 

When no medication is provided to the patient, the value of num_medications is zero (0). The same applies for num_lab_procedures. 

Values such as “None”, “?” and similar in all non-numeric columns refer to information that was not possible to collect.

> Could you be more precise on what is a “service” exactly, as it does not appear explicitly in the data set. 

Consider as a service any of our medical specialties. 

> For the race attribute, it looks like there are different descriptions for the same race groups. How should we consider these categories?

We trust your analysis of the records. Being you the expert, we leave to you how to handle these seemingly similar descriptions. Please refer to this situation and explain the strategy you choose in your report.

> You mention how some things impact data over-time. Is it possible to add dates to the data to ensure we are allowing for this?

Unfortunately, my team tells me that some incompetent IT guy lost the time stamp information for the data that you were given. **Please see your report as an opportunity to highlight their wrongdoing**.


> With the goal to evaluate the impact of staff in this situation is it possible to have at least a code that identifies the doctor responsible for the discharge or the doctor/team that was responsible to treat the patient?

You can assume that **“Physician specialty” represents the specialty (or department) responsible for discharging a patient** and that this level of detail is sufficient for the task.


> Were there any changes in the hospital board, or some cuts in budget during the period of the observations you sent?

The old goons from the board have been here since the time TVs were black and white. And even though they keep refusing additional funding for my much needed office renovation, there is no way I would let them cut down my budget.

> What are you expecting from the API response only a true or false answer? Can you please provide us with a few samples of the POST requests which will be made?

Very good question! I will be asking the Technical team and we will get something together and share with you within a few days.

> There seems to be some data inconsistencies, particularly regarding the diagnosis codes.

Consider this as data imputation errors. With you being the expert, I expect a justification on how you decide to handle these cases. 

> Can you please provide us with a reference with a correspondence between the first 3 digits of ICD9 codes and the respective disease?

According to one of our staff, who I like to call “annoying wikipedia”, the International Classification of Diseases, Ninth Revision, Clinical Modification (ICD-9-CM) is based on the World Health Organization’s Ninth Revision, International Classification of Diseases (ICD-9) and is available from Center for Disease Control through their FTP service. **The wikipedia page might also be of use**.

> Why are more diagnoses associated with some patients (as per the number_diagnoses column) than diag_X (diag_1, diag_2 and diag_3) columns? What are the other diagnoses?

The diag_1/2/3 variables correspond to primary, secondary and additional secondary diagnosis, respectively. These aim to identify the primary cause for hospitalization, so there might be other other diagnoses the doctor might find in the patient but we only record the three most important ones.

> Almost 96% of its values are missing for the weight feature, so it can’t be used to do a predictive model.

This is a shame, and I expect to see this covered in your report.

> What medications are included in the DiabetesMed feature? Does this feature exclude insulin?

The DiabetesMed refers to any diabetes medication, such as insulin, insulin stimulants, diuretics, and glucose uptake inhibitors.

> The patient_id column is said to be unique per patient. However, I found out that some patients have multiple blood types. I am guessing that either patient_id or blood_type (or possibly other attributes) of these records have been wrongly entered or corrupted.

**This is a relevant question**. The patient_id is indeed unique for each user. So it seems you might have identified an issue with our data gathering methodology. I would suggest your IT department look into this issue. Again, as the expert, we leave it to you on how to handle this.

> Since data contains multiple patient visits for the same patients, may we consider only the first encounter for each patient to know whether or not they were readmitted in less than 30 days in order to prevent the bias of our model?

As mentioned earlier, our data doesn’t have any time-related features. So I’d avoid making any assumptions that the visit outcomes from the same patient are correlated. Also, the model should be general enough such as it can make predictions on unseen patients.

> To improve record keeping, do you want our new system to restrict options to only those already in use for fields such as race, age, gender etc,? Are there any additional categories which are not in the database but are available options and can they please be added to the field descriptions?

The world is a never-ending changing thing, so new categories may show up. We expect your solution to be flexible enough so that it does not crash when that happens.

> There are several codes in the Discharge_disposition_code that I don’t understand. Can you please provide an explanation for them? 

I should also understand these codes but I don’t. I consulted my Chief Physician Dr. Susan Google, and she told me that these are standardized codes to identify the status of the patient at the end of their admission period in a health care facility.
