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

See example.ipynb for an example estimate


## Results up to 27/7/2020:

![](/new_crit_pred.jpg?raw=true "New Critical prediction")


![](/total_crit_pred.jpg?raw=true "Total Critical prediction")




