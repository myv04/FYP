import dash
from dash import dcc, html, dash_table, Input, Output
import plotly.graph_objs as go
import sqlite3
import json

# Dash App
dash_ai = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_ai/",
    suppress_callback_exceptions=True
)

@dash_ai.callback(
    Output("page-content", "children"),
    Input("url", "search")
)
def render_layout(search):
    colorblind = "cbmode=on" in search if search else False
    return generate_layout(colorblind)

def generate_layout(colorblind=False):
    # Connect to DB and fetch AI data
    conn = sqlite3.connect("student_performance.db")
    c = conn.cursor()
    c.execute("SELECT * FROM student_modules WHERE module_code = 'CS203'")
    data = c.fetchone()
    conn.close()

    module_code, module_name, attendance, grade, assignments_json, exams_json, deadlines_json = data
    assignments = json.loads(assignments_json)
    deadlines = json.loads(deadlines_json)

    # Prep values
    average_attendance = attendance
    remaining_attendance = 100 - average_attendance

    default_weights = {
        "Neural Network Implementation": 30,
        "Ethical Concerns in AI Development": 40,
        "Sentiment Analysis using NLP": 30
    }

    assignment_names = [a["name"] for a in assignments]
    assignment_statuses = [a["status"] for a in assignments]
    assignment_scores = [a.get("score") for a in assignments]
    assignment_weights = [a.get("weight", default_weights.get(a["name"], 0)) for a in assignments]

    total_weighted_score = sum(
        (score / 100) * weight for score, weight in zip(assignment_scores, assignment_weights) if score is not None
    )
    current_grade = total_weighted_score

    deadline_data = []
    for a in assignments:
        if a["status"] != "Completed":
            deadline_data.append({
                "Assignment": a["name"],
                "Deadline": a.get("deadline", "TBC"),
                "Days Left": a.get("days_left", "TBC")
            })

    # === Colorblind Support ===
    cb_colors = {
        "attendance": ["#009E73", "#e0e0e0"],
        "scores": ["#0072B2", "#D55E00"],
        "statuses": {
            "Completed": "#009E73",
            "Not Completed": "#E69F00",
            "Not Started": "#F0E442"
        },
        "grade_pass": "#009E73",
        "grade_fail": "#D55E00"
    }

    normal_colors = {
        "attendance": ["#3498db", "#e0e0e0"],
        "scores": ["#2ecc71" if s is not None else "#e74c3c" for s in assignment_scores],
        "statuses": {
            "Completed": "#2ecc71",
            "Not Completed": "#f1c40f",
            "Not Started": "#e74c3c"
        },
        "grade_pass": "#2ecc71",
        "grade_fail": "#e74c3c"
    }

    colors = cb_colors if colorblind else normal_colors

    # Charts
    attendance_chart = go.Figure(data=[go.Pie(
        labels=["Attendance", "Absent"],
        values=[average_attendance, remaining_attendance],
        hole=0.4,
        marker=dict(colors=colors["attendance"]),
        textinfo="label+percent"
    )])
    attendance_chart.update_layout(title="Artificial Intelligence - Attendance", title_x=0.5)

    assignment_chart = go.Figure(data=[go.Bar(
        x=assignment_names,
        y=[score if score is not None else 0 for score in assignment_scores],
        marker=dict(color=colors["scores"]),
        text=[f"{score}%" if score is not None else "N/A" for score in assignment_scores],
        textposition="outside"
    )])
    assignment_chart.update_layout(
        title="Assignment Scores",
        title_x=0.5,
        xaxis_title="Assignments",
        yaxis_title="Score",
        margin=dict(l=40, r=40, t=40, b=120),
        xaxis=dict(tickangle=0, automargin=True)
    )

    status_chart = go.Figure()
    for i in range(len(assignments)):
        status = assignment_statuses[i]
        name = assignment_names[i]
        weight = assignment_weights[i]
        status_chart.add_trace(go.Bar(
            x=["Artificial Intelligence"],
            y=[1],
            name=status,
            marker=dict(color=colors["statuses"].get(status, "#95a5a6")),
            hovertext=f"{name}<br>Status: {status}<br>Weight: {weight}%",
            hoverinfo="text"
        ))
    status_chart.update_layout(
        title="Assignments Status",
        barmode="stack",
        xaxis_title="Module",
        yaxis_title="Assignments",
        legend_title="Assignment Status"
    )

    return html.Div([
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content-inner", children=[
            html.H2("Artificial Intelligence Dashboard", style={
                'textAlign': 'center', 'color': '#34495e', 'marginBottom': '30px'
            }),

            html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '30px'}, children=[
                html.Div(dcc.Graph(figure=attendance_chart), style={
                    'backgroundColor': 'white', 'borderRadius': '10px', 'padding': '20px'
                }),
                html.Div(dcc.Graph(figure=assignment_chart), style={
                    'backgroundColor': 'white', 'borderRadius': '10px', 'padding': '20px'
                })
            ]),

            html.Div(style={
                'display': 'flex', 'justifyContent': 'center', 'marginTop': '30px', 'marginBottom': '30px'
            }, children=[
                html.Div(style={
                    'backgroundColor': 'white', 'borderRadius': '10px', 'padding': '20px',
                    'textAlign': 'center', 'width': '300px'
                }, children=[
                    html.H3("Current Grade", style={'color': '#34495e'}),
                    html.P(f"{current_grade:.2f}%", style={
                        'fontSize': '28px', 'fontWeight': 'bold',
                        'color': colors["grade_pass"] if current_grade >= 50 else colors["grade_fail"],
                        'backgroundColor': '#ecf0f1', 'borderRadius': '10px',
                        'display': 'inline-block', 'padding': '15px 30px'
                    })
                ])
            ]),

            html.Div(dcc.Graph(figure=status_chart), style={
                'backgroundColor': 'white', 'borderRadius': '10px',
                'padding': '20px', 'marginTop': '30px'
            }),

            html.Div(style={'display': 'flex', 'justifyContent': 'center', 'marginTop': '30px'}, children=[
                html.Div(style={
                    'backgroundColor': 'white', 'borderRadius': '10px',
                    'padding': '20px', 'width': '600px'
                }, children=[
                    html.H3("Ongoing Assignment Deadlines", style={
                        'textAlign': 'center', 'color': '#34495e'
                    }),
                    dash_table.DataTable(
                        columns=[
                            {"name": "Assignment", "id": "Assignment"},
                            {"name": "Deadline (DD/MM/YYYY)", "id": "Deadline"},
                            {"name": "Days Left", "id": "Days Left"}
                        ],
                        data=deadline_data,
                        style_header={'backgroundColor': '#3498db', 'color': 'white', 'fontWeight': 'bold'},
                        style_cell={'textAlign': 'center', 'padding': '10px'}
                    )
                ])
            ])
        ])
    ])

# Main layout wrapper
dash_ai.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

def init_dashboard(server):
    dash_ai.init_app(server)
