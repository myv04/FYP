from flask import Blueprint
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd

course_registers_bp = Blueprint("course_registers", __name__)

def init_course_registers(flask_app):
    dash_app = dash.Dash(
        __name__,
        server=flask_app,
        url_base_pathname="/course_registers/dash/",
        suppress_callback_exceptions=True
    )

    # Define Data for Both Courses
    data_science_data = [
        {"UNI ID": "DS1012", "NAME": "Alex Carter", "Role": "Student"},
        {"UNI ID": "DS4772", "NAME": "Bella Sanders", "Role": "Student"},
        {"UNI ID": "DS5732", "NAME": "Cameron Hughes", "Role": "Student"},
        {"UNI ID": "DS7477", "NAME": "Diana Wright", "Role": "Student"},
        {"UNI ID": "DS7861", "NAME": "Ethan Parker", "Role": "Student"},
        {"UNI ID": "DS9221", "NAME": "Felicity James", "Role": "Student"},
        {"UNI ID": "DS7221", "NAME": "Gabriel Lewis", "Role": "Student"},
        {"UNI ID": "DS6154", "NAME": "Hannah Stone", "Role": "Student"},
        {"UNI ID": "DS1486", "NAME": "Ian Turner", "Role": "Student"},
        {"UNI ID": "DS3966", "NAME": "Jasmine Collins", "Role": "Student"},
        {"UNI ID": "DS1166", "NAME": "Kevin Morris", "Role": "Student"},
        {"UNI ID": "DS6217", "NAME": "Lara Watson", "Role": "Student"},
        {"UNI ID": "DS6534", "NAME": "Michael Griffin", "Role": "Student"},
        {"UNI ID": "DS7280", "NAME": "Natalie Cooper", "Role": "Student"},
        {"UNI ID": "DS1929", "NAME": "Owen Richardson", "Role": "Student"},
        {"UNI ID": "DS8704", "NAME": "Paige Scott", "Role": "Student"},
        {"UNI ID": "DS5134", "NAME": "Quentin Ramirez", "Role": "Student"},
        {"UNI ID": "DS6980", "NAME": "Rebecca Bennett", "Role": "Student"},
        {"UNI ID": "DS3986", "NAME": "Stephen Howard", "Role": "Student"},
        {"UNI ID": "DS7376", "NAME": "Tracy Bell", "Role": "Student"},
        {"UNI ID": "DS6091", "NAME": "Ulysses Barnes", "Role": "Student"},
        {"UNI ID": "DS4026", "NAME": "Victoria Foster", "Role": "Student"},
        {"UNI ID": "DS4819", "NAME": "Walter Henderson", "Role": "Student"},
        {"UNI ID": "DS9065", "NAME": "Xander Nelson", "Role": "Student"},
        {"UNI ID": "DS9746", "NAME": "Yvette Campbell", "Role": "Student"},
        {"UNI ID": "DS3253", "NAME": "Zane Mitchell", "Role": "Student"},
        {"UNI ID": "DS6503", "NAME": "Amelia Ross", "Role": "Student"},
        {"UNI ID": "DS2850", "NAME": "Benjamin Ward", "Role": "Student"},
        {"UNI ID": "DS4513", "NAME": "Chloe Edwards", "Role": "Student"},
        {"UNI ID": "DS5015", "NAME": "David Fisher", "Role": "Student"},
        {"UNI ID": "DS3479", "NAME": "Emma Butler", "Role": "Student"},
        {"UNI ID": "DS7297", "NAME": "Frederick Murphy", "Role": "Student"},
        {"UNI ID": "DS7372", "NAME": "Grace Price", "Role": "Student"},
        {"UNI ID": "DS9041", "NAME": "Henry Stewart", "Role": "Student"},
        {"UNI ID": "DS6180", "NAME": "Isabella Torres", "Role": "Student"},
        {"UNI ID": "DS7380", "NAME": "Jackie Peterson", "Role": "Student"},
        {"UNI ID": "DS2398", "NAME": "Kurt Bailey", "Role": "Student"},
        {"UNI ID": "DS6589", "NAME": "Lucy Jenkins", "Role": "Student"},
        {"UNI ID": "DS2762", "NAME": "Mason Cooper", "Role": "Student"},
        {"UNI ID": "DS5804", "NAME": "Nina Adams", "Role": "Student"},
        {"UNI ID": "DS5362", "NAME": "Oscar Flores", "Role": "Student"},
        {"UNI ID": "DS5197", "NAME": "Penelope Russell", "Role": "Student"},
        {"UNI ID": "DS4441", "NAME": "Ryan Powell", "Role": "Student"},
        {"UNI ID": "DS8748", "NAME": "Sophia Simmons", "Role": "Student"},
        {"UNI ID": "DS8533", "NAME": "Theodore White", "Role": "Student"},
        {"UNI ID": "DS7065", "NAME": "Ursula Martin", "Role": "Student"},
        {"UNI ID": "DS3499", "NAME": "Vince Brown", "Role": "Student"},
        {"UNI ID": "DS5325", "NAME": "William Gonzales", "Role": "Student"},
        {"UNI ID": "DS7707", "NAME": "Xenia Moore", "Role": "Student"},
        {"UNI ID": "DS3801", "NAME": "Zoe Walker", "Role": "Student"},
        {"UNI ID": "DS0001", "NAME": "Dr. Emily Carter", "Role": "Lecturer"},
        {"UNI ID": "DS0002", "NAME": "Prof. Michael Reed", "Role": "Lecturer"},
        {"UNI ID": "DS0003", "NAME": "Dr. Sarah Johnson", "Role": "Lecturer"},
        {"UNI ID": "DS9991", "NAME": "Lisa Thompson", "Role": "Admin"},
        {"UNI ID": "DS9992", "NAME": "Mark Wilson", "Role": "Admin"},
    ]

    software_data = [
        {"UNI ID": "SE6352", "NAME": "Alice Johnson", "Role": "Student"},
        {"UNI ID": "SE8934", "NAME": "Bob Smith", "Role": "Student"},
        {"UNI ID": "SE6281", "NAME": "Charlie Davis", "Role": "Student"},
        {"UNI ID": "SE7925", "NAME": "David Martinez", "Role": "Student"},
        {"UNI ID": "SE6726", "NAME": "Eve Brown", "Role": "Student"},
        {"UNI ID": "SE1122", "NAME": "Frank Wilson", "Role": "Student"},
        {"UNI ID": "SE9571", "NAME": "Grace Taylor", "Role": "Student"},
        {"UNI ID": "SE3929", "NAME": "Hank Anderson", "Role": "Student"},
        {"UNI ID": "SE7971", "NAME": "Ivy Thomas", "Role": "Student"},
        {"UNI ID": "SE5495", "NAME": "Jack White", "Role": "Student"},
        {"UNI ID": "SE8563", "NAME": "Karen Harris", "Role": "Student"},
        {"UNI ID": "SE3882", "NAME": "Leo Martin", "Role": "Student"},
        {"UNI ID": "SE4819", "NAME": "Mona Clark", "Role": "Student"},
        {"UNI ID": "SE9943", "NAME": "Nathan Lewis", "Role": "Student"},
        {"UNI ID": "SE3065", "NAME": "Olivia Hall", "Role": "Student"},
        {"UNI ID": "SE8912", "NAME": "Peter Allen", "Role": "Student"},
        {"UNI ID": "SE9568", "NAME": "Quincy Young", "Role": "Student"},
        {"UNI ID": "SE7547", "NAME": "Rachel King", "Role": "Student"},
        {"UNI ID": "SE3979", "NAME": "Steve Wright", "Role": "Student"},
        {"UNI ID": "SE5835", "NAME": "Tina Scott", "Role": "Student"},
        {"UNI ID": "SE8744", "NAME": "Uma Green", "Role": "Student"},
        {"UNI ID": "SE7255", "NAME": "Victor Adams", "Role": "Student"},
        {"UNI ID": "SE5697", "NAME": "Wendy Baker", "Role": "Student"},
        {"UNI ID": "SE4181", "NAME": "Xander Nelson", "Role": "Student"},
        {"UNI ID": "SE4762", "NAME": "Yvonne Carter", "Role": "Student"},
        {"UNI ID": "SE5070", "NAME": "Zachary Mitchell", "Role": "Student"},
        {"UNI ID": "SE8734", "NAME": "Aaron Perez", "Role": "Student"},
        {"UNI ID": "SE2053", "NAME": "Bella Roberts", "Role": "Student"},
        {"UNI ID": "SE8111", "NAME": "Cody Gonzalez", "Role": "Student"},
        {"UNI ID": "SE9150", "NAME": "Diana Campbell", "Role": "Student"},
        {"UNI ID": "SE3215", "NAME": "Ethan Rodriguez", "Role": "Student"},
        {"UNI ID": "SE5869", "NAME": "Fiona Moore", "Role": "Student"},
        {"UNI ID": "SE6168", "NAME": "George Edwards", "Role": "Student"},
        {"UNI ID": "SE8238", "NAME": "Holly Flores", "Role": "Student"},
        {"UNI ID": "SE3932", "NAME": "Ian Cooper", "Role": "Student"},
        {"UNI ID": "SE7659", "NAME": "Julia Murphy", "Role": "Student"},
        {"UNI ID": "SE4522", "NAME": "Kevin Reed", "Role": "Student"},
        {"UNI ID": "SE9236", "NAME": "Laura Cox", "Role": "Student"},
        {"UNI ID": "SE1428", "NAME": "Mike Ward", "Role": "Student"},
        {"UNI ID": "SE8043", "NAME": "Nina Peterson", "Role": "Student"},
        {"UNI ID": "SE7543", "NAME": "Oscar Gray", "Role": "Student"},
        {"UNI ID": "SE3569", "NAME": "Paula Jenkins", "Role": "Student"},
        {"UNI ID": "SE3900", "NAME": "Quinn Russell", "Role": "Student"},
        {"UNI ID": "SE8183", "NAME": "Randy Torres", "Role": "Student"},
        {"UNI ID": "SE3509", "NAME": "Samantha Stevens", "Role": "Student"},
        {"UNI ID": "SE1763", "NAME": "Tommy Parker", "Role": "Student"},
        {"UNI ID": "SE9793", "NAME": "Ursula Evans", "Role": "Student"},
        {"UNI ID": "SE5731", "NAME": "Vince Morgan", "Role": "Student"},
        {"UNI ID": "SE9781", "NAME": "Whitney Bell", "Role": "Student"},
        {"UNI ID": "SE2024", "NAME": "Xavier Phillips", "Role": "Student"},
        {"UNI ID": "SE0001", "NAME": "Dr. James Anderson", "Role": "Lecturer"},
        {"UNI ID": "SE0002", "NAME": "Prof. Anna White", "Role": "Lecturer"},
        {"UNI ID": "SE0003", "NAME": "Dr. Robert Brown", "Role": "Lecturer"},
        {"UNI ID": "SE9991", "NAME": "John Spencer", "Role": "Admin"},
        {"UNI ID": "SE9992", "NAME": "Emma Davis", "Role": "Admin"},
    ]

    df = pd.DataFrame(data_science_data + software_data)

    dash_app.layout = html.Div([
        html.H1("📜 Course Registers", style={"textAlign": "center"}),
        html.Div([
            dcc.Dropdown(
                id="course-dropdown",
                options=[
                    {"label": "Software Engineering", "value": "SE"},
                    {"label": "Data Science", "value": "DS"}
                ],
                value="SE",
                clearable=False,
                style={"width": "40%", "marginRight": "10px"}
            ),
            dcc.Dropdown(
                id="role-dropdown",
                options=[
                    {"label": "All", "value": "All"},
                    {"label": "Student", "value": "Student"},
                    {"label": "Lecturer", "value": "Lecturer"},
                    {"label": "Admin", "value": "Admin"}
                ],
                value="All",
                clearable=False,
                style={"width": "40%"}
            )
        ], style={"display": "flex", "justifyContent": "center", "marginBottom": "20px"}),
        dash_table.DataTable(
            id="register-table",
            columns=[
                {"name": "UNI ID", "id": "UNI ID"},
                {"name": "NAME", "id": "NAME"},
                {"name": "Role", "id": "Role"}
            ],
            style_table={"margin": "auto", "width": "80%"},
            style_cell={"textAlign": "left", "padding": "10px"},
            style_header={
                "backgroundColor": "#2980b9",
                "color": "white",
                "fontWeight": "bold"
            }
        )
    ])

    @dash_app.callback(
        Output("register-table", "data"),
        [Input("course-dropdown", "value"),
         Input("role-dropdown", "value")]
    )
    def update_table(selected_course, selected_role):
        filtered_df = df[df["UNI ID"].str.startswith(selected_course)]
        if selected_role != "All":
            filtered_df = filtered_df[filtered_df["Role"] == selected_role]
        return filtered_df.to_dict("records")

    @course_registers_bp.route("/course_registers/dash/")
    def dash_app():
        return dash_app.index()

    flask_app.register_blueprint(course_registers_bp)

    return dash_app
