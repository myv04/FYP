from flask import Blueprint
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import random

software_engineering_dashboard = Blueprint("software_engineering_dashboard", __name__)

def init_software_engineering_dashboard(flask_app):
    dash_app = dash.Dash(
        name="software_engineering_dashboard",
        server=flask_app,
        url_base_pathname="/software_engineering_dashboard/",
        suppress_callback_exceptions=True
    )

    student_names = [
        "Alice Johnson", "Bob Smith", "Charlie Davis", "David Martinez", "Eve Brown",
        "Frank Wilson", "Grace Taylor", "Hank Anderson", "Ivy Thomas", "Jack White",
        "Karen Harris", "Leo Martin", "Mona Clark", "Nathan Lewis", "Olivia Hall",
        "Peter Allen", "Quincy Young", "Rachel King", "Steve Wright", "Tina Scott",
        "Uma Green", "Victor Adams", "Wendy Baker", "Xander Nelson", "Yvonne Carter",
        "Zachary Mitchell", "Aaron Perez", "Bella Roberts", "Cody Gonzalez", "Diana Campbell",
        "Ethan Rodriguez", "Fiona Moore", "George Edwards", "Holly Flores", "Ian Cooper",
        "Julia Murphy", "Kevin Reed", "Laura Cox", "Mike Ward", "Nina Peterson",
        "Oscar Gray", "Paula Jenkins", "Quinn Russell", "Randy Torres", "Samantha Stevens",
        "Tommy Parker", "Ursula Evans", "Vince Morgan", "Whitney Bell", "Xavier Phillips"
    ]

    student_ids = [f"SE{random.randint(1000,9999)}" for _ in student_names]
    attendance_scores = [random.randint(70, 100) if random.random() > 0.1 else random.randint(50, 69) for _ in student_names]

    assignment_1_status = ["Completed"] * 45 + ["Absent"] * 2 + ["Not Completed"] * 3
    random.shuffle(assignment_1_status)
    assignment_2_status = ["Completed"] * 45 + ["Absent"] * 2 + ["Not Completed"] * 3
    random.shuffle(assignment_2_status)

    assignment_1_scores = [random.randint(65, 98) if status == "Completed" else 0 for status in assignment_1_status]
    assignment_2_scores = [random.randint(65, 98) if status == "Completed" else 0 for status in assignment_2_status]

    # Ensure students with 0 score on one assignment still have scores on the other
    for i in range(len(student_names)):
        if assignment_1_scores[i] == 0 and assignment_2_scores[i] == 0:
            if random.choice([True, False]):
                assignment_1_scores[i] = random.randint(65, 98)
                assignment_1_status[i] = "Completed"
            else:
                assignment_2_scores[i] = random.randint(65, 98)
                assignment_2_status[i] = "Completed"

    exam_status = ["Fit to Sit" if random.random() > 0.05 else "Absent" for _ in student_names]
    exam_scores = [random.randint(55, 95) if status == "Fit to Sit" else 0 for status in exam_status]

    students_with_penalties = random.sample(range(len(student_names)), min(8, len(student_names)))  
    students_with_word_count = random.sample([i for i in range(len(student_names)) if i not in students_with_penalties], 3)

    penalty_flags_1 = ["" for _ in student_names]
    penalty_flags_2 = ["" for _ in student_names]

    for i in students_with_penalties:
        penalty_type = random.choice(["🚩 Academic Misconduct", "🚩 Exceptional Circumstances", "🚩 Lateness Penalty (-5%)"])
        if random.random() < 0.5:  
            penalty_flags_1[i] = penalty_type  
        else:
            penalty_flags_2[i] = penalty_type  

    for i in students_with_word_count:
        if penalty_flags_1[i] == "" and penalty_flags_2[i] == "":
            if random.random() < 0.5:
                penalty_flags_1[i] = "🚩 Word Count Penalty (-10%)"
            else:
                penalty_flags_2[i] = "🚩 Word Count Penalty (-10%)"

    def calculate_final_grade(a1, a2, exam, p1, p2):
        grade = (a1 * 0.25) + (a2 * 0.25) + (exam * 0.5)

        if p1 == '🚩 Lateness Penalty (-5%)' or p2 == '🚩 Lateness Penalty (-5%)':
            grade *= 0.95

        if p1 == '🚩 Word Count Penalty (-10%)' or p2 == '🚩 Word Count Penalty (-10%)':
            grade *= 0.9

        return round(grade, 2)

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
        "Assignment 1 (Bugs and Fixes)": assignment_1_scores,
        "Assignment 1 Status": assignment_1_status,
        "Assignment 1 Penalty": penalty_flags_1,
        "Assignment 2 (Software Architecture)": assignment_2_scores,
        "Assignment 2 Status": assignment_2_status,
        "Assignment 2 Penalty": penalty_flags_2,
        "Status": statuses
    })

    fig_grades = px.bar(df, x="Student", y="Final Grade", title="📊 Student Grades",
                        labels={"Final Grade": "Grade (%)"}, color="Final Grade", color_continuous_scale="Blues")
    fig_grades.update_layout(xaxis={'categoryorder':'total descending'})

    exam_fig = px.bar(df, x="Student", y="Exam Score", title="📝 Exam Scores (50% of Final Grade)",
                      labels={"Exam Score": "Score (%)"}, color="Exam Score", color_continuous_scale="Reds")
    exam_fig.update_layout(xaxis={'categoryorder':'total descending'})

    attendance_fig = px.pie(
        names=["100-90%", "90-80%", "80-70%", "70-60%", "Below 60%"],
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

    dash_app.layout = html.Div(children=[
        html.H1("📊 Software Engineering - Performance & Grades", style={"textAlign": "center"}),

        dcc.Graph(figure=fig_grades),

        dcc.Graph(figure=attendance_fig),

        html.H3("📈 Insights"),
        html.P(f"📊 Average Grade: {df['Final Grade'].mean():.2f}%"),
        html.P(f"🏆 Highest Grade: {df['Final Grade'].max()}%"),
        html.P(f"⚠️ Lowest Grade: {df['Final Grade'].min()}%"),

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
            style_table={"margin": "auto", "width": "95%"},
            style_cell={
                "textAlign": "center",
                "whiteSpace": "normal",
                "height": "auto",
            },
            style_header={"backgroundColor": "#2980b9", "color": "white"},
        ),

        dcc.Store(id='initial-table-data', data=df.to_dict('records'))
    ])

    @dash_app.callback(
        Output("assignment-chart", "figure"),
        [Input("assignment-dropdown", "value")],
        [State("data-table", "data")]
    )
    def update_assignment_chart(selected_assignment, table_data):
        df_updated = pd.DataFrame(table_data)
        
        fig = px.bar(df_updated, x="Student", y=selected_assignment, title=f"📑 {selected_assignment} (25% of Final Grade)",
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
                float(row['Assignment 1 (Bugs and Fixes)']),
                float(row['Assignment 2 (Software Architecture)']),
                float(row['Exam Score']),
                row['Assignment 1 Penalty'],
                row['Assignment 2 Penalty']
            ), axis=1)
            return df.to_dict('records')
        elif triggered_id == "discard-button":
            return initial_data
        return current_data

    return dash_app
