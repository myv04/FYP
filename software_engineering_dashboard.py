from flask import Blueprint
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from course_data import software_engineering_students
from data_persistence import load_data, save_data

software_engineering_dashboard = Blueprint("software_engineering_dashboard", __name__)

def init_software_engineering_dashboard(flask_app):
    dash_app = dash.Dash(
        name="software_engineering_dashboard",
        server=flask_app,
        url_base_pathname="/software_engineering_dashboard/",
        suppress_callback_exceptions=True
    )

    def calculate_final_grade(a1, a2, exam, p1, p2):
        grade = (a1 * 0.25) + (a2 * 0.25) + (exam * 0.5)

        if "Lateness Penalty" in p1 or "Lateness Penalty" in p2:
            grade *= 0.95
        if "Word Count Penalty" in p1 or "Word Count Penalty" in p2:
            grade *= 0.9

        return round(grade, 2)

    def prepare_dataframe(data):
        df = pd.DataFrame(data)
        df["Final Grade"] = df.apply(lambda row: calculate_final_grade(
            float(row.get("Assignment 1 (Bugs and Fixes)", 0)),
            float(row.get("Assignment 2 (Software Architecture)", 0)),
            float(row.get("Exam Score", 0)),
            row.get("Assignment 1 Penalty", ""),
            row.get("Assignment 2 Penalty", "")
        ), axis=1)
        return df

    loaded = load_data("software_engineering")
    if loaded:
        df = prepare_dataframe(loaded)
    else:
        df = pd.DataFrame(software_engineering_students)
        df["Student"] = df["name"]
        df["ID"] = df["id"]
        df["Attendance (%)"] = df["attendance"]
        df["Exam Status"] = df["exam_status"]
        df["Exam Score"] = df["exam_score"]
        df["Assignment 1 (Bugs and Fixes)"] = df["a1_score"]
        df["Assignment 1 Status"] = df["a1_status"]
        df["Assignment 1 Penalty"] = df["a1_penalty"]
        df["Assignment 2 (Software Architecture)"] = df["a2_score"]
        df["Assignment 2 Status"] = df["a2_status"]
        df["Assignment 2 Penalty"] = df["a2_penalty"]
        df["Status"] = df["status"]
        df = prepare_dataframe(df)

    column_order = [
        "ID", "Student", "Final Grade", "Attendance (%)", "Exam Status", "Exam Score",
        "Assignment 1 (Bugs and Fixes)", "Assignment 1 Status", "Assignment 1 Penalty",
        "Assignment 2 (Software Architecture)", "Assignment 2 Status", "Assignment 2 Penalty", "Status"
    ]
    df = df[column_order]

    dash_app.layout = html.Div(children=[
        html.H1("📊 Software Engineering - Performance & Grades", style={"textAlign": "center"}),

        dcc.Graph(id="grades-fig"),

        dcc.Graph(id="attendance-fig"),

        html.H3("📈 Insights"),
        html.P(id="avg-grade", style={"color": "#2c3e50"}),
        html.P(id="max-grade", style={"color": "#27ae60"}),
        html.P(id="min-grade", style={"color": "#c0392b"}),

        html.Label("Select Assignment:"),
        dcc.Dropdown(
            id="assignment-dropdown",
            options=[
                {"label": "Assignment 1 (Bugs and Fixes) - 25%", "value": "Assignment 1 (Bugs and Fixes)"},
                {"label": "Assignment 2 (Software Architecture) - 25%", "value": "Assignment 2 (Software Architecture)"}
            ],
            value="Assignment 1 (Bugs and Fixes)",
            clearable=False
        ),

        dcc.Graph(id="assignment-chart"),

        dcc.Graph(id="exam-fig"),

        html.H2("📜 Student Performance Table", style={"textAlign": "center", "margin-top": "30px"}),

        html.Div([
            html.Button("Edit", id="edit-button", n_clicks=0, style={'marginRight': '10px'}),
            html.Button("Confirm Changes", id="confirm-button", n_clicks=0, style={'display': 'none', 'marginRight': '10px'}),
            html.Button("Discard Changes", id="discard-button", n_clicks=0, style={'display': 'none'})
        ], style={"textAlign": "center", "margin-bottom": "10px"}),

        dash_table.DataTable(
            id="data-table",
            columns=[{"name": i, "id": i, "editable": False} for i in column_order],
            data=df.to_dict("records"),
            sort_action="native",
            style_table={"margin": "auto", "width": "95%"},
            style_cell={"textAlign": "center"},
            style_header={"backgroundColor": "#2980b9", "color": "white"}
        ),

        dcc.Store(id='initial-table-data', data=df.to_dict('records')),
        dcc.Store(id='live-data', data=df.to_dict('records'))
    ])

    @dash_app.callback(
        [Output("grades-fig", "figure"),
         Output("exam-fig", "figure"),
         Output("attendance-fig", "figure"),
         Output("avg-grade", "children"),
         Output("max-grade", "children"),
         Output("min-grade", "children")],
        Input("live-data", "data")
    )
    def update_all_figures(data):
        df_live = pd.DataFrame(data)

        fig_grades = px.bar(df_live, x="Student", y="Final Grade", title="📊 Student Grades",
                            labels={"Final Grade": "Grade (%)"}, color="Final Grade", color_continuous_scale="Blues")
        fig_grades.update_layout(xaxis={'categoryorder': 'total descending'})

        exam_fig = px.bar(df_live, x="Student", y="Exam Score", title="📝 Exam Scores (50% of Final Grade)",
                          labels={"Exam Score": "Score (%)"}, color="Exam Score", color_continuous_scale="Reds")
        exam_fig.update_layout(xaxis={'categoryorder': 'total descending'})

        attendance_fig = px.pie(
            names=["100-90%", "90-80%", "80-70%", "70-60%", "<60%"],
            values=[
                sum(90 <= x <= 100 for x in df_live["Attendance (%)"]),
                sum(80 <= x < 90 for x in df_live["Attendance (%)"]),
                sum(70 <= x < 80 for x in df_live["Attendance (%)"]),
                sum(60 <= x < 70 for x in df_live["Attendance (%)"]),
                sum(x < 60 for x in df_live["Attendance (%)"]),
            ],
            title="📌 Attendance Breakdown",
            hole=0.4
        )

        avg = f"📊 Average Grade: {df_live['Final Grade'].mean():.2f}%"
        max_ = f"🏆 Highest Grade: {df_live['Final Grade'].max()}%"
        min_ = f"⚠️ Lowest Grade: {df_live['Final Grade'].min()}%"

        return fig_grades, exam_fig, attendance_fig, avg, max_, min_

    @dash_app.callback(
        Output("assignment-chart", "figure"),
        [Input("assignment-dropdown", "value"),
         Input("live-data", "data")]
    )
    def update_assignment_chart(selected_assignment, table_data):
        df_updated = pd.DataFrame(table_data)
        fig = px.bar(df_updated, x="Student", y=selected_assignment, title=f"📑 {selected_assignment} (25%)",
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
            return cols, {'display': 'inline-block'}, {'display': 'inline-block'}, {'display': 'none'}
        else:
            cols = [{"name": i['name'], "id": i['id'], "editable": False} for i in existing_columns]
            return cols, {'display': 'none'}, {'display': 'none'}, {'display': 'inline-block'}

    @dash_app.callback(
        [Output("data-table", "data"), Output("live-data", "data")],
        [Input("confirm-button", "n_clicks"),
         Input("discard-button", "n_clicks")],
        [State("data-table", "data"),
         State("initial-table-data", "data")]
    )
    def update_table(confirm_clicks, discard_clicks, current_data, initial_data):
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == "confirm-button":
            df_new = prepare_dataframe(current_data)
            records = df_new.to_dict("records")
            save_data(records, "software_engineering")
            return records, records
        elif triggered_id == "discard-button":
            return initial_data, initial_data
        return current_data, current_data

    return dash_app
