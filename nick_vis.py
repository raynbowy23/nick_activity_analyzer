import os
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth

import config as cfg

"""
We want to clarify
    - locations
    - current users
    - weather
    - temperature
    - Daily average user
    - Daily total user
"""

def prepare_drive_authentication():

    # Set google drive authentication
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive

def get_data(drive):
    '''
    Get csv data from google drive
    '''
    f = drive.CreateFile({'id': os.environ['CSV_ID']})
    # delete this file at the end of the running
    f.GetContentFile('output.csv', mimetype='text/csv')
    indexes = ['date', 'Location', 'Total Capacity', 'Active People', 'Max Temperature', 'Min Temperature', 'Climate']
    df = pd.read_csv('output.csv', header=0, names=indexes, error_bad_lines=False)

    return df

# def plot_cumulative_state(df: pd.DataFrame, outfile: set):
#     fig.write_html(outfile, include_plotlyjs='cdn')


def visualize():
    # Rendering settings
    # pio.renderers.default = "browser"

    drive = prepare_drive_authentication()
    # Set data
    df = get_data(drive)
    print(df)
    # df = pd.DataFrame(content, columns=indexes)

    # TODO: get locs automatically
    locs = ['Nick Level 1 Fitness', 'Nick Level 2 Fitness', 'Nick Level 3 Fitness', 'Nick Power House', 'Nick Track', 'Nick Pool', 'Nick Courts 1 & 2', 'Nick Courts 3-6', 'Nick Courts 7 & 8', 'Shell Weight Machines', 'Shell Track', 'Shell Cardio Equipment']
    fig = go.Figure()
    colorscales = ['aggrnyl', 'agsunset', 'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'darkmint', 'electric', 'emrld', 'gnbu', 'greens', 'greys', 'hot', 'inferno', 'jet', 'magenta', 'magma', 'mint', 'orrd', 'oranges', 'oryel', 'peach', 'pinkyl', 'plasma', 'plotly3', 'pubu', 'pubugn', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdpu', 'redor', 'reds', 'sunset', 'sunsetdark', 'teal', 'tealgrn', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd', 'algae', 'amp', 'deep', 'dense', 'gray', 'haline', 'ice', 'matter', 'solar', 'speed', 'tempo', 'thermal', 'turbid', 'armyrose', 'brbg', 'earth', 'fall', 'geyser', 'prgn', 'piyg', 'picnic', 'portland', 'puor', 'rdgy', 'rdylbu', 'rdylgn', 'spectral', 'tealrose', 'temps', 'tropic', 'balance', 'curl', 'delta', 'edge', 'hsv', 'icefire', 'phase', 'twilight', 'mrybm', 'mygbm']
    random_color_num = np.random.randint(len(colorscales))

    j = 0
    buttons = []
    # Lined up along each locations
    for i, _loc in enumerate(locs):
        bool_list = df['Location'] == _loc

        date, loc, capacity, act_user, max_temp, min_temp, weather = df[bool_list]['date'], df[bool_list]['Location'], df[bool_list]['Total Capacity'], df[bool_list]['Active People'], df[bool_list]['Max Temperature'], df[bool_list]['Min Temperature'], df[bool_list]['Climate']

        # TODO: Calculate average active user and show below the figure

        # Create figures
        if i == 0:
            fig.add_trace(
                go.Scatter(
                    name='Active Muscles',
                    x=date,
                    y=act_user,
                    text=act_user,
                    hoverinfo='text',
                    mode='lines+markers',
                    marker={'color': act_user, 'colorscale': colorscales[random_color_num], 'showscale': True, 'colorbar': {'len': 0.8}}
                )
            )
            fig.add_trace(go.Scatter(x=date, y=capacity, name='Capacity'))
        buttons.append(dict(
            method='restyle',
            label=str(_loc),
            visible=True,
            args=[{'y':[act_user, capacity],
                    'x':[date],
                    'type': 'scatter'}],
            )
        )
        
        j += 1

    # Dropdown menus settings
    updatemenu = []
    custom_menu = dict()
    updatemenu.append(custom_menu)
    updatemenu[0]['buttons'] = buttons
    updatemenu[0]['direction'] = 'down'
    updatemenu[0]['showactive'] = True

    fig.update_layout(
        height=1000,
        width=1000,
        xaxis_rangeslider_visible=False,
        xaxis_rangeslider_thickness=0.1,
        updatemenus=updatemenu,
    )

    # Access to html file
    f_file = drive.CreateFile({'id': os.environ['FIGURE_HTML']})

    # Rendering
    f_html = pio.write_html(fig, file='figure.html')
    f_file.SetContentString(f_html)
    f_file.Upload()

if __name__ == "__main__":
    visualize()