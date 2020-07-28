# COVID-19 Israel critical case hospitalization model

Estimate total critical patients next week (+6 days from today)

Data required:
1. New daily critical patients, 50 days history from today
2. COVID-19 infection cases from 7 days ago, subgrouped to 3 age groups: [20-59], [60-74]. 75+
3. Total hospitalized critical patients today

The model returns the total estimated critical patients next week (+6 days from today)    

## To Run:
1. Load data

2. run the function (from critical_prediction_model.py):

```
predict_critical_cases(new_daily_critical_history,
                            cases_20_59_history, cases_60_74_history, cases_75_plus_history,
                            total_critical_today)
```
                            

See data.csv file above for an example of the required format

See [here](example.ipynb) for an example estimate


## Notes
The model was built from publicly available data from these sources:

* https://data.gov.il/dataset/covid-19

* https://datadashboard.health.gov.il/COVID-19/

* https://www.gov.il/he/departments/publications/?OfficeId=4153ab18-52bb-42dc-a347-b513faa428ca&limit=10&skip=0

We did not have full data, so model is built as our best estimate from the publicly available information (e.g. non-integer cases are a result of using percentages from "Merkaz Hameida pdfs").


## Results up to 27/7/2020:

![](/new_crit_pred.jpg?raw=true "New Critical prediction")


![](/total_crit_pred.jpg?raw=true "Total Critical prediction")




