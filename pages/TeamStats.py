from utils.football_pitch import FootballPitch
import streamlit as st


def pitch_tab():
    st.header("Football Pitch Visualization")
    st.markdown("""
    This tab displays a football pitch using the FootballPitch class. All pitch elements are drawn to scale using Plotly. You can use this as a base for further tactical visualizations or overlays.
    """)
    pitch = FootballPitch()
    fig = pitch.draw()
    st.plotly_chart(fig, use_container_width=True)

def main():
    """Team statistics dashboard placeholder for future visualizations."""
    st.sidebar.header("Team statistics")
    st.set_page_config(page_title="Team page statistics", page_icon="🌍")
    pitch_tab()
    st.markdown("""
    This page will feature team-level statistics and visualizations for the A-League. Stay tuned for updates!
    """)
    st.info("Team stats visualizations coming soon!")
    

if __name__ == "__main__":
    main()