# Using graph_objects
import plotly.graph_objects as go

import pandas as pd
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

dx = ["2015-02-17", "2015-02-18"]
dy = ["128.880005", "129.880005"]

fig = go.Figure([go.Scatter(x=dx, y=dy)])
fig.show()