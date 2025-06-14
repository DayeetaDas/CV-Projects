from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from datetime import date
 
login = LoginManager()
db = SQLAlchemy()

#User Model used as a table for the patient and pharmacist login details
class UserModel(UserMixin, db.Model):
    __tablename__ = 'Patient'
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())
    prescriptions = db.relationship('Prescription', backref='Patient', lazy=True)
    pBloodTest = db.relationship('PatientBloodTest', backref='Patient', lazy=True)

    def set_password(self,password): #set password for hashing
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password): #checking password 
        return check_password_hash(self.password_hash,password)

#Patient blood test table
class PatientBloodTest(db.Model): 
    __tablename__ = "PatientBloodTest"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    testDate = db.Column(db.Date)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.id'), nullable=False)

class Pharmacist(UserMixin, db.Model):
    __tablename__ = 'Pharmacist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    S_id = db.Column(db.Integer) #staff ID
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())
    prescriptions = db.relationship('Prescription', backref='Pharmacist', lazy=True) #FK to prescriptions table

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
#Prescriptions table
class Prescription(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    prescriptionDate = db.Column(db.Date, default=date.today) #Date at which prescription has been created
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.id'), nullable=False)
    pharmacist_id = db.Column(db.Integer, db.ForeignKey('Pharmacist.id'), nullable=False)
    status = db.Column(db.Boolean, nullable = False)
    medications = db.relationship('Medication', backref='prescription', lazy = True) #Linking prescriptions to medications table
    collection = db.relationship('collections', backref='prescription', lazy = True) #Linking prescriptions to collections table
    collection_status = db.Column(db.String(30)) #Prescriptions collections status

#Medication table
class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicationName = db.Column(db.String(100))
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescription.id'), nullable = False) #FK prescription id in Medications table
    bloodTest = db.relationship('BloodTest', backref='BloodTest', lazy = True)
    status = db.Column(db.Boolean, nullable = False) #status of medication

#Blood test table
class BloodTest(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    bloodTestName = db.Column(db.String(100))
    bloodTestDate = db.Column(db.Date)
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'), nullable = False) #FK medication id in Blood test table

#Collections table
class collections(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    collection_date = db.Column(db.String(50))
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescription.id'), nullable = False) #FK prescription id in Collections table 
    status = db.Column(db.String(30), nullable = False)

#loading the user model
@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))
 