import numpy as np
import argparse
import plotly.offline as py
import plotly.graph_objs as go
#================================
class database(object):
    DICT_ARGS = {
        'x': [0,1,2,'y axis','z axis'],
        'y': [1,2,0,'z axis','x axis'],
        'z': [2,0,1,'x axis','y axis']
    }
    def __init__(self):
        self.nodes3d = np.zeros(1)      # all nodes in 3d space (structured array) => [id, [x,y,z], initH, initTemp]
        self.nodes2d = np.zeros(1)      # all nodes on the designated section (structured array) => [id, [x,y,z], initH, initTemp]
        self.elements3d = np.zeros(1)   # all elements in 3d space (structured array) => [id, [node1, node2, node3, node4]]]
        self.elements2d = np.zeros(1)   # all elements sitting on the designated section (structured array) => [id, [node1, node2, node3, node4]]]
        self.isNodeInPlane = []
        self.plotdata3d = []
        self.plotdata2d = []
    def importNodes(self,fileName):
        self.nodes3d = np.loadtxt(fileName,dtype=[('id','int'),('xyz','3float32'),('initH','float'),('initT','float')])
    def importElements(self,fileName):
        self.elements3d = np.loadtxt(fileName,dtype=[('id','int'), ('nodes','4int32')])
        self.elements3d.sort(order='id')
    def select2dPlotNodes(self,args):
        nodes3d = self.nodes3d
        selected = []
        key = self.DICT_ARGS[args.sect[0]][0]
        for i in range(len(nodes3d)):
            if nodes3d['xyz'][i,key] == float(args.sect[1]):
                selected.append(nodes3d[i])
        self.nodes2d = np.asarray(selected,
            dtype=[('id','int'),('xyz','3float32'),('initH','float'),('initTemp','float')])
    def select2dPlotElements(self):
        node2dID = self.nodes2d['id']
        elements3dNodes = self.elements3d['nodes']
        elementsOnSection = []
        for i,node in enumerate(elements3dNodes):
            isNodeInPlane = list(map(lambda x: x in node2dID, list(node)))
            if sum(isNodeInPlane) == 3:
                elementsOnSection.append(self.elements3d[i])
                self.isNodeInPlane.append(isNodeInPlane)
        self.elements2d = np.asarray(elementsOnSection,
            dtype=[('id','int'), ('nodes','4int32')])
    def create3dPlotNodesData(self):
        coordinate = self.nodes3d['xyz']
        data = go.Scatter3d(
            x = coordinate[:,0],
            y = coordinate[:,1],
            z = coordinate[:,2],
            mode = 'markers',
            marker = dict(size=3,line=dict(color=coordinate[:,0],colorscale='Viridis',width=.5),opacity=0.8)
            )
        self.plotdata3d = [data]
    def create2dPlotNodesData(self,args):
        coordinate = self.nodes2d['xyz']
        nodeID = self.nodes2d['id']
        data = go.Scatter(
            x = coordinate[:,self.DICT_ARGS[args.sect[0]][1]],
            y = coordinate[:,self.DICT_ARGS[args.sect[0]][2]],
            mode='markers+text',
            marker=dict(size=3,line=dict(color='rgba(217, 217, 217, 0.14)',width=.5),opacity=0.8),
            text=nodeID,
            textfont=dict(
                family='sans serif',
                size=10,
                color='#ff7f0e'
            ),
            textposition='bottom',
            line=dict(
                color='#1f77b4',
                width=3
            )
        )
        self.plotdata2d = [data]
    def create3dPlotElementsData(self):
        for i,nodes in enumerate(self.elements3d):
            coordinate = []
            nodes = self.elements3d['nodes'][i]
            coordinate = [list(self.nodes3d[self.nodes3d['id'] == nodes[i]]['xyz'].reshape(-1)) for i in range(4)]
            coordinate.append(coordinate[0])
            coordinate = np.asarray(coordinate)
            data = go.Scatter3d(
                x = coordinate[:,0],
                y = coordinate[:,1],
                z = coordinate[:,2],
                mode='markers+lines',
                marker=dict(size=3,line=dict(color='rgba(217, 217, 217, 0.14)',width=.5),opacity=1),
                line=dict(
                    color='#1f77b4',
                    width=1
                )
            )
            self.plotdata3d.append(data)
    def create2dPlotElementsData(self,args):
        for i,nodes in enumerate(self.elements2d):
            coordinate = []
            nodes = self.elements2d['nodes'][i]
            index = self.isNodeInPlane[i].index(False)
            nodes = np.delete(nodes,index)
            nodeID = nodes
            coordinate = [list(self.nodes2d[self.nodes2d['id'] == nodes[i]]['xyz'].reshape(-1)) for i in range(3)]
            coordinate.append(coordinate[0])
            coordinate = np.asarray(coordinate)
            data = go.Scatter(
                x = coordinate[:,self.DICT_ARGS[args.sect[0]][1]],
                y = coordinate[:,self.DICT_ARGS[args.sect[0]][2]],
                # mode='markers+text+lines',
                mode='markers+lines',
                marker=dict(
                    size=2,line=dict(color='rgba(217, 217, 217, 0.14)',width=.5),opacity=1
                ),
                # text=nodeID,
                # textfont=dict(
                #     family='sans serif',
                #     size=10,
                #     color='#ff7f0e'
                # ),
                # textposition='bottom',
                line=dict(
                    color='#1f77b4',
                    width=1
                )
            )
            self.plotdata2d.append(data)
    def draw3d(self):
        fig = dict(data=self.plotdata3d, layout=self.layout3d())
        py.plot(fig, filename='simple-3d-scatter.html', auto_open=False)
    def draw2d(self,args):
        fig = dict(data=self.plotdata2d, layout=self.layout2d(args))
        py.plot(fig, filename='simple-2d-scatter.html', auto_open=False)
    def layout3d(self):
        layout = go.Layout(
            title='3d Model',
            showlegend=False,
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
                ),
                zaxis=dict(
                    title='z axis',
                    titlefont=dict(
                    family='Courier New, monospace',
                    size=20,
                    color='#7f7f7f'
                    )
                )
            )
        )
        return layout

    def layout2d(self,args):
        layout = dict(
            title='Sectional view at {} = {}'.format(args.sect[0],args.sect[1]),
            showlegend=False,
            xaxis=dict(
                title=self.DICT_ARGS[args.sect[0]][3],
                titlefont=dict(
                family='Courier New, monospace',
                size=20,
                color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title=self.DICT_ARGS[args.sect[0]][4],
                titlefont=dict(
                family='Courier New, monospace',
                size=20,
                color='#7f7f7f'
                )
            )
        )
        return layout
