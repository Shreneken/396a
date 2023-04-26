import matplotlib.pyplot as plt
import json

dictionary = json.load(open('./imdb/stats/movie_count_for_date.json', 'r'))
xAxis = [key for key, value in dictionary.items()]
yAxis = [value for key, value in dictionary.items()]
plt.grid(True)

## LINE GRAPH ##
plt.plot(xAxis,yAxis, color='maroon', marker='o')
plt.xlabel('Year')
plt.ylabel('Number of Movies')
ax = plt.gca()
ax.tick_params(axis='x', labelrotation = 90)

## BAR GRAPH ##
fig = plt.figure()
plt.bar(xAxis,yAxis, color='maroon')
plt.xlabel('Year')
plt.ylabel('Number of Movies')
ax = plt.gca()
ax.tick_params(axis='x', labelrotation = 90)
plt.show()