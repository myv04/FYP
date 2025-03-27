import dash
from dash import dcc, html
import plotly.graph_objs as go

# Create Dash app
dash_attendance = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_attendance/",
    suppress_callback_exceptions=True
)

# Attendance Data
attendance_percentage = 65
absent_percentage = 35

# Modules Attendance Data
module_attendance = {
    "Data Structures": 75,
    "Web Dev": 80,
    "AI": 70,
    "Database Management": 85,
    "Cybersecurity": 78
}

# Donut Chart (Overall Attendance)
attendance_chart = go.Figure(
    data=[go.Pie(
        labels=["Present", "Absent"],
        values=[attendance_percentage, absent_percentage],
        hole=0.5,
        marker=dict(colors=["#4CAF50", "#e74c3c"])
    )]
)
attendance_chart.update_layout(
    title="Overall Attendance",
    margin=dict(l=40, r=40, t=40, b=40)
)

# Bar Chart (Module-wise Attendance)
bar_chart = go.Figure(
    data=[go.Bar(
        x=list(module_attendance.keys()),
        y=list(module_attendance.values()),
        marker=dict(color=["#2ecc71", "#3498db", "#f1c40f", "#9b59b6", "#e67e22"])
    )]
)
bar_chart.update_layout(
    title="Module-wise Attendance",
    xaxis_title="Modules",
    yaxis_title="Attendance %",
    margin=dict(l=40, r=40, t=40, b=40)
)

# Dashboard Layout
dash_attendance.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f8f9fa', 'padding': '30px'}, children=[
    html.H2("Attendance Dashboard", style={'textAlign': 'center', 'color': '#34495e', 'marginBottom': '20px'}),

    # Attendance Donut Chart
    html.Div(dcc.Graph(figure=attendance_chart), style={
        'backgroundColor': 'white',
        'borderRadius': '10px',
        'padding': '20px',
        'marginBottom': '20px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
    }),

    # Module-wise Attendance Bar Chart
    html.Div(dcc.Graph(figure=bar_chart), style={
        'backgroundColor': 'white',
        'borderRadius': '10px',
        'padding': '20px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
    })
])

# Function to integrate with Flask
def init_dashboard(server):
    dash_attendance.init_app(server)
