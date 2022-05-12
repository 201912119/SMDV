import pandas

from bokeh.io import curdoc
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models import Range1d
from bokeh.models.tools import HoverTool
from bokeh.models.widgets import CheckboxGroup

from motion_detector import df #runs motion_detector.py and grabs the df output

curdoc().theme = 'dark_minimal'

# print(df)

# add tooltip column, datetime as strings
df["Enter_tooltip"]=df["Enter"].dt.strftime("%F %T.%3Nms")
df["Exit_tooltip"]=df["Exit"].dt.strftime("%F %T.%3Nms")
# print(df)

source = ColumnDataSource(df)

TOOLTIPS = [
    ("Enter","@Enter_tooltip"),
    ("Exit","@Exit_tooltip"),
]

hover_tool = HoverTool(tooltips=TOOLTIPS)

f = figure(width=500, height=100, x_axis_type="datetime", sizing_mode="scale_width", 
           title="Activity Detected")
f.add_tools(hover_tool)

f.y_range = Range1d(0,1)
f.yaxis.ticker = [0,1]
f.yaxis.visible=False

f.xaxis.axis_label = "Time"
f.xaxis.axis_label_text_font_style = "bold"
f.xaxis.major_tick_line_color = 'black'
f.xaxis.minor_tick_line_color = 'black'

f.xgrid.minor_grid_line_color = '#e5e5e5'
# print(f.xgrid.properties_with_values())

d1=f.quad(left="Enter", right="Exit", top=1, bottom=0, 
          source=source, color="red", alpha=0.5)

output_file("graph.html")

show(f)