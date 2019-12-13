import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objs as go

import numpy as np
import pandas as pd
import joblib

# from sklearn.neighbors import KNeighborsClassifier

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='US Congress Deep Dive'

########### define stuff

app.layout = html.Div([
    dcc.Markdown('### Hello! You\'ve reached my project app!'),
    dcc.Markdown('#### I got the idea when I found the dataset on ProPublica\'s website. This project is divided into three parts for now.'),
    html.A("For more detail into the project and my methodology, please check out my GitHub.",
        href='https://github.com/skshenoy/us_congress_bills',
        target="_blank",
        style={"size":20, "font-weight": "bold"}),
    html.Br(),
    dcc.Markdown('##### Part One: Legislator Insights'),
    dcc.Markdown("This part focuses on individual legislators and the bill-related activities they performed during a given term of Congress. Currently this information focuses mostly on their sponsorship and cosponsorship records. Next steps include pulling in voting records as well (probably using ProPublica’s Congress API). On top of that, I’m deciding how to incorporate and display other information, such as the leadership roles that a legislator may have held and any committees that they may have been appointed to."),
    dcc.Link('Click here to look at legislators!', href="/page-1", style={"font-weight": "bold"}),
    html.Br(),
    html.Br(),
    dcc.Markdown('##### Part Two: Congressional Insights'),
    dcc.Markdown("This part is some descriptive information about the term of Congress and its bills overall (e.g., bills that received the most support, legislators who sponsored the largest number of bills, etc.). Currently this section is not interactive and simply displays some of the interesting facts I pulled out while conducting EDA on this dataset. This is where the most change will happen (hopefully) soon, because I’m planning to broaden my analysis and add in other Congresses as well. Near the bottom of this page I’ve detailed the future exploration and next steps I’d like to take."),
    dcc.Link('Click here to look at Congresses!', href='/page-2', style={"font-weight": "bold"}),
    html.Br(),
    html.Br(),
    dcc.Markdown('##### Part Three: Fun with Models'),
    dcc.Markdown("This is where I started playing around with machine learning techniques to see if I could predict whether a bill would pass. Again, there's a *lot* in this dataset so I experimented with which features to use, trying to determine if any had a significant correlation with whether a bill would pass. I used the bill’s official title (because I’m always interested in some NLP and I wanted to include that in this project), but I also worked with the breakdown of cosponsors, the sponsor’s party, the number of amendments, the number of related bills, and so on. This page is a fun little diversion where you can pretend to be a member of Congress, make up a bill, and then see what my model predicts would have happened to it."),
    dcc.Link('Click here to try passing a bill!', href='/page-3', style={"font-weight": "bold"}),
    dcc.Markdown('### Thanks for visiting!'),
],
style={'marginLeft': '5%', 'marginRight': '5%'})


if __name__ == '__main__':
    app.run_server()
