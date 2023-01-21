TsingTao Corp.  

HI!CKATHON 2023

Date: 15/01/2023  

# I.	OVERVIEW
## 1.	Project Background and Description
 	Describe how this project came about, and the purpose.
The idea for this project came to our minds when we heard about actual needs in the industry: right now 70% of houses in France do not have any sensors for remote observation about the house. It makes it difficult in particular to conduct refurbishment operations, because it is unknown what refurbishment companies should focus on in order to decrease the energy consumption of the building. The purpose of our project is to introduce the app that would allow refurbishment companies to predict what features affect the most energy consumption and focus on changing them. Underneath our app lies a Machine Learning model that predicts energy consumption based on the set of house features.

## 2.	Project Scope
 	 Scope answers questions including what will be done, what won’t be done, and what the result will look like.

During the hackathon we outlined how our future product will look like: with our product we plan to cover the most of the houses in France. Since behavioral habits and house characteristics may be different in other countries, our product will not be applicable initially to other countries, however, we have a high potential for expansion if we collect additional data for other countries. As a result we imagine an app where refurbishment companies could pass parameters of the building in order to know what they should focus. As a prototype we don't have functionality for conducting a further analysis of fenergy consumption based on correlations with data, however in the future we plan to also provide consulting services for refurbishment companies.

## 3.	Presentation of the group
 	Include your specialization at school, etc.

| First name | Last name  | Year of studies & Profile      | School            | Skills          | Roles/Tasks   | Observations |
| ---------- | ---------- | ------------------------------ | ----------------- | --------------- | ------------- | ------------ |
| Semen      |Dolgoborodov| BX2025, Math/Physics           |Ecole Polytechnique|Data Science, ML |Work on model  | None         |
| Florian    |Labaye      | X2020, Computer Science        |Ecole Polytechnique|Data Science, ML |Work on model  | None         |
| Tien-Thinh |Tran-Thuong | 1 year, Computer Science       |ENSAE              |Data Science, ML |Work on model  | None         |
| Matthis    |Dolisy      | 2 year, Strategic Management   |IMT-BS             |Business modeling|Market research| None         |
| Juliette   |Demoly      |2 year,Data Science for business|HEC                |Data Science, ML |Data analysis  | None         |




## 4.	Task Management
 	Describe how you interacted and collaborated as a team, and the effect of every member’s unique background on the project.
We had an opportunity to work as a quite diverse team. We all study at different educational programs, and we think it contributed to the productive work in our team. The background of Matthis in business was indispensable for the market research and developing marketing strategies for our product. Tien-Thinh's background in deep learning allowed us to try building a linear regressor on Keras for testing the model. Florian was working on the Machine learning application of our model, he compared GradientBoostingRegressor with RandomForest, and was working to adjust hyperparameters. Semen did the data preprocessing adjusted to the developed model in order to have more stable learning with as much information as possible. Finally, Juliette provided valuable insights by analysing correlations of different data, and distributions of data. 


# II.	PROJECT MANAGEMENT
## 1.	Data Understanding
 	Provided the initial collection of data has already occurred, this step includes identifying and defining the relevant data, exploring the range, scale, formats, contents, and biases of the data, and evaluating the quality and validity of the resulting data.
For training we had a dataset of 1010684 rows and 70 meaningful features (the last feature was level_0 which denoted the id of the house). For some features we observed a large quantity of NaN values that we dealt with in the next step. We observed that some categorical values have an analogue of Nan, namely '[]', and we dealt with this problem during data pre-processing. We also classified the data based on its type: we observed 40 categorical features, 26 numerical features, and 4 boolean features. We did analysis of outliers for every feature as well as target value ('energy_consumption_per_annum'). We observed that if we would make a cut of bata based on 3 standard deviations we would loose quite a lot of data, so that's why for preprocesing we used less strict condition.


## 2.	Data Pre-processing
 	Explain how the selection of data was manipulated and modified to remove redundant features and improve the quality of the data. Describe the preprocessing techniques used, such as data augmentation.
Firstly, we dealt with outliers for every feature. As it was discussed in the previous part, we observed that if we would cut the outliers based on the 3 standard deviations we would loose too many data, so we cut the ouliers that fall beyond 4.5 standard deviations of the data distribution for every feature and the target. Then we merged the data based on the rows where all the features and target was left. 
After that, we dealt with ccolumns with many NaNs. The criteria was that if the amount of NaNs compared to the overall data is more than 30% then we would just drop that column. We did the similar procedure for the categorical features that contain a lot of '[]' values. 
After that we filled the remaining NaNs with the median value  of the column for numerical features, and with the mode value of the column for the categorical features.
Additionally, for 'consumption_measurement_date' feature we changed the precise date of measurements to the month value, because we deduced that fundementally energy consumtion depends on the season of the year. It is also important to note  that when we plotted the graph of eergy consumption against the measurement date, we saw the overall declining trend, but we didn't think it's a good feature of the model, because the trend is most probaly connected with confounding factors that are not easily observable.
In column 'outer_wall_thickness' we changed the string values to the float values based on the numbers that were in the string.
Also, we discarded the categorical features where there are many unique values because as it will be describe in the next part using them resulted in worse results.
Finally, we converted all categorical values into numerical values using one-hot encoding, and we replace True/False values in boolean features with 1/0.

## 3.	Modeling Development
 	Describe how you selected algorithms, how you calibrated them according to the data and how - in fine - you selected the best AI model using a well-defined set of metrics.
We had four main algorithms that we considered as part of our solution. 
The first 3 algorithms were RandomForest, GradientBoostingRegressor, and XGBoost Regressor from sklearn. For them we tried to use different preprocessing tehniques. For example, we tried to deal with the categorical features where there are many unique values by keeping only 5 the most commonly used values, and naming everything else by 'other'. However, after calculating the score of this approach using the explained variance we found out that the final score is worse than when we trained the model without these columns. Additionally, we tested different encoding techniques for our model, namely target encoding, and one-hot encoding. On the test dataset, one-hot encoding produced better results.  
  
The last model was based on deep learning, and was built using Keras. For that model we also built additional functions to parse some categorical features where there were multiple values into the array of these values which we then converted into the array of ones and zeros. We also tried to improve the result by adopting the following procedure: we first trained the model on the numerical feautures. Then we trained another model on the categorical features this model is called Encoder-Decoder (encoded as arrays of ones and zeroes). Finally, using transfer learning we combined these 2 models using 1 additional layer of 64 neurons, and outputed the single value as predicted energy consumption.
By comparing the model based on the explained variance score, we came to the the conclusion that XGBoost Regressor works best.

## 4.	 Deployment Strategy
 	What best practices/norms did you follow? How do you plan on deploying your AI solution?
We tried to follow all best practices and norms when training an AI model that exists in the industry. For example, we started by building a simple model with just numerical feautures in order to have a baseline, and then we just iterated trying out different techniques for pre-processing. Also, in the web app we didn't collect any personal data that we hadn't mentioned in advance, and we tried not to cause too much CO2 emissions during the training by making the quick tests of the model on 10% of all data. Transparency is important for us, and in the future we will do our best to keep up wit the standards. 
We see the roadmap for deploying our AI solution as follows: 
1) fine-tuning the model, and collecting more test data in order to be sure in the validity of our results
2) trying to attract the customers both organically with our web application and by contacting them directly
3) constantly evaluating the model using the new data we will acquire
4) launching the solution to provide the consulting services for refurbishment companies
5) expanding to other countries.


# III.	CARBON FOOTPRINT LIMITATION
 	Describe the taken measures/actions during the development of your solution in view of limiting the carbon footprint.
During the development of the solution there weren't a lot of things we could do in order to limit the carbon footprint. However, we tried to do what we could. For example, we trained the prototypes of our model only on 10% of the whole data in order to decrease computational resources needed, and as the result our carbon footprint.
Also, we highlighted the future benefits of our product for limiting the CO2 emissions. For example, we think that with our web app refurbishment companies will be more incentivized to conduct a restoration of old buildings focusing only on the most important factors. As a result we expect a huge decrease in the overall energy consumption in France.


# IV.	CONCLUSION
 	Tell us about the actual results, their limitations as well as future perspectives and improvements.
In the end, with the model we were able to get the score of 76.62 using XGBoost Regressor. Additionally, we made a prototype of the web-application where refurbishment companies can predict the energy consumption of their house of interest. Our solution is limited to the data that we had. In particular, this means that our model may have geographical constraints based on the training dataset. Also, it might be possible that some of the features tht are important for energy consumption were not captured. We see the following possibilities for future improvements of the model: collect data from other countries in order to expand our operations, and experiment with other features that were not present in training dataset to see if we canXGBoost Regressor improve the prediction of the model. Also, to expand the business operations we see a posibility of introducing consulting services to refurbishment companies regarding energy consumption insights.
