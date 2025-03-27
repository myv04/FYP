import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import dash_table

# Create Dash app
dash_student = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_student/",
    suppress_callback_exceptions=True
)

# Sample Data
average_attendance = 65  
remaining_attendance = 100 - average_attendance  

# Module labels and scores
module_labels = [
    "CS201: Data Structures & Algorithms",
    "CS202: Web Development",
    "CS203: Artificial Intelligence",
    "CS204: Database Management",
    "CS205: Cybersecurity"
]
module_scores = [70, 79, 25.5, 36, 68.8]  

# Assignments Data
assignments_data = {
    "CS202: Web Development": [
        {"name": "Responsive Design Project", "status": "Completed", "score": 82}
    ],
    "CS203: Artificial Intelligence": [
        {"name": "Neural Network Implementation", "status": "Completed", "score": 85},
        {"name": "Ethical Concerns in AI Development", "status": "Not Completed"},
        {"name": "Sentiment Analysis using NLP", "status": "Not Started"}
    ],
    "CS204: Database Management": [
        {"name": "Normalization Techniques", "status": "Completed", "score": 88},
        {"name": "SQL Query Optimization", "status": "Completed", "score": 92}
    ],
    "CS205: Cybersecurity": [
        {"name": "Network Security Protocols", "status": "Completed", "score": 95},
        {"name": "Ethical Hacking Fundamentals", "status": "Completed", "score": 88},
        {"name": "Malware Analysis", "status": "Not Started"}
    ]
}

# Exam Data with Updated Names
exam_data = {
    "CS201: Data Structures & Algorithms": {"name": "DSA Exam", "status": "Completed", "score": 78},
    "CS202: Web Development": {"name": "Web Dev Exam", "status": "Completed", "score": 76},
    "CS204: Database Management": {"name": "Database Exam", "status": "Not Completed"}
}

# Deadline Data
deadline_data = [
    {"Module": "CS203: Artificial Intelligence", "Assignment": "Ethical Concerns in AI Development", "Deadline": "21/03/2025", "Days Left": "10"},
    {"Module": "CS203: Artificial Intelligence", "Assignment": "Sentiment Analysis using NLP", "Deadline": "TBC", "Days Left": "TBC"},
    {"Module": "CS205: Cybersecurity", "Assignment": "Malware Analysis", "Deadline": "TBC", "Days Left": "TBC"}
]

# Colors for categories
status_colors = {
    "Completed": "#2ecc71",
    "Not Completed": "#e74c3c",
    "Not Started": "#f1c40f"
}

# Donut Chart (Average Attendance)
attendance_chart = go.Figure(
    data=[go.Pie(
        labels=["Attendance", "Absent"],
        values=[average_attendance, remaining_attendance],
        hole=0.5,
        marker=dict(colors=["#ff8d1a", "#e0e0e0"])
    )]
)
attendance_chart.update_layout(title="Average Attendance for the Year")

# Horizontal Bar Chart (Module Scores)
module_chart = go.Figure(
    data=[go.Bar(
        y=module_labels,
        x=module_scores,
        orientation="h",
        marker=dict(color=["#ff5733", "#ff8d1a", "#ffbd33", "#c70039", "#900c3f"])
    )]
)
module_chart.update_layout(
    title="Percentage of Grades per Module So Far",
    xaxis_title="Percentage (%)"
)

# Function to create a stacked bar chart with hover labels
def create_stacked_chart(selected_type):
    chart = go.Figure()
    
    if selected_type == "Assignments":
        for module, assignments in assignments_data.items():
            for assignment in assignments:
                status = assignment["status"]
                hover_text = f"{assignment['name']}<br>Status: {status}"
                
                if status == "Completed" and "score" in assignment:
                    hover_text += f"<br>Score: {assignment['score']}%"

                chart.add_trace(go.Bar(
                    x=[module],
                    y=[1],  
                    name=assignment["name"],
                    marker=dict(color=status_colors[status]),
                    text=hover_text,
                    hoverinfo="text"
                ))

    elif selected_type == "Exams":
        for module, exam in exam_data.items():
            status = exam["status"]
            hover_text = f"{exam['name']}<br>Status: {status}"
            
            if status == "Completed" and "score" in exam:
                hover_text += f"<br>Score: {exam['score']}%"

            chart.add_trace(go.Bar(
                x=[module],
                y=[1],
                name=exam["name"],
                marker=dict(color=status_colors[status]),
                text=hover_text,
                hoverinfo="text"
            ))

    chart.update_layout(
        title=f"{selected_type} Completion Status by Module",
        barmode="stack",
        xaxis_title="Modules",
        yaxis_title="Count",
        legend_title="Assignments/Exams"
    )
    return chart

# Default chart (Assignments view)
default_chart = create_stacked_chart("Assignments")

# Layout for Dashboard
dash_student.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f8f9fa', 'padding': '30px'}, children=[
    html.H2("Student Performance Dashboard", style={'textAlign': 'center', 'color': '#34495e', 'marginBottom': '30px'}),

    # Top Row: Attendance & Module Scores
    html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px'}, children=[
        html.Div(dcc.Graph(figure=attendance_chart), style={'backgroundColor': 'white', 'borderRadius': '10px', 'padding': '20px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
        html.Div(dcc.Graph(figure=module_chart), style={'backgroundColor': 'white', 'borderRadius': '10px', 'padding': '20px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'})
    ]),

    # Dropdown Filter (Centered & Styled)
    html.Div(style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'marginTop': '30px'}, children=[
        html.Label("Select Assessment Type:", style={'fontSize': '16px', 'marginRight': '10px'}),
        dcc.Dropdown(
            id='assessment-filter',
            options=[
                {'label': 'Assignments', 'value': 'Assignments'},
                {'label': 'Exams', 'value': 'Exams'}
            ],
            value='Assignments',
            clearable=False,
            style={'width': '300px'}
        )
    ]),

    # Stacked Bar Chart
    html.Div(dcc.Graph(id='stacked-chart'), style={'backgroundColor': 'white', 'borderRadius': '10px', 'padding': '20px', 'marginTop': '20px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),

    # Deadline Table
    html.Div([
        html.H3("Upcoming Deadlines", style={'textAlign': 'center', 'marginTop': '40px', 'color': '#34495e'}),
        dash_table.DataTable(
    columns=[
        {"name": "Module", "id": "Module"},
        {"name": "Assignment", "id": "Assignment"},  # ✅ Corrected to match deadline_data keys
        {"name": "Deadline", "id": "Deadline"},
        {"name": "Days Left", "id": "Days Left"}  # ✅ Now includes "Days Left" column
    ],
            data=deadline_data,
            style_table={'width': '100%', 'margin': 'auto'},
            style_header={'backgroundColor': '#4CAF50', 'color': 'white', 'fontWeight': 'bold', 'textAlign': 'center'},
            style_cell={'textAlign': 'center', 'padding': '10px'}
        )
    ], style={'marginTop': '20px'})
])

# Callback to update chart based on filter selection
@dash_student.callback(
    Output('stacked-chart', 'figure'),
    [Input('assessment-filter', 'value')]
)
def update_chart(selected_type):
    return create_stacked_chart(selected_type)

# Function to integrate with Flask
def init_dashboard(server):
    dash_student.init_app(server)
