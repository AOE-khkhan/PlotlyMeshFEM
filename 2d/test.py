import numpy as np
import plotly.offline as py
import plotly.graph_objs as go

plotdata = []
nodes = [[0,0,0],[1,0,5],[2,0,9],[0,1,8],[1,1,-2],[2,1,9]] #normal
nodes = [[0,0,0],[1,0.001,5],[2,0,9],[0,1.001,8],[1,1,-2],[2,1,9]] #weird
nodes = np.asarray(nodes)
# draw contour
data = go.Contour(
    x=nodes[:,0],
    y=nodes[:,1],
    z=nodes[:,2],
)
plotdata.append(data)
# draw
fig = dict(data=plotdata)
py.plot(fig, filename='2d-mesh.html')
