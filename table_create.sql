CREATE DATABASE housemon_db;

use housemon_db;

/*
physical unit name and long description 
*/
CREATE TABLE physical_unit (
    id INT NOT NULL AUTO_INCREMENT UNIQUE,
    name CHAR(20) NOT NULL,
    description CHAR(100),
    PRIMARY KEY(id)
);

/*
A single kind of sensor package that you might
buy a whole bunch of at once 
*/
CREATE TABLE sensor_type (
    id INT NOT NULL AUTO_INCREMENT UNIQUE,
    name CHAR(100) NOT NULL,
    physical_unit INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(physical_unit)
        REFERENCES physical_unit(id)
);

/* 
This is a named location somewhere in the world. 
It has an official open location code, plus a more
colloquial description like "downstairs bathroom" or
something like that 
*/
CREATE TABLE location (
    id INT NOT NULL AUTO_INCREMENT UNIQUE,
    description CHAR(100) NOT NULL UNIQUE,
    olc_code CHAR(16) NOT NULL,
    PRIMARY KEY (id)
);


/*
 This is an individual sensor, of type "sensor_type", 
 it has a current location plus a "name" which is 
 probably a unique serial number or something 
 like that 
*/
CREATE TABLE sensor (
    id INT NOT NULL AUTO_INCREMENT UNIQUE,
    type INT NOT NULL,
    location INT NOT NULL,
    name CHAR(100) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (type)
        REFERENCES sensor_type(id),
    FOREIGN KEY (location)
        REFERENCES location(id)
);

/*
All the sensor measurements including time, location, 
the individual sensor, the raw value, and any 
calibrated value
*/
CREATE TABLE measurement (
        id INT NOT NULL AUTO_INCREMENT UNIQUE,
        time INT UNSIGNED NOT NULL,
        sensor_id INT NOT NULL,
        raw_value FLOAT,
        PRIMARY KEY (id),
        FOREIGN KEY (sensor_id)
            REFERENCES sensor(id)
);

/*
This is a table of thermometer calibrations, really 
just meant to be an example. This has capability of
holding up to a 3-point calibration with a time
stamp. The idea there is you can accumulate 
calibrations and maybe you want to see how they are
drifting or whatever. 

CREATE TABLE thermometer_cal (
    id INT NOT NULL AUTO_INCREMENT UNIQUE,
    sensor_id INT NOT NULL,
    time INT UNSIGNED NOT NULL,
    cal_1_pt DOUBLE,
    cal_1_val DOUBLE,
    cal_2_pt DOUBLE,
    cal_2_val DOUBLE,
    cal_3_pt DOUBLE,
    cal_3_val DOUBLE,
    PRIMARY KEY (id),
    FOREIGN KEY (sensor_id)
        REFERENCES sensor(id)
);
*/