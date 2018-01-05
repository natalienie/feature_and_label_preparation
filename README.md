# feature_and_label_preparation
this is used to generate feature and label from data of poloniex API.

user could select start_date and end_date and period to choose the size of data frame.

the feature consist of (0,128,2) shape, that is i am treating the 128 consecutive [price, macd] as one feature.

label would be of 3 classes [-1, 0 , 1. ]

1 represent an increase of price over certain magnitude
-1 represent a decrease of price over certain magnitude
0 represent everything else.

I am not sure whether such kind of label is effective? 

would appreciate if could have some feedback on better ways to class the label. Thanks ~~
