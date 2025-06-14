import os
import unittest
from app import app, db

#####  Unit testing ####

## To run the unit testing it is important to make changes to the app.py file before.
## Please comment out the @login_required in app.py file


class FlaskTestCase(unittest.TestCase):
    #Flask set up test
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type = 'html/text')
        self.assertEqual(response.status_code, 200)
        
    #### Testing to login page for admin ####
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type ='html/text')
        self.assertTrue(b'Welcome to OCP Pharmacy' in response.data)

    def test_Pharmacist_correct_login(self):
        tester = app.test_client(self)
        response = tester.post('/', data = dict(email = 'jj@yahoo.com', password = 'anything'),
        follow_redirects = True
        )
        self.assertTrue(b'Staff Member Details' in response.data)
    
    def test_Pharmacist_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post('/', data = dict(email = 'jj332r@yahoo.com', password = 'anyt42f4fhing'))
        self.assertTrue(b'Login Unsuccessful' in response.data)

    ### Testing login page for Patient ### 

    def test_Patient_correct_login(self):
        tester = app.test_client(self)
        response = tester.post('/login', data = dict(email = 'jj@yahoo.com', password = 'anything'),
        follow_redirects = True
        )
        self.assertTrue(b'Welcome to OCP Pharmacy' in response.data)
    
    def test_Patient_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post('/login', data = dict(email = 'jj332r@yahoo.com', password = 'anyt42f4fhing'))
        self.assertTrue(b'Login Unsuccessful' in response.data)
    

    ### Testing requests page ###
    
    def test_requests_1(self):
        tester = app.test_client(self)
        response = tester.get('/requests', content_type ='html/text')
        self.assertTrue( b'<td>Prescription requires attention</td>' in response.data)
    
    def test_requests_2(self):
        tester = app.test_client(self)
        response = tester.get('/requests', content_type ='html/text')
        self.assertTrue( b'Prescription ID' in response.data)

    def test_requests_1(self):
        tester = app.test_client(self)
        response = tester.get('/requests', content_type ='html/text')
        self.assertTrue( b'Name' in response.data)

    def test_requests_2(self):
        tester = app.test_client(self)
        response = tester.get('/requests', content_type ='html/text')
        self.assertTrue( b'Medication' in response.data)

    def test_requests_3(self):
        tester = app.test_client(self)
        response = tester.get('/requests', content_type ='html/text')
        self.assertTrue( b'Prescription Date' in response.data)    
    
    def test_requests_4(self):
        tester = app.test_client(self)
        response = tester.get('/requests', content_type ='html/text')
        self.assertTrue( b'Status' in response.data)

    def test_requests_5(self):
        tester = app.test_client(self)
        response = tester.get('/requests', content_type ='html/text')
        self.assertTrue( b'Collection Status' in response.data)

    def test_requests_6(self):
        tester = app.test_client(self)
        response = tester.get('/requests', content_type ='html/text')
        self.assertTrue( b'Prescription requires attention' in response.data)
    
    def test_requests_7(self):
        tester = app.test_client(self)
        response = tester.get('/requests', content_type ='html/text')
        self.assertTrue( b'Uncollected' in response.data)


    ### Testing prescription page 
    
    def test_prescription_1(self):
        tester = app.test_client(self)
        response = tester.post('/requests', data = dict(prescription_id = 4),
        follow_redirects=True)
        self.assertTrue(b'Dayeeta' in response.data)
    
    def test_prescription_2(self):
        tester = app.test_client(self)
        response = tester.post('/requests', data = dict(prescription_id = 5),
        follow_redirects=True)
        self.assertTrue(b'Rishi' in response.data)
    
    def test_prescription_3(self):
        tester = app.test_client(self)
        response = tester.post('/requests', data = dict(prescription_id = 2),
        follow_redirects=True)
        self.assertTrue(b'Maya' in response.data)
    
    def test_prescription_4(self):
        tester = app.test_client(self)
        response = tester.post('/requests', data = dict(prescription_id = 2),
        follow_redirects=True)
        self.assertTrue(b'Prescription Details' in response.data)

    def test_prescription_5(self):
        tester = app.test_client(self)
        response = tester.post('/requests', data = dict(prescription_id = 2),
        follow_redirects=True)
        self.assertTrue(b'Medicines' in response.data)
    

    
    
    
    ### Testing collections page ###
    def test_collections(self):
        tester = app.test_client(self)
        response = tester.get('/collections', content_type ='html/text')
        self.assertTrue( b'Prescription ID' in response.data)

    def test_collections_1(self):
        tester = app.test_client(self)
        response = tester.get('/collections', content_type ='html/text')
        self.assertTrue( b'Name' in response.data)

    def test_collections_2(self):
        tester = app.test_client(self)
        response = tester.get('/collections', content_type ='html/text')
        self.assertTrue( b'Medications' in response.data)

    def test_collections_3(self):
        tester = app.test_client(self)
        response = tester.get('/collections', content_type ='html/text')
        self.assertTrue( b'Collection Date' in response.data)    
    
    def test_collections_4(self):
        tester = app.test_client(self)
        response = tester.get('/collections', content_type ='html/text')
        self.assertTrue( b'Collection Status' in response.data)

    def test_collections_5(self):
        tester = app.test_client(self)
        response = tester.get('/collections', content_type ='html/text')
        self.assertTrue( b'Collected' in response.data)

    def test_collections_6(self):
        tester = app.test_client(self)
        response = tester.get('/collections', content_type ='html/text')
        self.assertTrue( b'Waiting for collection' in response.data)

    

    ### Testing CollectionsPage ###

    def test_collectionP_1(self):
        tester = app.test_client(self)
        response = tester.post('/collections', data = dict(collection_id = 1),
        follow_redirects=True)
        self.assertTrue(b'Rishi Singh' in response.data)
    
    def test_collectionP_1_1(self):
        tester = app.test_client(self)
        response = tester.post('/collections', data = dict(collection_id = 1),
        follow_redirects=True)
        self.assertTrue(b'Collection Details' in response.data)
    
    def test_collectionP_1_3(self):
        tester = app.test_client(self)
        response = tester.post('/collections', data = dict(collection_id = 1),
        follow_redirects=True)
        self.assertTrue(b'Olanzapine, Medikinet, Amiodarone' in response.data)
    
    def test_collectionP_1_3(self):
        tester = app.test_client(self)
        response = tester.post('/collections', data = dict(collection_id = 1),
        follow_redirects=True)
        self.assertTrue(b'Prescription is ready to be collected. The prescription includes Olanzapine, Medikinet, Amiodarone' in response.data)
    
    def test_collectionP_2(self):
        tester = app.test_client(self)
        response = tester.post('/collections', data = dict(collection_id = 2),
        follow_redirects=True)
        self.assertTrue(b'Maya' in response.data)

    def test_collectionP_2_1(self):
        tester = app.test_client(self)
        response = tester.post('/collections', data = dict(collection_id = 2),
        follow_redirects=True)
        self.assertTrue(b'Mon, 15 Feb 2021 00:00:00 GMT' in response.data)
    
    ### Testing medications page ###

    def test_medication_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/medications', content_type ='html/text')
        self.assertTrue(b'Collections' in response.data)
    
    def test_medication_page_1(self):
        tester = app.test_client(self)
        response = tester.get('/medications', content_type ='html/text')
        self.assertTrue(b'Medication Page' in response.data)

    def test_medication_page_2(self):
        tester = app.test_client(self)
        response = tester.get('/medications', content_type ='html/text')
        self.assertTrue(b'Paracetamol' in response.data)
    
    def test_medication_page_3(self):
        tester = app.test_client(self)
        response = tester.get('/medications', content_type ='html/text')
        self.assertTrue(b'Acetaminophen' in response.data)

    def test_medication_page_4(self):
        tester = app.test_client(self)
        response = tester.get('/medications', content_type ='html/text')
        self.assertTrue(b'56 tablet' in response.data)

    ### Testing change password admin ###

    def test_changePassword_Admin_loads(self):
        tester = app.test_client(self)
        response = tester.get('/changePasswordAdmin', content_type ='html/text')
        self.assertTrue(b'Change User Password' in response.data)

    def test_changePassword_Admin_1(self):
        tester = app.test_client(self)
        response = tester.get('/changePasswordAdmin', content_type ='html/text')
        self.assertTrue(b'New Password' in response.data)
    
    def test_changePassword_Admin_2(self):
        tester = app.test_client(self)
        response = tester.get('/changePasswordAdmin', content_type ='html/text')
        self.assertTrue(b'Confirm New Password' in response.data)


if __name__ == '__main__':
    unittest.main()