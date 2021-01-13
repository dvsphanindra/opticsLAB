from matplotlib import pyplot as plt

from vispy.color import Color

class SpotDiagram:
	def __init__(self, data_x, data_y, marker, colors):
		colorInfo=[]
		for color in colors:
			colorInfo.append(Color(color).__getattribute__("rgb"))
		
		fig = plt.figure()
		ax = fig.add_subplot(1, 1, 1)
		plt.scatter(data_x, data_y, marker=marker,color=colorInfo)
		
		#Move left y-axis and bottom x-axis to centre, passing through (0,0)
		ax.spines['left'].set_position('center')
		ax.spines['bottom'].set_position('center')
		plt.grid(True)
		
		# Eliminate upper and right axes
		ax.spines['right'].set_color('none')
		ax.spines['top'].set_color('none')
		#
		# Show ticks in the left and lower axes only
		ax.xaxis.set_ticks_position('bottom')
		ax.yaxis.set_ticks_position('left')
