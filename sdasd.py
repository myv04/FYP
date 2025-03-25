import random
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from flask import Blueprint

# ✅ Create Flask Blueprint
student_attendance_insights = Blueprint("student_attendance_insights", __name__, template_folder="templates")

def init_student_attendance_insights(flask_app):
    dash_app = dash.Dash(
        name="student_attendance_insights",
        server=flask_app,
        url_base_pathname="/student_attendance_insights/",
        suppress_callback_exceptions=True
    )

    # ✅ Sample Data Science Student Data
    students = [
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

    # ✅ Data Science Lectures (12 weeks)
    lectures = [
        "Data Wrangling", "Big Data", "Data Visualization", "Statistics",
        "Machine Learning", "Deep Learning", "NLP", "AI Ethics",
        "Reinforcement Learning", "Cloud Computing for AI", "Model Deployment", "Data Science Projects"
    ]

    weeks = [f"Week {i+1}" for i in range(12)]
    week_labels = [f"Week {i+1} ({lectures[i]})" for i in range(12)]  # Custom x-axis labels

    student_graphs = []
    for student_id, student_name, attendance in students:
        student_data = []
        for i, (week, lecture) in enumerate(zip(weeks, lectures)):
            attended = 100 if random.random() < (attendance / 100) else 0  
            student_data.append({"Week": week_labels[i], "Lecture": lecture, "Attendance %": attended})

        student_df = pd.DataFrame(student_data)

        # ✅ Create Scatter-Line Graph for Each Student
        fig = px.line(student_df, x="Week", y="Attendance %",
                      markers=True, 
                      title=f"{student_id} - {student_name}",
                      hover_data={"Attendance %": True})

        fig.update_traces(mode="lines+markers")

        # ✅ Uniform Axis Settings
        fig.update_layout(
            yaxis=dict(range=[-5, 105], tickvals=[0, 50, 100], title="Attendance %"),
            xaxis=dict(title="Week", tickangle=-45, tickmode='array', tickvals=week_labels, ticktext=week_labels),
            hovermode="x unified",
            margin=dict(l=30, r=30, t=50, b=80),
            font=dict(family="Arial, sans-serif", size=14),
            title_x=0.5,  # Center title
            paper_bgcolor="#f9f9f9",  # Light grey background
            plot_bgcolor="#ffffff",  # White plot background
            title_font=dict(size=16, color="#333"),  # Darker title color
        )

        student_graphs.append(
            html.Div(
                dcc.Graph(figure=fig), 
                style={'width': '48%', 'display': 'inline-block', 'padding': '15px', 'borderRadius': '10px', 'backgroundColor': 'white', 'boxShadow': '0px 2px 5px rgba(0,0,0,0.1)'}
            )
        )

    # ✅ Define Dash Layout (Better Styling)
    dash_app.layout = html.Div([
        html.H1("📊 Data Science Attendance Dashboard", 
                style={"textAlign": "center", "fontSize": "28px", "fontWeight": "bold", "color": "#333", "marginBottom": "20px"}),
        html.Div(student_graphs, style={"display": "flex", "flex-wrap": "wrap", "justify-content": "center", "padding": "20px", "backgroundColor": "#f4f4f4"})
    ])

    return dash_app
