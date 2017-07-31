# Via Coding Challenge
## Initial Data
Link - http://www.andresmh.com/nyctaxitrips/
Trip Data Example:
['FA7C898E583A26D4DE294604DC8AA42B', '2B32A3B1F439C621150208BF31D21C7B', 'VTS', '1','2013-01-01 00:52:00', '2013-01-01 00:59:00', '1', '420', '1.08', '-73.982445', '40.742771000000005', '-73.996574', '40.744583']

## Question 1
A driver is considered on-shift starting after their first pick-up and until they go for at least a 
1-hour period without a rider in their car, at which point their current shift ends (ending with their
last drop-off). How would you predict, at a given point in time, how many drivers would cross a
10-hour on-shift threshold in the next 30 minutes?
### Solution
## Question 2
Create a “live” (streaming) indicator warning of drivers with high probability of crossing that
threshold. Use this indicator to create a list of drivers expected to cross this threshold within the
next 30 minutes of 2013-04- 09 15:00:00.
### Solution
## Question 3
The taxicab dispatcher also wants to identify drivers who are on a roll – these are drivers
who have 5 rides in a row, with less than 10 minutes of empty time between each of the rides
(less than 10 minutes between the drop-off of one ride and the pick-up of the next). Which
drivers were on a roll the most during the entire timespan?
### Solution
## Question 4
Around New York City, there are a few taxi stands where drivers have to wait in a line before
picking up passengers and where passengers wait in a line for taxis. How would you identify
these taxi stands? Can you find examples in this data?
### Solution
## Question 5
What additional data might be useful in predicting whether a driver will cross the 10-hour on-
shift threshold?
## Question 6
For question 2, how would you change your indicator if rides could be canceled mid-ride?
For example, if the driver accidentally started the meter without a rider actually boarding? Or if
rides could be rescinded after the fact? (While all taxi rides in this data set were completed,
would you have to change anything if a ride were started but never completed?)
## Question 7
How would you identify anomalous rides (e.g., rides that shouldn’t be possible, pickups that
shouldn’t be possible)?
