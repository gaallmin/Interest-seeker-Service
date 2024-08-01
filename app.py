import sqlalchemy as db
from sqlalchemy import create_engine
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from config import db_config

connection_str = (
    f"mssql+pyodbc://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?"
    "DRIVER=ODBC+Driver+17+for+SQL+Server"
    "Encrypt=yes;TrustServerCertificate=yes"
)

engine = create_engine(connection_str)

try:
    with engine.connect() as conn:
        print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)

# def query_database(query, params=None):
#     with engine.connect() as conn:
#         df = pd.read_sql(query, conn, params=params)
#     return df

# interest_option = {
#     "No high point available": 0.00,
#     "Realistic": 1.00,
#     "Investigative": 2.00,
#     "Artistic": 3.00,
#     "Social": 4.00,
#     "Enterprising": 5.00,
#     "Conventional": 6.00
# }

# app = dash.Dash(__name__)

# app.layout = html.Div([
#     html.H1("Skills, Knowledge, and Interests Matching Dashboard"),
#     html.H2("Let's First Identify your Interests"),
#     html.Label("Select your Highest Interest:"),
#     dcc.Dropdown(
#         id="interest-highest",
#         options=[{'label': key, 'value':value} for key, value in interest_option.items()],
#         placeholder='Select your highest interest'
#     ),

#     html.Label("Select your Second Highest Interest:"),
#     dcc.Dropdown(
#         id="interest-second",
#         options=[{'label': key, 'value':value} for key, value in interest_option.items()],
#         placeholder='Select your second highest interest'
#     ),

#     html.Label("Select your Third Highest Interest:"),
#     dcc.Dropdown(
#         id="interest-third",
#         options=[{'label': key, 'value':value} for key, value in interest_option.items()],
#         placeholder='Select your third highest interest'
#     ),

#     html.Button(id='submit-button',n_clicks=0, children='Submit'),
#     html.Div(id='output-result')
# ])


# @app.callback(
#         Output('output-result', 'children'),
#         [Input('submit-button','n_clicks')],
#         [State('interest-highest','value'), State('interest-second','value'),State('interest-third','value')]
# )

# def update_output(n_clicks, highest_interest, second_interest, third_interest):
#     if n_clicks >0:

#         interest_query = f"""
#         SELECT onetsec_code
#         FROM interests
#         WHERE scale_id='IH'
#         AND (
#             (element_id = '1.B.1.f' AND data_value = :highest_interest) AND
#             (element_id = '1.B.1.g' AND data_value = :second_interest) AND
#             (element_id = '1.B.1.h' AND data_value = :third_interest)
#         )
#         GROUP BY onetsoc_code;
#         """
#         params = {
#             'highest_interest': highest_interest,
#             'second_interest': second_interest,
#             'third_interest': third_interest
#         }
        
#         df_interest = query_database(interest_query, params=params)
#         return df_interest.to_html()

# # def updated_related_info(selected_interest):
# #     knowledge_query = f"""
# #     SELECT DISTINCT k.element_id, k.data_value
# #     FROM interest i
# #     JOIN knowledge k ON i.onetsoc_code = k.onetsoc_code
# #     WHERE i.element_id = '{selected_interest}' AND k.scale_id = 'IM'
# #     """
# #     skills_query = f"""
# #     SELECT DISTINCT s.element_id, s.data_value
# #     FROM interest i
# #     JOIN skills s on i.onetsoc_code = s.onetsoc_code
# #     WHERE i.element_id = '{selected_interest}' AND s.scale_id = 'IM'
# #     """

# #     abilities_query = f"""
# #     SELECT DISTINCT a.element_id, a.data_value
# #     FROM interest i
# #     JOIN abilities a on i.onetsoc_code = a.onetsoc_code
# #     WHERE i.element_id = '{selected_interest}' AND a.scale_id = 'IM'
# #     """

# #     knowledge_df = query_database(knowledge_query)
# #     skills_df = query_database(skills_query)
# #     abilities_df = query_database(abilities_query)

# #     related_info = html.Div([
# #         html.H3("Related Knowledge:"),
# #         html.U1([html.Li(f"{row['element_id']} (Rating_Importance: {row['data_value']})") for _, row in knowledge_df.interrows()]),
# #         html.H3("Related Skills:"),
# #         html.U1([html.Li(f"{row['element_id']} (Rating_Importance: {row['data_value']})") for _, row in skills_df.interrows()]),
# #         html.H3("Related Abilities:"),
# #         html.U1([html.Li(f"{row['element_id']} (Rating_Importance: {row['data_value']})") for _, row in abilities_df.interrows()])
# #     ])

# #     return related_info

# # @app.callback(
# #     Output('matching-graph', 'figure'),
# #     [Input('interest-dropdown', 'value')]
# # )

# # def update_graph(selected_interest):
# #     query = f"""
# #     SELECT i.onetsoc_code, i.data_value as interest_value, k.data_value as knowledge_value, s.data_value as skills_value, a.data_value as abilities_value
# #     FROM interest i
# #     JOIN knowledge k ON i.onetsoc_code = k.onetsoc_code
# #     JOIN skills s ON i.onetsoc_code = s.onetsoc_code
# #     JOIN abilities a ON i.onetsoc_code = a.onetsoc_code
# #     WHERE i.element_id = '{selected_interest}'
# #     """

# #     matching_df = query_database(query)

# #     fig = {
# #         'data':[
# #             {'x':matching_df['onetsoc_code'], 'y':matching_df['interest_value'], 'type':'bar','name':'Interest'},
# #             {'x':matching_df['onetsoc_code'], 'y':matching_df['knowledge_value'], 'type':'bar','name':'knowledge'},
# #             {'x':matching_df['onetsoc_code'], 'y':matching_df['skills_value'], 'type':'bar','name':'skills'},
# #             {'x':matching_df['onetsoc_code'], 'y':matching_df['abilities_value'], 'type':'bar','name':'abilities'},
# #         ],
# #         'layout': {'title':'Matching Skills, Knowledge, Skills, Abilities'}
# #     }

# #     return fig

# if __name__ == '__main__':
#     app.run_server(debug=True)