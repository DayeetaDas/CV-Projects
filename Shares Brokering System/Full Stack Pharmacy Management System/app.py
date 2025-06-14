import flask
from flask_mail import Mail, Message
import smtplib
import email
import os
from flask import Flask,render_template,request,redirect, flash, session, url_for
from flask_login import login_required, current_user, login_user, logout_user
from flask_login_multi.login_manager import LoginManager
from flask_bootstrap import Bootstrap
from database import UserModel, db,login, PatientBloodTest, Pharmacist,Prescription, Medication, collections,BloodTest
from datetime import date, timedelta, datetime

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'xyz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharmacyDB3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

 
db.init_app(app)
login.init_app(app)
login.login_view = 'login'

#loading the user details for login
@login.user_loader
def load_user(user_id):
    return UserModel.query.get(user_id)

#model view created to authenticate user.
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.authenticated

admin = Admin(app)
admin.add_view(ModelView(Pharmacist, db.session))
admin.add_view(ModelView(UserModel, db.session))

#creation of tables in databse
@app.before_first_request
def create_all():
    db.create_all()


#Login for Admin
@app.route('/', methods = ['POST', 'GET'])
def loginAdmin():
    if request.method == 'POST':
        session.pop('user', None)
        email = request.form['email'] #requesting email and password from the form
        admin = Pharmacist.query.filter_by(email = email).first() #SQL Alchemy search by email
        if admin is not None and admin.check_password(request.form['password']): #check for admin
            login_user(admin)
            session['user_name'] = admin.name
            session['user_Sid'] = admin.S_id
            session['user_ID'] = admin.id
            return redirect('/profileAdmin') #returns the admin home page
        else:
            flash("Login Unsuccessful.", "info") #flashs error message at unsuccessful login
    return render_template('loginAdmin.html') #the login page is returned on unsucessful login 
    
#Login page for patient
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/patientpage')
        else:
            flash("Login Unsuccessful", "info")
    return render_template('login.html')

# Register page for patient 
@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        #user details are requested from the form
        if UserModel.query.filter_by(email=email).first(): #If email is already used error occurs.
            return ('Email already Present')

        user = UserModel(name=name, surname= surname, email=email, username=username)
        user.set_password(password)
        current_user.name = name
        current_user.surname = surname
        db.session.add(user)
        db.session.commit() #details are committed to the database
        return redirect('/profile1') #patient home page is returned
    return render_template('register.html') #register home page is returned

#logout page for pharmacist
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

#logout page for user 
@app.route('/logoutPatient')
def logoutPatient():
    logout_user()
    return redirect('/login')

#Patients home page which returns their username and surname
@app.route('/patientpage')
#@login_required
def patientpage():

    return render_template('patientpage.html', name = current_user.name, surename = current_user.surname)

#medications page - staitc page just being routed 
@app.route('/medications')
#@login_required
def medicationpage():
    
    return render_template('medications.html')

#patient home page showing patients name and surname
@app.route('/profile1')
#@login_required
def profile():
    
    return render_template('profile1.html', name = current_user.name, surname = current_user.surname)

#profile admin is the pharmacist home page
@app.route('/profileAdmin')
#@login_required
def profileAdmin():
    
    return render_template('profileAdmin.html', name = session['user_name'], id = session['user_Sid'])

#Request page shows the list of prescriptions in the system
@app.route('/requests', methods = ['POST', 'GET'])
#@login_required
def requests():
    #list of medicines, dates, bloodtests and summary
    listData = []
    medi = []
    medicine = ""
    date = ""
    collection = ""
    collection_details = ""
    validBloodTests = []
    invalidBloodTests = []
    summary = []
    summary3 = ""
    
    
    prescriptionsList = Prescription.query.filter_by(collection_status = "Uncollected").all() #SQL Alchemy query for uncollected prescriptions
    print(prescriptionsList)
    for prescription in prescriptionsList: #iteration through the prescripiton list 
        medNames2 = []
        medNames = " "
        patients = UserModel.query.filter_by(id = prescription.patient_id).first() #Query for patients with an unique prescription ID 
        meds = Medication.query.filter_by(prescription_id = prescription.id).all() #Qurty for medications with prescription ID 
        print(len(meds)) #length of medicaitons
        testDate = " "
        for med in meds: #iteration through the number of medications with that prescription id
            print(med.medicationName)
            medNames2.append(med.medicationName)
            medNames = ', '.join(medNames2) #Joining list of medications with a comma
            print(med.id)
            bloodTests = BloodTest.query.filter_by(medication_id = med.id).all() #Query of bloodtest depending on medication ID 
            lenBTest = len(bloodTests)
            print(lenBTest)
            if lenBTest == 0: #if no blood tests are in the blood tests then blood test is not required 
                print("No blood test is required for " + med.medicationName)
                med.status = True
                db.session.commit() #medication status is commited to the DB 
            for bloodTest in bloodTests: #Loop through bloodtests 
                print(bloodTest)
                pBloodTest = PatientBloodTest.query.filter_by(patient_id = prescription.patient_id, name = bloodTest.bloodTestName).all() #patient blood tests are queried 
                lenBT = len(pBloodTest)
                print(pBloodTest)
                if lenBT == 0: # if there are no patient blood tests with the prescription id and blood test name
                    med.status = False #med status false and blood test is required 
                    print("Blood test required for " + bloodTest.bloodTestName)
                    db.session.commit()
                for test in pBloodTest:
                    if(test.testDate >= bloodTest.bloodTestDate): #Blood test validity check 
                        med.status = True
                        db.session.commit()
                        print("Blood Test valid")
                    else:                        
                        med.status = False
                        print(prescription.status)
                        print("Blood test " + bloodTest.bloodTestName +" out of date for " + med.medicationName )
                        db.session.commit()
                    
                if med.status == False:
                    prescription.status == False
                    db.session.commit()
                else:
                    prescription.status == True
                    db.session.commit()

        if (prescription.status == True):
            print(prescription.status)
            status = "Prescriptions is Approved"
        elif(prescription.status == False):
            status = "Prescription requires attention"
                        
        tup = (patients.name, prescription.id, medNames, prescription.prescriptionDate, status, prescription.collection_status) #initalised as a tuple
        listData.append(tup) #data appended to list
    print(listData)
                        
    if request.method == 'POST':
        session.pop('user', None)
        prescriptionID = request.form['prescription_id']
        bloodTestRequired = " "  
        try:
            prescriptionQ = Prescription.query.filter_by(id = prescriptionID).first() #Querying of related data 
            user = UserModel.query.filter_by(id = prescriptionQ.patient_id).first()
            meds = Medication.query.filter_by(prescription_id = prescriptionQ.id).all()
            pBloodTest = PatientBloodTest.query.filter_by(patient_id = prescriptionID).all()
        except AttributeError as error:
            print("no such entry")
        
        #pBloodTest = PatientBloodTest.query.filter_by(patient_id = prescriptionID, name = bloodTest.bloodTestName).all()

        if user is not None:

            session['patient_name'] = user.name
            session['patient_surname'] = user.surname
            session['patient_id'] = user.id
            session['patient_mail'] = user.email

            for med in meds:
                medi.append(med.medicationName)
                medicine = ', '.join(medi)

            for test in pBloodTest:
                date = test.testDate

            if prescriptionQ.status == True: #creating prescription summary 
                summary3 = "Prescription is ready to be collected. The prescription includes " + medicine
                collection = prescriptionQ.prescriptionDate + timedelta(days = 5)
                collection_details = str(collection) + ", Please come anytime between 2:30 pm - 4:30 pm for collecting medications."

                
            elif prescriptionQ.status == False :
                usermeds = Medication.query.filter_by(status = False, prescription_id = prescriptionQ.id).all()
                print(usermeds)
                for usermed in usermeds:
                    bloodTests1 = BloodTest.query.filter_by(medication_id = usermed.id).all()
                    lenbloodTest = len(bloodTests1)
                    for bloodTest in bloodTests1:
                        print(bloodTest)
                        pBloodTest1 = PatientBloodTest.query.filter_by(patient_id = prescriptionQ.patient_id, name = bloodTest.bloodTestName).all()
                        lenBT = len(pBloodTest1)
                        print(pBloodTest1)
                        if lenBT == 0:
                            summarise = bloodTest.bloodTestName + " blood test is required for the medication " + usermed.medicationName
                            print(summarise)
                            summary.append(summarise)
                            summary3 = '. '.join(summary)
                        
                        else:
                            for test in pBloodTest1:
                                if(test.testDate <= bloodTest.bloodTestDate):
                                    summarise = ("Blood test " + bloodTest.bloodTestName +" out of date for " + med.medicationName)
                                    summary.append(summarise)
                                    summary3 = '.\n'.join(summary)
                            
        
                collection_details = "A test is out of date. \nPlease review blood tests by contacting your GP."
                print(summary3)


                #using sessions to hold key data 
            session['medicine'] = medicine
            session['prescriptionID'] = prescriptionID
            session['status'] = prescriptionQ.status
            session['presDate'] = prescriptionQ.prescriptionDate
            session['collection_status'] = prescriptionQ.collection_status
            session['collectionDate'] = str(collection)
            session['collection'] = collection_details
            session['summary3'] = summary3

            return redirect('/prescription') #returns prescriptions page which shows individual prescription of user
    return render_template('requests.html', requests = listData) #returns list data to the requests page

#Collections page shows the patients ready for collection
@app.route('/collections', methods = ['POST', 'GET'])
#@login_required
def Collections():
    collectionsData = []
    collectionQ = collections.query.all()#Querying all of the collections table 
    for collection1 in collectionQ:
        print(collection1)
        prescriptionR = Prescription.query.filter_by(id = collection1.prescription_id).first()
        medicationR = Medication.query.filter_by(prescription_id = prescriptionR.id).all()
        patientR = UserModel.query.filter_by(id = prescriptionR.patient_id).first()
        medi = []
        medNames = ""
        for med in medicationR: #iterating through medicaitons 
            medi.append(med.medicationName)
            medNames = ', '.join(medi)

        tup1 = (collection1.prescription_id, patientR.name, medNames, collection1.collection_date, collection1.status)
        collectionsData.append(tup1)
    print(collectionsData)

    if request.method == 'POST': 
        session.pop('user', None)
        collectionID = request.form['collection_id']
        user = UserModel.query.filter_by(id = collectionID).first()
        try:
            prescriptionQ = Prescription.query.filter_by(id = collectionID).first()
            user = UserModel.query.filter_by(id = prescriptionQ.patient_id).first()
            meds = Medication.query.filter_by(prescription_id = prescriptionQ.id).all()
            pBloodTest = PatientBloodTest.query.filter_by(patient_id = collectionID).all()
        except AttributeError as error:
            print("No such entry could be found please try again.","info")
        if user is not None:
            session['patient_name'] = user.name
            session['patient_surname'] = user.surname
            session['patient_id'] = user.id
            session['patient_mail'] = user.email
            
            medi2 = []
            medicine = ""

            for med in meds:
                medi2.append(med.medicationName)
                medicine = ', '.join(medi2)
            

            for test in pBloodTest:
                date = test.testDate

            if prescriptionQ.status == True:
                summary3 = "Prescription is ready to be collected. The prescription includes " + medicine
                collection = prescriptionQ.prescriptionDate + timedelta(days = 5)
                collection_details = str(collection) + ", Please come anytime between 2:30 pm - 4:30 pm for collecting medications."

                
            elif prescriptionQ.status == False :
                usermeds = Medication.query.filter_by(status = False, prescription_id = prescriptionQ.id).all()
                print(usermeds)
                for usermed in usermeds:
                    bloodTests1 = BloodTest.query.filter_by(medication_id = usermed.id).all()
                    for bloodTest in bloodTests1:
                        print(bloodTest)
                        pBloodTest1 = PatientBloodTest.query.filter_by(patient_id = prescriptionQ.patient_id, name = bloodTest.bloodTestName).all()
                        lenBT = len(pBloodTest1)
                        print(pBloodTest1)
                        if lenBT == 0:
                            summarise = bloodTest.bloodTestName + " blood test is required for the medication " + usermed.medicationName
                            print(summarise)
                            summary.append(summarise)
                            summary3 = '. '.join(summary)
                        
                        else:
                            for test in pBloodTest1:
                                if(test.testDate <= bloodTest.bloodTestDate):
                                    summarise = ("Blood test " + bloodTest.bloodTestName +" out of date for " + med.medicationName)
                                    summary.append(summarise)
                                    summary3 = '.\n'.join(summary)
                            
        
                collection_details = "A test is out of date. \nPlease review your blood tests and contact your GP."
                print(summary3)
            
            print(collectionID)
            session['medicine'] = medicine
            session['colID'] = collectionID
            session['status'] = prescriptionQ.status
            session['presDate'] = prescriptionQ.prescriptionDate
            session['collection_status'] = prescriptionQ.collection_status
            session['collectionDate'] = str(collection)
            session['collection'] = collection_details
            session['summary3'] = summary3
        return redirect('/collectionsPage') 

    return render_template('collections.html', collections = collectionsData)

#prescriptions page shows details of a prescription 
@app.route('/prescription',methods = ['POST', 'GET'])
#@login_required
def prescription():
    if request.method == 'POST':
        if session['status'] == True: #checks for the status of prescription - this function shows the ability to  send emails 
            string = "Dear "+ str(session['patient_name']) + " " + str(session['patient_surname']) + "," + "\n" + "These are your prescribed medicines: " + str(session['medicine']) +"." + str(session['collection']) + "\n" + "Kind regards," + "\n" + "Open Source Pundits"
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("punditsopensource@gmail.com", "opensource") #email login
            server.sendmail("sourceopen50@gmail.com", session['patient_mail'], string)
            session['emailMessage'] = string #email message
            prescriptionsList1 = Prescription.query.filter_by(collection_status = "Uncollected", id = session['prescriptionID']).first()
            print(prescriptionsList1)
            prescriptionsList1.collection_status = "Waiting for collection"           
            newCollection = collections(collection_date = session['collectionDate'], prescription_id = prescriptionsList1.id, status = "Waiting for collection")
            db.session.add(newCollection)
            db.session.commit() #database commit

        else:
            string = "Dear "+ str(session['patient_name']) + " " + str(session['patient_surname']) + "," + "\n" + "You prescription status has been upheld please read the following:" +"\n" + str(session['summary3'])+ ". Please contact your GP." + "\n" + "Kind regards," + "\n" + "Open Source Pundits"
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("punditsopensource@gmail.com", "opensource")
            server.sendmail("sourceopen50@gmail.com", session['patient_mail'], string)
            session['emailMessage'] = string
        return redirect("/mail") # redirected to mail confirmation  page

        
    #prescriptions page details are returned to the page
    return render_template('prescription.html', name = session['patient_name'], surname = session['patient_surname'], 
                            id = session['patient_id'], medicine = session['medicine'], date = session['presDate'],
                            collection = session['collection'], email = session['patient_mail'], summary = session['summary3'])

#Collection page shows a summary of details of the collection
@app.route('/collectionsPage',methods = ['POST', 'GET'])
#@login_required
def collectionsPage():
    collectionPatient = collections.query.filter_by(prescription_id = session['colID']).first() #If user has already collected then user must not be able to get reminder or collected button functionality 
    if collectionPatient.status == "Collected":
        print("No")
    else:
        if request.method == 'POST': 
            if request.form['action'] == "collected":
                prescriptionsList1 = Prescription.query.filter_by(collection_status = "Waiting for collection", id = session['patient_id']).first() #changing collection status to collected
                collectionQ = collections.query.filter_by(prescription_id = session['colID']).first()
                print(collectionQ)
                collectionQ.status = "Collected"
                prescriptionsList1.collection_status = "Collected"
                db.session.commit()
                return redirect("/collections")
            elif request.form['action'] == "send_reminder": #sending a reminder to the user by email
                string = "Dear "+ str(session['patient_name']) + " " + str(session['patient_surname']) + "," + "\n" + "These are your prescribed medicines: " + str(session['medicine']) +"." + "Please come anytime to collect." + "\n" + "Kind regards," + "\n" + "Open Source Pundits"
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login("punditsopensource@gmail.com", "opensource")
                server.sendmail("punditsopensource@gmail.com", session['patient_mail'], string)
                session['emailMessage'] = string
            return redirect("/reminder")
    
    return render_template('collectionsPage.html', name = session['patient_name'], surname = session['patient_surname'], 
                            id = session['patient_id'], medicine = session['medicine'], date = session['presDate'],
                            collection = session['collection'], email = session['patient_mail'], summary = session['summary3'])
#confirmation of email being sent 
@app.route('/mail')
#@login_required
def mail_sent():
    return render_template('mail.html', emailMessage = session['emailMessage'], name = session['patient_name'], surname = session['patient_surname'], email = session['patient_mail'] )
#cofirmation of reminder being sent
@app.route('/reminder')
#@login_required
def reminder_sent():
    return render_template('reminder.html', emailMessage = session['emailMessage'], name = session['patient_name'], surname = session['patient_surname'], email = session['patient_mail'] )

#settings page for patient 
@app.route('/Settings')
#@login_required
def settings():

    return render_template('Settings.html', name = current_user.name, surename = current_user.surname)

#Ability to change password of the user 
@app.route('/changePassword', methods = ['POST', 'GET'])
#@login_required
def changePassword():
    if request.method == 'POST':
        password = request.form['newpassword']
        confirmpassword = request.form['confirmpassword']
        userID = current_user.id 
        if password == confirmpassword:
            current_user.set_password(password)
            db.session.commit()
            return redirect("/changePassword")
            flash("Password has been reset", "info")
        else:
            flash("Passwords do not match try again.", "info")
            return redirect("/changePassword")
            
    return render_template('changePassword.html')

#Collections page for patient shows the patients orders and collection status 
@app.route('/collectionsPatient')
#@login_required
def collection_patient():
    #prescription id, medications, collection date, prescription status ,collection status
    patient_id = current_user.id
    print(patient_id)
    prescriptionPatient = Prescription.query.filter_by(patient_id = patient_id).all()
    listColPatients = []
    for prescriptionP in prescriptionPatient: #Iteration through prescriptions 
        if prescriptionP.status == True:
            print(prescriptionP.id)
            medicationsPatient = Medication.query.filter_by(prescription_id = prescriptionP.id).all() # Querying 
            collectionsPatient = collections.query.filter_by(prescription_id = prescriptionP.id).first()
            print(collectionsPatient)
            mediPatient = []
            medicinePatient = ""
            for medicationP in medicationsPatient: #iteration through medications
                mediPatient.append(medicationP.medicationName)
                medicinePatient = ', '.join(mediPatient)
            tupPatient = (prescriptionP.id, medicinePatient,collectionsPatient.collection_date, "Prescription has been approved.", prescriptionP.collection_status)
            listColPatients.append(tupPatient)
        else:
            medicationsPatient = Medication.query.filter_by(prescription_id = prescriptionP.id).all()
            mediPatient = []
            medicinePatient = ""
            for medicationP in medicationsPatient:
                mediPatient.append(medicationP.medicationName)
                medicinePatient = ', '.join(mediPatient)
            tupPatient = (prescriptionP.id, medicinePatient,"-", "Please check email for update.", prescriptionP.collection_status)
            listColPatients.append(tupPatient)

    return render_template('collectionsPatient.html', collectionPatientL = listColPatients)
#settings page for admin
@app.route('/settingsAdmin')
#@login_required
def settingsAdmin():

    return render_template('settingsAdmin.html', name = session['user_name'])
#Changing password for admin
@app.route('/changePasswordAdmin', methods = ['POST', 'GET'])
#@login_required
def changePasswordAdmin():
    if request.method == 'POST':
        password = request.form['newpassword']
        confirmpassword = request.form['confirmpassword']
        userID = session['user_ID'] 
        admin = Pharmacist.query.filter_by(id = userID).first()
        if password == confirmpassword:
            admin.set_password(password)
            db.session.commit()
            return redirect("/changePassword")
            flash("Password has been reset", "info")
        else:
            flash("Passwords do not match try again.", "info")
            return redirect("/changePassword")
            
    return render_template('changePasswordAdmin.html')

#Error handling 
@app.errorhandler(500)
def not_found(e):
    return render_template("500.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

@app.errorhandler(400)
def not_found(e):
    return render_template("400.html")



if __name__ =="__main__":
    app.run(debug=True)


 