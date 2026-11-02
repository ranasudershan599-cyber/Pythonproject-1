"""Streamlit interface for the educational flight route planner."""
import csv
from pathlib import Path
import streamlit as st
from algorithms import build_graph, dijkstra, bfs_fewest_legs, dfs_path

DATA = Path(__file__).parent / "data" / "routes.csv"

st.set_page_config(page_title="Flight Route Planner", page_icon="✈️", layout="wide")
st.title("✈️ Flight Route Planner")
st.caption("A  mini project demonstrating graph search and shortest paths.")

if not DATA.exists():
    st.error(f"Dataset not found at `{DATA}`. Please ensure the CSV file exists.")
    st.stop()

with DATA.open(encoding="utf-8", newline="") as handle:
    routes = list(csv.DictReader(handle))

airports = sorted({r["source"] for r in routes} | {r["destination"] for r in routes})

if not airports:
    st.warning("The routes dataset is empty.")
    st.stop()

left, right = st.columns(2)
start_default = airports.index("Delhi") if "Delhi" in airports else 0
goal_default = airports.index("Mumbai") if "Mumbai" in airports else (1 if len(airports) > 1 else 0)

start = left.selectbox("From", airports, index=start_default)
goal = right.selectbox("To", airports, index=goal_default)

metric = st.selectbox("Optimize by", ["Distance (km)", "Estimated time (hours)", "Fare (₹)"])
weight = {"Distance (km)": "distance_km", "Estimated time (hours)": "time_hours", "Fare (₹)": "fare_inr"}[metric]

if start == goal:
    st.info("Choose two different airports.")
else:
    graph = build_graph(routes, weight)
    path, total = dijkstra(graph, start, goal)
    if path:
        st.subheader("Best route by " + metric.lower())
        st.success(" → ".join(path))
        unit = "km" if weight == "distance_km" else ("hours" if weight == "time_hours" else "₹")
        st.metric("Total " + metric.split(" ")[0].lower(), f"{total:,.1f} {unit}")
        st.write(f"Stops: {max(0, len(path)-2)} · Flight legs: {len(path)-1}")

        st.subheader("Algorithm comparison")
        bfs_route = bfs_fewest_legs(graph, start, goal)
        dfs_route = dfs_path(graph, start, goal)
        st.write("Fewest-leg route (BFS): " + (" → ".join(bfs_route) if bfs_route else "No route"))
        st.write("One route found by DFS: " + (" → ".join(dfs_route) if dfs_route else "No route"))
        st.caption("BFS minimizes number of legs; it does not necessarily minimize the selected metric.")
    else:
        st.warning("No route connects these airports in the sample dataset.")

with st.expander("Sample route data"):
    st.dataframe(routes, use_container_width=True)

st.caption("Educational sample data only. Routes, fares, and times are not live airline information.")

# python -m streamlit run app.py   