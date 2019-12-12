import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc

import numpy as np
import pandas as pd
import joblib

from sklearn.neighbors import KNeighborsClassifier

pd.set_option('max_columns', 100)

import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# congress_reps_df = pd.read_csv('~/Documents/Portfolio/congress-work/data/clean/ALL_CONGRESS_REPS.csv')
# overall_sponsorship_df = pd.read_csv('~/Documents/Portfolio/congress-work/data/clean/overall_sponsorship_aggs.csv')
# spons_by_subj_df = pd.read_csv('~/Documents/Portfolio/congress-work/data/clean/sponsorship_by_subj_agg.csv')
# cosponsorship_info = pd.read_csv('~/Documents/Portfolio/congress-work/data/clean/cosponsorship_summary_info.csv')
# bill_summary_info = pd.read_csv('~/Documents/Portfolio/congress-work/data/clean/bills_and_passage_subject_and_type.csv')
# leg_knn_info = pd.read_csv('~/Documents/Portfolio/congress-work/data/clean/leg_knn_info.csv').set_index('cosponsors')
# # # leg_knn = joblib.load('~/Documents/Portfolio/congress-work/assets/similar_legs_knn.joblib')/
# leg_knn = joblib.load('./assets/similar_legs_knn.joblib')
#
# def get_summary(bioguide_id):
#     leg_vals = overall_sponsorship_df.loc[overall_sponsorship_df['bioguide_id'] == bioguide_id].values[0]
#     if leg_vals[3] == 'rep':
#         if leg_vals[5] == '0':
#             line1 = 'Representative ' + leg_vals[1] + ', ' + leg_vals[6] + ' from ' + leg_vals[4] + ' (at-large district)'
#         else:
#             line1 = 'Representative ' + leg_vals[1] + ', ' + leg_vals[6] + ' from ' + leg_vals[4] + '-' + leg_vals[5]
#     else:
#         line1 = 'Senator ' + leg_vals[1] + ', ' + leg_vals[6] + ' from ' + leg_vals[4]
#
#     line2 = '    - ' + 'started term on ' + leg_vals[7] + ', ended term on ' + leg_vals[8] + f' (in office for {leg_vals[9]} days)'
#     if leg_vals[10] == 0:
#         line3 = '    - ' + 'sponsored ' + str(leg_vals[10]) + ' bills'
#     elif leg_vals[10] == 1:
#         line3 = '    - ' + 'sponsored ' + str(leg_vals[10]) + ' bill with an overall rate of passage of ' + str(np.round(leg_vals[11], 3))
#     else:
#         line3 = '    - ' + 'sponsored ' + str(leg_vals[10]) + ' bills with an overall rate of passage of ' + str(np.round(leg_vals[11], 3))
#     return [line1, line2, line3]
#
# def fix_string_list(cell):
#     real = []
#     for b in cell.split():
#         real.append(b.replace('[', '').replace(']', '').replace('\'', '').replace(',', ''))
#     return real
#
# def get_cosponsorship_summary(leg_id):
#     cospon_summary = []
#     leg = cosponsorship_info.loc[cosponsorship_info['cosponsors'] == leg_id]
#     leg_cospons = fix_string_list(leg['bills'].values[0])
#     leg_bills = bill_summary_info.loc[bill_summary_info['bill_id'].isin(leg_cospons)]
#     cospon_summary.append(f"    - cosponsored {leg['num_bills_cosponsored'].values[0]} bills with an overall rate of passage of {np.round(leg_bills['enacted_as'].mean(), 3)}")
#     leg_agg = leg_bills.groupby('subjects_top_term').agg(
#         num_bills=('bill_id', 'size'), pass_rate=('enacted_as', 'mean')).reset_index()
#     for subj in leg_agg.values:
#         line = f'        - {subj[1]} {subj[0]} bills with a rate of passage of {subj[2]}'
#         cospon_summary.append(line)
#     return cospon_summary
#
# def get_similar_legs(leg_id, n):
#     one_leg = leg_knn_info.loc[leg_knn_info.index == leg_id]
#     indices = leg_knn.kneighbors(one_leg, return_distance=False)[0]
#     neighbors = leg_knn_info.iloc[indices,:].iloc[1:].index.values
#     summaries = []
#     for n in neighbors[:n]:
#         n_sum = get_summary(n)
#         summaries.append(n_sum)
#     return summaries

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Markdown('''
    #### Please select a legislator! [Or check out predicting stuff!](www.google.com)
    '''),

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

    # dcc.Dropdown(
    #     id='state-dropdown',
    #     style={'height': '30px', 'width': '20%', 'display': 'inline-block'},
    #     options=[{'label': i, 'value': i} for i in congress_reps_df['state'].sort_values().unique()] + [{'label': 'All', 'value': 'All'}],
    #     value='All'
    # ),
    #
    # html.P('Legislator:'),
    #
    # dcc.Dropdown(
    #     id='legislator-dropdown',
    #     options=[{'label': i, 'value': congress_reps_df.loc[congress_reps_df['name'] == i]['bioguide_id'].values[0]} for i in congress_reps_df['name'].unique()],
    #     value='Select...'
    # ),

    html.Div(
        id='legislator-output'
    )
])

# @app.callback(
#     Output('legislator-dropdown', 'options'),
#     [Input('congress-num-dropdown', 'value'),
#     Input('chamber-dropdown', 'value'),
#     Input('state-dropdown', 'value')])
# def set_legislator_choices_options(congress_num, chamber, state):
#     # removing this for now because i'm just hardcoding the 115
#     # dff = df.loc[df['congress_num'] == congress_num]
#     dff = congress_reps_df
#     if chamber != 'Both':
#         if chamber == 'Senate':
#             dff = dff.loc[dff['type'] == 'sen']
#         else:
#             dff = dff.loc[dff['type'] == 'rep']
#     if state != 'All':
#         dff = dff.loc[dff['state'] == state]
#
#     return [{'label': i, 'value': dff.loc[dff['name'] == i]['bioguide_id'].values[0]} for i in dff['name'].unique()]
#
# @app.callback(
#     Output('legislator-output', 'children'),
#     [Input('legislator-dropdown', 'value')])
# def set_display_children(leg_id):
#     if leg_id != 'Select...':
#         return [html.Br(),
#             dcc.Tabs(
#                 id="tabs-options",
#                 value='tab-1-summary',
#                 children=[
#                     dcc.Tab(id='tab-1', label='Legislator Summary', value='tab-1-summary'),
#                     dcc.Tab(id='tab-2', label='Similar Legislators', value='tab-2-similar-legs')]
#                 )]
#     else:
#         return ''
#
# @app.callback(
#     Output('tab-1', 'children'),
#     [Input('tabs-options', 'value'),
#      Input('legislator-dropdown', 'value')])
# def make_deep_dive_chart(tab, leg_id):
#     if tab == 'tab-1-summary':
#         summary = get_summary(leg_id)
#         output = f'##### {summary[0]}\n'
#         output += f'> **{summary[1]}**\n\n'
#         output += f'> **{summary[2]}**\n\n'
#
#         cospons_summary = get_cosponsorship_summary(leg_id)
#         output += f'> ** {cospons_summary[0]}**\n\n'
#         # for subj in cospons_summary[1:]:
#         #     output += f'> {subj}' +'\n\n'
#
#         dff = spons_by_subj_df.loc[spons_by_subj_df['bioguide_id'] == leg_id]
#         return html.Div([
#                 dcc.Markdown(output),
#                 html.Br(),
#                 html.P('Choose a subject to look at more closely.'),
#                 dcc.Dropdown(
#                     id='legislator-subject-dropdown',
#                     style={'height': '30px', 'width': '80%'},
#                     options=[{'label': i, 'value': i} for i in dff['subjects_top_term'].unique()] + [{'label': 'All', 'value': 'All'}],
#                     value='All'
#                 ),
#                 html.Br(),
#                 dcc.Graph(id='legislator-deep-dive')
#             ])
#
# @app.callback(
#     Output('legislator-deep-dive', 'figure'),
#     [Input('legislator-dropdown', 'value'),
#      Input('legislator-subject-dropdown', 'value')]
# )
# def render_graph(leg_id, subj):
#     if subj == 'All':
#         trace = go.Bar(x=list(range(10)), y=list(range(10)))
#         layout = go.Layout(title=f'{subj} NOT HAPPENING YET')
#         return {
#             'data':[trace],
#             'layout':layout
#         }
#     else:
#         trace = go.Bar(x=list(range(10)), y=list(range(10)))
#         layout = go.Layout(title=f'{subj} NOT HAPPENING YET')
#         return {
#             'data':[trace],
#             'layout':layout
#         }
#
# # EVERYTHING HERE SHOULD BE IN THE GRAPH CALLBACK
# # Input('legislator-deep-dive-subject', 'value')])
#         # dff = spons_by_subj_df.loc[spons_by_subj_df['bioguide_id'] == leg_id]
#         # if dff['by_subj_bills_sponsored'].values[0] == 'not applicable':
#         #     return {'data': [], 'layout': go.Layout(title='No Sponsored Bills')}
#         #
#         # if 'All' == 'All': # was 'subj'
#         #     trace = go.Bar(x=dff['subjects_top_term'], y=dff['by_subj_bills_sponsored'],
#         #                     hovertext='Passage Rate: ' + dff['by_subj_pass_rate'], hoverinfo="text",
#         #                     # marker=dict(color=color.tolist())
#         #     )
#         #     layout = go.Layout(title='Bills Sponsored By Subject',
#         #                         colorway=["#EF963B", "#EF533B"],# hovermode="closest",
#         #                         xaxis={'title': "Subject", 'titlefont': {'color': 'black', 'size': 14},
#         #                                'tickfont': {'size': 9, 'color': 'black'}},
#         #                         yaxis={'title': "Number of bills", 'titlefont': {'color': 'black', 'size': 14, },
#         #                                'tickfont': {'color': 'black'}})
#         # else:
#         #     dff = dff.loc[dff['subjects_top_term'] == subj]
#         #     trace = go.Bar(x=[subj], y=dff['by_subj_pass_rate'])
#         #     layout = go.Layout(title=f'Rate of Passage for Sponsored {subj} Bills',
#         #                         colorway=["#EF963B", "#EF533B"],# hovermode="closest",
#         #                         xaxis={'title': "Subject", 'titlefont': {'color': 'black', 'size': 14},
#         #                                'tickfont': {'size': 12, 'color': 'black'}},
#         #                         yaxis={'title': "Rate of Passage", 'titlefont': {'color': 'black', 'size': 14, },
#         #                                'tickfont': {'color': 'black'}})
#
#         # return {
#         #     'data':[trace],
#         #     'layout':layout
#         # }
#
#     # dff = df[(df[selected_product1] >= 2) & (df[selected_product2] >= 2)]
#     # trace1 = go.Bar(x=dff['state'], y=dff[selected_product1], name=selected_product1.title(), )
#     # trace2 = go.Bar(x=dff['state'], y=dff[selected_product2], name=selected_product2.title(), )
#
#     # return {
#     #     'data': [trace1, trace2],
#     #     'layout': go.Layout(title=f'State vs Export: {selected_product1.title()}, {selected_product2.title()}',
#     #                         colorway=["#EF963B", "#EF533B"], hovermode="closest",
#     #                         xaxis={'title': "State", 'titlefont': {'color': 'black', 'size': 14},
#     #                                'tickfont': {'size': 9, 'color': 'black'}},
#     #                         yaxis={'title': "Export price (million USD)", 'titlefont': {'color': 'black', 'size': 14, },
#     #                                'tickfont': {'color': 'black'}})}
#
#     # layout = #define layout
#     # figure = go.Figure(data=[trace], layout=layout)
#     # retrun figure
#
# @app.callback(
#     Output('tab-2', 'children'),
#     [Input('tabs-options', 'value')])
# def render_tab_one(tab):
#     if tab == 'tab-2-similar-legs':
#         # what should go here:
#         # - the checkboxes for sponsorship/voting
#         # - the knn radio
#         # - a space for the knn output
#         return html.Div([
#             html.H5('Find legislators with similar records of cosponsorship.'),
#             dcc.Checklist(
#                 id='legislators-knn-checklist',
#                 options=[
#                     {'label': 'by cosponsorship', 'value': 'by cosponsorship'},
#                     {'label': 'by voting record', 'value': 'by voting record'}
#                 ],
#                 value=['by cosponsorship', 'by voting record'],
#                 labelStyle={'display': 'inline-block', 'margin-right':'12%'}
#             ),
#             html.Br(),
#             dcc.RadioItems(
#                 id='legislators-knn-radio',
#                 options=[
#                     {'label': '5 most similar', 'value': 5},
#                     {'label': '10 most similar', 'value': 10},
#                     {'label': '15 most similar', 'value': 15}
#                 ],
#                 value=5,
#                 labelStyle={'display': 'inline-block', 'margin-right':'12%'}
#             ),
#             html.Br(),
#             html.Div(id='legislators-knn-output')
#         ])
#
# @app.callback(
#     Output('legislators-knn-output', 'children'),
#     [Input('legislator-dropdown', 'value'),
#      Input('legislators-knn-radio', 'value')])
# def set_display_neighbors(leg_id, knn_num):
#     similar_legs = get_similar_legs(leg_id, knn_num)
#     output = '###### Legislators with similar records:\n'
#     for leg in similar_legs:
#         output += f'> ** {leg[0]}**' +'\n\n'
#     return dcc.Markdown(output)

if __name__ == '__main__':
    app.run_server(debug=True)
