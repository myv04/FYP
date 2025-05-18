import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import sqlite3
import json

# Fetch data
def fetch_dsa_data():
    conn = sqlite3.connect("student_performance.db")
    c = conn.cursor()
    c.execute("SELECT attendance, grade, exams_json FROM student_modules WHERE module_code = 'CS201'")
    row = c.fetchone()
    conn.close()
    if row:
        attendance, grade, exams_json = row
        exams = json.loads(exams_json)
        exam_score = exams[0]["score"] if exams else 0
        exam_name = exams[0]["name"] if exams else "DSA Exam"
        return attendance, grade, exam_name, exam_score
    return 0, 0, "DSA Exam", 0

# Dash setup
dash_dsa = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_dsa/",
    suppress_callback_exceptions=True
)

@dash_dsa.callback(
    Output("page-content", "children"),
    Input("url", "search")
)
def render_layout(search):
    colorblind = "cbmode=on" in search if search else False
    return generate_layout(colorblind)

def generate_layout(colorblind=False):
    average_attendance, current_grade, exam_name, exam_score = fetch_dsa_data()
    remaining_attendance = 100 - average_attendance

    # Palette switch
    primary_color = "#0072B2" if colorblind else "#2ecc71"
    secondary_color = "#D55E00" if colorblind else "#e74c3c"
    pie_colors = ["#009E73", "#e0e0e0"] if colorblind else ["#ff8d1a", "#e0e0e0"]

    # Charts
    attendance_chart = go.Figure(data=[go.Pie(
        labels=["Attendance", "Absent"],
        values=[average_attendance, remaining_attendance],
        hole=0.4,
        marker=dict(colors=pie_colors),
        textinfo="label+percent",
    )])
    attendance_chart.update_layout(title="Data Structures & Algorithms - Attendance", title_x=0.5)

    exam_chart = go.Figure()
    exam_chart.add_trace(go.Bar(
        x=["DSA Exam"],
        y=[exam_score],
        marker=dict(color=primary_color),
        text=[f"{exam_score}%"],
        textposition="auto",
    ))
    exam_chart.update_layout(
        title="Data Structures & Algorithms Exam",
        title_x=0.5,
        xaxis_title="Exam",
        yaxis_title="Score",
        yaxis=dict(range=[0, 100])
    )

    status_chart = go.Figure()
    status_chart.add_trace(go.Bar(
        x=["Data Structures & Algorithms"],
        y=[1],
        name="DSA Exam",
        marker=dict(color=primary_color),
        hovertext=f"{exam_name} - Score: {exam_score}%"
    ))
    status_chart.update_layout(
        title="Exam Status",
        barmode="stack",
        xaxis_title="Course",
        yaxis_title="Status",
        legend_title="Status"
    )

    return html.Div(style={
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f8f9fa',
        'padding': '30px'
    }, children=[
        html.H2("Data Structures & Algorithms Dashboard", style={
            'textAlign': 'left',
            'color': '#34495e',
            'marginBottom': '30px'
        }),

        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '30px'}, children=[
            html.Div(dcc.Graph(figure=attendance_chart), style={
                'backgroundColor': 'white',
                'borderRadius': '10px',
                'padding': '20px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
            }),
            html.Div(dcc.Graph(figure=exam_chart), style={
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
                    'color': primary_color if current_grade >= 50 else secondary_color,
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
        })
    ])

dash_dsa.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

def init_dashboard(server):
    dash_dsa.init_app(server)
