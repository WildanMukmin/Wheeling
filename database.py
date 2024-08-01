import mysql.connector
import matplotlib.pyplot as plt
from collections import defaultdict

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="skating"
        )
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT NOT NULL
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Assessments (
            assessment_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            date DATE,
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS AssessmentDetails (
            detail_id INT AUTO_INCREMENT PRIMARY KEY,
            assessment_id INT,
            aspect ENUM('keseimbangan', 'kekuatan', 'flexibilitas', 'ketahanan', 'core', 'kemauan'),
            score INT CHECK (score BETWEEN 1 AND 100),
            FOREIGN KEY (assessment_id) REFERENCES Assessments(assessment_id)
        )
        """)

    def add_student(self, name, age):
        self.cursor.execute("INSERT INTO Students (name, age) VALUES (%s, %s)", (name, age))
        self.conn.commit()

    def delete_student(self, student_id):
        self.cursor.execute("DELETE FROM Students WHERE student_id = %s", (student_id,))
        self.conn.commit()

    def add_assessment(self, student_id, date, scores):
        self.cursor.execute("INSERT INTO Assessments (student_id, date) VALUES (%s, %s)", (student_id, date))
        assessment_id = self.cursor.lastrowid
        for aspect, score in scores.items():
            self.cursor.execute("INSERT INTO AssessmentDetails (assessment_id, aspect, score) VALUES (%s, %s, %s)", (assessment_id, aspect, score))
        self.conn.commit()

    def get_all_students(self):
        self.cursor.execute("SELECT * FROM Students")
        return self.cursor.fetchall()
    
    def get_assessments_by_student_id(self, student_id):
        self.cursor.execute("""
            SELECT a.date, ad.aspect, ad.score
            FROM Assessments a
            JOIN AssessmentDetails ad ON a.assessment_id = ad.assessment_id
            WHERE a.student_id = %s
            ORDER BY a.date
        """, (student_id,))
        return self.cursor.fetchall()

    def get_assessments_data(self):
        self.cursor.execute("""
            SELECT s.name, a.date, ad.aspect, ad.score
            FROM Students s
            JOIN Assessments a ON s.student_id = a.student_id
            JOIN AssessmentDetails ad ON a.assessment_id = ad.assessment_id
            ORDER BY s.name, a.date
        """)
        return self.cursor.fetchall()
