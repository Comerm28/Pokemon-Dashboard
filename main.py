import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px

# Path to CSV
CSV_FILE = 'pokemon_dashboard.csv'

# Load and preprocess data
def load_data():
    df = pd.read_csv(CSV_FILE)
    # Convert playtime to minutes
    df[['hours', 'minutes']] = df['Playtime'].str.split(':', expand=True).astype(int)
    df['Playtime_minutes'] = df['hours'] * 60 + df['minutes']
    return df

df = load_data()

# Summary statistics
total_entries = len(df)
unique_games = df['Game'].nunique()
total_playtime_hours = df['Playtime_minutes'].sum() / 60
avg_playtime_hours = df['Playtime_minutes'].mean() / 60

# Averages for numeric fields
numeric_cols = [
    'Pokedex Caught', 'Pokedex Seen', 'Pokemon in Box', 'Money',
    'Legendaries Caught', 'Shinies Caught', 'Fun Rating', 'Team Favorability'
]
avg_stats = df[numeric_cols].mean().round(2).to_dict()

# Categorical percentage distributions
cat_vars = ['Platform', 'Battle Style', 'Starter']
cat_perc = {
    col: (df[col].value_counts(normalize=True) * 100).round(2)
    for col in cat_vars
}

# Plotly figures
platform_fig = px.bar(
    x=cat_perc['Platform'].index,
    y=cat_perc['Platform'].values,
    labels={'x': 'Platform', 'y': 'Percentage'},
    title='Platform Distribution (%)'
)
battle_fig = px.bar(
    x=cat_perc['Battle Style'].index,
    y=cat_perc['Battle Style'].values,
    labels={'x': 'Battle Style', 'y': 'Percentage'},
    title='Battle Style Distribution (%)'
)
starter_fig = px.bar(
    x=cat_perc['Starter'].index,
    y=cat_perc['Starter'].values,
    labels={'x': 'Starter', 'y': 'Percentage'},
    title='Starter Distribution (%)'
)

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = dbc.Container(
    [
        html.H1('Pokémon Dashboard', className='my-4'),

        # Summary statistics
        html.H2('Summary Statistics'),
        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardBody([
                html.H5('Total Entries', className='card-title'),
                html.P(f"{total_entries}", className='card-text')
            ])]), width=4),
            dbc.Col(dbc.Card([dbc.CardBody([
                html.H5('Unique Games', className='card-title'),
                html.P(f"{unique_games}", className='card-text')
            ])]), width=4),
            dbc.Col(dbc.Card([dbc.CardBody([
                html.H5('Total Playtime (hrs)', className='card-title'),
                html.P(f"{total_playtime_hours:.2f}", className='card-text')
            ])]), width=4),
        ], className='mb-4'),

        # Averages section
        html.H2('Average Statistics'),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5('Avg Playtime (hrs)', className='card-title'),
                html.P(f"{avg_playtime_hours:.2f}", className='card-text')
            ])), width=3),
            *[
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H5(f'Avg {col}', className='card-title'),
                    html.P(f"{avg_stats[col]}", className='card-text')
                ])), width=3)
                for col in numeric_cols[:3]
            ],
        ]),
        dbc.Row([
            *[
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H5(f'Avg {col}', className='card-title'),
                    html.P(f"{avg_stats[col]}", className='card-text')
                ])), width=3)
                for col in numeric_cols[3:6]
            ],
        ]),
        dbc.Row([
            *[
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H5(f'Avg {col}', className='card-title'),
                    html.P(f"{avg_stats[col]}", className='card-text')
                ])), width=3)
                for col in numeric_cols[6:]
            ],
        ], className='mb-4'),

        # Categorical distributions
        html.H2('Categorical Distributions'),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=platform_fig), width=4),
            dbc.Col(dcc.Graph(figure=battle_fig), width=4),
            dbc.Col(dcc.Graph(figure=starter_fig), width=4),
        ]),
    ],
    fluid=True
)

# Run server
if __name__ == '__main__':
    app.run_server(debug=True)