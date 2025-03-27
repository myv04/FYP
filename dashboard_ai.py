import dash
from dash import dcc, html, dash_table
import plotly.graph_objs as go
from datetime import datetime, timedelta

# Create Dash app
dash_ai = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_ai/",
    suppress_callback_exceptions=True
)

# Sample Data
average_attendance = 75
remaining_attendance = 100 - average_attendance

# Fixed Assignment Data
assignment_names = [
    "Neural Network Implementation",
    "Ethical Concerns in AI Development",
    "Sentiment Analysis using NLP"
]
assignment_statuses = ["Completed", "Not Completed", "Not Started"]
assignment_scores = [85, None, None]  # Only completed assignments have scores
assignment_weights = [30, 40, 30]  # Percentage weight of each assignment

# Count Statuses
completed_count = assignment_statuses.count("Completed")
in_progress_count = assignment_statuses.count("Not Completed")
not_started_count = assignment_statuses.count("Not Started")

# Generate Deadlines for Ongoing Assignments (Ensure TBC for "Not Started")
current_date = datetime.now()
deadline_data = []
for i in range(len(assignment_names)):
    if assignment_statuses[i] != "Completed":  # Exclude completed assignments
        deadline_data.append({
            "Assignment": assignment_names[i],
            "Deadline": "TBC" if assignment_statuses[i] == "Not Started" else (current_date + timedelta(days=(7 + i * 3))).strftime('%d/%m/%Y'),
            "Days Left": "TBC" if assignment_statuses[i] == "Not Started" else (current_date + timedelta(days=(7 + i * 3)) - current_date).days
        })

# Calculate Weighted Grade
total_weighted_score = sum((assignment_scores[i] / 100) * assignment_weights[i] for i in range(len(assignment_scores)) if assignment_scores[i] is not None)
current_grade = total_weighted_score  # Directly reflects weighted contribution

# Donut Chart (Attendance)
attendance_chart = go.Figure(
    data=[go.Pie(
        labels=["Attendance", "Absent"],
        values=[average_attendance, remaining_attendance],
        hole=0.4,
        marker=dict(colors=["#3498db", "#e0e0e0"]),
        textinfo="label+percent",
    )]
)
attendance_chart.update_layout(title="Artificial Intelligence - Attendance", title_x=0.5)

# Bar Chart (Assignment Scores) - Fixed Labels
assignment_chart = go.Figure(
    data=[go.Bar(
        x=assignment_names,
        y=[score if score is not None else 0 for score in assignment_scores],
        marker=dict(color=["#2ecc71" if score is not None else "#e74c3c" for score in assignment_scores]),
        text=[f"{score}%" if score is not None else "N/A" for score in assignment_scores],
        textposition="outside",  # Ensures labels are properly visible
    )]
)
assignment_chart.update_layout(
    title="Assignment Scores",
    title_x=0.5,
    xaxis_title="Assignments",
    yaxis_title="Score",
    xaxis=dict(
        tickangle=0,  # Keep text horizontal
        tickmode="array",
        tickvals=list(range(len(assignment_names))),
        ticktext=assignment_names,
        automargin=True  # Ensures proper spacing
    ),
    margin=dict(l=40, r=40, t=40, b=120)  # Extra bottom margin for names
)

# Assignment Status Chart
status_categories = ["Not Started", "Not Completed", "Completed"]
status_colors = {"Not Started": "#e74c3c", "Not Completed": "#f1c40f", "Completed": "#2ecc71"}

status_chart = go.Figure()
for i in range(len(assignment_names)):
    status_chart.add_trace(go.Bar(
        x=["Artificial Intelligence"],
        y=[1],  # Each assignment counts as 1
        name=assignment_statuses[i],
        marker=dict(
            color=status_colors[assignment_statuses[i]]
        ),
        hovertext=f"{assignment_names[i]}, Weight: {assignment_weights[i]}% ({assignment_statuses[i]})"
    ))

status_chart.update_layout(
    title="Assignments Status",
    barmode="stack",
    xaxis_title="Module",
    yaxis_title="Assignments",
    legend_title="Assignment Status",
    legend=dict(itemclick="toggle", itemdoubleclick="toggleothers")
)

# Dashboard Layout
dash_ai.layout = html.Div(style={
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#f8f9fa',
    'padding': '30px'
}, children=[

    html.H2("Artificial Intelligence Dashboard", style={
        'textAlign': 'center', 
        'color': '#34495e', 
        'marginBottom': '30px'
    }),

    # First Row: Attendance & Assignment Scores Charts
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

    # Assignment Status Chart
    html.Div(dcc.Graph(figure=status_chart), style={
        'backgroundColor': 'white',
        'borderRadius': '10px',
        'padding': '20px',
        'marginTop': '30px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
    }),

    # Updated Assignment Deadlines Table
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
            'width': '600px'
        }, children=[
            html.H3("Ongoing Assignment Deadlines", style={'color': '#34495e', 'textAlign': 'center'}),
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

# Function to integrate with Flask
def init_dashboard(server):
    dash_ai.init_app(server)
