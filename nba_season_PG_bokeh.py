#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd
from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool, Slider, Select, CategoricalColorMapper
from bokeh.palettes import Spectral6, Viridis256, Plasma256
from bokeh.layouts import widgetbox, row, column, gridplot


df_nba = pd.read_csv('nba_season_PG.csv')
df_nba = df_nba.drop(df_nba.columns[0], axis=1)
df_nba = df_nba.loc[df_nba['Pos'].notna()]
df_nba['Year'] = df_nba['Year'].astype(int)
df_nba['Pos'] = df_nba['Pos'].apply(lambda x: x[-1])
df_nba = df_nba.sort_values(by=['Player', 'Year'])

source = ColumnDataSource(data={
        'Year'   : df_nba[df_nba['Player'].str.match('Michael Jordan')].Year,
        'y'      : df_nba[df_nba['Player'].str.match('Michael Jordan')].PTS,
        'Player' : df_nba[df_nba['Player'].str.match('Michael Jordan')].Player,
        'Pos'    : df_nba[df_nba['Player'].str.match('Michael Jordan')].Pos,
        'Tm'    : df_nba[df_nba['Player'].str.match('Michael Jordan')].Tm
    })
# set up groups for colors
Tm_list = df_nba.Tm.unique().tolist()
Pos_list = df_nba.Pos.unique().tolist()
Player_list = df_nba.Player.unique().tolist()

color_mapper = CategoricalColorMapper(factors=Tm_list, palette=Plasma256)
plot = figure()
plot.circle(x='Year', y='y', fill_alpha=0.8, size=12, source=source,
            color=dict(field='Tm', transform=color_mapper), legend='Tm')
plot.xaxis.axis_label = 'Year'
plot.x_range.start = min(source.data['Year'])-2
plot.x_range.end = max(source.data['Year'])+2
plot.y_range.start = min(source.data['y'])*0.95
plot.y_range.end = max(source.data['y'])*1.05

def update_plot(attr, old, new):
    #plr = slider.value
    plr = plr_select.value
    #print(plr)
    y = y_select.value
    #print(y)
    #plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    new_data = {
        'Year' : df_nba[df_nba['Player'].str.match(plr)].Year,
        'y' : df_nba[df_nba['Player'].str.match(plr)][y],
        'Player' : df_nba[df_nba['Player'].str.match(plr)].Player,
        'Pos' : df_nba[df_nba['Player'].str.match(plr)].Pos,
        'Tm' : df_nba[df_nba['Player'].str.match(plr)].Tm
    }
    # Assign new_data to source.data
    source.data = new_data
    # Set the range of all axes
    plot.x_range.start = min(source.data['Year'])-2
    plot.x_range.end = max(source.data['Year'])+2
    plot.y_range.start = min(source.data['y'])*0.95
    plot.y_range.end = max(source.data['y'])*1.05
    # Add title to plot
    plot.title.text = 'Seasonal data of %s' % plr

#slider = Slider(start=1950, end=2016, step=1, value=1950, title='Year')
#slider.on_change('value', update_plot)

plr_select = Select(
    options=Player_list,
    value='Michael Jordan',
    title='Select a player'
)
plr_select.on_change('value', update_plot)

y_select = Select(
    options=['PTS', 'PTS_PG', 'AST', 'AST_PG', 'TRB', 'TRB_PG', 'BLK', 'BLK_PG', 'STL', 'STL_PG'],
    value='PTS',
    title='y-axis data'
)
y_select.on_change('value', update_plot)

layout = row(widgetbox(plr_select, y_select), plot)
curdoc().add_root(layout)
#show(layout)
#output_file('hover_glyph.html')
