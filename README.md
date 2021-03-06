# Via Coding Challenge
## Repository structure

    .
    ├── Question1
    │   ├── MySQL Tables
    │   │   ├── Sunday.txt                # How many drivers crossed 9.5-hour and 10-hour thresholds on Sunday for each minute
    │   │   ├── Sunday_Prob.txt           # Conditional probability for each minute on Sunday
    │   │   └── ...                       # Similar files for other days of week
    │   ├── clean_db.py                   # Support script to clean tables
    │   ├── cond_prob.py                  # Script to calculate conditional probabilities
    │   └── fill_week_minutes_tables.py   # Count drivers who crossed 9.5-hour and 10-hour thresholds for each minute
    ├── Question2                    
    │   ├── alarm_list.py                 # Script returns drivers who crossed 9.5 in 30 minutes before 2013-04-09 15:00:00
    │   ├── alarm_list_20.txt             # Script returns drivers who crossed 9.5 in 20 minutes before 2013-04-09 15:00:00
    │   └── ave_ride_gap_time.py          # Support script to find average gap and ride times
    ├── Question3
    │   ├── MySQL Tables
    │   │   └── ONROLL Table.txt          # Drivers ranked by counting on-roll times
    │   └── count_on_roll.py              # Script to count on-roll times for each driver for the whole year
    ├── Question4
    │   ├── Clusters_NY.png               # Visualization of an clusterization example
    │   ├── clusters.py                   # Script used DBSCAN method to find clusters
    │   ├── result_mean.csv               # Result with centers of clusters
    │   └── result_qua.csv                # Result with number of members in each cluster
    ├── Images
    │   └── ...                           #Image files for README.md 
    └── README.md

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
probability. At a point of time, we say that condition _A_ holds for a driver if he crossed a 9.5-hour 
threshold (30 minutes less than in the problem itself) less than 30 minutes ago. Similarly, condition _B_
holds for a driver if he/she crosses a 10-hour threshold in next 30-minutes. Our goal is to compute _P(B|A)_.
At a given point of time, we can compute the number _n_ of drivers satisfying condition _A_ (only such drivers
can possibly cross 10-hour threshold in next 30 minutes). Then we predict the number _N_ of drivers who will
cross a 10-hour threshold as _N=P(B|A)*n_.    
We assume that _P(B|A)_ depends only on the day of the week and time (particular minute), so we can compute it
from the data. We split all the week into days and days into minutes. For each minute we count how many
drivers crossed 9.5-hour and 10-hour threshold in that minute (script _/Question1/fill_week_minutes_tables.py_ ). Then for each minute, we find the number of drivers
who passed 9.5-hour threshold at most 30 minutes earlier (satisfy condition _A_ at this moment) and a similar
number for those who cross 10-hour threshold in next 30-minutes (satisfy condition _B_). The desired probability
_P(B|A)_ is their ratio.    

**Friday 9.5 threshold distribution**  
![alt text][fd]  

**Sunday 10 threshold distribution**  
![alt text][sd]

[sd]: https://github.com/Samariya57/Via_Coding_Challenge/blob/master/Images/Sunday_10.jpg "Sunday distribution"
[fd]: https://github.com/Samariya57/Via_Coding_Challenge/blob/master/Images/Friday_95.jpg "Friday distribution"  

As result of the approach, we have conditional probabilities for each minute for every week day.
So to predict the number of drivers who cross a 10-hour threshold in 30 minutes after a particular moment we
have to count how many drivers crossed 9.5-hour threshold in last 30 minutes and multiply this number by the
conditional probability for this week day and this minute.
**Example**  
*Input:* 2013-04-09 15:00:00 , 2340 // Tuesday, minute 900    
*Output:* 2340*0.8031 = 1879  
## Question 2
Create a “live” (streaming) indicator warning of drivers with high probability of crossing that
threshold. Use this indicator to create a list of drivers expected to cross this threshold within the
next 30 minutes of 2013-04-09 15:00:00.
### Current solution
We notify a driver when he/she crosses 9-hour-and-40-minutes threshold. We take 20 minutes before the 
10-hour threshold as an estimate for "dangerous" times period based on a computation that
an average gap between rides is 9 minutes and a mean length of a ride is 12 minutes. Thus if there's
no client at the moment and 20 minutes are left before the 10-hours threshold, a driver has a high probability
to cross this threshold if he/she tries to take one more passenger.
### Ways to modify
To make the current solution more flexible we can give alarms depending on if a driver has a passenger
when he/she is 9h30m on-shift. If at this moment there is a passenger, we send an alarm immediately,
because there is enough time to pick only one more customer after this is dropped-off. If there is no one,
we wait until the driver crosses 9h40m-threshold or a new passenger is picked up, whenever is sooner, and
then send a warning.

A much more personalized approach is to send notifications to drivers based on historical behavior of
a particular driver. For example, if a driver always stops after 9h40m on-shift then the
probability that he/she crosses the 10-hours threshold is negligibly small and we don't send him/her
a notification. However to use this method we must have big historical data for each driver
which is not always possible, i.e. at the beginning of the year or his/her career. There's also
a side effect that a driver may not understand who don't know the method may think that it's a bug
that the system works differently for him/her and his/her colleague.  
## Question 3
The taxicab dispatcher also wants to identify drivers who are on a roll – these are drivers
who have 5 rides in a row, with less than 10 minutes of empty time between each of the rides
(less than 10 minutes between the drop-off of one ride and the pick-up of the next). Which
drivers were on a roll the most during the entire timespan?  
### Current solution
We used metric where we count +1 to the particular driver each time when he reaches 5 rides on a roll.  
Details: we don't count extra +1 when he reaches 10,15 etc. rides on a roll.  
As the output of the approach, we have a table with all drivers ranked by the number of times when they reached 5 rides on a roll for the whole year.
### Ways to modify
* We may allow the user to specify the time range for the count.  
* Also we can use different metrics if they match better business purposes of this ranking.
I.e. to add instead of +1 the number of hours on a roll to measure how much time in total
a driver was on a roll. Or count +2 if a driver has 10 hours on shift, +3 for 15 hours and so on.
## Question 4
Around New York City, there are a few taxi stands where drivers have to wait in a line before
picking up passengers and where passengers wait in a line for taxis. How would you identify
these taxi stands? Can you find examples in this data?
### Current solution
Passengers in a line take taxis in almost the same place (not exactly in the same one, but in
a close neighborhood) and these events happen in a sequence. Thus one can detect these places
by analyzing the density of events in space and time.  
We will use a simplified method by assuming that these lines have a high long-term impact
and analyze only high density in space. In other words, if there is a place with a line which
exists for a very short time and disappears soon it is ignored. We focus on stable lines which
often appear in the same place.
For this purpose, we use **DBSCAN** method for clustering pickup places.
As output of this approach, we have list of clusters (centers and number of pickups in cluster).   
At this moment I precessed only sample of data, however, we already can recognise several terminals
in JFK and LaGuardia airports, for example.

![alt text][clusters]

[clusters]: https://github.com/Samariya57/Via_Coding_Challenge/blob/master/Question4/Clusters_NY.png "Clusters"  

### Ways to modify
After adding time to our calculations we will have to use **Getis-Ord** metric.
## Question 5
What additional data might be useful in predicting whether a driver will cross the 10-hour on-
shift threshold?
### Answer
Internal sources
* Historical data about drivers' activity for previous years (see Question 2).  
External sources
* Weather/forecast. For example, if it rains people take taxi more often.
* Information about MTA breakdown and changes in the schedule.
* Information about big events near the driver such as ends of festivals, sports games, concerts, etc.
## Question 6
For question 2, how would you change your indicator if rides could be canceled mid-ride?
For example, if the driver accidentally started the meter without a rider actually boarding? Or if
rides could be rescinded after the fact? (While all taxi rides in this data set were completed,
would you have to change anything if a ride were started but never completed?)  
### Answer
This affects only the first approach described in "Ways to modify" for Question 2. If a driver
who has got an alarm cancels a ride and we are sure that it's canceled, not finished, we need
to recheck if he still needs to be alarmed based on our criterions.
## Question 7
How would you identify anomalous rides (e.g., rides that shouldn’t be possible, pickups that
shouldn’t be possible)?  
### Answer
There are several types of anomalies in rides and unfortunately, different methods should be
used to identify them. We have the following types:
* A driver makes next pickup before a drop-off of the previous passenger. For each driver, we store
last drop-off time and can compare it with the pickup time of a new ride of this driver. 
* Pick-up or drop-off location is outside NYC (use range in longitude and latitude), in the
water (check types in result from Google Maps Reverse Geocoding) or in the middle of a park.
* Too fast rides. We can sort obviously impossible cases such as zero/negative time.
For other cases, we compare average speed estimated from distance and time with the speed limit.
