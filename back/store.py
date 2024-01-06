import sqlite3
import json
import cv2
import numpy as np
# from methods import *
import os
import imghdr

def create_database():
    conn = sqlite3.connect('image_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY,
            filename TEXT NOT NULL,
            color_descriptor TEXT,
            form_descriptors TEXT,
            UNIQUE(filename)
        )
    ''')

    conn.commit()
    conn.close()


def insert_image(filename, color_descriptor, form_descriptors):
    conn = sqlite3.connect('image_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO images (filename, color_descriptor, form_descriptors)
        VALUES (?, ?, ?)
    ''', (filename, json.dumps(color_descriptor), json.dumps(form_descriptors)))

    conn.commit()
    conn.close()


def read_all_images():
    conn = sqlite3.connect('image_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM images')
    rows = cursor.fetchall()

    conn.close()
    return [__read_image(row) for row in rows]


def read_image_by_id(image_id):
    conn = sqlite3.connect('image_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM images WHERE id = ?', (image_id,))
    row = cursor.fetchone()

    conn.close()
    if row:
        return __read_image(row)


def __read_image(image):
    return {'id': image[0],"path":image[1], 'color_descriptor': json.loads(image[2]), 'form_descriptors': json.loads(image[3])}


def get_image_path(image_id):
    conn = sqlite3.connect('image_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT filename FROM images WHERE id = ?', (image_id,))
    row = cursor.fetchone()

    conn.close()
    if row:
        return row[0]

def is_image(file_path):
    return imghdr.what(file_path) is not None

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            if is_image(file_path):
                image = cv2.imread(file_path)
                color_descriptor = color_method(image)
                form_descriptors = form_method(image)
                insert_image(file_path, color_descriptor, form_descriptors)

# if __name__ == '__main__':
    # create_database()
    # process_folder('images')
        
    
