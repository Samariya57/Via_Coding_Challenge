# Via Coding Challenge
## Initial Data  
Link - http://www.andresmh.com/nyctaxitrips/  
Trip Data Example:  
['medallion', 'hack_license', 'vendor_id', 'rate_code', 'pickup_datetime', 'dropoff_datetime', 'passenger_count', 'trip_time_in_secs', 'trip_distance', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude']  
['FA7C898E583A26D4DE294604DC8AA42B', '2B32A3B1F439C621150208BF31D21C7B', 'VTS', '1','2013-01-01 00:52:00', '2013-01-01 00:59:00', '1', '420', '1.08', '-73.982445', '40.742771000000005', '-73.996574', '40.744583']  
  
**I sorted each file by pickup time in advance to work with this data as streaming data**

## Question 1
A driver is considered on-shift starting after their first pick-up and until they go for at least a 
1-hour period without a rider in their car, at which point their current shift ends (ending with their
last drop-off). How would you predict, at a given point in time, how many drivers would cross a
10-hour on-shift threshold in the next 30 minutes?
### Current solution
We predict the number of drivers who cross a 10-hour threshold by computing the following conditional
probability. At a point of time we say that condition _A_ holds for a driver if he crossed a 9.5-hour 
threshold (30 minutes less than in the problem itself) less than 30 minutes ago. Similarly, condition _B_
holds for a driver if he/she crosses a 10-hour threshold in next 30-minutes. Our goal is to compute _P(B|A)_.
At a given point of time we can compute the number _n_ of drivers satisfying condition _A_ (only such drivers
can possibly cross 10-hour threshold in next 30 minutes). Then we predict the number _N_ of drivers who will
cross a 10-hour threshold as _N=P(B|A)*n_.    
We assume that _P(B|A)_ depends only on day of the week and time (particular minute), so we can compute it
from the data. We split all the week into days and days into minutes. For each minute we count how many
drivers crossed 9.5-hour and 10-hour threhold in that minute. Then for each minute we find the number of drivers
who passed 9.5-hour threshold at most 30 minutes earlier (satisfy condition _A_ at this moment) and similar
number for those who crosses 10-hour theshold in next 30-minutes (satisfy condition _B_). The desired probability
_P(B|A)_ is their ratio.  
As result of the approach we have conditional probabilities for each minute for every week day.
So to predict the number of drivers who cross a 10-hour threshold in 30 minutes after a particular moment we have 
to count how many drivers crossed 9.5-hour threshold in last 30 minutes and multiply this number by the
conditional probability for this week day and this minute.
**Example**  
*Input:* 2013-04-09 15:00:00 , 1000  
*Output:*   
## Question 2
Create a “live” (streaming) indicator warning of drivers with high probability of crossing that
threshold. Use this indicator to create a list of drivers expected to cross this threshold within the
next 30 minutes of 2013-04-09 15:00:00.
### Current solution

## Question 3
The taxicab dispatcher also wants to identify drivers who are on a roll – these are drivers
who have 5 rides in a row, with less than 10 minutes of empty time between each of the rides
(less than 10 minutes between the drop-off of one ride and the pick-up of the next). Which
drivers were on a roll the most during the entire timespan?  
### Current solution
We used metric where we count +1 to particular driver each time, when he reachs 5 rides on a roll.  
Details: we don't count extra +1 when he reaches 10,15 etc. rides on a roll.  
As output of the approach we have a table with all drivers ranked by number of times when they reached 5 rides on a roll for the whole year.
### Alternative solution
* We may allow user to specify time range for the count.  
* Also we can use different metrics if they match better business purposes of this ranking.
I.e. instead of +1 add the number of hours on a roll to measure how much time in total
a driver was on a roll. Or count +2 if a driver has 10 hours on shift, +3 for 15 hours and so on.
## Question 4
Around New York City, there are a few taxi stands where drivers have to wait in a line before
picking up passengers and where passengers wait in a line for taxis. How would you identify
these taxi stands? Can you find examples in this data?
### Current solution
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
