import json
import pandas as pd
from pathlib import Path
from utils.football_pitch import FootballPitch
import streamlit as st
from utils.navigation_bar import Navbar
from utils.loading import load_json
import os

def match_metadata_table(match_dict):
    """Return a pandas DataFrame with key metadata for the selected match (A-League format)."""
    meta = {
        "Match ID": match_dict.get("id"),
        "Date & Time": match_dict.get("date_time"),
        "Home Team": match_dict.get("home_team", {}).get("name"),
        "Away Team": match_dict.get("away_team", {}).get("name"),
        "Home Score": match_dict.get("home_team_score"),
        "Away Score": match_dict.get("away_team_score"),
        "Stadium": match_dict.get("stadium", {}).get("name"),
        "Stadium City": match_dict.get("stadium", {}).get("city"),
        "Stadium Capacity": match_dict.get("stadium", {}).get("capacity"),
        "Competition": match_dict.get("competition_edition", {}).get("name"),
        "Round": match_dict.get("competition_round", {}).get("name"),
        "Season": match_dict.get("competition_edition", {}).get("season", {}).get("name"),
    }
    return pd.DataFrame(meta.items(), columns=["Field", "Value"])

def get_team_logo(team_name):
    """Return the path to the team logo SVG file based on team name."""
   
    logo_dir = "aleague_logos"
    # Normalize team name for matching
    normalized = normalized = team_name.lower()
    # Try to find a logo file that contains the normalized team name
    for logo_file in os.listdir(logo_dir):
        if normalized in logo_file.lower():
            return os.path.join(logo_dir, logo_file)
    # Fallback: return None if not found
    return None

def display_team_logo(team_name):
    """Display team name with logo and score in Streamlit."""
    logo_path = get_team_logo(team_name)
    st.image(logo_path, width=120)

def pitch_tab():
    """Display the football pitch visualization."""
    st.header("Football Pitch Visualization")
    st.markdown("""
    This tab displays a football pitch using the FootballPitch class. All pitch elements are drawn to scale using Plotly. You can use this as a base for further tactical visualizations or overlays.
    """)
    pitch = FootballPitch()
    fig = pitch.draw()
    st.plotly_chart(fig, use_container_width=True)

def get_players_tables(match_dict, home_team_id, away_team_id):
    """Return two DataFrames for home and away players with number, last name, and kit color."""
    home_players = []
    away_players = []
    # Get kit colors, fallback to gray if missing
    home_kit_color = match_dict.get("home_team_kit", {}).values[0].get("jersey_color") or "#cccccc"
    away_kit_color = match_dict.get("away_team_kit", {}).values[0].get("jersey_color") or "#cccccc"
    players = match_dict.get("players")[0]
    for p in players:
        # Assign kit color based on team
        kit_color = home_kit_color if p.get("team_id") == home_team_id else away_kit_color
        entry = {
            "Number": p.get("number"),
            "Name": p.get("last_name"),
            "Kit": kit_color
        }
        if p.get("team_id") == home_team_id:
            home_players.append(entry)
        else:
            away_players.append(entry)
    home_df = pd.DataFrame(home_players)
    away_df = pd.DataFrame(away_players)
    return home_df, away_df

def main():
    Navbar()
    st.sidebar.header("Team statistics")
    st.set_page_config(page_title="Team page statistics", page_icon="🌍")
    matches = load_json("opendata/data/matches.json")
    matches.set_index("id", inplace=True)
    matches_ids = matches.index.values.tolist()
    selected_idx = st.selectbox("Select Match", matches_ids, format_func=lambda i: matches.loc[i]['home_team']['short_name'] + " vs " + matches.loc[i]['away_team']['short_name'] + " (" + str(matches.loc[i]['date_time']) + ")")
    match = matches.loc[selected_idx]
    match_metadata_df = load_json(f"opendata/data/matches/{selected_idx}/{selected_idx}_match.json", lines=True)
    st.subheader("Match Overview")
    home_score, away_score = match_metadata_df["home_team_score"].values[0], match_metadata_df["away_team_score"].values[0]
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        display_team_logo(match['home_team']['short_name'])
    with col2:
        st.markdown(f'<div style="text-align:center;font-size:1.5em;font-weight:bold;">{home_score} - {away_score}</div>', unsafe_allow_html=True)
    with col3:
        display_team_logo(match['away_team']['short_name'])
    st.markdown("### Match Metadata")
    st.dataframe(match_metadata_table(match_metadata_df.iloc[0].to_dict()), use_container_width=True)
    # Pitch with interactive data
    pitch_tab()
    # Players tables below the pitch
    home_team_id, away_team_id = match_metadata_df["home_team"].iloc[0]["id"], match_metadata_df["away_team"].iloc[0]["id"]
    home_df, away_df = get_players_tables(match_metadata_df, home_team_id, away_team_id)
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("#### Home Players")
        for _, row in home_df.iterrows():
            st.markdown(f'<div style="display:flex;align-items:center;margin-bottom:4px;">'
                        f'<span style="width:18px;height:18px;border-radius:50%;background:{row["Kit"]};display:inline-block;margin-right:12px;"></span>'
                        f'<span style="font-weight:bold;margin-right:12px;">{row["Number"]}</span>'
                        f'<span style="margin-left:4px;">{row["Name"]}</span>'
                        f'</div>', unsafe_allow_html=True)
    with col_right:
        st.markdown("#### Away Players")
        for _, row in away_df.iterrows():
            st.markdown(f'<div style="display:flex;align-items:center;margin-bottom:4px;">'
                        f'<span style="width:18px;height:18px;border-radius:50%;background:{row["Kit"]};display:inline-block;margin-right:12px;"></span>'
                        f'<span style="font-weight:bold;margin-right:12px;">{row["Number"]}</span>'
                        f'<span style="margin-left:4px;">{row["Name"]}</span>'
                        f'</div>', unsafe_allow_html=True)
    st.markdown("""
    This page will feature team-level statistics and visualizations for the A-League. Stay tuned for updates!
    """)
    st.info("Team stats visualizations coming soon!")

if __name__ == "__main__":
    main()