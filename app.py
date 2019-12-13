import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import os
port = int(os.environ.get('PORT', 5000))

import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier

########### Define your variables
tabtitle='US Congress Deep Dive'
githublink='https://github.com/skshenoy/us_congress_bills'

# HOME PAGE

index_layout = html.Div(children=[
    dcc.Markdown('### Hello???! You\'ve reached my project app!'),
    dcc.Markdown('#### I got the idea when I found the dataset on ProPublica\'s website. This project is divided into three parts for now.'),
    html.A("For more detail into the project and my methodology, please check out my GitHub.",
        href=githublink,
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
    ])

# PAGE TWO

house_one = "H.R.2519 - The American Legion 100th Anniversary Commemorative Coin Act (385; **passed**)"
house_two = "H.R.930 - Lymphedema Treatment Act (385; introduced)"
house_three = "H.R.820 - Childhood Cancer STAR Act (371; introduced)"
house_four = "H.R.299 - Blue Water Navy Vietnam Veterans Act of 2018 (330; passed House)"
house_five = "H.R.392 - Fairness for High-Skilled Immigrants Act of 2017 (329; introduced)"

senate_one = "S.2823 - Music Modernization Act (80; introduced)"
senate_two = "A resolution objecting to United Nations Security Council Resolution 2334 and to all efforts that undermine direct negotiations between Israel and the Palestinians for a secure and peaceful settlement. (78; introduced)"
senate_three = "Fix NICS Act of 2017 (77; introduced)"
senate_four = "S.1182 - National Flood Insurance Program Extension Act of 2018 (76; **passed**)"
senate_five = "S.Res.512 - A resolution designating the week of May 13 through May 19, 2018, as \"National Police Week\" (76; agreed to)"

page_2_layout = html.Div([
    dcc.Markdown('#### Please enjoy looking through some of my findings! [Or return home.](/)'),

    dcc.Markdown(
'''This page mainly contains basic information about a Congress's bills. Currently this page is not interactive and just displays some information I pulled out, but at the bottom I've gone into more detail about what I plan to do next with this section.'''
    ),
    html.Br(),

    dcc.Markdown('###### Most Supported Bills'),
    html.P("Here, 'support' is measured by number of cosponsors (the number in the parenthetical), displayed by the bill's official title. This was to get an idea for what kinds of legislation end up with broad, inherently-bipartisan support. The final status of the bill is also included in the parenthetical, and pulling out this data is when I started to realize that number of cosponsors might be nowhere near as strong a predictor for bill passage as I had initially thought. (Note: the Senate bills listed are excluding a number of unanimous or effectively-unanimous bills, mostly motions to recognize individuals who passed away. I excluded those from this table because that was not the kind of legislation I was interested in representing here.)"),

    dcc.Markdown(
f'''
House of Representatives | Senate
--- | ---
{house_one} | {senate_one}
{house_two} | {senate_two}
{house_three} | {senate_three}
{house_four} | {senate_four}
{house_five} | {senate_five}
'''
    ),
    html.Br(),

    dcc.Markdown('###### Who sponsored the most bills?'),
    html.P("This section is present because I got interested in which individuals spent the most time introducing and sponsoring legislation. The rate of passage listed here is calculated based on the number of the individual's sponsored bills that actually ended up being passed."),
    dcc.Markdown(
'''
Legislator | Number of Bills | Rate of Passage (%)
--- | ---
Senator Orrin Hatch (R) - UT | 125 | 0.032
Senator Charles Grassley (R) -  IA | 97 | 0.062
Senator Marco Rubio (R) -  FL | 92 | 0.022
Senator Amy Klobuchar (D) - MN | 92 | 0.033
Senator Benjamin Cardin (D) - MD | 87 | 0.0
'''
    ),
    html.Br(),

    dcc.Markdown('###### Who sponsored the fewest bills?'),
    html.P("On the flipside, I was also curious to see who was spending their time elsewhere (for example, in one of the following lists, members of leadership from both parties are present)."),
    dcc.Markdown(
'''**10 representatives and 1 senator who weren\'t in office for the full term sponsored none. The following served full terms and sponsored one bill each that did not pass:**

Representative Peter Visclosky (D) - IN-1

Representative Emanuel Cleaver (D) - MO-5

Representative Nancy Pelosi (D) - CA-12

Representative Trey Gowdy (R) - SC-4

Representative Paul Ryan (R) - SC-4

Representative Jim Jordan (R) - OH-4
'''
    ),
    html.Br(),

    dcc.Markdown('###### Who has the best passage rate?'),
    html.P("Then I got interested in seeing who has the 'best' or 'most successful' track record in terms of their bills getting passed. Three of these guys are from Texas! And they've all sponsored less than 15 bills each."),
    dcc.Markdown(
'''
District | Legislator | Number of Bills | Rate of Passage (%)
--- | --- | ---
TX-28 | Representative Henry Cuellar (D) | 9 | 0.333
TX-8 | Representative Kevin Brady (R) | 14 | 0.286
IL-12 | Representative Mike Bost (R) | 11 | 0.272
CT-1 | Representative John Larson (D) | 8 | 0.25
TX-13 | Representative Mac Thornberry (R) | 12 | 0.25
'''
    ),
    html.Br(),

    dcc.Markdown('###### Who has the worst passage rate?'),
    html.P("Again on the flipside, I was curious who either had bad luck or perhaps wasn't particularly effective at their job (if we oversimplified the entire legislative process all the way down to just who sponsored a bill)."),
    dcc.Markdown('**326 legislators who have sponsored at least 1 bill each (58.8% of them) have a passage rate of 0%.**'),
    html.Br(),

    dcc.Markdown('###### What about Austin\'s representatives?'),
    html.P("This is entirely just to humor myself and make it a little more personally relevant. Some of this is interesting stuff!"),
    dcc.Markdown(
'''
District | Legislator | Number of Bills | Rate of Passage (%)
--- | --- | --- | ---
TX-10 | Michael McCaul (R)  |33 | 0.091
TX-17 | Bill Flores (R)  | 12 | 0.0
TX-21 | Lamar Smith (R)  |13 | 0.077
TX-25 | Roger Williams (R)  | 14 | 0.0
TX-31 | John Carter (R)  | 8 | 0.125
TX-35 | Lloyd Doggett (D)  | 18 | 0.0
- | Senator John Cornyn (R) | 81 | 0.074
- | Senator Ted Cruz (R) | 66 | 0.015
'''
    ),
    html.Br(),

    dcc.Markdown('###### Graphs of overall bill passage will be updated here soon.'),
    html.Br(),

    dcc.Markdown('###### Next Steps'),
    dcc.Markdown(
"""Firstly, I need to clean up my EDA notebook further and port some of those graphs over into Dash and add them in here. After that though, my main plan is to add in other terms of Congress to see what the overall trends are. For example, the 115th Congress was a term where both chambers and the presidency were controlled by the same party (although it was also described by some as ‘very unproductive’ despite this fact). I’m *very* interested in comparing this with other possible scenarios (split legislative control, legislative and presidency controlled by different parties, etc., for each major party) to see patterns in performance, especially over time.

I’m also interested in looking at levels of bipartisanship and how they may have changed over time. For my purposes, I’m thinking of the concept of ‘bipartisanship’ as shared or mutual support for a bill, but I’m still working on defining an actual metric for it (I’m thinking maybe polarity as the inverse, where bill support is severely skewed to one party or the other? Or perhaps ratios of support per party).
"""),

    html.Br(),
    html.Br(),
    dcc.Link('Click here to look at legislators!', href="/page-1"),
    html.Br(),
    dcc.Link('Click here to try to pass a bill!', href="/page-3"),
    html.Br(),
    dcc.Link('Click here to return to the home page.', href="/", style={"font-weight": "bold"}),
])

# PAGE THREE

df = pd.read_csv('./assets/data/bills_and_support.csv').dropna()
available_subjects = df['subjects_top_term'].unique()

bill_text = pd.read_csv('./assets/data/bill_title_text_for_model.csv')
title_text_knn = joblib.load('./assets/knn_text_model.joblib')

page_3_layout = html.Div([
    dcc.Markdown('''#### Please make up a bill! [Or return home.](/)'''),
    dcc.Markdown(
"""This is where you can have some fun and see what my pre-trained model thinks of the bill you’re about to make up. For simplicity’s sake, this will look at whether your bill would pass the chamber you introduce it in, based on: the chamber; the bill’s subject; which party you’re from; how many cosponsors you have from each party; and the bill’s title.

Unlike other interactive components on this app that update near-instantaneously, the output for this will take a few seconds to run and display. This is due to the fact that, although the predictive model has already been trained and here is only predicting based on your input, another model is being re-trained with every submission — under the predicted outcome, you will also be able to see other bills that supposedly have similar titles to the one you entered. You’ll also be able to see if those bills passed.
"""),

    html.Br(),
    html.P('Select which Congress you would like to be in:'),
    dcc.Dropdown(
        id='congress-term',
        options=[{'label': 115, 'value': 115}], # currently no other choice, suckers
        value=115
    ),

    html.Br(),
    html.P('Select the most important subject for this bill:'),
    dcc.Dropdown(
            id='submitted-bill-subject',
            options=[{'label': i, 'value': i} for i in available_subjects]
    ),

    html.Br(),
    html.P('Which chamber are you in?'),
    dcc.RadioItems(
        id='chamber-radio',
        options=[
            {'label': 'House of Representatives', 'value': 'house'},
            {'label': 'Senate', 'value': 'senate'}
        ],
        value='senate',
        labelStyle={'display': 'inline-block', 'margin-right':'2%'}
    ),

    html.Br(),
    html.P('Which party are you in?'),
    dcc.RadioItems(
        id='sponsor-party-radio',
        options=[
            {'label': 'Democrat', 'value': 'Democrat'},
            {'label': 'Republican', 'value': 'Republican'},
            {'label': 'Independent', 'value': 'Independent'}
        ],
        labelStyle={'display': 'inline-block', 'margin-right':'2%'}
    ),

    html.Br(),
    html.P('How many Democrats are cosponsoring your bill?'),
    html.Div(
        dcc.Slider(
            id='num-democrats-cosponsoring',
            min=0,
            max=48,
            step=1,
            marks={i: str(i) for i in range(1, 49, 2)},
            value=0),
        style={'width': '60%','display': 'inline-block'}
    ),

    html.Br(),
    html.Br(),
    html.P('How many Republicans are cosponsoring your bill?'),
    html.Div(
        dcc.Slider(
            id='num-republicans-cosponsoring',
            min=0,
            max=55,
            marks={i: str(i) for i in range(1, 56, 2)},
            value=0),
        style={'width': '60%','display': 'inline-block'}
        ),

    html.Br(),
    html.Br(),
    html.P('How many Independents are cosponsoring your bill?'),
    html.Div(
        dcc.Slider(
            id='num-independents-cosponsoring',
            min=0,
            max=2,
            marks={i: str(i) for i in range(1, 3)},
            value=0),
        style={'width': '60%','display': 'inline-block'}
        ),

    html.Br(),
    html.Br(),
    html.Div([
        html.Div(
            id='output-container-button',
            children='Make up a title and click submit!'),
        dcc.Input(
            id='submitted-bill-title',
            type='text'),
        html.Button('Submit',
            id='title-submit-button')
        ]
    ),

    html.Br(),
    html.Br(),

    html.Div(
        id='overall-output'
    ),

    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Link('Click here to look at legislators!', href="/page-1"),
    html.Br(),
    dcc.Link('Click here to look at terms of Congress!', href="/page-2"),
    html.Br(),
    dcc.Link('Click here to return to the home page.', href="/", style={"font-weight": "bold"}),
])





########### Set up the chart
# no


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

app.config.suppress_callback_exceptions = True

########### Set up the layout

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

############# ALL CALLBACKS UNDER HERE I GUESS

# navigating around

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    # return index_layout
    if pathname == '/page-2':
        return page_2_layout
    # elif pathname == '/page-2':
    #     return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    else:
        return index_layout
    # # You could also return a 404 "URL not found" page here


# page 2 has no callbacks right now

# page 3

@app.callback([Output('num-republicans-cosponsoring', 'max'),
             Output('num-republicans-cosponsoring', 'marks'),
             Output('num-republicans-cosponsoring', 'style')],
            [Input('chamber-radio', 'value')])
def update_cosponsor_options(chamber):
    if chamber == 'senate':
        return 55, {i: str(i) for i in range(1, 56, 2)}, {'width': '60%','display': 'inline-block'}
    else:
        return 250, {i: str(i) for i in range(1, 251, 8)}, {'width': '92%','display': 'inline-block'}

@app.callback([Output('num-democrats-cosponsoring', 'max'),
             Output('num-democrats-cosponsoring', 'marks'),
             Output('num-democrats-cosponsoring', 'style')],
            [Input('chamber-radio', 'value')])
def update_cosponsor_options(chamber):
    if chamber == 'senate':
        return 48, {i: str(i) for i in range(1, 49, 2)}, {'width': '60%','display': 'inline-block'}
    else:
        return 200, {i: str(i) for i in range(1, 201, 7)}, {'width': '85%','display': 'inline-block'}

@app.callback([Output('num-independents-cosponsoring', 'max'),
             Output('num-independents-cosponsoring', 'marks'),
             Output('num-independents-cosponsoring', 'style')],
            [Input('chamber-radio', 'value')])
def update_cosponsor_options(chamber):
    if chamber == 'senate':
        return 2, {i: str(i) for i in range(1, 3)}, {'width': '60%','display': 'inline-block'}
    else:
        return 0, {0: str(0)}, {'width': '0%','display': 'inline-block'}

@app.callback(Output('output-container-button', 'children'),
    [Input('title-submit-button', 'n_clicks')])
def update_output(n_clicks):
    if n_clicks == None:
        return 'Make up a title and click submit!'
    else:
        return 'Your bill has been submitted! Let\'s see if it passes!'

@app.callback(Output('overall-output', 'children'),
    [Input('submitted-bill-title', 'value'),
     Input('title-submit-button', 'n_clicks'),
     Input('num-democrats-cosponsoring', 'value'),
     Input('num-republicans-cosponsoring', 'value')])
def predict_and_tell(incoming_title, submitted_yet, dems, repubs):
    if submitted_yet != None:
        the_df = pd.concat([bill_text, pd.DataFrame([{'bill_id':'input_bill', 'titles_text':incoming_title, 'enacted_as':0}])])

        # vectorizer = CountVectorizer()
        # X = vectorizer.fit_transform(the_df['titles_text'])
        # real_X = pd.DataFrame(X.todense(), index=the_df['bill_id'])
        #
        # knn_mess = KNeighborsClassifier(6)
        # knn_mess.fit(real_X, the_df['enacted_as'])
        # my_bill = real_X.loc[real_X.index == 'input_bill']
        # indices = knn_mess.kneighbors(my_bill, return_distance=False)[0]
        #
        # output = []
        # for x in real_X.iloc[indices,:].iloc[1:].index:
        #     curr_bill = bill_text.loc[bill_text['bill_id'] == x]
        #     if curr_bill['enacted_as'].values[0] == 1:
        #         output.append(f"- {x}: {curr_bill['titles_text'].values[0]} Passed.")
        #     else:
        #         output.append(f"- {x}: {curr_bill['titles_text'].values[0]} Did not pass.")

        prediction = title_text_knn.predict(incoming_title)

        if prediction == 1:
            pred = '**Congratulations, your bill passed!**'
        else:
            pred = '**Unfortunately, your bill did not pass. Sorry about that.**'

        return [
            dcc.Markdown(pred),

#             html.Br(),
#
#             dcc.Markdown(
# f'''###### Here are some bills with similar titles to yours:
# > **{output[0]}**
#
# > **{output[1]}**
#
# > **{output[2]}**
#
# > **{output[3]}**
#
# > **{output[4]}**'''
)]

if __name__ == '__main__':
    app.run_server()
