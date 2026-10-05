# ============================================================
# FILE: database.py - FINAL FOR DAY 11
# ROLE: Database Engineer (DE)
# PURPOSE: All database read/write functions in one place.
# ============================================================
  
import mysql.connector 
from dotenv import load_dotenv 
import os 
  
# Load secret values from .env file 
load_dotenv() 
  
def get_connection(): 
    """Opens a connection to MySQL."""
    return mysql.connector.connect( 
        host=os.getenv("DB_HOST"), 
        user=os.getenv("DB_USER"), 
        password=os.getenv("DB_PASSWORD"), 
        database=os.getenv("DB_NAME"), 
    ) 
  
# ============================================================
# FROM DAY 10 -- Patient functions (same as before)
# ============================================================
  
def get_patient(patient_id): 
    conn = get_connection() 
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,)) 
    patient = cursor.fetchone()
    conn.close() 
    return patient 
  
def get_all_patients(): 
    conn = get_connection() 
    cursor = conn.cursor(dictionary=True) 
    cursor.execute("SELECT id, name, age, gender FROM patients ORDER BY id") 
    patients = cursor.fetchall()
    conn.close() 
    return patients 
  
# ============================================================
# NEW FOR DAY 11 -- 3 functions add zale
# ============================================================
  
def find_empty_bed(ward): 
    """
    Ward madhe khali bed aahe ka te shodhte.
    Example: ward = "General"
    """
    conn = get_connection() 
    cursor = conn.cursor(dictionary=True) 
    cursor.execute(
        """
        SELECT bed_id, bed_number, bed_type 
        FROM beds 
        WHERE ward = %s AND is_occupied = 0 
        LIMIT 1 
        """, 
        (ward,) 
    ) 
    bed = cursor.fetchone() 
    conn.close() 
    return bed    # None if no empty bed

def get_on_duty_nurse(ward): 
    """
    Tya ward madhe duty var kon nurse aahe te shodhte.
    """
    conn = get_connection() 
    cursor = conn.cursor(dictionary=True) 
    cursor.execute(
        """
        SELECT nurse_name, shift_start, shift_end 
        FROM staff_shifts 
        WHERE ward = %s AND is_on_duty = 1 
        LIMIT 1 
        """, 
        (ward,) 
    ) 
    nurse = cursor.fetchone() 
    conn.close() 
    return nurse   # None if no one on duty
  
def assign_bed_to_patient(patient_id, bed_id, nurse_name): 
    """
    Patient la bed assign karte.
    1. beds table madhe is_occupied = 1 karte
    2. bed_assignments madhe history lihite
    """
    conn = get_connection() 
    cursor = conn.cursor() 
  
    try: 
        # Step 1: Mark bed as occupied
        cursor.execute(
            """
            UPDATE beds 
            SET is_occupied = 1, patient_id = %s 
            WHERE bed_id = %s 
            """, 
            (patient_id, bed_id) 
        ) 
  
        # Step 2: Write history log
        cursor.execute(
            """
            INSERT INTO bed_assignments 
            (patient_id, bed_id, nurse_assigned, assigned_at, assigned_by) 
            VALUES (%s, %s, %s, NOW(), 'ai_agent') 
            """, 
            (patient_id, bed_id, nurse_name) 
        ) 
  
        conn.commit()
        conn.close() 
        return True 
  
    except Exception as e: 
        conn.rollback() 
        conn.close() 
        print(f"Database error: {e}") 
        return False
    
    
