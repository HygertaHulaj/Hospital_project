import streamlit as st
import pandas as pd 
import sqlite3

conn = sqlite3.connect('Hospital.sqlite')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS Patients(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Birth_date TEXT,
    Phone_number INTEGER,
    Type_of_visit TEXT,
    Doctor_id INTEGER,
    FOREIGN KEY (Doctor_id) REFERENCES Doctors(ID))""")


cur.execute("""CREATE TABLE IF NOT EXISTS Doctors(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Birth_date TEXT,
    Phone_number INTEGER,
    Specialisation TEXT)""")

def add_patient(Name, Phone_number, Birth_date, Type_of_visit):
    cur.execute("INSERT INTO Patients (Name, Phone_number, Birth_date, Type_of_visit) VALUES (?, ?, ?, ?)",
              (Name, Phone_number, Birth_date, Type_of_visit))
    conn.commit()
    st.success('Patient added to database!')
def add_doctors(Name, Phone_number, Birth_date, Specialisation):
    cur.execute("INSERT INTO Doctors (Name, Phone_number, Birth_date, Specialisation) VALUES (?, ?, ?, ?)",
              (Name, Phone_number, Birth_date, Specialisation))
    conn.commit()
    st.success('Doctors added to database!')
def update_patient(ID, Name=None, Phone_number=None, Birth_date=None, Type_of_visit=None):
    update_cols = []
    update_vals = []
    if Name is not None:
        update_cols.append('Name = ?')
        update_vals.append(Name)
    if Phone_number is not None:
        update_cols.append('Phone_number = ?')
        update_vals.append(Phone_number)
    if Birth_date is not None:
        update_cols.append('Birth_date = ?')
        update_vals.append(Birth_date)
    if Type_of_visit is not None:
        update_cols.append('Type_of_visit = ?')
        update_vals.append(Type_of_visit)
    if len(update_cols) == 0:
        st.warning('Please specify at least one field to update')
        return
    update_cols_str = ', '.join(update_cols)
    update_vals.append(ID)
    cur.execute(f"UPDATE Patients SET {update_cols_str} WHERE ID = ?", update_vals)
    conn.commit()
    st.success('Patient information updated')

def view_patients():
    st.subheader('List of patients')
    cur.execute("SELECT * FROM Patients")
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=['ID', 'Name', 'Phone number', 'Birth Date', 'Type of Visit'])
    st.dataframe(df)
def view_doctors():
    st.subheader('List of doctors')
    cur.execute("SELECT * FROM Doctors")
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=['ID', 'Name', 'Phone number', 'Birth Date', 'Specialisation'])
    st.dataframe(df)
def delete_patient(patient_id):
    cur.execute("DELETE FROM Patients WHERE ID=?", (patient_id,))
    conn.commit()
    st.success('Patient deleted from database!')

def main():
    st.title('Hospital Hygerta Hulaj')
    menu = ['Welcome','Add Patient', 'View Patients', 'Add Doctors','View Doctors']
    choice = st.sidebar.selectbox('Select an option', menu)
    if choice == 'Welcome':
        st.header('Welcome to our Hospital :sunglasses:')
    elif choice == 'Add Patient':
        st.subheader('Add new patient')
        Name = st.text_input('Name')
        Birth_date= st.text_input('Date of birth')
        Phone_number = st.text_input('Phone number')
        Type_of_visit = st.selectbox('Type of visit', ['Surgery', 'Normal Visit', 'Urgency'])
        if st.button('Add Patient'):
            add_patient(Name, Phone_number, Birth_date, Type_of_visit)
    elif choice == 'Add Doctors':
        st.subheader('Add new doctor')
        Name = st.text_input('Name')
        Birth_date= st.text_input('Date of birth')
        Phone_number = st.text_input('Phone number')
        Specialisation = st.selectbox('Specialisation', ['Mjeku familjar', 'Kardiolog', 'Oftamotologu'])
        if st.button('Add Doctor'):
            add_doctors(Name, Phone_number, Birth_date, Specialisation)
    elif choice == 'View Patients':
        view_patients()
        dropbox = ['Delete Patient','Update Patient']
        choices = st.selectbox('Select an option', dropbox)
        if choices == 'Delete Patient':
            st.subheader('Delete patient')
            patient_id = st.text_input('Patient ID')
            if st.button('Delete Patient'):
                delete_patient(patient_id)
        elif choices == 'Update Patient':
            patient_id = st.text_input('Patient ID')
            Name = st.text_input('Name')
            Birth_date= st.text_input('Date of birth')
            Phone_number = st.text_input('Phone number')
            Type_of_visit = st.selectbox('Type of visit', ['Surgery', 'Normal Visit', 'Urgency'])
            if st.button('Update Patient'):
                update_patient(patient_id, Name, Phone_number, Birth_date, Type_of_visit)

        
        

    elif choice == 'View Doctors':
        view_doctors()

if __name__ == '__main__':
    main()

conn.commit()
conn.close()
