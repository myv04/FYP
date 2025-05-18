import dash
from dash import html, Input, Output
import sqlite3


dash_courses = dash.Dash(
    __name__,
    routes_pathname_prefix="/course_dashboard/",
    suppress_callback_exceptions=True
)


def fetch_courses():
    try:
        conn = sqlite3.connect("courses.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, code, students_enrolled, lecturers_assigned, status FROM courses")
        courses = cursor.fetchall()
        conn.close()
        return courses
    except Exception as e:
        print(f"Database error: {e}")
        return []

def add_course():
    try:
        conn = sqlite3.connect("courses.db")
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO courses (name, code, students_enrolled, lecturers_assigned, status) VALUES (?, ?, ?, ?, ?)",
                       ("New Course", "NEW101", 0, 1, "Active"))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")


dash_courses.layout = html.Div(
    children=[
        html.H1("Course Management", style={"textAlign": "center"}),
        html.H2("Course Overview", style={"textAlign": "center"}),
        html.Table(
            style={
                "width": "90%",
                "margin": "20px auto",
                "borderCollapse": "collapse",
                "border": "1px solid #ccc"
            },
            children=[
                html.Thead(
                    html.Tr([
                        html.Th("Course Name", style={"border": "1px solid #ccc"}),
                        html.Th("Course Code", style={"border": "1px solid #ccc"}),
                        html.Th("Students Enrolled", style={"border": "1px solid #ccc"}),
                        html.Th("Lecturers Assigned", style={"border": "1px solid #ccc"}),
                        html.Th("Status", style={"border": "1px solid #ccc"}),
                        html.Th("Actions", style={"border": "1px solid #ccc"})
                    ])
                ),
                html.Tbody(id="course-table-body")
            ]
        ),
        html.Div(
            style={"textAlign": "center"},
            children=[
                html.Button("Add Course", id="add-course-btn", n_clicks=0),
                html.Button("Refresh Data", id="refresh-btn", n_clicks=0)
            ]
        )
    ]
)


@dash_courses.callback(
    Output("course-table-body", "children"),
    [Input("refresh-btn", "n_clicks"), Input("add-course-btn", "n_clicks")]
)
def update_table(refresh_clicks, add_clicks):
    
    if add_clicks > 0:
        add_course()

    
    courses = fetch_courses()

    table_rows = []
    for course in courses:
        table_rows.append(
            html.Tr([
                html.Td(course[1], style={"border": "1px solid #ccc"}),  # Course Name
                html.Td(course[2], style={"border": "1px solid #ccc"}),  # Course Code
                html.Td(course[3], style={"border": "1px solid #ccc"}),  # Students Enrolled
                html.Td(course[4], style={"border": "1px solid #ccc"}),  # Lecturers Assigned
                html.Td(course[5], style={"border": "1px solid #ccc"}),  # Status
                html.Td(
                    children=[
                        html.Button("Edit", id=f"edit-course-{course[0]}", style={"border": "1px solid #ccc"}),
                        html.Button("Delete", id=f"delete-course-{course[0]}", style={"border": "1px solid #ccc"})
                    ],
                    style={"border": "1px solid #ccc"}
                )
            ])
        )

    return table_rows


def init_course_dashboard(server):
    dash_courses.init_app(server)
