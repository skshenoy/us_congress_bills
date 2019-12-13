import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

########### Define your variables
beers=['Chesapeake Stout', 'Snake Dog IPA', 'Imperial Porter', 'Double Dog IPA']
ibu_values=[35, 60, 85, 75]
abv_values=[5.4, 7.1, 9.2, 4.3]
color1='lightblue'
color2='darkgreen'
mytitle='Beer Comparison'
tabtitle='fml!'
myheading='DOES THIS ACTUALLY UPDATE'
label1='IBU'
label2='ABV'
githublink='https://github.com/skshenoy/us_congress_bills'

########### Set up the chart
bitterness = go.Bar(
    x=beers,
    y=ibu_values,
    name=label1,
    marker={'color':color1}
)
alcohol = go.Bar(
    x=beers,
    y=abv_values,
    name=label2,
    marker={'color':color2}
)

beer_data = [bitterness, alcohol]
beer_layout = go.Layout(
    barmode='group',
    title = mytitle
)

beer_fig = go.Figure(data=beer_data, layout=beer_layout)


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(children=[
    dcc.Markdown('### Hello! You\'ve reached my project app!'),
    dcc.Markdown('#### I got the idea when I found the dataset on ProPublica\'s website. This project is divided into three parts for now.'),
    html.A("For more detail into the project and my methodology, please check out my GitHub.",
        href=githublink,
        target="_blank",
        style={"size":20, "font-weight": "bold"}),
    html.Br(),
    dcc.Markdown('##### Part One: Legislator Insights'),
    dcc.Markdown("This part focuses on individual legislators and the bill-related activities they performed during a given term of Congress. Currently this information focuses mostly on their sponsorship and cosponsorship records. Next steps include pulling in voting records as well (probably using ProPublica’s Congress API). On top of that, I’m deciding how to incorporate and display other information, such as the leadership roles that a legislator may have held and any committees that they may have been appointed to."),
    html.Br(),
    html.A('Data Source', href=sourceurl),
    ]
)

if __name__ == '__main__':
    app.run_server()
