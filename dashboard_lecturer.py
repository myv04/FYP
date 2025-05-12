import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import textwrap
from incase.shared_dashboard_data import get_processed_se_data, get_processed_ds_data

# Initialize Dash app
dash_lecturer = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_lecturer/",
    suppress_callback_exceptions=True
)

# Load data
se_df = get_processed_se_data()
ds_df = get_processed_ds_data()

# Layout generator with colorblind toggle
def generate_layout(colorblind=False):
    average_attendance = round((se_df["Attendance"].mean() + ds_df["Attendance"].mean()) / 2, 2)
    remaining_attendance = 100 - average_attendance

    module_labels = [
        "Course: Software Engineering (Module: Agile Development)",
        "Course: Data Science (Module: Machine Learning)"
    ]
    module_scores = [
        round(se_df["Final Grade"].mean(), 2),
        round(ds_df["Final Grade"].mean(), 2)
    ]

    assignment_1_se = se_df["Assignment 1 Status"].value_counts().to_dict()
    assignment_2_se = se_df["Assignment 2 Status"].value_counts().to_dict()
    assignment_1_ds = ds_df["Assignment 1 Status"].value_counts().to_dict()
    assignment_2_ds = ds_df["Assignment 2 Status"].value_counts().to_dict()

    assignments_data = {
        "Agile Development - Assignment 1 (Bugs and Fixes)": [
            assignment_1_se.get("Completed", 0),
            assignment_1_se.get("Completed with Penalty", 0),
            assignment_1_se.get("Not Completed", 0),
            assignment_1_se.get("Absent", 0)
        ],
        "Agile Development - Assignment 2 (Software Architecture)": [
            assignment_2_se.get("Completed", 0),
            assignment_2_se.get("Completed with Penalty", 0),
            assignment_2_se.get("Not Completed", 0),
            assignment_2_se.get("Absent", 0)
        ],
        "Machine Learning - Assignment 1 (Data Analysis)": [
            assignment_1_ds.get("Completed", 0),
            assignment_1_ds.get("Completed with Penalty", 0),
            assignment_1_ds.get("Not Completed", 0),
            assignment_1_ds.get("Absent", 0)
        ],
        "Machine Learning - Assignment 2 (Machine Learning)": [
            assignment_2_ds.get("Completed", 0),
            assignment_2_ds.get("Completed with Penalty", 0),
            assignment_2_ds.get("Not Completed", 0),
            assignment_2_ds.get("Absent", 0)
        ]
    }

    # Color palettes
    module_colors = ["#0072B2", "#D55E00"] if colorblind else ["#1f77b4", "#ff7f0e"]
    assignment_colors = ["#009E73", "#F0E442", "#E69F00", "#56B4E9"] if colorblind else ["#2ecc71", "#e74c3c", "#f1c40f", "#95a5a6"]

    # Charts
    attendance_chart = go.Figure(data=[go.Pie(
        labels=["Attendance", "Absent"],
        values=[average_attendance, remaining_attendance],
        hole=0.5,
        marker=dict(colors=["#2ca02c", "#e0e0e0"])
    )])
    attendance_chart.update_layout(title="📌 Average Attendance for Students taught by you", title_x=0.5)

    module_chart = go.Figure(data=[go.Bar(
        y=module_labels,
        x=module_scores,
        orientation="h",
        marker=dict(color=module_colors)
    )])
    module_chart.update_layout(
        title="📊 Average Student Performance per Module (%)",
        xaxis_title="Average Score (%)",
        title_x=0.5
    )

    stacked_chart = go.Figure()
    categories = ["Completed", "Completed with Penalty", "Not Completed", "Absent"]
    for i, category in enumerate(categories):
        stacked_chart.add_trace(go.Bar(
            x=list(assignments_data.keys()),
            y=[assignments_data[key][i] for key in assignments_data],
            name=category,
            marker=dict(color=assignment_colors[i])
        ))

    wrapped_labels = [('<br>'.join(textwrap.wrap(label, width=20))) for label in assignments_data.keys()]
    stacked_chart.update_layout(
        title="📑 Assignments Completion per Module",
        barmode="stack",
        xaxis=dict(
            tickvals=list(assignments_data.keys()),
            ticktext=wrapped_labels,
            automargin=True
        ),
        yaxis=dict(title="Number of Assignments", range=[0, 80]),
        margin=dict(b=200, l=50, r=50, t=100),
        title_x=0.5,
        height=800,
        width=1400
    )

    return html.Div(style={
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f8f9fa',
        'padding': '30px',
        'maxWidth': '1400px',
        'margin': '0 auto'
    }, children=[
        html.H2("📊 Lecturer Performance Dashboard", style={
            'textAlign': 'center',
            'color': '#34495e',
            'marginBottom': '30px'
        }),
        html.Div(style={
            'display': 'grid',
            'gridTemplateColumns': '1fr 1fr',
            'gap': '30px'
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
        html.Div(dcc.Graph(figure=stacked_chart), style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'marginTop': '30px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        })
    ])


# Layout with routing support for colorblind mode
dash_lecturer.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content", children=generate_layout().children)
])

@dash_lecturer.callback(
    Output("page-content", "children"),
    Input("url", "search")
)
def update_layout(search):
    colorblind = "cbmode=on" in search if search else False
    return generate_layout(colorblind=colorblind).children

# Flask integration
def init_lecturer_dashboard(server):
    dash_lecturer.init_app(server)
