import dash
from dash import dcc, html
import plotly.graph_objs as go

# Create Dash app
dash_dsa = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_dsa/",  # Ensure it matches the URL in the iframe
    suppress_callback_exceptions=True
)

# Sample Data for Data Structures & Algorithms Exam
average_attendance = 85  
remaining_attendance = 100 - average_attendance  

# Exam Details
exam_name = "DSA Exam"
exam_score = 78  # Student's final exam score
exam_weight = 100  # Example weight for the exam

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
attendance_chart.update_layout(title="Data Structures & Algorithms - Attendance", title_x=0.5)

# Bar Chart (Exam Score)
exam_chart = go.Figure()
exam_chart.add_trace(go.Bar(
    x=["DSA Exam"],
    y=[exam_score],
    name="Exam Score",
    marker=dict(color="#2ecc71" if exam_score >= 50 else "#e74c3c"),
    text=[f"{exam_score}%"],
    textposition="auto"
))
exam_chart.update_layout(
    title="Data Structures & Algorithms Exam",
    title_x=0.5,
    xaxis_title="Exam",
    yaxis_title="Score"
)

# Exam Status Chart
status_chart = go.Figure()
status_chart.add_trace(go.Bar(
    x=["Data Structures & Algorithms"],
    y=[1],
    name="Exam",
    marker=dict(color="#2ecc71" if exam_score >= 50 else "#e74c3c"),
    hovertext=[f"{exam_name}, Weight: {exam_weight}%"],
    hoverinfo="text"
))
status_chart.update_layout(
    title="Exam Status",
    xaxis_title="Course",
    yaxis_title="Status",
    showlegend=False
)

# Dashboard Layout
dash_dsa.layout = html.Div(style={
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#f8f9fa',
    'padding': '30px'
}, children=[

    html.H2("Data Structures & Algorithms Dashboard", style={
        'textAlign': 'center',
        'color': '#34495e',
        'marginBottom': '30px'
    }),

    # First Row: Attendance & Exam Score Chart
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
        html.Div(dcc.Graph(figure=exam_chart), style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        })
    ]),

    # Current Grade Section
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
            html.P(f"{exam_score}%", style={
                'fontSize': '28px',
                'fontWeight': 'bold',
                'color': '#2ecc71' if exam_score >= 50 else '#e74c3c',
                'backgroundColor': '#ecf0f1',
                'borderRadius': '10px',
                'display': 'inline-block',
                'padding': '15px 30px',
                'boxShadow': '0 2px 5px rgba(0,0,0,0.1)'
            })
        ])
    ]),

    # Exam Status Chart
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
    dash_dsa.init_app(server)
