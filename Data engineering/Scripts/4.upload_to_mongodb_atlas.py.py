import pandas as pd
import time
from pymongo import MongoClient

connection_string = "mongodb+srv://Venu:Venu8854@cluster0.xg8cnqc.mongodb.net/?appName=Cluster0"
client = MongoClient(connection_string)

db = client["meeting_pipeline"]
collection = db["transcripts"]

file_path = r"C:\DataEnginereeing1\meetings_mongodb_ready_final11.csv"
df = pd.read_csv(file_path)

# Keep only first 500 rows
df = df.head(500)

data = df.to_dict(orient="records")

inserted = 0

for doc in data:
    collection.insert_one(doc)
    inserted += 1
    print(f"Inserted {inserted}")
    time.sleep(0.05)

print("Upload completed!")
print("Total documents:", collection.count_documents({}))

client.close()
