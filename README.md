# MA705 Individual Project Jinru Wei
 MA705 Individual Project Carmax Dashboard

This Dashboard was created to show inventory information for CARMAX website.
The data was collected from https://www.carmax.com/cars, and was scrapped using BeautifulSoup 4.

The dataset includes 14 variables:

Type: SUV, Truck, Crossover, Sedan, Coupe, Convertible, Luxury, Sport Car, Diesel Engine, Van, Hybrid, Wagon, Electric Vehicle

Year

Make

Model

Price

Milleage

Average Review

Transmission

Color

Interior Color

Features: Main equipment

Availabilty: whether available in Norwood or can be transported

Description: description of the car

Car Image: the image url

The cleaned dataset was saved as carmax2.csv.

Then a dashboard has been built based on the carmax2 dataset mainly includes the following parts:

1. An inventory versus Year bar chart

2. A car picture and description visulization plot

3. A scatter plot that can be customize among Year, Price, Milleage and Average Review

4. A table includes the entire dataset that can be customize according to user's preference.
