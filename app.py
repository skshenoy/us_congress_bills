import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import os
port = int(os.environ.get('PORT', 5000))

import pandas as pd
import numpy as np
import sklearn
import joblib

########### Define your variables
tabtitle='US Congress Deep Dive'
githublink='https://github.com/skshenoy/us_congress_bills'

# HOME PAGE

index_layout = html.Div(children=[
    dcc.Markdown('#### Hello, you\'ve reached my project app!'),
    dcc.Markdown('##### I got the idea for this side project after findding the dataset on ProPublica\'s website. This project is divided into three parts for now. The goal of this project is for more practice with data manipulation and presentation, as opposed to a more rigorous analysis of Congressional activity itself. The analysis here is somewhat basic and oversimplifies the legislative process.'),
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
    dcc.Markdown('#### Thanks for checking this out!'),
    ])

# PAGE ONE

congress_reps_df = pd.read_csv('./assets/data/all_congress_reps.csv')
overall_sponsorship_df = pd.read_csv('./assets/data/overall_sponsorship_aggs.csv')
spons_by_subj_df = pd.read_csv('./assets/data/sponsorship_by_subj_agg.csv')
cosponsorship_info = pd.read_csv('./assets/data/cosponsorship_summary_info.csv')
bill_summary_info = pd.read_csv('./assets/data/bills_and_passage_subject_and_type.csv')

def get_summary(bioguide_id):
    leg_vals = overall_sponsorship_df.loc[overall_sponsorship_df['bioguide_id'] == bioguide_id].values[0]
    if leg_vals[3] == 'rep':
        if leg_vals[5] == '0':
            line1 = 'Representative ' + leg_vals[1] + ', ' + leg_vals[6] + ' from ' + leg_vals[4] + ' (at-large district)'
        else:
            line1 = 'Representative ' + leg_vals[1] + ', ' + leg_vals[6] + ' from ' + leg_vals[4] + '-' + leg_vals[5]
    else:
        line1 = 'Senator ' + leg_vals[1] + ', ' + leg_vals[6] + ' from ' + leg_vals[4]

    line2 = '    - ' + 'started term on ' + leg_vals[7] + ', ended term on ' + leg_vals[8] + f' (in office for {leg_vals[9]} days)'
    if leg_vals[10] == 0:
        line3 = '    - ' + 'sponsored ' + str(leg_vals[10]) + ' bills'
    elif leg_vals[10] == 1:
        line3 = '    - ' + 'sponsored ' + str(leg_vals[10]) + ' bill with an overall rate of passage of ' + str(np.round(leg_vals[11], 3))
    else:
        line3 = '    - ' + 'sponsored ' + str(leg_vals[10]) + ' bills with an overall rate of passage of ' + str(np.round(leg_vals[11], 3))
    return [line1, line2, line3]

def fix_string_list(cell):
    real = []
    for b in cell.split():
        real.append(b.replace('[', '').replace(']', '').replace('\'', '').replace(',', ''))
    return real

def get_cosponsorship_summary(leg_id):
    cospon_summary = []
    leg = cosponsorship_info.loc[cosponsorship_info['cosponsors'] == leg_id]
    leg_cospons = fix_string_list(leg['bills'].values[0])
    leg_bills = bill_summary_info.loc[bill_summary_info['bill_id'].isin(leg_cospons)]
    cospon_summary.append(f"    - cosponsored {leg['num_bills_cosponsored'].values[0]} bills with an overall rate of passage of {np.round(leg_bills['enacted_as'].mean(), 3)}")
    leg_agg = leg_bills.groupby('subjects_top_term').agg(num_bills=('bill_id', 'size'), pass_rate=('enacted_as', 'mean')).reset_index()
    for subj in leg_agg.values:
        line = f'        - {subj[1]} {subj[0]} bills with a rate of passage of {subj[2]}'
        cospon_summary.append(line)
    return cospon_summary

page_1_layout = html.Div([
    dcc.Markdown('#### Please select a legislator! [Or return home.](/)'),

    dcc.Markdown(
'''This page focuses on individual legislators and their bill-related activities. (You don't need to change the values for any of the first three dropdowns; they're only present to make your search easier and narrow the possible legislators down.)

Once you select an individual, you will be able to see their record in more detail and also find other legislators with similar records.'''
    ),

    html.Div(
        html.P('Congress:'),
        style={'width': '37%', 'display': 'inline-block'},
    ),

    html.Div(
        html.P('Chamber:'),
        style={'width': '37%', 'display': 'inline-block'},
    ),

    html.Div(
        html.P('State:'),
        style={'width': '20%', 'display': 'inline-block'},
    ),

    dcc.Dropdown(
        id='congress-num-dropdown',
        style={'height': '30px', 'width': '37%', 'display': 'inline-block'},
        # options= [{'label': i, 'value': i} for i in df['congress_num'].unique()],
        # CURRENTLY HARDCODING IT IN TO BE 115 BECAUSE THAT'S THE ONLY ONE I HAVE
        # AND I CBF TO FIX THE LABELING RN
        options= [{'label': '115th (Jan 2017 - Jan 2019)', 'value': 115}],
        value=115
    ),

    dcc.Dropdown(
        id='chamber-dropdown',
        style={'height': '30px', 'width': '37%', 'display': 'inline-block'},
        options=[{'label': i, 'value': i} for i in ['Senate', 'House of Representatives', 'Both']],
        value='Both'
    ),

    dcc.Dropdown(
        id='state-dropdown',
        style={'height': '30px', 'width': '20%', 'display': 'inline-block'},
        options=[{'label': i, 'value': i} for i in congress_reps_df['state'].sort_values().unique()] + [{'label': 'All', 'value': 'All'}],
        value='All'
    ),

    html.P('Legislator:'),

    dcc.Dropdown(
        id='legislator-dropdown',
        options=[{'label': i, 'value': congress_reps_df.loc[congress_reps_df['name'] == i]['bioguide_id'].values[0]} for i in congress_reps_df['name'].unique()],
        value='Select...'
    ),

    html.Div(
        id='legislator-output'
    ),

    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Link('Click here to look at terms of Congress!', href="/page-2"),
    html.Br(),
    dcc.Link('Click here to try to pass a bill!', href="/page-3"),
    html.Br(),
    dcc.Link('Click here to return to the home page.', href="/", style={"font-weight": "bold"}),
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
"""This is where you can have some fun and see what my pre-trained model thinks of the bill you’re about to make up. For simplicity’s sake, this will look at whether your bill would pass the chamber you introduce it in, based on: the chamber; the bill’s subject; which party you’re from; how many cosponsors you have from each party; and the bill’s title."""),

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

# home page/navigating around

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    else:
        return index_layout
    # # You could also return a 404 "URL not found" page here

# page 1

@app.callback(
    Output('legislator-dropdown', 'options'),
    [Input('congress-num-dropdown', 'value'),
    Input('chamber-dropdown', 'value'),
    Input('state-dropdown', 'value')])
def set_legislator_choices_options(congress_num, chamber, state):
    # removing this for now because i'm just hardcoding the 115
    # dff = df.loc[df['congress_num'] == congress_num]
    dff = congress_reps_df
    if chamber != 'Both':
        if chamber == 'Senate':
            dff = dff.loc[dff['type'] == 'sen']
        else:
            dff = dff.loc[dff['type'] == 'rep']
    if state != 'All':
        dff = dff.loc[dff['state'] == state]

    return [{'label': i, 'value': dff.loc[dff['name'] == i]['bioguide_id'].values[0]} for i in dff['name'].unique()]

@app.callback(
    Output('legislator-output', 'children'),
    [Input('legislator-dropdown', 'value')])
def set_display_children(leg_id):
    if leg_id != 'Select...':
        return [html.Br(),
            dcc.Tabs(
                id="tabs-options",
                value='tab-1-summary',
                children=[
                    dcc.Tab(id='tab-1', label='Legislator Summary', value='tab-1-summary'),
                    dcc.Tab(id='tab-2', label='Similar Legislators', value='tab-2-similar-legs')]
                )]
    else:
        return ''

@app.callback(
    Output('tab-1', 'children'),
    [Input('tabs-options', 'value'),
     Input('legislator-dropdown', 'value')])
def make_deep_dive_chart(tab, leg_id):
    if tab == 'tab-1-summary':
        summary = get_summary(leg_id)
        output = f'##### {summary[0]}\n'
        output += f'> **{summary[1]}**\n\n'
        output += f'> **{summary[2]}**\n\n'

        # cospons_summary = get_cosponsorship_summary(leg_id)
        # output += f'> ** {cospons_summary[0]}**\n\n'
        # for subj in cospons_summary[1:]:
        #     output += f'> {subj}' +'\n\n'

        dff = spons_by_subj_df.loc[spons_by_subj_df['bioguide_id'] == leg_id]
        return html.Div([
                dcc.Markdown(output),
                html.Br(),
                html.P('Choose a subject to look at more closely.'),
                dcc.Dropdown(
                    id='legislator-subject-dropdown',
                    style={'height': '30px', 'width': '80%'},
                    options=[{'label': i, 'value': i} for i in dff['subjects_top_term'].unique()] + [{'label': 'All', 'value': 'All'}],
                    value='All'
                ),
                html.Br(),
                dcc.Graph(id='legislator-deep-dive')
            ])

@app.callback(
    Output('legislator-deep-dive', 'figure'),
    [Input('legislator-dropdown', 'value'),
     Input('legislator-subject-dropdown', 'value')]
)
def render_graph(leg_id, subj):
    dff = spons_by_subj_df.loc[spons_by_subj_df['bioguide_id'] == leg_id]
    if dff['by_subj_bills_sponsored'].values[0] == 'not applicable':
        return {'data': [], 'layout': go.Layout(title='No Sponsored Bills')}

    if subj == 'All':
        trace = go.Bar(x=dff['subjects_top_term'], y=dff['by_subj_bills_sponsored'],
                        hovertext='Passage Rate: ' + dff['by_subj_pass_rate'], hoverinfo="text",
                        # marker=dict(color=color.tolist())
        )
        layout = go.Layout(title='Bills Sponsored By Subject',
                            colorway=["#EF963B", "#EF533B"],# hovermode="closest",
                            xaxis={'title': "Subject", 'titlefont': {'color': 'black', 'size': 14},
                                   'tickfont': {'size': 9, 'color': 'black'}},
                            yaxis={'title': "Number of bills", 'titlefont': {'color': 'black', 'size': 14, },
                                   'tickfont': {'color': 'black'}})
    else:
        dff = dff.loc[dff['subjects_top_term'] == subj]
        trace = go.Bar(x=[subj], y=dff['by_subj_pass_rate'])
        layout = go.Layout(title=f'Rate of Passage for Sponsored {subj} Bills',
                            colorway=["#EF963B", "#EF533B"],# hovermode="closest",
                            xaxis={'title': "Subject", 'titlefont': {'color': 'black', 'size': 14},
                                   'tickfont': {'size': 12, 'color': 'black'}},
                            yaxis={'title': "Rate of Passage", 'titlefont': {'color': 'black', 'size': 14, },
                                   'tickfont': {'color': 'black'}})
    return {
        'data':[trace],
        'layout':layout
    }

@app.callback(
    Output('tab-2', 'children'),
    [Input('tabs-options', 'value')])
def render_tab_one(tab):
    if tab == 'tab-2-similar-legs':
        return html.Div([
            html.H5('Find legislators with similar records of cosponsorship.'),
            html.Br(),
            dcc.RadioItems(
                id='legislators-knn-radio',
                options=[
                    {'label': '5 most similar', 'value': 5},
                    {'label': '10 most similar', 'value': 10},
                    {'label': '15 most similar', 'value': 15}
                ],
                value=5,
                labelStyle={'display': 'inline-block', 'margin-right':'12%'}
            ),
            html.Br(),
            html.Div(id='legislators-knn-output')
        ])

@app.callback(
    Output('legislators-knn-output', 'children'),
    [Input('legislator-dropdown', 'value'),
     Input('legislators-knn-radio', 'value')])
def set_display_neighbors(leg_id, knn_num):
    # similar_legs = get_similar_legs(leg_id, knn_num)
    # output = '###### Legislators with similar records:\n'
    # for leg in similar_legs:
    #     output += f'> ** {leg[0]}**' +'\n\n'
    # return dcc.Markdown(output)
    return dcc.Markdown("**Currently refactoring due to filesize limitations.**")

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
        prediction = title_text_knn.predict(pd.Series([incoming_title]))

        if prediction == 1:
            pred = '**Congratulations, your bill passed!**'
        else:
            pred = '**Unfortunately, your bill did not pass. Sorry about that.**'

        return dcc.Markdown(pred)

if __name__ == '__main__':
    app.run_server()
