# Report 1

| Section  | Subsection  | Reader  | Description | Expected # of pages (approx) |
| ---  | ---  | ---  | --- | --- |
| 1. Client requirements | 1.1 Summary  | Business | Summarize all client requirements in a business context, both about the API and the analysis. Do not assume the reader has prior context. | 0.5 |
|  | 1.2 Requirements clarifications  | Business + Technical | Consider that this is what you send the client ahead of time to close ambiguities from the business requirements. It should turn ambiguous business requirements into hard technical metrics. You should also explain which requirements are possible to achieve and which are not. | 0.5 |
| 2. Dataset analysis | 2.1 General analysis  | Business | Provide a concise description and analysis of the dataset. Assume that the reader is not the person who sent you the requirements, and does not know the dataset. Use visualizations when possible to synthesize information, rather than raw numbers. You should keep your business questions in mind here, but the goal is to have an overview picture of the dataset. Any in-depth discussion about business questions should be in section 2.2. | 2 |
|  | 2.2 Business questions analysis  | Business | Answer the business questions, non-API related, that were posed directly to you, keeping in mind that the audience here is the client. Base your answers to the business questions in your analysis of the data. Refer to the annexes whenever you need to support a claim. Stick to the hard facts that you can support with data. | 1 |
|  | 2.3 Conclusions and Recommendations  | Business  | In this section you should give your professional opinion about more subjective topics, such as what specialities may merit further investigation, or interpretations of your findings.  Any recommendation to your client is expected to be done here. | 0.5 |
| 3. Modelling  | 3.1 Model expected outcomes overview  | Business | This is the section your client is most likely to read (delegating the rest to their IT department). Based on your prototype and preliminary results, describe here what outcomes you expect from the production run and set justified expectations on model performance (and other topics you consider relevant), making clear what is realistic. Also, explain if you make any decision regarding tradeoffs, e.g. between model performance and bias. | 0.5 |
|  | 3.2 Model specifications | Technical | This is the section the IT department will read to understand your proposed model implementation and know how to replicate it. Describe your proposal and briefly justify it, with the expectation that your reader is someone who knows data science, but not necessarily Python. Since they might want to redo your setup in another language, aim for a more generic and explicit description of your setup and avoid sticking too much to Python specifics (without having to worry about the natural slight differences in implementation between the various languages). Discussion about treatments to address biases (if there’s any) in your data should be mentioned here. | 1 |
|  | 3.3 Analysis of expected outcomes based on training set | Technical | What outcomes do you expect, based on the results you obtained with the training set? Make use of some quantitative and visual analysis to justify the claims you made in section 3.1. Consider all the client requirements at this point and mention some of the critical thinking that lead to your implementation choice. Discussion about model choices or tradeoffs should be mentioned here. | 0.5 |
|  | 3.4 Alternatives considered | Technical | What alternatives did you consider prior to deciding on a model? Why were those alternatives discarded? | 0.5 |
|  | 3.5 Known issues and risks | Technical  | What do you foresee is likely to go wrong with the current approach? Be critical about your model and the expectations that you set. Be mindful that a “no risk model” does not exist.  | 0.5 |
| 4. Model Deployment  | 4.1 Deployment specifications  | Technical  | Explain to a technical audience how to replicate the model deployment. Specifications on your application structure, what the structure of the data it receives, should be clarified here. | 1 |
|  | 4.2 Known issues and risks | Technical  | Regarding your application, explain what issues and risks you expect from your model deployment. What would potentially break your application? | 0.5 |
| 5. Annexes | 5.1 Dataset technical analysis | Technical  | Technical summary of the dataset. Feel free to write a small script that outputs this.  | 3 |
|  | 5.2 Business questions technical support  | Technical  | In-depth support for your answers.  | 1 |
|  | 5.3 Model technical analysis  | Technical  | In depth analysis for your non-business answers.  | 2 |
|  |
|  |  |  |  | 15 |

# Report 2

| Section  | Subsection  | Reader  | Description | Expected # of pages (approx) |
| ---  | ---  | ---  | --- | --- |
| 1. Business Conclusions | 1.1 Summary  | Business + Technical | How well were you able to meet the performance and all requirements that you outlined in report 1 | 1 |
| 2. Results Analysis | 2.1 Model Performance | Technical  | Based upon the performance that you expected and reported in report #1, how did you do on the observations for which you know the outcome. | 2 |
|  | 2.2 Success on requirements  | Technical  | Based upon the requirements that you identified in report 1, how did the new population and your model behave compared to what you reported and expected. | 2 |
|  | 2.3 Population Analysis | Technical  | Did the population change much from what you saw when you trained the model and did report 1 on. | 2 |
| 3. Next Steps | 3.1 Next Steps | Business + Technical | Talk about known things that you could implement to clearly make improvements as well as more exploratory tasks about how to move forward or even reframe the problem in a way that is best for the client. | 1 |
| 4. Deployment Issues | 4.1 Re-deployment | Technical  | Did you voluntarily re-deploy for any reason at all? Explain and justify. | 0-1 |
|  | 4.2 Unexpected problems | Technical  | Unexpected problems encountered during deployment. Did it crash? Did you get unexpected data? Were there things about the production environment that was suprising? This and more. | 1 |
|  | 4.3 What would you do differently next time | Technical  | Explain the learnings and what should be improved  | 0.5 |