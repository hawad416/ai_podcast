
import streamlit as st
from datetime import datetime


st.title("🍭 Hawa's Creative Studio 🍭")
st.subheader("my episodes 🎞️")

st.sidebar.header("🍭 p o d s 🍭")

st.sidebar.page_link("main.py", label="🎙️ Create New Podcast")
st.sidebar.page_link("./pages/another.py", label="▶️ My Episodes")


podcasts = [
    {
        "title": "Episode 1: How Soccer Can Help Young Girls Build Confidence",
        "date": "2024-05-01",
        "image": "soccer.jpeg",
        "mp3": "episodes/ali_debow_soccer.mp3"
    },
    {
        "title": "Episode 2: Rethinking How we Hire with Sam Dore, Madrona Venture Labs",
        "date": "2024-05-08",
        "image": "mvl.png",
        "mp3": "episodes/sam-mvl-hiring.mp3"
    },
    {
        "title": "Episode 3: Hire People Who Give a Shit, Alexandr Wang",
        "date": "2024-05-08",
        "image": "alex.jpeg",
        "mp3": "episodes/alexandr_wang_hiring.mp3"

    }
    # Add more episodes as needed
]

st.title("Podcast Episodes")

# Function to create a card
def create_podcast_card(title, date, image, mp3):
    st.image(image, width=200)
    st.subheader(title)
    st.caption(f"Date Created: {date}")
    st.audio(mp3)

# Display each podcast episode in a card
for podcast in podcasts:
    with st.container():
        create_podcast_card(
            podcast["title"],
            datetime.strptime(podcast["date"], '%Y-%m-%d').strftime('%B %d, %Y'),
            podcast["image"],
            podcast["mp3"]
        )
        st.markdown("---")  # Divider between card

