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