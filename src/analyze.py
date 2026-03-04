import pandas as pd
from sqlalchemy import create_engine, text
import os

def main():
    engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5433/chicago_db')
    query = """
    WITH MaxDate AS (
        SELECT MAX(crime_date::DATE) AS max_date
        FROM chicago_crimes
    ),
    DailyTheft AS (
        SELECT 
            district,
            crime_date::DATE AS report_date,
            COUNT(id) AS daily_count
        FROM chicago_crimes
        WHERE primary_type = 'THEFT' AND district IS NOT NULL
        GROUP BY district, crime_date::DATE
    ),
    RollingAvg AS (
        SELECT 
            district,
            report_date,
            daily_count,
            AVG(daily_count) OVER (
                PARTITION BY district 
                ORDER BY report_date
                RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW
            ) AS rolling_avg_7d
        FROM DailyTheft
    )
    SELECT 
        r.district,
        r.report_date,
        r.daily_count,
        ROUND(r.rolling_avg_7d, 2) AS rolling_avg_7d
    FROM RollingAvg r
    CROSS JOIN MaxDate m
    WHERE r.report_date >= m.max_date - INTERVAL '30 days'
    ORDER BY r.district ASC, r.report_date DESC;
    """
    
    print("Executing complex query for 7-day rolling average...")
    
    with engine.connect() as conn:
        df = pd.read_sql_query(text(query), conn)
        
    print(f"Query successful! Retrieved {len(df)} rows.")
    
    os.makedirs('output', exist_ok=True)
    output_file = 'output/theft_rolling_avg_30days.csv'
    df.to_csv(output_file, index=False)
    
    print(f"Successfully saved results to {output_file}")
    print(df.head())

if __name__ == "__main__":
    main()