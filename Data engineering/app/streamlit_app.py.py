import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

#
# PAGE CONFIGURATION
# 

st.set_page_config(
    page_title="Meeting Intelligence Dashboard",
    layout="wide"
)

st.title("Meeting Intelligence Dashboard")

# 
# LOAD DATA (RELATIVE PATHS)
# 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

structured_path = os.path.join(DATA_DIR, "Meetingbank_postgresql.csv")
transcripts_path = os.path.join(DATA_DIR, "meetingbank_mongodb.csv")

structured_df = pd.read_csv(structured_path)
transcripts_df = pd.read_csv(transcripts_path)

#
# CLEANING
# 

structured_df["meeting_id"] = structured_df["meeting_id"].astype(str).str.strip()
transcripts_df["meeting_id"] = transcripts_df["meeting_id"].astype(str).str.strip()

structured_df["meeting_date"] = pd.to_datetime(
    structured_df["meeting_date"], errors="coerce"
)

# Duration is in seconds → convert to minutes
structured_df["duration_minutes"] = structured_df["duration"] / 60

# Avoid division by zero
structured_df["words_per_minute"] = structured_df.apply(
    lambda row: row["word_count"] / row["duration_minutes"]
    if row["duration_minutes"] > 0 else 0,
    axis=1
)

# 
# SIDEBAR FILTER
# 

st.sidebar.header("Filters")

selected_city = st.sidebar.selectbox(
    "Select City",
    sorted(structured_df["city"].dropna().unique())
)

filtered_df = structured_df[
    structured_df["city"] == selected_city
]

# 
# METRICS
# 

st.subheader(f"Overview for {selected_city}")

col1, col2, col3 = st.columns(3)

col1.metric("Total Meetings", len(filtered_df))
col2.metric("Total Words", int(filtered_df["word_count"].sum()))
col3.metric("Total Speakers", int(filtered_df["speaker_count"].sum()))

st.markdown("---")

# 
# 1️ Meetings Per Year
# 

st.subheader("Meetings Per Year")

yearly_df = (
    filtered_df
    .groupby(filtered_df["meeting_date"].dt.year)
    .size()
    .reset_index(name="total_meetings")
)

fig1, ax1 = plt.subplots()
ax1.bar(yearly_df["meeting_date"], yearly_df["total_meetings"])
ax1.set_xlabel("Year")
ax1.set_ylabel("Total Meetings")

st.pyplot(fig1)

st.markdown("---")

# 
# 2️ Average Duration by Agenda Type
#

st.subheader("Average Meeting Duration by Agenda Type (Minutes)")

top_agendas = (
    filtered_df["agenda_type"]
    .value_counts()
    .head(10)
    .index
)

agenda_filtered = filtered_df[
    filtered_df["agenda_type"].isin(top_agendas)
]

avg_duration = (
    agenda_filtered
    .groupby("agenda_type")["duration_minutes"]
    .mean()
    .reset_index()
    .sort_values(by="duration_minutes", ascending=True)
)

fig2, ax2 = plt.subplots()
ax2.barh(avg_duration["agenda_type"], avg_duration["duration_minutes"])
ax2.set_xlabel("Average Duration (Minutes)")
ax2.set_ylabel("Agenda Type")

st.pyplot(fig2)

st.markdown("---")

# 
# 3️ Discussion Intensity
#

st.subheader("Discussion Intensity (Words per Minute)")

intensity_df = (
    filtered_df
    .groupby("meeting_date")["words_per_minute"]
    .mean()
    .reset_index()
)

fig3, ax3 = plt.subplots()
ax3.plot(intensity_df["meeting_date"], intensity_df["words_per_minute"])
plt.xticks(rotation=45)
ax3.set_xlabel("Meeting Date")
ax3.set_ylabel("Words per Minute")

st.pyplot(fig3)

st.markdown("---")

# 
# 4️ Meetings Per City (Overall)
# 

st.subheader("Total Meetings by City (Overall)")

city_df = (
    structured_df
    .groupby("city")
    .size()
    .reset_index(name="total_meetings")
    .sort_values(by="total_meetings", ascending=False)
)

fig4, ax4 = plt.subplots()
ax4.bar(city_df["city"], city_df["total_meetings"])
plt.xticks(rotation=45)
ax4.set_xlabel("City")
ax4.set_ylabel("Total Meetings")

st.pyplot(fig4)

st.markdown("---")

#
# TRANSCRIPT VIEWER
#

st.subheader("View Transcript")

selected_meeting = st.selectbox(
    "Select Meeting ID",
    filtered_df["meeting_id"]
)

transcript_row = transcripts_df[
    transcripts_df["meeting_id"] == selected_meeting
]

if not transcript_row.empty:
    transcript_text = transcript_row.iloc[0]["transcript"]

    if pd.notna(transcript_text) and transcript_text.strip() != "":
        st.text_area(
            "Transcript",
            transcript_text,
            height=350
        )
    else:
        st.warning("Transcript content not available.")
else:
    st.warning("Transcript not found.")