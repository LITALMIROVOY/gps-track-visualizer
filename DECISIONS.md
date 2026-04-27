# DECISIONS.md

## Framework Choice
**Decision:** I chose **Streamlit** for the user interface rather than a traditional desktop GUI framework (like PyQt or Tkinter). 
**Alternative Considered:** Building a standalone executable using PyQt.
**Justification:** The assignment asks for a "Python application". 
				Streamlit allowed me to  build a  interactive and responsive UI.
				It provides smooth integration with Plotly, which was selected for my map animations.

## Architectural Choices
**Decision:** Total separation of Data Parsing (`DataLoader`), Business Logic (`Car`), Presentation (`Visualizer`), and Orchestration (`main.py`).
**Justification:** Section 4.1 explicitly bans "God classes." By separating them i ensure that if i want to change the rendering engine
					i only need to swap the `Visualizer` class without touching the `DataLoader` or `Car`.

**Decision:** Leveraging `dataclass` for `GPSPoint`.
**Alternative Considered:** Using raw Pandas DataFrames throughout the app.
**Justification:** While Pandas is powerful, passing DataFrames everywhere obscures the data contract .
					By converting the sanitized Pandas rows into typed `GPSPoint` objects, the `Car` class can interact with strict types,
					ensuring safety and better IDE autocomplete support. Pandas is strictly isolated to the `DataLoader` for efficient CSV parsing and vectorised cleanup.

## Handling Edge Cases
**Decision:** I implemented bounds-checking on coordinates (Lat between -90 and 90, Lon between -180 and 180) and filled missing altitude values with `0.0`.
**Justification:** GPS hardware can occasionally glitch. Rather than throwing out an entire trajectory because an altitude sensor failed, i fallback to sea-level. 
					However, impossible coordinates (e.g., Latitude 200) mean the point is fundamentally broken,
					so those are dropped to prevent the map library from crashing.

## AI-Driven Workflow
**How AI was utilized:**
- **Initial Prototyping:** Used an AI coding assistant (Gemini 3.1 Pro) to rapidly draft the  Plotly animation logic.
- **Documentation:** The AI was utilized to draft the Mermaid sequence/class diagrams.
- **cleanup:** I used it to clean up the code , correct spelling mistakes , and adding documentation. 
- **debugging:** I used the tool for debugging'  especially in the visualization part that i had more struggles in.
- **Deliverables:** I used it to separate my classes into different files. 

## Future Improvements
Given more time, I would implement:
1. **Map Matching:**Implementing Map Matching algorithms to snap the GPS points to actual roads, correcting for hardware inaccuracies
2. **Unit Testing:** Add `pytest` coverage for `DataLoader` to formally verify the edge-case handling.
