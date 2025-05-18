import dash
from dash import dcc, html, dash_table
import plotly.graph_objs as go
from datetime import datetime, timedelta
import sqlite3
import json


def save_module_data(module_code, module_name, attendance, grade, assignments, exams, deadlines):
    conn = sqlite3.connect("student_performance.db")
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO student_modules
        (module_code, module_name, attendance, grade, assignments_json, exams_json, deadlines_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        module_code,
        module_name,
        attendance,
        grade,
        json.dumps(assignments),
        json.dumps(exams),
        json.dumps(deadlines)
    ))
    conn.commit()
    conn.close()


dash_cybersecurity = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_cybersecurity/",
    suppress_callback_exceptions=True
)


average_attendance = 78
remaining_attendance = 100 - average_attendance

assignments = [
    {"name": "Network Security Protocols", "score": 95, "weight": 40, "status": "Completed"},
    {"name": "Ethical Hacking Fundamentals", "score": 88, "weight": 35, "status": "Completed"},
    {"name": "Malware Analysis", "score": None, "weight": 25, "status": "Not Started"},
]


total_weighted_score = sum((a["score"] / 100) * a["weight"] for a in assignments if a["score"] is not None)
current_grade = total_weighted_score


current_date = datetime.now()
deadline_data = []
for assignment in assignments:
    if assignment["status"] != "Completed":
        deadline_data.append({
            "Assignment": assignment["name"],
            "Deadline": "TBC" if assignment["status"] == "Not Started" else (current_date + timedelta(days=7)).strftime('%d/%m/%Y'),
            "Days Left": "TBC" if assignment["status"] == "Not Started" else (current_date + timedelta(days=7) - current_date).days
        })


save_module_data(
    module_code="CS205",
    module_name="Cybersecurity",
    attendance=average_attendance,
    grade=current_grade,
    assignments=[{k: a[k] for k in ["name", "score", "status"]} for a in assignments],
    exams=[],
    deadlines=deadline_data
)

# Donut Chart (Attendance)
attendance_chart = go.Figure(
    data=[go.Pie(
        labels=["Attendance", "Absent"],
        values=[average_attendance, remaining_attendance],
        hole=0.4,
        marker=dict(colors=["#2ecc71", "#e0e0e0"]),
        textinfo="label+percent",
    )]
)
attendance_chart.update_layout(title="Cybersecurity - Attendance", title_x=0.5)

# Bar Chart (Assignment Scores)
assignment_chart = go.Figure(
    data=[go.Bar(
        x=[a["name"] for a in assignments],
        y=[a["score"] if a["score"] is not None else 0 for a in assignments],
        marker=dict(color=["#2ecc71" if a["score"] is not None else "#e74c3c" for a in assignments]),
        text=[f"{a['score']}%" if a["score"] is not None else "N/A" for a in assignments],
        textposition="auto"
    )]
)
assignment_chart.update_layout(title="Assignment Scores", title_x=0.5, xaxis_title="Assignments", yaxis_title="Score")

# Assignment Status Chart
status_categories = ["Not Started", "Not Completed", "Completed"]
status_colors = {"Not Started": "#e74c3c", "Not Completed": "#f1c40f", "Completed": "#2ecc71"}

status_chart = go.Figure()
for status in status_categories:
    status_chart.add_trace(go.Bar(
        x=["Cybersecurity"] * len([a for a in assignments if a["status"] == status]),
        y=[1] * len([a for a in assignments if a["status"] == status]),
        name=status,
        marker=dict(color=status_colors[status]),
        hovertext=[f"{a['name']}, Weight: {a['weight']}% ({a['status']})" for a in assignments if a["status"] == status],
        hoverinfo="text"
    ))

status_chart.update_layout(
    title="Assignments Status",
    barmode="stack",
    xaxis_title="Module",
    yaxis_title="Assignments",
    legend_title="Assignment Status",
    legend=dict(itemclick="toggle", itemdoubleclick="toggleothers")
)

# Layout
dash_cybersecurity.layout = html.Div(style={
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#f8f9fa',
    'padding': '30px'
}, children=[
    html.H2("Cybersecurity Dashboard", style={
        'textAlign': 'center',
        'color': '#34495e',
        'marginBottom': '30px'
    }),

    html.Div(style={
        'display': 'grid',
        'gridTemplateColumns': '1fr 1fr',
        'gap': '30px',
        'justifyContent': 'center',
        'alignItems': 'center'
    }, children=[
        html.Div(dcc.Graph(figure=attendance_chart), style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        }),
        html.Div(dcc.Graph(figure=assignment_chart), style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        })
    ]),

    html.Div(style={
        'display': 'flex',
        'justifyContent': 'center',
        'marginTop': '30px',
        'marginBottom': '30px'
    }, children=[
        html.Div(style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
            'textAlign': 'center',
            'width': '300px'
        }, children=[
            html.H3("Current Grade", style={'color': '#34495e'}),
            html.P(f"{current_grade:.2f}%", style={
                'fontSize': '28px',
                'fontWeight': 'bold',
                'color': '#2ecc71' if current_grade >= 50 else '#e74c3c',
                'backgroundColor': '#ecf0f1',
                'borderRadius': '10px',
                'display': 'inline-block',
                'padding': '15px 30px',
                'boxShadow': '0 2px 5px rgba(0,0,0,0.1)'
            })
        ])
    ]),

    html.Div(dcc.Graph(figure=status_chart), style={
        'backgroundColor': 'white',
        'borderRadius': '10px',
        'padding': '20px',
        'marginTop': '30px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
    }),

    html.Div(style={
        'display': 'flex',
        'justifyContent': 'center',
        'marginTop': '30px'
    }, children=[
        html.Div(style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'width': '500px',
            'textAlign': 'center'
        }, children=[
            html.H3("Ongoing Assignment Deadlines", style={'color': '#34495e'}),
            dash_table.DataTable(
                columns=[
                    {"name": "Assignment", "id": "Assignment"},
                    {"name": "Deadline (DD/MM/YYYY)", "id": "Deadline"},
                    {"name": "Days Left", "id": "Days Left"}
                ],
                data=deadline_data,
                style_table={'margin': 'auto', 'width': '100%'},
                style_header={'backgroundColor': '#3498db', 'color': 'white', 'textAlign': 'center'},
                style_cell={'textAlign': 'center'}
            )
        ])
    ])
])


def init_dashboard(server):
    dash_cybersecurity.init_app(server)
