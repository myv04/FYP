from flask import Blueprint
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import random

data_science_dashboard = Blueprint("data_science_dashboard", __name__)

def init_data_science_dashboard(flask_app):
    dash_app = dash.Dash(
        name="data_science_dashboard",
        server=flask_app,
        url_base_pathname="/data_science_dashboard/",
        suppress_callback_exceptions=True
    )

    student_names = [
        "Alex Carter", "Bella Sanders", "Cameron Hughes", "Diana Wright", "Ethan Parker",
        "Felicity James", "Gabriel Lewis", "Hannah Stone", "Ian Turner", "Jasmine Collins",
        "Kevin Morris", "Lara Watson", "Michael Griffin", "Natalie Cooper", "Owen Richardson",
        "Paige Scott", "Quentin Ramirez", "Rebecca Bennett", "Stephen Howard", "Tracy Bell",
        "Ulysses Barnes", "Victoria Foster", "Walter Henderson", "Xander Nelson", "Yvette Campbell",
        "Zane Mitchell", "Amelia Ross", "Benjamin Ward", "Chloe Edwards", "David Fisher",
        "Emma Butler", "Frederick Murphy", "Grace Price", "Henry Stewart", "Isabella Torres",
        "Jackie Peterson", "Kurt Bailey", "Lucy Jenkins", "Mason Cooper", "Nina Adams",
        "Oscar Flores", "Penelope Russell", "Ryan Powell", "Sophia Simmons", "Theodore White",
        "Ursula Martin", "Vince Brown", "William Gonzales", "Xenia Moore", "Zoe Walker"
    ]

    student_ids = [f"DS{random.randint(1000,9999)}" for _ in student_names]
    attendance_scores = [random.randint(55, 100) if random.random() > 0.1 else random.randint(30, 49) for _ in student_names]

    assignment_1_status = ["Completed"] * 48 + ["Not Completed"] * 2
    random.shuffle(assignment_1_status)
    assignment_2_status = ["Completed"] * 48 + ["Not Completed"] * 2
    random.shuffle(assignment_2_status)

    assignment_1_scores = [random.randint(50, 95) if status == "Completed" else 0 for status in assignment_1_status]
    assignment_2_scores = [random.randint(50, 95) if status == "Completed" else 0 for status in assignment_2_status]

    penalty_flags_1 = ["🚩 Academic Misconduct" if random.random() < 0.05 else
                       "🚩 Exceptional Circumstances" if random.random() < 0.05 else
                       "🚩 Lateness Penalty (-5%)" if random.random() < 0.1 else "" for _ in student_names]

    penalty_flags_2 = ["🚩 Academic Misconduct" if random.random() < 0.05 else
                       "🚩 Exceptional Circumstances" if random.random() < 0.05 else
                       "🚩 Lateness Penalty (-5%)" if random.random() < 0.1 else "" for _ in student_names]

    exam_status = ["Fit to Sit" if random.random() > 0.05 else "Absent" for _ in student_names]
    exam_scores = [random.randint(50, 95) if status == "Fit to Sit" else 0 for status in exam_status]

    def calculate_final_grade(a1, a2, exam, p1, p2):
        grade = (a1 * 0.4) + (a2 * 0.3) + (exam * 0.3)
        
        if "Lateness Penalty" in p1:
            grade -= a1 * 0.4 * 0.05
        if "Lateness Penalty" in p2:
            grade -= a2 * 0.3 * 0.05
        
        return round(max(grade, 0), 2)

    final_grades = [calculate_final_grade(a1, a2, exam, p1, p2) 
                    for a1, a2, exam, p1, p2 in zip(assignment_1_scores, assignment_2_scores,
                                                    exam_scores, penalty_flags_1, penalty_flags_2)]

    statuses = ["Enrolled"] * 45 + ["Deferred"] * 3 + ["Dropped"] * 2
    random.shuffle(statuses)

    df = pd.DataFrame({
        "ID": student_ids,
        "Student": student_names,
        "Final Grade": final_grades,
        "Attendance (%)": attendance_scores,
        "Exam Status": exam_status,
        "Exam Score": exam_scores,
        "Assignment 1 (Data Analysis)": assignment_1_scores,
        "Assignment 1 Status": assignment_1_status,
        "Assignment 1 Penalty": penalty_flags_1,
        "Assignment 2 (Machine Learning)": assignment_2_scores,
        "Assignment 2 Status": assignment_2_status,
        "Assignment 2 Penalty": penalty_flags_2,
        "Status": statuses
    })

    fig_grades = px.bar(df, x="Student", y="Final Grade", title="📊 Data Science - Student Grades",
                        labels={"Final Grade": "Grade (%)"}, color="Final Grade", color_continuous_scale="Greens")
    fig_grades.update_layout(xaxis={'categoryorder':'total descending'})

    attendance_fig = px.pie(
        names=["100-90%", "90-80%", "80-70%", "70-60%", "<60%"],
        values=[
            sum(90 <= x <= 100 for x in attendance_scores),
            sum(80 <= x < 90 for x in attendance_scores),
            sum(70 <= x < 80 for x in attendance_scores),
            sum(60 <= x < 70 for x in attendance_scores),
            sum(x < 60 for x in attendance_scores),
        ],
        title="📌 Attendance Breakdown",
        hole=0.4
    )

    exam_fig = px.bar(df, x="Student", y="Exam Score", title="📝 Exam Scores",
                      labels={"Exam Score": "Score (%)"}, color="Exam Score", color_continuous_scale="Reds")
    exam_fig.update_layout(xaxis={'categoryorder':'total descending'})

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
            columns=[{"name": i, "id": i, "editable": False} for i in df.columns],
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
        fig.update_layout(xaxis={'categoryorder':'total descending'})
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
            if edit_clicks % 2 == 1:  # Odd clicks: enable editing
                cols = [{"name": i['name'], "id": i['id'], "editable": True} for i in existing_columns]
                return (cols,
                        {'display': 'inline-block', 'marginRight': '10px'},
                        {'display': 'inline-block'},
                        {'display': 'none'})  # Hide Edit, Show Confirm/Discard
            else:  # Even clicks: disable editing
                cols = [{"name": i['name'], "id": i['id'], "editable": False} for i in existing_columns]
                return (cols,
                        {'display': 'none', 'marginRight': '10px'},
                        {'display': 'none'},
                        {'display': 'inline-block'})  # Show Edit, Hide Confirm/Discard
        else:  # triggered by Confirm or Discard
            cols = [{"name": i['name'], "id": i['id'], "editable": False} for i in existing_columns]
            return (cols,
                    {'display': 'none', 'marginRight': '10px'},
                    {'display': 'none'},
                    {'display': 'inline-block'})  # Show Edit, Hide Confirm/Discard

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
            df = pd.DataFrame(current_data)
            df['Final Grade'] = df.apply(lambda row: calculate_final_grade(
                float(row['Assignment 1 (Data Analysis)']),
                float(row['Assignment 2 (Machine Learning)']),
                float(row['Exam Score']),
                row['Assignment 1 Penalty'],
                row['Assignment 2 Penalty']
            ), axis=1)
            return df.to_dict('records')
        elif triggered_id == "discard-button":
            return initial_data
        return current_data

    return dash_app
