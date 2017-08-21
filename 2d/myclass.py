import numpy as np
import argparse
import plotly.offline as py
import plotly.graph_objs as go
#================================
class database(object):
    def __init__(self):
        self.nodes = None
        self.elements = None
        self.plotdata = []
    def importNodes(self,fileName):
        self.nodes = np.loadtxt(fileName,dtype=[('id','uint32'),('xy','2float32'),('val','float32')])
    def importElements(self,fileName):
        self.elements = np.loadtxt(fileName,dtype=[('id','uint32'), ('nodes','4uint32')])
        self.elements.sort(order='id')
    def createElements(self):
        for i,element in enumerate(self.elements):
            nodesID = element['nodes']
            # === T3 below ===
            if nodesID[3] == 0:
                nodesID = np.delete(nodesID, 3)
                coordinate = [list(self.nodes[self.nodes['id'] == nodesID[j]]['xy'].reshape(-1)) for j in range(3)]
                val = [list(self.nodes[self.nodes['id'] == nodesID[j]]['val'])[0] for j in range(3)]
            # === R4 below ===
            else:
                coordinate = [list(self.nodes[self.nodes['id'] == nodesID[j]]['xy'].reshape(-1)) for j in range(4)]
                val = [list(self.nodes[self.nodes['id'] == nodesID[j]]['val'])[0] for j in range(4)]
            coordinate.append(coordinate[0])
            coordinate = np.asarray(coordinate)
            val.append(val[0])
            nodesID = list(nodesID)
            nodesID.append(nodesID[0])
            hovertext = ['Val = ' + str(i) for i in val]
            hovertext = ['Nodes ID = ' + str(i) + ' ' + str(j) for i,j in zip(nodesID,hovertext)]
            data = go.Scatter(
                x = coordinate[:,0],
                y = coordinate[:,1],
                mode='markers+lines+text',
                marker=dict(
                    size=1,
                ),
                line=dict(
                    color='#cccccc',
                    width=0.5
                ),
                hovertext=hovertext,
                textfont=dict(
                    family='sans serif',
                    size=10,
                    color='#ff7f0e'
                ),
                textposition='bottom',
                )
            self.plotdata.append(data)
    def createContour(self):
        val = self.nodes['val']
        contourMax = np.max(val)
        contourMin = np.min(val)
        contourSize = 0.1*(contourMax - contourMin)
        coordinate = self.nodes['xy']
        val = self.nodes['val']
        data = go.Contour(
            x=coordinate[:,0],
            y=coordinate[:,1],
            z=val,
            # connectgaps=False,
            contours=dict(
                start=contourMin,
                end=contourMax,
                size=contourSize,
            ),
        )
        self.plotdata.append(data)
    def draw(self):
        fig = dict(data=self.plotdata, layout=self.layout())
        py.plot(fig, filename='2d-mesh.html')
    def layout(self):
        layout = go.Layout(
            title='2D Model',
            showlegend=False,
            hovermode = 'closest',
            scene = dict(
                xaxis=dict(
                    title='x axis',
                    titlefont=dict(
                    family='Courier New, monospace',
                    size=20,
                    color='#7f7f7f'
                    )
                ),
                yaxis=dict(
                    title='y axis',
                    titlefont=dict(
                    family='Courier New, monospace',
                    size=20,
                    color='#7f7f7f'
                    )
                )
            )
        )
        return layout
