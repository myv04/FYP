from flask import Blueprint
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import json
import os


course_registers = Blueprint("course_registers", __name__)

def load_data():
    file_path = "course_registers.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("⚠️ JSON decode error in course_registers.json")
                return []
    else:
        print("⚠️ course_registers.json not found.")
        return []

def init_course_registers(app):
    data = load_data()
    if not data:
        data = [{"UNI ID": "", "NAME": "", "Role": ""}]  

    df = pd.DataFrame(data)

    dash_app = dash.Dash(
        name="course_registers",
        server=app,
        url_base_pathname="/course_registers/",
        suppress_callback_exceptions=True
    )

    courses = {
        "Software Engineering": "SE",
        "Data Science": "DS"
    }

    roles = ["All", "Student", "Lecturer", "Admin"]

    
    dash_app.layout = html.Div([
        html.H2("📜 Course Registers", style={"textAlign": "center", "marginBottom": "20px"}),

        html.Div([
            dcc.Dropdown(
                id="course-dropdown",
                options=[{"label": k, "value": v} for k, v in courses.items()],
                value="SE",
                style={
                    "width": "280px", "marginRight": "15px",
                    "fontSize": "17px"
                }
            ),
            dcc.Dropdown(
                id="role-dropdown",
                options=[{"label": r, "value": r} for r in roles],
                value="All",
                style={
                    "width": "220px", "marginRight": "15px",
                    "fontSize": "17px"
                }
            ),
            dcc.Input(
                id="search-input",
                type="text",
                placeholder="Search names or IDs (comma-separated)...",
                debounce=True,
                style={
                    "width": "350px", "marginRight": "15px",
                    "padding": "10px", "fontSize": "16px"
                }
            ),
            html.Button("Clear", id="clear-button", n_clicks=0, style={
                "fontSize": "16px", "padding": "10px 16px", "height": "44px",
                "backgroundColor": "#bdc3c7", "border": "none", "cursor": "pointer"
            })
        ], style={
            "display": "flex", "justifyContent": "center", "alignItems": "center", "marginBottom": "25px", "flexWrap": "wrap"
        }),

        html.Div(id="count-summary", style={
            "textAlign": "center", "fontSize": "18px", "marginBottom": "20px"
        }),

        dash_table.DataTable(
            id="course-table",
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict("records"),
            sort_action="native",
            page_size=25,
            style_table={"margin": "0 auto", "width": "95%"},
            style_cell={"textAlign": "left", "fontSize": "15px"},
            style_header={"backgroundColor": "#2980b9", "color": "white", "fontWeight": "bold"},
        )
    ])

    
    @dash_app.callback(
        Output("search-input", "value"),
        Input("clear-button", "n_clicks"),
        prevent_initial_call=True
    )
    def clear_input(n_clicks):
        return ""

    @dash_app.callback(
        [Output("course-table", "data"),
         Output("count-summary", "children")],
        [Input("course-dropdown", "value"),
         Input("role-dropdown", "value"),
         Input("search-input", "value")]
    )
    def update_table(course_prefix, role_filter, search_text):
        dff = pd.DataFrame(load_data())
        if dff.empty:
            return [], "No records found."

        
        filtered = dff[dff["UNI ID"].str.startswith(course_prefix)]

        
        if role_filter != "All":
            filtered = filtered[filtered["Role"] == role_filter]

        
        if search_text:
            search_terms = [term.strip().lower() for term in search_text.split(",") if term.strip()]
            if search_terms:
                filtered = filtered[filtered.apply(
                    lambda row: any(
                        term in str(row["NAME"]).lower() or term in str(row["UNI ID"]).lower()
                        for term in search_terms
                    ),
                    axis=1
                )]

        
        total = len(filtered)
        role_counts = filtered["Role"].value_counts().to_dict()
        summary = (
            f"🔢 {total} total | 🧑‍🎓 Students: {role_counts.get('Student', 0)} | "
            f"📚 Lecturers: {role_counts.get('Lecturer', 0)} | 🛠 Admins: {role_counts.get('Admin', 0)}"
        )

        return filtered.to_dict("records"), summary

    return dash_app
