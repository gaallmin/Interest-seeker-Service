import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import _mysql_connector

app = dash.Dash(__name__)

db_config = {
    'user' : 'root',
    'password' :'minjegal0408!',
    'host' : 'localhost',
    'port' :3306,
    'database' :'interest_db'
}

def query_database(query):
    conn = _mysql_connector.connect(**db_config)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

interest_option = ['Realistic','Investigative']

app.layout = html.Div([
    html.H1("Skills, Knowledge, and Interests Matching Dashboard"),
    html.Label("Select Interest:"),
    dcc.Dropdown(
        id="interest-dropdown",
        options=[{'label1': i, 'value': i} for i in interest_option],
        value=interest_option[0]
    ),
    html.Div(id='related-info'),
    dcc.Graph(id='matching-graph')
])
#fix
'''
interest.sql 
element_id ='1.B.1.g' is the highest interest point
take the value and match it with only one element,
have to think about how to match the data
'''

@app.callback(
    Output('related-info','childeren'),
    [Input('interest-dropdown','value')]
)

def updated_related_info(selected_interest):
    knowledge_query = f"""
    SELECT DISTINCT k.element_id, k.data_value
    FROM interest i
    JOIN knowledge k ON i.onetsoc_code = k.onetsoc_code
    WHERE i.element_id = '{selected_interest}' AND k.scale_id = 'IM'
    """
    skills_query = f"""
    SELECT DISTINCT s.element_id, s.data_value
    FROM interest i
    JOIN skills s on i.onetsoc_code = s.onetsoc_code
    WHERE i.element_id = '{selected_interest}' AND s.scale_id = 'IM'
    """

    abilities_query = f"""
    SELECT DISTINCT a.element_id, a.data_value
    FROM interest i
    JOIN abilities a on i.onetsoc_code = a.onetsoc_code
    WHERE i.element_id = '{selected_interest}' AND a.scale_id = 'IM'
    """

    knowledge_df = query_database(knowledge_query)
    skills_df = query_database(skills_query)
    abilities_df = query_database(abilities_query)

    related_info = html.Div([
        html.H3("Related Knowledge:"),
        html.U1([html.Li(f"{row['element_id']} (Rating_Importance: {row['data_value']})") for _, row in knowledge_df.interrows()]),
        html.H3("Related Skills:"),
        html.U1([html.Li(f"{row['element_id']} (Rating_Importance: {row['data_value']})") for _, row in skills_df.interrows()]),
        html.H3("Related Abilities:"),
        html.U1([html.Li(f"{row['element_id']} (Rating_Importance: {row['data_value']})") for _, row in abilities_df.interrows()])
    ])

    return related_info

@app.callback(
    Output('matching-graph', 'figure'),
    [Input('interest-dropdown', 'value')]
)

def update_graph(selected_interest):
    query = f"""
    SELECT i.onetsoc_code, i.data_value as interest_value, k.data_value as knowledge_value, s.data_value as skills_value, a.data_value as abilities_value
    FROM interest i
    JOIN knowledge k ON i.onetsoc_code = k.onetsoc_code
    JOIN skills s ON i.onetsoc_code = s.onetsoc_code
    JOIN abilities a ON i.onetsoc_code = a.onetsoc_code
    WHERE i.element_id = '{selected_interest}'
    """

    matching_df = query_database(query)

    fig = {
        'data':[
            {'x':matching_df['onetsoc_code'], 'y':matching_df['interest_value'], 'type':'bar','name':'Interest'},
            {'x':matching_df['onetsoc_code'], 'y':matching_df['knowledge_value'], 'type':'bar','name':'knowledge'},
            {'x':matching_df['onetsoc_code'], 'y':matching_df['skills_value'], 'type':'bar','name':'skills'},
            {'x':matching_df['onetsoc_code'], 'y':matching_df['abilities_value'], 'type':'bar','name':'abilities'},
        ],
        'layout': {'title':'Matching Skills, Knowledge, Skills, Abilities'}
    }

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)