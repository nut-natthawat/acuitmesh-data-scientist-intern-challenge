import pandas as pd
from sqlalchemy import create_engine, text
import os

def check_data_integrity(df):
    total_rows = len(df)
    missing_coords = df['Latitude'].isnull().sum()
    missing_percentage = (missing_coords / total_rows) * 100
    print(f"--- Data Integrity Check ---")
    print(f"Total records loaded: {total_rows}")
    print(f"Missing Latitude/Longitude: {missing_coords} rows ({missing_percentage:.2f}%)")
    return missing_percentage

def main():
    data_path = 'D:/internship/acuitmesh-data-scientist-intern-challenge/data/Crimes_-_2001_to_Present_20260304.csv'
    
    print("Load data from CSV")
    df = pd.read_csv(data_path, nrows=100000)
    
    check_data_integrity(df)
    
    print("\nTransforming data")
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df.rename(columns={'date': 'crime_date'}, inplace=True)
    
    df['crime_date'] = pd.to_datetime(df['crime_date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
    df['updated_on'] = pd.to_datetime(df['updated_on'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
    
    print("Ingesting data to PostgreSQL")
    engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5433/chicago_db')
    
    df.to_sql('chicago_crimes', engine, if_exists='append', index=False, chunksize=10000)
    
    print("Updating Geospatial Points")
    with engine.begin() as conn:
        conn.execute(text("""
            ALTER TABLE chicago_crimes 
            ADD COLUMN IF NOT EXISTS geom GEOMETRY(Point, 4326);
        """))
        
        conn.execute(text("""
            UPDATE chicago_crimes 
            SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL AND geom IS NULL;
        """))
        
    print("Pipeline completed successfully!")
if __name__ == "__main__":
    main()