import dash
from dash import dcc, html
import plotly.graph_objs as go

# Create Dash app
dash_webdev = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_webdev/",
    suppress_callback_exceptions=True
)

# Sample Data
average_attendance = 80
remaining_attendance = 100 - average_attendance

# Exam and Assignment Data
exam_name = "Final Web Development Exam"
assignment_name = "Responsive Design Project"
assignment_status = "Completed"
assignment_score = 82  # More realistic
exam_score = 76  # More realistic

# Weight Distribution
exam_weight = 50
assignment_weight = 50

# Calculate Weighted Grade
assignment_weighted = (assignment_score / 100) * assignment_weight
exam_weighted = (exam_score / 100) * exam_weight
current_grade = assignment_weighted + exam_weighted

# Donut Chart (Attendance)
attendance_chart = go.Figure(
    data=[go.Pie(
        labels=["Attendance", "Absent"],
        values=[average_attendance, remaining_attendance],
        hole=0.4,
        marker=dict(colors=["#ff8d1a", "#e0e0e0"]),
        textinfo="label+percent",
    )]
)
attendance_chart.update_layout(title="Web Development - Attendance", title_x=0.5)

# Bar Chart (Exam and Assignment Scores)
exam_assignment_chart = go.Figure()
exam_assignment_chart.add_trace(go.Bar(
    x=[exam_name, assignment_name],
    y=[exam_score, assignment_score],
    marker=dict(color=["#3498db", "#2ecc71"]),
    text=[f"{exam_score}%", f"{assignment_score}%"],  # Display text directly on bars
    textposition="auto",
))
exam_assignment_chart.update_layout(
    title="Exam & Assignment Scores",
    title_x=0.5,
    xaxis_title="Assessments",
    yaxis_title="Score",
    yaxis=dict(range=[0, 100]),  # Ensures full visibility of scores
)

# Exam & Assignment Status Chart (With Hover Info for Weight)
status_chart = go.Figure()
status_chart.add_trace(go.Bar(
    x=["Web Development"],
    y=[1],
    name="Exam Completed",
    marker=dict(color="#3498db"),
    hovertext=f"{exam_name} - Weight: {exam_weight}%"
))
status_chart.add_trace(go.Bar(
    x=["Web Development"],
    y=[1],
    name="Assignment Completed",
    marker=dict(color="#2ecc71"),
    hovertext=f"{assignment_name} - Weight: {assignment_weight}%"
))
status_chart.update_layout(
    title="Exam & Assignment Status",
    barmode="stack",
    xaxis_title="Module",
    yaxis_title="Assessments",
    legend_title="Status"
)

# Dashboard Layout
dash_webdev.layout = html.Div(style={
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#f8f9fa',
    'padding': '30px'
}, children=[

    html.H2("Web Development Dashboard", style={
        'textAlign': 'center', 
        'color': '#34495e', 
        'marginBottom': '30px'
    }),

    # First Row: Attendance & Exam/Assignment Scores
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
        html.Div(dcc.Graph(figure=exam_assignment_chart), style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        })
    ]),

    # Current Grade
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

    # Exam & Assignment Status Chart
    html.Div(dcc.Graph(figure=status_chart), style={
        'backgroundColor': 'white',
        'borderRadius': '10px',
        'padding': '20px',
        'marginTop': '30px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
    })
])

# Function to integrate with Flask
def init_dashboard(server):
    dash_webdev.init_app(server)
