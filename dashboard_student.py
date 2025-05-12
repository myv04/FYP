import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import dash_table
import sqlite3
import json
from urllib.parse import parse_qs, urlparse

# Create Dash app
dash_student = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_student/",
    suppress_callback_exceptions=True
)

# Function to fetch all modules from the database
def fetch_all_progress():
    conn = sqlite3.connect("student_performance.db")
    c = conn.cursor()
    c.execute("SELECT * FROM student_modules")
    rows = c.fetchall()
    conn.close()

    modules = []
    for row in rows:
        module = {
            "module_code": row[0],
            "module_name": row[1],
            "attendance": row[2],
            "grade": row[3],
            "assignments": json.loads(row[4]),
            "exams": json.loads(row[5]),
            "deadlines": json.loads(row[6])
        }
        modules.append(module)
    return modules

# Combine assignments and exams for stacked chart
def create_stacked_chart(chart_type, status_colors):
    chart = go.Figure()

    if chart_type == "Assignments":
        for module, assignments in assignments_data.items():
            for assignment in assignments:
                status = assignment["status"]
                hover_text = f"{assignment['name']}<br>Status: {status}"
                if "score" in assignment:
                    hover_text += f"<br>Score: {assignment['score']}%"

                chart.add_trace(go.Bar(
                    x=[module],
                    y=[1],
                    name=assignment["name"],
                    marker=dict(color=status_colors.get(status, "#95a5a6")),
                    text=hover_text,
                    hoverinfo="text"
                ))
    elif chart_type == "Exams":
        for module, exam in exam_data.items():
            status = exam["status"]
            hover_text = f"{exam['name']}<br>Status: {status}"
            if "score" in exam:
                hover_text += f"<br>Score: {exam['score']}%"

            chart.add_trace(go.Bar(
                x=[module],
                y=[1],
                name=exam["name"],
                marker=dict(color=status_colors.get(status, "#95a5a6")),
                text=hover_text,
                hoverinfo="text"
            ))

    chart.update_layout(
        title=f"{chart_type} Completion Status by Module",
        barmode="stack",
        xaxis_title="Modules",
        yaxis_title="Count",
        legend_title="Assignments/Exams"
    )
    return chart

# Generate layout dynamically with colorblind mode
def generate_layout(colorblind=False):
    global assignments_data, exam_data  # ensure we can reuse it

    modules = fetch_all_progress()

    average_attendance = 65
    remaining_attendance = 100 - average_attendance

    module_labels = [f'{m["module_code"]}: {m["module_name"]}' for m in modules]
    module_scores = [m["grade"] for m in modules]

    module_colors = ["#0072B2", "#D55E00", "#009E73", "#F0E442", "#56B4E9"] if colorblind else \
                    ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6"]

    status_colors = {
        "Completed": "#009E73" if colorblind else "#2ecc71",
        "Not Completed": "#E69F00" if colorblind else "#e74c3c",
        "Not Started": "#F0E442" if colorblind else "#f1c40f"
    }

    assignments_data = {}
    for module in modules:
        label = f'{module["module_code"]}: {module["module_name"]}'
        assignments_data[label] = module["assignments"]

    exam_data = {}
    for module in modules:
        label = f'{module["module_code"]}: {module["module_name"]}'
        for exam in module["exams"]:
            exam_data[label] = {
                "name": exam["name"],
                "status": exam["status"],
                "score": exam.get("score", None)
            }

    deadline_data = []
    for module in modules:
        for deadline in module["deadlines"]:
            deadline_data.append({
                "Module": f'{module["module_code"]}: {module["module_name"]}',
                "Assignment": deadline.get("name", "N/A"),
                "Deadline": deadline.get("deadline", "TBC"),
                "Days Left": deadline.get("days_left", "TBC")
            })

    # Attendance chart
    attendance_chart = go.Figure(data=[go.Pie(
        labels=["Attendance", "Absent"],
        values=[average_attendance, remaining_attendance],
        hole=0.5,
        marker=dict(colors=["#ff8d1a", "#e0e0e0"])
    )])
    attendance_chart.update_layout(title="Average Attendance for the Year", title_x=0.5)

    # Grades bar chart
    module_chart = go.Figure(data=[go.Bar(
        y=module_labels,
        x=module_scores,
        orientation="h",
        marker=dict(color=module_colors)
    )])
    module_chart.update_layout(
        title="Percentage of Grades per Module So Far",
        xaxis_title="Percentage (%)"
    )

    default_chart = create_stacked_chart("Assignments", status_colors)

    return html.Div(style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f8f9fa', 'padding': '30px'}, children=[
        html.H2("Student Performance Dashboard", style={'textAlign': 'center', 'color': '#34495e', 'marginBottom': '30px'}),

        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px'}, children=[
            html.Div(dcc.Graph(figure=attendance_chart), style={'backgroundColor': 'white', 'borderRadius': '10px', 'padding': '20px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
            html.Div(dcc.Graph(figure=module_chart), style={'backgroundColor': 'white', 'borderRadius': '10px', 'padding': '20px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'})
        ]),

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

        html.Div(dcc.Graph(id='stacked-chart', figure=default_chart), style={'backgroundColor': 'white', 'borderRadius': '10px', 'padding': '20px', 'marginTop': '20px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),

        html.Div([
            html.H3("Upcoming Deadlines", style={'textAlign': 'center', 'marginTop': '40px', 'color': '#34495e'}),
            dash_table.DataTable(
                columns=[
                    {"name": "Module", "id": "Module"},
                    {"name": "Assignment", "id": "Assignment"},
                    {"name": "Deadline", "id": "Deadline"},
                    {"name": "Days Left", "id": "Days Left"}
                ],
                data=deadline_data,
                style_table={'width': '100%', 'margin': 'auto'},
                style_header={'backgroundColor': '#4CAF50', 'color': 'white', 'fontWeight': 'bold', 'textAlign': 'center'},
                style_cell={'textAlign': 'center', 'padding': '10px'}
            )
        ], style={'marginTop': '20px'})
    ])

# Dynamic layout loader
dash_student.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

@dash_student.callback(
    Output("page-content", "children"),
    Input("url", "search")
)
def display_layout(search):
    colorblind = "cbmode=on" in search if search else False
    return generate_layout(colorblind=colorblind)

@dash_student.callback(
    Output('stacked-chart', 'figure'),
    [Input('assessment-filter', 'value')]
)
def update_chart(selected_type):
    search = dash.callback_context.inputs["url.search"] if "url.search" in dash.callback_context.inputs else ""
    colorblind = "cbmode=on" in search if search else False
    return create_stacked_chart(selected_type, {
        "Completed": "#009E73" if colorblind else "#2ecc71",
        "Not Completed": "#E69F00" if colorblind else "#e74c3c",
        "Not Started": "#F0E442" if colorblind else "#f1c40f"
    })

# Flask integration
def init_dashboard(server):
    dash_student.init_app(server)
