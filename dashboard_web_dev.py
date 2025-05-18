import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import sqlite3
import json

# Create Dash app
dash_webdev = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_webdev/",
    suppress_callback_exceptions=True
)

# Fetch Data
def get_webdev_data():
    conn = sqlite3.connect("student_performance.db")
    c = conn.cursor()
    c.execute("SELECT * FROM student_modules WHERE module_code = 'CS202'")
    row = c.fetchone()
    conn.close()

    if row:
        return {
            "attendance": row[2],
            "grade": row[3],
            "assignments": json.loads(row[4]),
            "exams": json.loads(row[5])
        }
    return None

@dash_webdev.callback(
    Output("page-content", "children"),
    Input("url", "search")
)
def update_layout(search):
    colorblind = "cbmode=on" in search if search else False
    return generate_layout(colorblind=colorblind)

def generate_layout(colorblind=False):
    data = get_webdev_data()

    attendance = data["attendance"] if data else 80
    grade = data["grade"] if data else 79
    assignments = data["assignments"] if data else []
    exams = data["exams"] if data else []

    assignment = assignments[0] if assignments else {"name": "Responsive Design Project", "status": "Completed", "score": 82}
    exam = exams[0] if exams else {"name": "Final Web Development Exam", "status": "Completed", "score": 76}

    assignment_score = assignment.get("score", 82)
    exam_score = exam.get("score", 76)

    exam_weight = 50
    assignment_weight = 50
    assignment_weighted = (assignment_score / 100) * assignment_weight
    exam_weighted = (exam_score / 100) * exam_weight
    current_grade = assignment_weighted + exam_weighted

    # Color sets
    cb_colors = {
        "pie": ["#009E73", "#e0e0e0"],
        "bars": ["#0072B2", "#D55E00"],
        "pass": "#009E73",
        "fail": "#D55E00"
    }

    normal_colors = {
        "pie": ["#ff8d1a", "#e0e0e0"],
        "bars": ["#3498db", "#2ecc71"],
        "pass": "#2ecc71",
        "fail": "#e74c3c"
    }

    colors = cb_colors if colorblind else normal_colors

    # Charts
    attendance_chart = go.Figure(data=[go.Pie(
        labels=["Attendance", "Absent"],
        values=[attendance, 100 - attendance],
        hole=0.4,
        marker=dict(colors=colors["pie"]),
        textinfo="label+percent"
    )])
    attendance_chart.update_layout(title="Web Development - Attendance", title_x=0.5)

    exam_assignment_chart = go.Figure()
    exam_assignment_chart.add_trace(go.Bar(
        x=[exam["name"], assignment["name"]],
        y=[exam_score, assignment_score],
        marker=dict(color=colors["bars"]),
        text=[f"{exam_score}%", f"{assignment_score}%"],
        textposition="auto"
    ))
    exam_assignment_chart.update_layout(
        title="Exam & Assignment Scores",
        title_x=0.5,
        xaxis_title="Assessments",
        yaxis_title="Score",
        yaxis=dict(range=[0, 100])
    )

    status_chart = go.Figure()
    status_chart.add_trace(go.Bar(
        x=["Web Development"],
        y=[1],
        name="Exam Completed",
        marker=dict(color=colors["bars"][0]),
        hovertext=f"{exam['name']} - Weight: {exam_weight}%"
    ))
    status_chart.add_trace(go.Bar(
        x=["Web Development"],
        y=[1],
        name="Assignment Completed",
        marker=dict(color=colors["bars"][1]),
        hovertext=f"{assignment['name']} - Weight: {assignment_weight}%"
    ))
    status_chart.update_layout(
        title="Exam & Assignment Status",
        barmode="stack",
        xaxis_title="Module",
        yaxis_title="Assessments",
        legend_title="Status"
    )

    return html.Div(style={
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f8f9fa',
        'padding': '30px'
    }, children=[
        html.H2("Web Development Dashboard", style={
            'textAlign': 'center',
            'color': '#34495e',
            'marginBottom': '30px'
        }),
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '30px'}, children=[
            html.Div(dcc.Graph(figure=attendance_chart), style={'backgroundColor': 'white', 'borderRadius': '10px', 'padding': '20px'}),
            html.Div(dcc.Graph(figure=exam_assignment_chart), style={'backgroundColor': 'white', 'borderRadius': '10px', 'padding': '20px'})
        ]),
        html.Div(style={'display': 'flex', 'justifyContent': 'center', 'marginTop': '30px'}, children=[
            html.Div(style={
                'backgroundColor': 'white',
                'borderRadius': '10px',
                'padding': '20px',
                'textAlign': 'center',
                'width': '300px'
            }, children=[
                html.H3("Current Grade", style={'color': '#34495e'}),
                html.P(f"{current_grade:.2f}%", style={
                    'fontSize': '28px',
                    'fontWeight': 'bold',
                    'color': colors["pass"] if current_grade >= 50 else colors["fail"],
                    'backgroundColor': '#ecf0f1',
                    'borderRadius': '10px',
                    'display': 'inline-block',
                    'padding': '15px 30px'
                })
            ])
        ]),
        html.Div(dcc.Graph(figure=status_chart), style={'backgroundColor': 'white', 'borderRadius': '10px', 'padding': '20px', 'marginTop': '30px'})
    ])

dash_webdev.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

def init_dashboard(server):
    dash_webdev.init_app(server)
