import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.graph_objs as go
import sqlite3

# ✅ Initialize Dash app
dash_courses = dash.Dash(
    __name__,
    routes_pathname_prefix="/course_dashboard/",
    suppress_callback_exceptions=True
)

# ✅ Fetch data from database
def fetch_courses():
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, students_enrolled, lecturers_assigned FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return courses

# ✅ Layout for Dashboard
dash_courses.layout = html.Div(children=[
    html.H1("📚 Course Overview", style={'textAlign': 'center'}),

    # ✅ Table for Course Details
    dash_table.DataTable(
        id="course-table",
        columns=[
            {"name": "Course Name", "id": "name"},
            {"name": "Students Enrolled", "id": "students"},
            {"name": "Lecturers Assigned", "id": "lecturers"}
        ],
        style_table={"width": "80%", "margin": "auto"},
        style_cell={"textAlign": "center"},
        sort_action="native"
    ),

    # ✅ Bar Chart for Course Insights
    dcc.Graph(id="course-bar-chart"),

    # ✅ Refresh Button
    html.Button("Refresh Data", id="refresh-btn", n_clicks=0, style={'margin': '20px'})
])

# ✅ Callbacks to update the dashboard
@dash_courses.callback(
    [Output("course-table", "data"), Output("course-bar-chart", "figure")],
    [Input("refresh-btn", "n_clicks")]
)
def update_dashboard(_):
    courses = fetch_courses()

    # ✅ Prepare table data
    table_data = [
        {"name": row[0], "students": row[1], "lecturers": row[2]} for row in courses
    ]

    # ✅ Prepare bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[row[0] for row in courses], y=[row[1] for row in courses], name="Students Enrolled"))
    fig.add_trace(go.Bar(x=[row[0] for row in courses], y=[row[2] for row in courses], name="Lecturers Assigned"))
    fig.update_layout(title="📊 Course Insights", xaxis_title="Course", barmode="group")

    return table_data, fig

# ✅ Function to integrate with Flask
def init_course_dashboard(server):
    dash_courses.init_app(server)
