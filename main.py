import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

def load_data(csv_path):
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return None

def scatter_tab(df):
    st.header("Scatter Plot: Compare Two Stats")
    stat_options = [col for col in df.columns if df[col].dtype in ["float64", "int64"] and col not in ["team_id", "player_id"]]
    x_stat = st.selectbox("Select X axis stat", stat_options, index=0)
    y_stat = st.selectbox("Select Y axis stat", stat_options, index=1)
    fig1 = px.scatter(
        df,
        x=x_stat,
        y=y_stat,
        hover_name="player_name",
        color="team_name",
        title=f"{x_stat} vs {y_stat} by Team",
    )
    st.plotly_chart(fig1, use_container_width=True)

def player_comparison_tab(df):
    st.header("Player Stats Comparison")
    team_options = df["team_name"].unique()
    selected_team = st.selectbox("Select Team", team_options)
    team_players = df[df["team_name"] == selected_team]["player_name"].unique()
    selected_player = st.selectbox("Select Player", team_players)
    player_row = df[(df["team_name"] == selected_team) & (df["player_name"] == selected_player)].iloc[0]
    stat_cols = [col for col in df.columns if df[col].dtype in ["float64", "int64"] and col not in ["team_id", "player_id"]]
    stats = player_row[stat_cols]
    ranks = df[stat_cols].rank(method="min", ascending=False)
    player_ranks = ranks.loc[player_row.name]
    best = ranks.max()
    worst = ranks.min()
    colors = []
    for col in stat_cols:
        if player_ranks[col] == best[col]:
            colors.append("green")
        elif player_ranks[col] == worst[col]:
            colors.append("red")
        else:
            colors.append("orange")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=stat_cols,
        y=stats,
        marker_color=colors,
        text=[f"Rank: {int(player_ranks[col])}" for col in stat_cols],
        textposition="outside",
    ))
    fig2.update_layout(title=f"{selected_player} ({selected_team}) Stats Comparison", xaxis_title="Stat", yaxis_title="Value", showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

def main():
    csv_path = os.path.join("opendata", "data", "aggregates", "aus1league_physicalaggregates_20242025_midfielders.csv")
    st.title("AUS League Player Stats Explorer")
    df = load_data(csv_path)
    if df is not None:
        tab1, tab2 = st.tabs(["Scatter Plot by Stats", "Player Stats Comparison"])
        with tab1:
            scatter_tab(df)
        with tab2:
            player_comparison_tab(df)
    else:
        st.error(f"File not found: {csv_path}")

if __name__ == "__main__":
    main()