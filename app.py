import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


########### Define your variables
tabtitle='US Congress Deep Dive'
githublink='https://github.com/skshenoy/us_congress_bills'

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
    # dcc.Link('Click here to look at legislators!', href="/page-1", style={"font-weight": "bold"}),
    html.Br(),
    html.Br(),
    dcc.Markdown('##### Part Two: Congressional Insights'),
    dcc.Markdown("This part is some descriptive information about the term of Congress and its bills overall (e.g., bills that received the most support, legislators who sponsored the largest number of bills, etc.). Currently this section is not interactive and simply displays some of the interesting facts I pulled out while conducting EDA on this dataset. This is where the most change will happen (hopefully) soon, because I’m planning to broaden my analysis and add in other Congresses as well. Near the bottom of this page I’ve detailed the future exploration and next steps I’d like to take."),
    dcc.Link('Click here to look at Congresses!', href='/page-2', style={"font-weight": "bold"}),
    html.Br(),
    html.Br(),
    dcc.Markdown('##### Part Three: Fun with Models'),
    dcc.Markdown("This is where I started playing around with machine learning techniques to see if I could predict whether a bill would pass. Again, there's a *lot* in this dataset so I experimented with which features to use, trying to determine if any had a significant correlation with whether a bill would pass. I used the bill’s official title (because I’m always interested in some NLP and I wanted to include that in this project), but I also worked with the breakdown of cosponsors, the sponsor’s party, the number of amendments, the number of related bills, and so on. This page is a fun little diversion where you can pretend to be a member of Congress, make up a bill, and then see what my model predicts would have happened to it."),
    # dcc.Link('Click here to try passing a bill!', href='/page-3', style={"font-weight": "bold"}),
    dcc.Markdown('### Thanks for visiting!'),
    ])

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

    # dcc.Markdown('# THIS IS WHERE GRAPHS GO AAAAAAAA'),
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

########### Set up the chart
# no


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    # return index_layout
    if pathname == '/page-2':
        return page_2_layout
    # elif pathname == '/page-2':
    #     return page_2_layout
    # elif pathname == '/page-3':
    #     return page_3_layout
    else:
        return index_page
    # # You could also return a 404 "URL not found" page here

if __name__ == '__main__':
    app.run_server()
