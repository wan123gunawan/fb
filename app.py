import streamlit as st
import requests
import pandas as pd

st.title("📊 Facebook Engagement Analyzer")

access_token = st.text_input("Access Token")
page_id = st.text_input("Page ID")

if st.button("Ambil Data"):
    url = f"https://graph.facebook.com/v18.0/{page_id}/posts"

    params = {
        "fields": "message,created_time,shares,likes.summary(true),comments.summary(true)",
        "access_token": access_token
    }

    response = requests.get(url, params=params)
    data = response.json()

    posts = data.get("data", [])

    results = []

    for post in posts:
        message = post.get("message", "")[:50]
        created = post.get("created_time")

        likes = post.get("likes", {}).get("summary", {}).get("total_count", 0)
        comments = post.get("comments", {}).get("summary", {}).get("total_count", 0)
        shares = post.get("shares", {}).get("count", 0)

        engagement = likes + comments + shares

        results.append({
            "Tanggal": created,
            "Post": message,
            "Likes": likes,
            "Comments": comments,
            "Shares": shares,
            "Engagement": engagement
        })

    df = pd.DataFrame(results)

    st.dataframe(df)

    st.subheader("📈 Grafik Engagement")
    st.line_chart(df["Engagement"])
