import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_analytics(portfolio, financial_data):
    print(financial_data.iloc[2, :])
    financial_data_plot(financial_data)


def financial_data_plot(financial_data):
    # INFO - Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.1, subplot_titles=("Financial Data", "Volume"),
                        row_width=[0.2, 0.7])

    # INFO - Include candlestick with rangeselector
    fig.add_trace(go.Candlestick(
        x=financial_data['Date'],
        open=financial_data['Open'], high=financial_data['High'],
        low=financial_data['Low'], close=financial_data['Adj Close'],
        name="OHLC Timeseries"), row=1, col=1)

    # INFO - Include a go.Bar trace for volumes
    # fig.add_trace(go.Bar(x=financial_data['Date'], y=financial_data['Volume'],
    #              marker_color='red', showlegend=False), row=2, col=1)
#
    # fig.update_layout(
    #    title='Historical price chart',
    #    xaxis_tickfont_size=12,
    #    yaxis=dict(
    #        title='Price ($/share)',
    #        titlefont_size=14,
    #        tickfont_size=12,
    #    ),
    #    autosize=True,
    #    # autosize=False,
    #    # width=1920,
    #    # height=1080,
    #    margin=dict(l=50, r=50, b=100, t=100, pad=4),
#
    # )

    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.show()
