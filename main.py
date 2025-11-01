import streamlit as st
import pandas as pd
import os
from utils.navigation_bar import Navbar

def main():
    Navbar()

    st.set_page_config(
        page_title="Football Analytics Cup Dashboard",
        page_icon="⚽",
    )

    st.write("""
    # Welcome to the Football Analytics Cup Dashboard! ⚽

    Explore player and team statistics, visualizations, and match insights for the A-League. Use the sidebar to select a dashboard page.
    """)

    st.sidebar.success("Select a dashboard page from the sidebar.")

if __name__ == '__main__':
    main()