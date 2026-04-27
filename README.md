# GPS Track Visualizer

This is a Python web application that loads a CSV file containing timestamped GPS positions of a vehicle and visualizes the car's track as an animation that plays back over time.

## Prerequisites

- Python 3.10 or higher.
- `pip` package manager.

## Installation

1. Navigate to the root directory of this project (`project/`).
2. Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

## Running the Application

This project is built using **Streamlit**, a Python framework for data applications. To run the application, you must use the `streamlit` command from your terminal.

1. Ensure you are in the root directory of the project (`project/`).
2. Run the following command:

```bash
streamlit run src/main.py
```

3. The application will start a local server and automatically open your default web browser to the application URL (usually `http://localhost:8501`).
4. Upload your `car_track.csv` file using the drag-and-drop interface in the browser to view the visualization.
