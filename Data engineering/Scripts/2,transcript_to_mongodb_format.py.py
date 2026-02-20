import pandas as pd

# Load cleaned dataset
df = pd.read_csv(r"C:\Users\venu8\Downloads\meetingbank_cleaned.csv")

# Select only MongoDB-required columns
mongo_df = df[["uid", "transcript", "summary"]].copy()

# Rename uid → meeting_id
mongo_df.rename(columns={"uid": "meeting_id"}, inplace=True)

# If agenda column exists, include it
if "agenda_items" in df.columns:
    mongo_df["agenda_items"] = df["agenda_items"]

# Save MongoDB-ready file
output_path = r"C:\DataEnginereeing1\meetings_mongodb_ready1.csv"
mongo_df.to_csv(output_path, index=False)

print("MongoDB dataset created:", output_path)
