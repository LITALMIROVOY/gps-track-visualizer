import pandas as pd
import plotly.graph_objects as go
from typing import Optional, Any
from .models import Car

class Visualizer:
    """
    Responsible for converting the Car domain object into a visual representation
    using Plotly. It handles generating animation frames and the layout.
    """
    def __init__(self, car: Car):
        self.car = car
        # Create a dataframe specific for visualization (Plotly works well with pandas)
        self.df = pd.DataFrame([{
            'lat': point.lat,
            'lon': point.lon,
            'alt': point.alt,
            'time': point.time
        } for point in self.car.route])

        if not self.df.empty:
            self.start_time = self.df['time'].iloc[0]
        else:
            self.start_time = 0.0

    def get_board(self, point: pd.Series, dist: float) -> str:
        """Returns the HTML formatted string for the live coordinates annotation."""
        seconds_passed = point['time'] - self.start_time
        return (f"<b>Live Coordinates</b><br>"
                f"Distance Traveled: {dist:.2f} km<br>"
                f"Time Elapsed: {seconds_passed:.1f}s<br>"
                f"Latitude: {point['lat']:.5f}<br>"
                f"Longitude: {point['lon']:.5f}<br>"
                f"Altitude: {point['alt']} m")

    def get_figure(self) -> Optional[go.Figure]:
        """Builds and returns the animated Plotly figure."""
        if self.df.empty:
            return None
            
        initial_point = self.df.iloc[0]
        
        # Static background line showing the entire route
        trace_line = go.Scattermapbox(
            mode='lines',
            lat=[initial_point['lat']],
            lon=[initial_point['lon']],
            line=dict(width=2, color='blue'),
            name='Route',
        )
        
        # Moving dot representing the car
        trace_dot = go.Scattermapbox(
            mode='markers',
            lat=[initial_point['lat']],
            lon=[initial_point['lon']],
            marker=dict(size=14, color='red'),
            name='Car',
            hoverinfo='skip'
        )

        fig = go.Figure(data=[trace_line, trace_dot])

        frames = []
        # Sample frames to ensure performance isn't degraded on huge files
        max_frames = 200
        step = max(1, len(self.df) // max_frames)
        
        frame_indices = list(range(1, len(self.df) + 1, step))
        if frame_indices[-1] != len(self.df):
            frame_indices.append(len(self.df))
            
        for i in frame_indices:
            current_df = self.df.iloc[:i]
            current_point = current_df.iloc[-1]
            dist_to_show = self.car.get_distance_up_to(i - 1)

            frame = go.Frame(
                data=[
                    go.Scattermapbox(lat=current_df['lat'], lon=current_df['lon'], mode='lines'),
                    go.Scattermapbox(lat=[current_point['lat']], lon=[current_point['lon']], mode='markers')
                ], 
                layout=go.Layout(
                    mapbox=dict(
                        center=dict(lat=current_point['lat'], lon=current_point['lon'])
                   ),
                    annotations=[dict(
                        text=self.get_board(current_point, dist_to_show),
                        showarrow=False, xref="paper", yref="paper",
                        x=0.02, y=0.98, align="left",
                        bgcolor="rgba(255, 255, 255, 0.9)", bordercolor="black", borderwidth=1
                    )]
                ),
                name=str(current_point['time'])
            )
            frames.append(frame)
            
        fig.frames = frames
        
        # Animation Sliders
        sliders = [{
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [
                {
                    "args": [[f.name], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                    "label": f.name.split(" ")[-1],
                    "method": "animate",
                } for f in frames
            ]
        }]
        
        # Map Layout and Play Controls
        fig.update_layout(
            title="Car GPS Track Animation",
            uirevision='constant',
            mapbox=dict(
                style="open-street-map", 
                center=dict(lat=initial_point['lat'], lon=initial_point['lon']),
                zoom=12, 
            ),
            margin={"r":0,"t":40,"l":0,"b":0},
            height=600,
            annotations=[
                dict(
                    text=self.get_board(initial_point, 0),
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.02, y=0.98,
                    align="left",
                    bgcolor="rgba(255, 255, 255, 0.9)",
                    bordercolor="black",
                    borderwidth=1,
                    font=dict(size=14, color="black")
                )
            ],
            updatemenus=[dict(
                type="buttons",
                buttons=[
                    dict(label="Play",
                         method="animate",
                         args=[None, {"frame": {"duration": 200, "redraw": True}, "fromcurrent": True, "mode": "immediate"}]),
                    dict(label="Play 1.5x",
                         method="animate",
                         args=[None, {"frame": {"duration": 133, "redraw": True}, "fromcurrent": True, "mode": "immediate"}]),
                    dict(label="Play 2x",
                         method="animate",
                         args=[None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True, "mode": "immediate"}]),
                    dict(label="Pause",
                         method="animate",
                         args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
                ],
                direction="left",
                pad={"r": 10, "t": 87},
                showactive=False,
                x=0.1,
                xanchor="right",
                y=0,
                yanchor="top"
            )],
            sliders=sliders
        )
        return fig
