from flask import Blueprint
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from course_data import data_science_students
from data_persistence import save_data, load_data



data_science_dashboard = Blueprint("data_science_dashboard", __name__)

def init_data_science_dashboard(flask_app):
    dash_app = dash.Dash(
        name="data_science_dashboard",
        server=flask_app,
        url_base_pathname="/data_science_dashboard/",
        suppress_callback_exceptions=True
    )

    df = pd.DataFrame(data_science_students)

    def calculate_final_grade(a1, a2, exam, p1, p2):
        grade = (a1 * 0.4) + (a2 * 0.3) + (exam * 0.3)
        if "Lateness Penalty" in p1:
            grade -= a1 * 0.4 * 0.05
        if "Lateness Penalty" in p2:
            grade -= a2 * 0.3 * 0.05
        return round(max(grade, 0), 2)

    df["Final Grade"] = df.apply(lambda row: calculate_final_grade(
        row["a1_score"], row["a2_score"], row["exam_score"], row["a1_penalty"], row["a2_penalty"]
    ), axis=1)

    df["Student"] = df["name"]
    df["ID"] = df["id"]
    df["Attendance (%)"] = df["attendance"]
    df["Exam Status"] = df["exam_status"]
    df["Exam Score"] = df["exam_score"]
    df["Assignment 1 (Data Analysis)"] = df["a1_score"]
    df["Assignment 1 Status"] = df["a1_status"]
    df["Assignment 1 Penalty"] = df["a1_penalty"]
    df["Assignment 2 (Machine Learning)"] = df["a2_score"]
    df["Assignment 2 Status"] = df["a2_status"]
    df["Assignment 2 Penalty"] = df["a2_penalty"]
    df["Status"] = df["status"]

    desired_columns = [
        "ID", "Student", "Final Grade", "Attendance (%)", "Exam Status", "Exam Score",
        "Assignment 1 (Data Analysis)", "Assignment 1 Status", "Assignment 1 Penalty",
        "Assignment 2 (Machine Learning)", "Assignment 2 Status", "Assignment 2 Penalty", "Status"
    ]
    df = df[desired_columns]

    fig_grades = px.bar(df, x="Student", y="Final Grade", title="📊 Data Science - Student Grades",
                        labels={"Final Grade": "Grade (%)"}, color="Final Grade", color_continuous_scale="Greens")
    fig_grades.update_layout(xaxis={'categoryorder': 'total descending'})

    attendance_fig = px.pie(
        names=["100-90%", "90-80%", "80-70%", "70-60%", "<60%"],
        values=[
            sum(90 <= x <= 100 for x in df["Attendance (%)"]),
            sum(80 <= x < 90 for x in df["Attendance (%)"]),
            sum(70 <= x < 80 for x in df["Attendance (%)"]),
            sum(60 <= x < 70 for x in df["Attendance (%)"]),
            sum(x < 60 for x in df["Attendance (%)"]),
        ],
        title="📌 Attendance Breakdown",
        hole=0.4
    )

    exam_fig = px.bar(df, x="Student", y="Exam Score", title="📝 Exam Scores",
                      labels={"Exam Score": "Score (%)"}, color="Exam Score", color_continuous_scale="Reds")
    exam_fig.update_layout(xaxis={'categoryorder': 'total descending'})

    dash_app.layout = html.Div(children=[
        html.H1("📊 Data Science - Performance & Grades", style={"textAlign": "center"}),
        dcc.Graph(figure=fig_grades),
        dcc.Graph(figure=attendance_fig),
        html.H3("📈 Insights"),
        html.P(f"📊 Average Grade: {df['Final Grade'].mean():.2f}%", style={"color": "#2c3e50"}),
        html.P(f"🏆 Highest Grade: {df['Final Grade'].max()}%", style={"color": "#27ae60"}),
        html.P(f"⚠️ Lowest Grade: {df['Final Grade'].min()}%", style={"color": "#c0392b"}),
        html.Label("Select Assignment:"),
        dcc.Dropdown(
            id="assignment-dropdown",
            options=[
                {"label": "Assignment 1 (Data Analysis) - Worth: 40%", "value": "Assignment 1 (Data Analysis)"},
                {"label": "Assignment 2 (Machine Learning) - Worth: 30%", "value": "Assignment 2 (Machine Learning)"}
            ],
            value="Assignment 1 (Data Analysis)",
            clearable=False
        ),
        dcc.Graph(id="assignment-chart"),
        dcc.Graph(figure=exam_fig),
        html.H2("📜 Student Performance Table", style={"textAlign": "center", "margin-top": "30px"}),
        html.Div([
            html.Button("Edit", id="edit-button", n_clicks=0, style={'marginRight': '10px'}),
            html.Button("Confirm Changes", id="confirm-button", n_clicks=0, style={'display': 'none', 'marginRight': '10px'}),
            html.Button("Discard Changes", id="discard-button", n_clicks=0, style={'display': 'none'})
        ], style={"textAlign": "center", "margin-bottom": "10px"}),
        dash_table.DataTable(
            id="data-table",
            columns=[{"name": col, "id": col, "editable": False} for col in desired_columns],
            data=df.to_dict("records"),
            sort_action="native",
            style_table={"margin": "auto", "width": "90%"},
            style_cell={"textAlign": "center"},
            style_header={"backgroundColor": "#2980b9", "color": "white"}
        ),
        dcc.Store(id='initial-table-data', data=df.to_dict('records'))
    ])

    @dash_app.callback(
        Output("assignment-chart", "figure"),
        Input("assignment-dropdown", "value")
    )
    def update_assignment_chart(selected_assignment):
        fig = px.bar(df, x="Student", y=selected_assignment, title=f"📑 {selected_assignment}",
                     labels={selected_assignment: "Score (%)"}, color=selected_assignment, color_continuous_scale="Oranges")
        fig.update_layout(xaxis={'categoryorder': 'total descending'})
        return fig

    @dash_app.callback(
        [Output("data-table", "columns"),
         Output("confirm-button", "style"),
         Output("discard-button", "style"),
         Output("edit-button", "style")],
        [Input("edit-button", "n_clicks"),
         Input("confirm-button", "n_clicks"),
         Input("discard-button", "n_clicks")],
        [State("data-table", "columns")]
    )
    def toggle_edit_mode(edit_clicks, confirm_clicks, discard_clicks, existing_columns):
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'edit-button':
            cols = [{"name": i['name'], "id": i['id'], "editable": True} for i in existing_columns]
            return (cols,
                    {'display': 'inline-block', 'marginRight': '10px'},
                    {'display': 'inline-block'},
                    {'display': 'none'})
        else:
            cols = [{"name": i['name'], "id": i['id'], "editable": False} for i in existing_columns]
            return (cols,
                    {'display': 'none', 'marginRight': '10px'},
                    {'display': 'none'},
                    {'display': 'inline-block'})

    @dash_app.callback(
        Output("data-table", "data"),
        [Input("confirm-button", "n_clicks"),
         Input("discard-button", "n_clicks")],
        [State("data-table", "data"),
         State("initial-table-data", "data")]
    )
    def update_table(confirm_clicks, discard_clicks, current_data, initial_data):
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == "confirm-button":
            df_new = pd.DataFrame(current_data)
            df_new['Final Grade'] = df_new.apply(lambda row: calculate_final_grade(
                float(row['Assignment 1 (Data Analysis)']),
                float(row['Assignment 2 (Machine Learning)']),
                float(row['Exam Score']),
                row['Assignment 1 Penalty'],
                row['Assignment 2 Penalty']
            ), axis=1)
            return df_new.to_dict('records')
        elif triggered_id == "discard-button":
            return initial_data
        return current_data
