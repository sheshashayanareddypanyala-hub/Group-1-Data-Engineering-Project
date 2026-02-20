#  Meeting Intelligence Dashboard

##  Project Overview

This project builds an interactive Meeting Intelligence Dashboard using Streamlit.

The dashboard analyzes structured meeting metadata and transcript data to generate insights such as:

- Total meetings per city
- Meetings per year
- Average meeting duration by agenda type
- Discussion intensity (Words per Minute)
- Interactive transcript viewer


------------------------------------------------------------

##  Real-World Architecture (Production Version)

In the real-world implementation:

- Structured metadata was stored in Amazon RDS (PostgreSQL)
- Transcript data was stored in MongoDB Atlas
- Metadata was processed and converted into structured CSV format
- Transcript JSON files were processed and converted into MongoDB-ready format
- Python scripts were used to upload data to both cloud databases
- Streamlit was used for visualization

For security reasons, cloud credentials and connection strings are NOT included in this repository.

Instead, CSV exports of both databases are provided for demonstration.


------------------------------------------------------------

##  Project Structure

meeting-intelligence-dashboard/
│
├── data/
│   ├── Meetingbank_postgresql.csv
│   ├── meetingbank_mongodb.csv
│
├── app/
│   └── streamlit_app.py
│
├── scripts/
│   ├── metadata_to_postgresql_format.py
│   ├── transcript_to_mongodb_format.py
│   ├── upload_to_rds.py
│   └── upload_to_mongodb_atlas.py
│
├── requirements.txt
└── README.md


------------------------------------------------------------

##  Technologies Used

- Python
- Pandas
- Matplotlib
- Streamlit
- PostgreSQL (Amazon RDS – Production)
- MongoDB Atlas (Production)


------------------------------------------------------------

## Data Engineering Workflow

1. Raw metadata files processed using Python
2. Structured CSV generated for PostgreSQL
3. Transcript JSON files processed and converted
4. MongoDB-ready CSV generated
5. Data uploaded to:
   - Amazon RDS (PostgreSQL)
   - MongoDB Atlas
6. CSV exports used for public demo visualization


------------------------------------------------------------

## How to Run the Visualization

1. Clone the repository

   git clone https://github.com/your-username/meeting-intelligence-dashboard.git
   cd meeting-intelligence-dashboard

2. Install dependencies

   pip install -r requirements.txt

3. Run the Streamlit app

   streamlit run app/streamlit_app.py

The dashboard will open automatically in your browser.


------------------------------------------------------------

## Dashboard Features

✔ City-based filtering  
✔ Key performance metrics  
✔ Meetings per year visualization  
✔ Agenda-based duration analysis  
✔ Discussion intensity trend  
✔ Interactive transcript viewer  


------------------------------------------------------------

## Security & Best Practices

- No hardcoded database credentials
- No cloud access keys stored in repository
- Upload scripts exclude credentials
- Uses relative file paths for portability
- Production architecture separated from demo version


------------------------------------------------------------

##  Purpose of This Project

This project demonstrates:

- End-to-end Data Engineering workflow
- Cloud database integration (RDS + MongoDB Atlas)
- Data cleaning and transformation using Pandas
- ETL pipeline scripting
- Interactive dashboard development using Streamlit
- Secure and professional GitHub project structuring


------------------------------------------------------------

##  Author

Developed as part of a Data Engineering learning project.
