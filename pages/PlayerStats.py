from utils.comparisson_tabs import scatter_tab, player_comparison_tab
from utils.loading import load_data
import os
import streamlit as st

def main():
    st.sidebar.header("Player statistics")
    st.set_page_config(page_title="Player page statistics", page_icon="🌍")
    """Player statistics dashboard with interactive tabs for scatter plots and comparisons."""
    st.title("A-League Player Statistics")
    csv_path = os.path.join("opendata", "data", "aggregates", "aus1league_physicalaggregates_20242025_midfielders.csv")
    df = load_data(csv_path)
    tab1, tab2 = st.tabs(["Scatter Plot by Stats", "Player Stats Comparison"])
    if df is not None:
        with tab1:
            scatter_tab(df)
        with tab2:
            player_comparison_tab(df)
    if df is None:
        st.error(f"File not found: {csv_path}")

if __name__ == "__main__":
    main()