import os
import pandas as pd
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

def get_data():
    '''
    Get csv data from google drive
    '''
    # Set google drive authentication
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

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

    # Set data
    df = get_data()
    print(df)
    # df = pd.DataFrame(content, columns=indexes)

    # TODO: get locs automatically
    locs = ['Nick Level 1 Fitness', 'Nick Level 2 Fitness', 'Nick Level 3 Fitness', 'Nick Power House', 'Nick Track', 'Nick Pool', 'Nick Courts 1 & 2', 'Nick Courts 3-6', 'Nick Courts 7 & 8', 'Shell Weight Machines', 'Shell Track', 'Shell Cardio Equipment']
    fig = make_subplots(rows=4, cols=3, subplot_titles=(locs))

    # Lined up along each locations
    for loc in locs:
        bool_list = df['Location'] == loc

        date, loc, capacity, act_user, max_temp, min_temp, weather = df[bool_list]['date'], df[bool_list]['Location'], df[bool_list]['Total Capacity'], df[bool_list]['Active People'], df[bool_list]['Max Temperature'], df[bool_list]['Min Temperature'], df[bool_list]['Climate']

        # Calculate average active user?

        # Create figures
        # fig.add_trace(go.Scatter(x=date, y=capacity, fillcolor='red', name='Capacity'))
        fig.add_trace(go.Scatter(x=date, y=act_user, name='{} - Active Muscles'.format(loc)))

        fig.update_layout(autosize=False, height=400, width=400, title_text='Location - Active Muscles')

    # Rendering
    # fig.show(renderer="svg")
    # fig.show()
    pio.write_html(fig, file='docs/figure.html', auto_open=True)


if __name__ == "__main__":
    visualize()