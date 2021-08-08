# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 18:19:46 2021

@author: Chad
"""

def add_temperature(cnx_details, record):
    import mysql.connector as mariadb
    try:
        connection = mariadb.connect(
            user = cnx_details[0],
            password = cnx_details[1],
            database = cnx_details[2],
            host = cnx_details[3],
            port = cnx_details[4])
        
        cursor = connection.cursor()
    except mariadb.Error as err: 
        print("Error in add_temperatures while connecting to db: {}".format(err))
        return -1
    
    insert_query = """INSERT INTO measurement (time, sensor_id, raw_value) VALUES (%s, %s, %s) """
    
    cursor.execute(insert_query, record)
        
    connection.commit()
    cursor.close();
    connection.close();

def get_sensor_id(cnx_details, name):
    import mysql.connector as mariadb
    
    try:       
        connection = mariadb.connect(
        user = cnx_details[0],
        password = cnx_details[1],
        database = cnx_details[2],
        host = cnx_details[3],
        port = cnx_details[4])
    
        cursor = connection.cursor()
    
        id_query = "SELECT id FROM sensor WHERE name='%s'" % name
        cursor.execute(id_query, name)
               
    except mariadb.Error as err: 
        print("Error in get_sensor_id: {}".format(err))
        return -1
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    sensor_id = cursor.next()[0]        
    cursor.close()
    connection.close()
    return sensor_id    
    

def add_new_sensor_type(cnx_details, name):
    import mysql.connector as mariadb
    
    checker = lambda x: str.isalnum(x) | str.isspace(x)
    name = ''.join(filter(checker, name.strip()))
            
    try:
        connection = mariadb.connect(
            user = cnx_details[0],
            password = cnx_details[1],
            database = cnx_details[2],
            host = cnx_details[3],
            port = cnx_details[4])
    
        cursor = connection.cursor()
        insert_query = """INSERT INTO sensor_type (name) VALUES (%s) """
        cursor.execute(insert_query, name)
        connection.commit()
    
        id_query = """SELECT id FROM sensor_type WHERE name=(%s)"""
        cursor.execute(id_query, name)
               
    except mariadb.Error as err: 
        print("Error in add_new_sensor_type: {}".format(err))
        return -1
    
    finally:
        if connection.isconnected():
            cursor.close()
            connection.close()
 

    new_id = cursor.next()[0]        
    cursor.close()
    connection.close()
    return new_id    
    
    
    cursor.close();
    connection.close();

def add_new_location(cnx_details, description, olc_code):
    import openlocationcode.openlocationcode as olc
    import mysql.connector as mariadb    
    
    checker = lambda x: str.isalnum(x) | str.isspace(x);
    description = ''.join(filter(checker, description.strip()))
    
    if olc.isValid(olc_code):
        query = "INSERT INTO location (description, olc_code) VALUES (\"" + description + "\", \"" + olc_code + "\");"
    else:
        print("Invalid open location code")
        return -1
        
    id_query = "SELECT id FROM location WHERE description = \"" + description + "\";"
    
    try:
        connection = mariadb.connect(
            user = cnx_details[0],
            password = cnx_details[1],
            database = cnx_details[2],
            host = cnx_details[3],
            port = cnx_details[4])
        
        cursor = connection.cursor()        
        cursor.execute(query)
        connection.commit()
        cursor.execute(id_query)

    except mariadb.Error as err:
        print("Error in add_new_location() {}".format(err))
    finally:
        if connection.isconnected():
            cursor.close()
            connection.close()

    new_id = cursor.next()[0]        
    cursor.close()
    connection.close()
    return new_id
