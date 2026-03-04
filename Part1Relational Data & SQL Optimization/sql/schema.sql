CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE chicago_crimes (
    id BIGINT PRIMARY KEY,
    case_number VARCHAR(20),
    crime_date TIMESTAMP,
    block VARCHAR(100),
    iucr VARCHAR(10),
    primary_type VARCHAR(100),
    description TEXT,
    location_description VARCHAR(100),
    arrest BOOLEAN,
    domestic BOOLEAN,
    beat VARCHAR(10),
    district VARCHAR(10),
    ward VARCHAR(10),
    community_area VARCHAR(10),
    fbi_code VARCHAR(10),
    x_coordinate FLOAT,
    y_coordinate FLOAT,
    year INT,
    updated_on TIMESTAMP,
    latitude FLOAT,
    longitude FLOAT,
    location VARCHAR(100),
    geom GEOMETRY(Point, 4326)
);

CREATE INDEX idx_crimes_date ON chicago_crimes(crime_date);
CREATE INDEX idx_crimes_type_district ON chicago_crimes(primary_type, district);
CREATE INDEX idx_crimes_geom ON chicago_crimes USING GIST(geom);