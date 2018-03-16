
import plotly.plotly as py
import plotly.graph_objs as go
trace1= go.Scatter(x=[0,0.5,1,2,2.2],y=[1.23,2.5,0.42,3,1])
layout= go.Layout(images= [dict(
                  source= "https://images.plot.ly/language-icons/api-home/python-logo.png",
                  xref= "x",
                  yref= "y",
                  x= 0,
                  y= 3,
                  sizex= 2,
                  sizey= 2,
                  sizing= "stretch",
                  opacity= 0.5,
                  layer= "below")])
fig=go.Figure(data=[trace1],layout=layout)
py.iplot(fig)