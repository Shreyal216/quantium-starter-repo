import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go

# Load the processed data
df = pd.read_csv('output.csv')

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Create the Dash app
app = dash.Dash(__name__)

# Define custom CSS styles
styles = {
    'container': {
        'fontFamily': 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
        'backgroundColor': '#f8f9fa',
        'padding': '40px 20px',
        'minHeight': '100vh'
    },
    'header': {
        'textAlign': 'center',
        'marginBottom': '40px',
        'color': '#2c3e50'
    },
    'title': {
        'fontSize': '2.5em',
        'fontWeight': 'bold',
        'marginBottom': '10px',
        'color': '#e74c3c'
    },
    'subtitle': {
        'fontSize': '1.1em',
        'color': '#7f8c8d',
        'marginBottom': '30px'
    },
    'controlPanel': {
        'backgroundColor': 'white',
        'padding': '25px',
        'borderRadius': '8px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
        'marginBottom': '30px',
        'maxWidth': '600px',
        'margin': '0 auto 30px auto'
    },
    'radioLabel': {
        'fontSize': '1.1em',
        'fontWeight': '600',
        'color': '#2c3e50',
        'marginBottom': '15px'
    },
    'radioButton': {
        'display': 'flex',
        'gap': '20px',
        'justifyContent': 'center',
        'flexWrap': 'wrap'
    },
    'chartContainer': {
        'backgroundColor': 'white',
        'padding': '30px',
        'borderRadius': '8px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
        'marginBottom': '30px'
    },
    'analysisBox': {
        'backgroundColor': 'white',
        'padding': '25px',
        'borderRadius': '8px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
        'maxWidth': '900px',
        'margin': '0 auto',
        'borderLeft': '5px solid #e74c3c'
    },
    'analysisTitle': {
        'fontSize': '1.4em',
        'fontWeight': 'bold',
        'color': '#2c3e50',
        'marginBottom': '15px'
    },
    'analysisText': {
        'fontSize': '1em',
        'color': '#555',
        'lineHeight': '1.6'
    }
}

# Define the app layout
app.layout = html.Div([
    html.Div([
        # Header
        html.Div([
            html.H1("Soul Foods Pink Morsel Sales Dashboard", style=styles['title']),
            html.P("Interactive visualization of Pink Morsel sales data by region", 
                   style=styles['subtitle'])
        ], style=styles['header']),

        # Control Panel with Radio Buttons
        html.Div([
            html.Label("Select Region:", style=styles['radioLabel']),
            dcc.RadioItems(
                id='region-radio',
                options=[
                    {'label': ' All Regions', 'value': 'all'},
                    {'label': ' North', 'value': 'north'},
                    {'label': ' East', 'value': 'east'},
                    {'label': ' South', 'value': 'south'},
                    {'label': ' West', 'value': 'west'}
                ],
                value='all',
                style=styles['radioButton'],
                inline=False,
                labelStyle={'display': 'inline-block', 'marginRight': '20px', 'cursor': 'pointer'}
            )
        ], style=styles['controlPanel']),

        # Chart Container
        html.Div([
            dcc.Graph(id='sales-chart')
        ], style=styles['chartContainer']),

        # Analysis Section
        html.Div([
            html.H3("📊 Analysis", style=styles['analysisTitle']),
            html.P(
                "The red dashed line indicates the Pink Morsel price increase on January 15, 2021. "
                "Use the region selector above to filter sales data by region and analyze how the price increase "
                "affected sales in different areas. The data clearly shows whether sales increased or decreased after the price change.",
                style=styles['analysisText']
            )
        ], style=styles['analysisBox'])

    ], style=styles['container'])
], style={'margin': '0', 'padding': '0'})

# Callback to update chart based on region selection
@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-radio', 'value')
)
def update_chart(selected_region):
    # Filter data based on selected region
    if selected_region == 'all':
        filtered_df = df.copy()
        daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
        chart_title = 'Daily Sales - All Regions'
    else:
        filtered_df = df[df['region'] == selected_region]
        daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
        chart_title = f'Daily Sales - {selected_region.capitalize()} Region'
    
    daily_sales = daily_sales.sort_values('date')
    
    # Create figure with data and price increase line
    figure = {
        'data': [
            go.Scatter(
                x=daily_sales['date'],
                y=daily_sales['sales'],
                mode='lines',
                name='Daily Sales',
                line=dict(color='#e74c3c', width=3),
                hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br><b>Sales:</b> $%{y:,.2f}<extra></extra>'
            ),
            # Vertical line for price increase
            go.Scatter(
                x=['2021-01-15', '2021-01-15'],
                y=[0, daily_sales['sales'].max() * 1.1],
                mode='lines',
                name='Price Increase',
                line=dict(color='#3498db', width=2, dash='dash'),
                hoverinfo='skip'
            )
        ],
        'layout': go.Layout(
            title=chart_title,
            xaxis={
                'title': 'Date',
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': 'rgba(200,200,200,0.2)'
            },
            yaxis={
                'title': 'Sales ($)',
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': 'rgba(200,200,200,0.2)'
            },
            hovermode='x unified',
            height=500,
            template='plotly_white',
            plot_bgcolor='rgba(240,240,240,0.5)',
            font=dict(size=12, family='Segoe UI, sans-serif'),
            margin=dict(l=60, r=40, t=60, b=60)
        )
    }
    
    return figure

if __name__ == '__main__':
    app.run(debug=True)