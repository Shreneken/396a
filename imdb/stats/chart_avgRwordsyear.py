import matplotlib.pyplot as plt
import json
import math

dictionary = json.load(open('./imdb/stats/avg_words_review_per_year.json', 'r'))
xAxis = [key for key, value in dictionary.items()]
yAxis = [math.floor(value['average_words_year']) for key, value in dictionary.items()]
plt.grid(True)

## LINE GRAPH ##
plt.plot(xAxis,yAxis, color='purple', marker='o')
plt.xlabel('Year')
plt.ylabel('Average Words per review')
ax = plt.gca()
ax.tick_params(axis='x', labelrotation = 90)

## BAR GRAPH ##
fig = plt.figure()
plt.bar(xAxis,yAxis, color='purple')
plt.xlabel('variable')
plt.ylabel('Average Words per review')
ax = plt.gca()
ax.tick_params(axis='x', labelrotation = 90)
plt.show()