import streamlit as st
from supabase_client import get_supabase_client
import pandas as pd

# Set the page configuration
st.set_page_config(
    page_title="Leaderboard",
    page_icon="🏆",
    layout="centered",
)

# Page header
st.markdown("<h1 style='text-align: center;'>🏆 Leaderboard</h1>", unsafe_allow_html=True)
supabase = get_supabase_client()

# Fetch top 10 users by points
response = supabase.table('profiles').select('username, points').order('points', desc=True).limit(10).execute()
data = response.data

if data:
    # Create a DataFrame and add a ranking column starting at 1
    df = pd.DataFrame(data)
    df.insert(0, 'Rank', range(1, len(df) + 1))  # Add 'Rank' column at the start

    # Generate the HTML table
    rows = ""
    for _, row in df.iterrows():
        rows += f"""
        <tr>
            <td>{row['Rank']}</td>
            <td>{row['username']}</td>
            <td>{row['points']}</td>
        </tr>
        """

    leaderboard_html = f"""
    <style>
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 18px;
            text-align: center;
        }}
        thead {{
            background-color: #f2a03b;
            color: white;
        }}
        th, td {{
            padding: 10px;
            border: 1px solid #ddd;
        }}
        tbody tr:nth-child(odd) {{
            background-color: #f9f9f9;
        }}
        tbody tr:nth-child(even) {{
            background-color: #ffffff;
        }}
        tbody tr:hover {{
            background-color: #f1f1f1;
        }}
    </style>
    <table>
        <thead>
            <tr>
                <th>Rank</th>
                <th>Username</th>
                <th>Points</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """

    # Render the leaderboard table
    st.components.v1.html(leaderboard_html, height=400)
else:
    st.info("No data available. The leaderboard will update once users participate.")
