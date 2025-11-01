import streamlit as st


def Navbar():
    with st.sidebar:
        st.page_link('main.py', label='Home page', icon='🔥')
        st.page_link('pages/PlayerStats.py', label='Players Statistics', icon='⚽')
        st.page_link('pages/MatchStats.py', label='Match Statistics', icon='🛡️')
        st.page_link('pages/TeamStats.py', label='Team Statistics', icon='🛡️')