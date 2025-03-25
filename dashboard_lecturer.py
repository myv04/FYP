import dash
from dash import dcc, html
import plotly.graph_objs as go
import textwrap

# Create Dash app
dash_lecturer = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_lecturer/",
    suppress_callback_exceptions=True
)

# 📌 Sample Data (Lecturer Perspective)
average_attendance = 85
remaining_attendance = 100 - average_attendance

# 📌 Updated module labels (Only Two Modules)
module_labels = [
    "Course: Software Engineering (Module: Agile Development)",
    "Course: Data Science (Module: Machine Learning)"
]

# 📌 Updated Assignments Data with New Legends
assignments_data = {
    "Agile Development - Assignment 1 (Bugs and Fixes)": [42, 3, 3, 2],  # Completed, Completed with Penalty, Not Completed, Absent
    "Agile Development - Assignment 2 (Software Architecture)": [37, 8, 4, 1],
    "Machine Learning - Assignment 1 (Data Analysis)": [40, 8, 2, 0],
    "Machine Learning - Assignment 2 (Machine Learning)": [42, 5, 3, 0]
}

# 📌 Colors for consistency
colors = ["#1f77b4", "#ff7f0e"]
assignment_colors = ["#2ecc71", "#e74c3c", "#f1c40f", "#95a5a6"]  # Colors for Completed, Completed with Penalty, Not Completed, Absent

# 📌 Donut Chart (Average Attendance)
attendance_chart = go.Figure(
    data=[go.Pie(
        labels=["Attendance", "Absent"],
        values=[average_attendance, remaining_attendance],
        hole=0.5,
        marker=dict(colors=["#2ca02c", "#e0e0e0"])
    )]
)
attendance_chart.update_layout(title="📌 Average Attendance for Students taught by you", title_x=0.5)

# 📌 Horizontal Bar Chart (Module Performance - Average Scores)
module_chart = go.Figure(
    data=[go.Bar(
        y=module_labels,
        x=[82, 88],
        orientation="h",
        marker=dict(color=colors)
    )]
)
module_chart.update_layout(title="📊 Average Student Performance per Module (%)", xaxis_title="Average Score (%)", title_x=0.5)

# 📌 Stacked Bar Chart (Assignments Completion by Students - Updated)
stacked_chart = go.Figure()
categories = ["Completed", "Completed with Penalty", "Not Completed", "Absent"]

for i, category in enumerate(categories):
    stacked_chart.add_trace(go.Bar(
        x=list(assignments_data.keys()),
        y=[assignments_data[assignment][i] for assignment in assignments_data],
        name=category,
        marker=dict(color=assignment_colors[i])
    ))

# Use textwrap to break long text into multiple lines
wrapped_labels = [('<br>'.join(textwrap.wrap(label, width=20))) for label in assignments_data.keys()]

stacked_chart.update_layout(
    title="📑 Assignments Completion per Module",
    barmode="stack",
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=12),
        tickvals=list(assignments_data.keys()),
        ticktext=wrapped_labels,
        automargin=True,
    ),
    yaxis=dict(
        title="Number of Assignments",
        range=[0, 80]  # Updated y-axis range to accommodate up to 80
    ),
    margin=dict(b=200, l=50, r=50, t=100),  # Adjusted margins
    title_x=0.5,
    height=800,  # Increased chart height for better visibility
    width=1400   # Increased chart width to stretch it out
)

# 📌 Layout for Dashboard
dash_lecturer.layout = html.Div(style={
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#f8f9fa',
    'padding': '30px',
    'maxWidth': '1400px',  # Increased max width to match the chart
    'margin': '0 auto'  # Center the content
}, children=[
    html.H2("📊 Lecturer Performance Dashboard", style={
        'textAlign': 'center',
        'color': '#34495e',
        'marginBottom': '30px'
    }),

    # 📌 Top Row: Two Charts Side by Side (Attendance & Module Performance)
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
        html.Div(dcc.Graph(figure=module_chart), style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        })
    ]),

    # 📌 Bottom Row: Full-Width Stacked Chart for Assignments
    html.Div(dcc.Graph(figure=stacked_chart), style={
        'backgroundColor': 'white',
        'borderRadius': '10px',
        'padding': '20px',
        'marginTop': '30px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
        'width': '100%'  # Ensure the chart takes full width
    })
])

# 📌 Function to integrate with Flask
def init_lecturer_dashboard(server):
    dash_lecturer.init_app(server)
