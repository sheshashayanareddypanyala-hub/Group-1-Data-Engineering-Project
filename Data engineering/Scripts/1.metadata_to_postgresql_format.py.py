import json
import os
import pandas as pd
import re
from datetime import datetime

# ---------- PATHS ----------
metadata_path = r"C:\Users\venu8\Downloads\MeetingBank\Metadata\MeetingBank.json"
transcript_root = r"C:\Users\venu8\Downloads\MeetingBank\Audio&Transcripts"

# ---------- LOAD METADATA ----------
with open(metadata_path, "r", encoding="utf-8") as f:
    metadata = json.load(f)

records = []

# ---------- PROCESS MEETINGS ----------
for meeting_id, details in metadata.items():

    city = meeting_id.split("_")[0]

    # ---------- robust date extraction ----------
    meeting_date = None
    match = re.search(r'(\d{8})', meeting_id)
    if match:
        try:
            meeting_date = datetime.strptime(match.group(1), "%m%d%Y").date()
        except:
            meeting_date = None

    duration = details.get("VideoDuration", None)
    if duration is not None and duration < 0:
        duration = None

    transcript_file = details.get("Transcripts", "")

    transcript_path = None
    for root, dirs, files in os.walk(transcript_root):
        if transcript_file in files:
            transcript_path = os.path.join(root, transcript_file)
            break

    speaker_set = set()
    word_count = 0

    if transcript_path:
        with open(transcript_path, "r", encoding="utf-8") as tf:
            tdata = json.load(tf)

        # ---------- fallback duration from transcript ----------
        if duration is None:
            try:
                duration = int(tdata.get("duration", 0)) / 1_000_000
            except:
                duration = None

        # ---------- speaker & word count ----------
        if "segments" in tdata:
            for seg in tdata["segments"]:

                speaker = seg.get("speaker")
                if speaker is not None:
                    speaker_set.add(speaker)

                for alt in seg.get("nbest", []):
                    for w in alt.get("words", []):
                        word_count += 1

    speaker_count = len(speaker_set)

    # ---------- agenda type ----------
    agenda_type = None
    if "itemInfo" in details:
        types = [i.get("type") for i in details["itemInfo"].values() if i.get("type")]
        if types:
            agenda_type = types[0]

    records.append({
        "meeting_id": meeting_id,
        "city": city,
        "meeting_date": meeting_date,
        "duration": duration,
        "agenda_type": agenda_type,
        "speaker_count": speaker_count,
        "word_count": word_count
    })

# ---------- SAVE FINAL CSV ----------
df = pd.DataFrame(records)
df.to_csv("meetings_postgres_ready_final_v8.csv", index=False)

print("Final cleaned dataset created: meetings_postgres_ready_final_v5.csv")
