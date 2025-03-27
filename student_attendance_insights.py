import random
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
from flask import Blueprint

student_attendance_insights = Blueprint("student_attendance_insights", __name__, template_folder="templates")

def init_student_attendance_insights(flask_app):
    dash_app = dash.Dash(
        name="student_attendance_insights",
        server=flask_app,
        url_base_pathname="/student_attendance_insights/",
        suppress_callback_exceptions=True
    )

    # Software Engineering Student Data
    se_students = [
        ("SE6352", "Alice Johnson", 95), ("SE8934", "Bob Smith", 91), ("SE6281", "Charlie Davis", 98),
        ("SE7925", "David Martinez", 84), ("SE6726", "Eve Brown", 64), ("SE1122", "Frank Wilson", 76),
        ("SE9571", "Grace Taylor", 65), ("SE3929", "Hank Anderson", 83), ("SE7971", "Ivy Thomas", 84),
        ("SE5495", "Jack White", 78), ("SE8563", "Karen Harris", 80), ("SE3882", "Leo Martin", 73),
        ("SE4819", "Mona Clark", 99), ("SE9943", "Nathan Lewis", 71), ("SE3065", "Olivia Hall", 92),
        ("SE8912", "Peter Allen", 57), ("SE9568", "Quincy Young", 90), ("SE7547", "Rachel King", 100),
        ("SE3979", "Steve Wright", 92), ("SE5835", "Tina Scott", 63), ("SE8744", "Uma Green", 85),
        ("SE7255", "Victor Adams", 83), ("SE5697", "Wendy Baker", 92), ("SE4181", "Xander Nelson", 93),
        ("SE4762", "Yvonne Carter", 87), ("SE5070", "Zachary Mitchell", 81), ("SE8734", "Aaron Perez", 97),
        ("SE2053", "Bella Roberts", 92), ("SE8111", "Cody Gonzalez", 89), ("SE9150", "Diana Campbell", 80),
        ("SE3215", "Ethan Rodriguez", 50), ("SE5869", "Fiona Moore", 54), ("SE6168", "George Edwards", 87),
        ("SE8238", "Holly Flores", 71), ("SE3932", "Ian Cooper", 92), ("SE7659", "Julia Murphy", 89),
        ("SE4522", "Kevin Reed", 99), ("SE9236", "Laura Cox", 78), ("SE1428", "Mike Ward", 99),
        ("SE8043", "Nina Peterson", 79), ("SE7543", "Oscar Gray", 96), ("SE3569", "Paula Jenkins", 99),
        ("SE3900", "Quinn Russell", 75), ("SE8183", "Randy Torres", 94), ("SE3509", "Samantha Stevens", 65),
        ("SE1763", "Tommy Parker", 82), ("SE9793", "Ursula Evans", 85), ("SE5731", "Vince Morgan", 82),
        ("SE9781", "Whitney Bell", 81), ("SE2024", "Xavier Phillips", 75)
    ]

    # Data Science Student Data
    ds_students = [
        ("DS1012", "Alex Carter", 71), ("DS4772", "Bella Sanders", 30), ("DS5732", "Cameron Hughes", 72),
        ("DS7477", "Diana Wright", 97), ("DS7861", "Ethan Parker", 61), ("DS9221", "Felicity James", 57),
        ("DS7221", "Gabriel Lewis", 91), ("DS6154", "Hannah Stone", 62), ("DS1486", "Ian Turner", 82),
        ("DS3966", "Jasmine Collins", 58), ("DS1166", "Kevin Morris", 90), ("DS6217", "Lara Watson", 84),
        ("DS6534", "Michael Griffin", 96), ("DS7280", "Natalie Cooper", 81), ("DS1929", "Owen Richardson", 66),
        ("DS8704", "Paige Scott", 68), ("DS5134", "Quentin Ramirez", 62), ("DS6980", "Rebecca Bennett", 92),
        ("DS3986", "Stephen Howard", 57), ("DS7376", "Tracy Bell", 82), ("DS6091", "Ulysses Barnes", 96),
        ("DS4026", "Victoria Foster", 94), ("DS4819", "Walter Henderson", 75), ("DS9065", "Xander Nelson", 84),
        ("DS9746", "Yvette Campbell", 57), ("DS3253", "Zane Mitchell", 58), ("DS6503", "Amelia Ross", 60),
        ("DS2850", "Benjamin Ward", 61), ("DS4513", "Chloe Edwards", 94), ("DS5015", "David Fisher", 59),
        ("DS3479", "Emma Butler", 60), ("DS7297", "Frederick Murphy", 57), ("DS7372", "Grace Price", 80),
        ("DS9041", "Henry Stewart", 93), ("DS6180", "Isabella Torres", 68), ("DS7380", "Jackie Peterson", 81),
        ("DS2398", "Kurt Bailey", 97), ("DS6589", "Lucy Jenkins", 84), ("DS2762", "Mason Cooper", 100),
        ("DS5804", "Nina Adams", 90), ("DS5362", "Oscar Flores", 83), ("DS5197", "Penelope Russell", 70),
        ("DS4441", "Ryan Powell", 71), ("DS8748", "Sophia Simmons", 72), ("DS8533", "Theodore White", 79),
        ("DS7065", "Ursula Martin", 73), ("DS3499", "Vince Brown", 71), ("DS5325", "William Gonzales", 85),
        ("DS7707", "Xenia Moore", 88), ("DS3801", "Zoe Walker", 73)
    ]

    # Lectures
    se_lectures = [
        "Application Software", "Databases", "Operating Systems", "Networking",
        "Cybersecurity", "Cloud Computing", "Software Testing", "Artificial Intelligence",
        "Machine Learning", "Web Development", "Mobile Development", "DevOps"
    ]

    ds_lectures = [
        "Data Wrangling", "Big Data", "Data Visualization", "Statistics",
        "Machine Learning", "Deep Learning", "NLP", "AI Ethics",
        "Reinforcement Learning", "Cloud Computing for AI", "Model Deployment", "Data Science Projects"
    ]

    weeks = [f"Week {i+1}" for i in range(12)]
    se_week_labels = [f"Week {i+1} ({se_lectures[i]})" for i in range(12)]
    ds_week_labels = [f"Week {i+1} ({ds_lectures[i]})" for i in range(12)]

    def create_student_graphs(students, week_labels, course):
        student_graphs = {}
        for student_id, student_name, attendance in students:
            student_data = []
            for i, week in enumerate(week_labels):
                attended = 100 if random.random() < (attendance / 100) else 0
                student_data.append({"Week": week, "Attendance %": attended})

            student_df = pd.DataFrame(student_data)

            fig = px.line(student_df, x="Week", y="Attendance %",
                          markers=True,
                          title=f"{student_id} - {student_name}'s Attendance",
                          hover_data={"Attendance %": True})

            fig.update_traces(mode="lines+markers")
            fig.update_layout(
                yaxis=dict(range=[-5, 105], tickvals=[0, 50, 100], title="Attendance %"),
                xaxis=dict(title="Week", tickangle=-45, tickmode='array', tickvals=week_labels, ticktext=week_labels),
                hovermode="x unified",
                margin=dict(l=20, r=20, t=40, b=40),
                paper_bgcolor="#f9f9f9",
                plot_bgcolor="#ffffff",
            )

            student_graphs[f"{student_id} - {student_name}"] = dcc.Graph(
                figure=fig,
                style={
                    'width': '48%',
                    'display': 'inline-block',
                    'padding': '15px',
                    'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)',
                    'borderRadius': '10px'
                }
            )

        return student_graphs

    se_graphs = create_student_graphs(se_students, se_week_labels, "Software Engineering")
    ds_graphs = create_student_graphs(ds_students, ds_week_labels, "Data Science")

    dash_app.layout = html.Div([
        html.H1("Student Attendance Dashboard", style={"textAlign": "center", "marginBottom": "20px"}),
        dcc.Dropdown(
            id='course-dropdown',
            options=[
                {'label': 'Software Engineering', 'value': 'SE'},
                {'label': 'Data Science', 'value': 'DS'}
            ],
            value='SE',
            style={'width': '50%', 'margin': '0 auto 20px'}
        ),
        dcc.Dropdown(
            id='student-dropdown',
            multi=True,
            style={'width': '50%', 'margin': '0 auto 20px'}
        ),
        html.Div(id='graphs-container', style={
            "display": "flex",
            "flexWrap": "wrap",
            "justifyContent": "center",
            "gap": "20px",
            "padding": "20px"
        })
    ])

    @dash_app.callback(
        Output('student-dropdown', 'options'),
        Output('student-dropdown', 'value'),
        Input('course-dropdown', 'value')
    )
    def update_student_dropdown(selected_course):
        if selected_course == 'SE':
            options = [{'label': f"{id} - {name}", 'value': f"{id} - {name}"} for id, name, _ in se_students]
        else:
            options = [{'label': f"{id} - {name}", 'value': f"{id} - {name}"} for id, name, _ in ds_students]
        return options, []

    @dash_app.callback(
        Output('graphs-container', 'children'),
        Input('course-dropdown', 'value'),
        Input('student-dropdown', 'value')
    )
    def update_graphs(selected_course, selected_students):
        if selected_course == 'SE':
            graphs = se_graphs
        else:
            graphs = ds_graphs
        
        if selected_students:
            return [graphs[student] for student in selected_students]
        else:
            return list(graphs.values())

    return dash_app
