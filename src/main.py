import streamlit as st
import sys
import os

# Add the project root to the sys.path so we can import local modules 
# regardless of where streamlit is run from
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import DataLoader
from src.models import Car
from src.visualizer import Visualizer

def main():
    st.set_page_config(page_title="GPS Track Visualizer", page_icon="🚗", layout="wide")
    
    st.title("GPS Track Visualizer 🚗")
    st.markdown("Upload a CSV file containing timestamped GPS positions to visualize the car's track.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            with st.spinner("Loading and processing data..."):
                loader = DataLoader(uploaded_file)
                points = loader.load_data()
                
                if not points:
                    st.error("No valid data points found in the CSV.")
                    return
                    
                car = Car(points)
                total_dist = car.get_total_distance()
                duration = car.get_duration()
                
            # Create a nice layout for metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Total Distance", value=f"{total_dist:.2f} km")
            with col2:
                st.metric(label="Total Duration", value=f"{duration} s")
            with col3:
                st.metric(label="Total Data Points", value=len(points))

            st.divider()
            
            with st.spinner("Generating animation..."):
                viz = Visualizer(car)
                fig = viz.get_figure()
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Could not generate visualization.")
                    
        except KeyError as e:
            st.error(f"Missing required columns in CSV: {e}")
        except ValueError as e:
            st.error(f"Data problem: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.info("Please upload a CSV file with 'lat', 'lon', and 'time' columns.")

if __name__ == "__main__":
    main()
