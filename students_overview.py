from flask import Blueprint, render_template
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

students_overview = Blueprint("students_overview", __name__, template_folder="templates")

def init_students_overview(flask_app):
    dash_app = dash.Dash(
        __name__,
        server=flask_app,
        url_base_pathname="/students_overview_dashboard/",
        suppress_callback_exceptions=True,
        external_stylesheets=["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"]
    )

    software_engineering_data = [
        ("Alice Johnson", 90.25), ("Bob Smith", 81.5), ("Charlie Davis", 77), ("David Martinez", 80.75),
        ("Eve Brown", 84.75), ("Frank Wilson", 72), ("Grace Taylor", 91), ("Hank Anderson", 73),
        ("Ivy Thomas", 93.25), ("Jack White", 76.5), ("Karen Harris", 68.5), ("Leo Martin", 84.75),
        ("Mona Clark", 76.5), ("Nathan Lewis", 63.25), ("Olivia Hall", 76), ("Peter Allen", 84),
        ("Quincy Young", 79.5), ("Rachel King", 91.5), ("Steve Wright", 85.5), ("Tina Scott", 74.75),
        ("Uma Green", 71.55), ("Victor Adams", 76), ("Wendy Baker", 91), ("Xander Nelson", 79),
        ("Yvonne Carter", 82.75), ("Zachary Mitchell", 75.6), ("Aaron Perez", 75.5), ("Bella Roberts", 81.25),
        ("Cody Gonzalez", 72.91), ("Diana Campbell", 76.25), ("Ethan Rodriguez", 88), ("Fiona Moore", 76.05),
        ("George Edwards", 78), ("Holly Flores", 77.75), ("Ian Cooper", 66), ("Julia Murphy", 70.25),
        ("Kevin Reed", 81.75), ("Laura Cox", 85.5), ("Mike Ward", 83.75), ("Nina Peterson", 70),
        ("Oscar Gray", 79.5), ("Paula Jenkins", 75.5), ("Quinn Russell", 81.5), ("Randy Torres", 92),
        ("Samantha Stevens", 75.75), ("Tommy Parker", 79.75), ("Ursula Evans", 32.3), ("Vince Morgan", 86),
        ("Whitney Bell", 74.25), ("Xavier Phillips", 70.5)
    ]

    data_science_data = [
        ("Alex Carter", 65.3), ("Bella Sanders", 70.77), ("Cameron Hughes", 55.62), ("Diana Wright", 77.9),
        ("Ethan Parker", 73.5), ("Felicity James", 67.7), ("Gabriel Lewis", 77.4), ("Hannah Stone", 60.1),
        ("Ian Turner", 71.19), ("Jasmine Collins", 61.6), ("Kevin Morris", 91.3), ("Lara Watson", 70.7),
        ("Michael Griffin", 71.9), ("Natalie Cooper", 56.8), ("Owen Richardson", 55.38), ("Paige Scott", 73.2),
        ("Quentin Ramirez", 47.7), ("Rebecca Bennett", 65.44), ("Stephen Howard", 76.28), ("Tracy Bell", 76.8),
        ("Ulysses Barnes", 68.3), ("Victoria Foster", 84.4), ("Walter Henderson", 72.8), ("Xander Nelson", 72.4),
        ("Yvette Campbell", 70.2), ("Zane Mitchell", 72.4), ("Amelia Ross", 68.2), ("Benjamin Ward", 64.03),
        ("Chloe Edwards", 72.9), ("David Fisher", 76.6), ("Emma Butler", 63.7), ("Frederick Murphy", 71.2),
        ("Grace Price", 77), ("Henry Stewart", 67.5), ("Isabella Torres", 79.9), ("Jackie Peterson", 79.4),
        ("Kurt Bailey", 65.6), ("Lucy Jenkins", 73.7), ("Mason Cooper", 46.5), ("Nina Adams", 73.5),
        ("Oscar Flores", 43.7), ("Penelope Russell", 91.4), ("Ryan Powell", 67.1), ("Sophia Simmons", 70.27),
        ("Theodore White", 67.7), ("Ursula Martin", 79.1), ("Vince Brown", 75.5), ("William Gonzales", 77.4),
        ("Xenia Moore", 71.3), ("Zoe Walker", 56.4)
    ]

    def get_top_and_at_risk(data, course):
        sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
        top_performing = [{"Student": s[0], "Course": course, "Grade": s[1]} for s in sorted_data[:5]]
        at_risk = [{"Student": s[0], "Course": course, "Grade": s[1]} for s in sorted_data if s[1] < 60]
        return top_performing, at_risk

    top_performing_se, at_risk_se = get_top_and_at_risk(software_engineering_data, "Software Engineering")
    top_performing_ds, at_risk_ds = get_top_and_at_risk(data_science_data, "Data Science")

    avg_grades = pd.DataFrame({
        "Course": ["Software Engineering", "Data Science"],
        "Grade": [sum(g for _, g in software_engineering_data) / len(software_engineering_data),
                  sum(g for _, g in data_science_data) / len(data_science_data)]
    })
    fig_avg_grade_course = px.bar(
        avg_grades, x="Course", y="Grade",
        title="📊 Average Grade per Course",
        color="Grade", color_continuous_scale="Blues"
    )

    avg_attendance = pd.DataFrame({
        "Course": ["Software Engineering", "Data Science"],
        "Attendance": [78.5, 74.8]
    })
    fig_attendance_course = px.bar(
        avg_attendance, x="Course", y="Attendance",
        title="📌 Average Attendance per Course",
        color="Attendance", color_continuous_scale="Greens"
    )

    def categorize_grade(grade):
        if grade >= 70:
            return '100-70%'
        elif grade >= 60:
            return '70-60%'
        elif grade >= 50:
            return '60-50%'
        else:
            return '50-40%'

    software_distribution = [categorize_grade(grade) for _, grade in software_engineering_data]
    data_science_distribution = [categorize_grade(grade) for _, grade in data_science_data]

    grade_ranges = ['100-70%', '70-60%', '60-50%', '50-40%']
    software_counts = [software_distribution.count(range) for range in grade_ranges]
    data_science_counts = [data_science_distribution.count(range) for range in grade_ranges]

    grade_distribution = pd.DataFrame({
        "Grade Range": grade_ranges,
        "Software Engineering": software_counts,
        "Data Science": data_science_counts
    })

    fig_grade_distribution = px.bar(
        grade_distribution, x="Grade Range", y=["Software Engineering", "Data Science"],
        title="📊 Grade Distribution by Course",
        barmode="group"
    )

    performance_comparison = pd.DataFrame({
        "Metric": ["Assignments", "Exams"],
        "Software Engineering": [78, 85],
        "Data Science": [74, 82]
    })
    fig_performance_comparison = px.bar(
        performance_comparison, x="Metric", y=["Software Engineering", "Data Science"],
        title="📈 Performance Comparison (Assignments vs Exams)",
        barmode="group"
    )

    dash_app.layout = html.Div(style={"fontFamily": "Arial, sans-serif", "padding": "20px", "maxWidth": "1200px", "margin": "auto"}, children=[
        html.H1("📌 Students Overview", style={"textAlign": "center", "color": "#2c3e50"}),
        html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"}, children=[
            dcc.Graph(figure=fig_avg_grade_course),
            dcc.Graph(figure=fig_attendance_course)
        ]),
        html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px", "marginTop": "30px"}, children=[
            dcc.Graph(figure=fig_grade_distribution),
            dcc.Graph(figure=fig_performance_comparison)
        ]),
        html.Div([
            html.H3("🚨 At-Risk Students", style={"color": "#e74c3c", "textAlign": "center"}),
            dcc.Dropdown(
                id='at-risk-dropdown',
                options=[
                    {'label': 'Software Engineering', 'value': 'SE'},
                    {'label': 'Data Science', 'value': 'DS'}
                ],
                value='SE',
                style={'width': '50%', 'margin': '10px auto'}
            ),
            dash_table.DataTable(
                id='at-risk-table',
                columns=[{"name": i, "id": i} for i in ["Student", "Course", "Grade"]],
                style_table={"overflowX": "auto", "margin": "auto", "width": "80%"},
                style_header={"backgroundColor": "#e74c3c", "color": "white", "fontWeight": "bold"},
                style_cell={"textAlign": "center"}
            )
        ], style={"marginBottom": "30px"}),
        html.Div([
            html.H3("🌟 Top Performing Students", style={"color": "#16a085", "textAlign": "center"}),
            dcc.Dropdown(
                id='top-performing-dropdown',
                options=[
                    {'label': 'Software Engineering', 'value': 'SE'},
                    {'label': 'Data Science', 'value': 'DS'}
                ],
                value='SE',
                style={'width': '50%', 'margin': '10px auto'}
            ),
            dash_table.DataTable(
                id='top-performing-table',
                columns=[{"name": i, "id": i} for i in ["Student", "Course", "Grade"]],
                style_table={"overflowX": "auto", "margin": "auto", "width": "80%"},
                style_header={"backgroundColor": "#16a085", "color": "white", "fontWeight": "bold"},
                style_cell={"textAlign": "center"}
            )
        ])
    ])

    @dash_app.callback(
        Output('at-risk-table', 'data'),
        Input('at-risk-dropdown', 'value')
    )
    def update_at_risk_table(value):
        if value == 'SE':
            return at_risk_se
        else:
            return at_risk_ds

    @dash_app.callback(
        Output('top-performing-table', 'data'),
        Input('top-performing-dropdown', 'value')
    )
    def update_top_performing_table(value):
        if value == 'SE':
            return top_performing_se
        else:
            return top_performing_ds

    return dash_app

@students_overview.route("/students_overview")
def students_overview_page():
    return render_template("students_overview.html")