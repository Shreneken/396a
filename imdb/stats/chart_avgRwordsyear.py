import matplotlib.pyplot as plt
import json

dictionary = json.load(open('./imdb/stats/avg_words_review_per_year.json', 'r'))[0]
xAxis = [key for key, value in dictionary.items()]
yAxis = [value for key, value in dictionary.items()]
plt.grid(True)

## LINE GRAPH ##
plt.plot(xAxis,yAxis, color='maroon', marker='o')
plt.xlabel('variable')
plt.ylabel('value')
ax = plt.gca()
ax.tick_params(axis='x', labelrotation = 90)

## BAR GRAPH ##
fig = plt.figure()
plt.bar(xAxis,yAxis, color='maroon')
plt.xlabel('variable')
plt.ylabel('value')
ax = plt.gca()
ax.tick_params(axis='x', labelrotation = 90)
plt.show()