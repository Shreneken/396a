import matplotlib.pyplot as plt
import json
import math

curr_data = 'words_per_rating'
zero_data = ()

dictionary = json.load(open('./imdb/stats/reviews_per_rating.json', 'r'))
xAxis = [key for key, value in dictionary.items() if key not in zero_data]
temp = [value for key, value in dictionary.items() if key not in zero_data]
print(temp)
yAxis = [math.floor(x[curr_data]) for x in temp]
plt.grid(True)

## LINE GRAPH ##
plt.plot(xAxis,yAxis, color='maroon', marker='o')
plt.xlabel('Ratings')
plt.ylabel('Total number of Words')
ax = plt.gca()
ax.tick_params(axis='x', labelrotation = 90)

## BAR GRAPH ##
fig = plt.figure()
plt.bar(xAxis,yAxis, color='maroon')
plt.xlabel('Ratings')
plt.ylabel('Total number of Words')
ax = plt.gca()
ax.tick_params(axis='x', labelrotation = 90)
plt.show()