from django.urls import reverse,resolve
from rest_framework.test import APITestCase
from .models import User
from rest_framework import status



class Create_User_Test(APITestCase):
    """ Create User Test Case"""

    def test_user_create(self):
        """ User can create  """

        url = reverse('user-list')
        data = {'username': 'bablu3', 'email': 'bablu3@gmail.com',
                'password': 'bablu@123', 'first_name': 'bablu',
                'last_name': 'bablu', 'date_of_birth': '2023-01-01',
                'phone_number': 2012123, 'street': 'nigdi',
                'city': 'pune','zipcode':411044,'state': 'maharashtra', 'country': 'india'}
        response = self.client.post( url,data, format='json')
        self.assertEqual( response.status_code ,201 )
        print("POST method status code:" ,response.status_code)

    def test_anonymous_user_create(self):
        """ Anonymous User Test """

        url = reverse('user-list')
        data = {'username': 'bablu4', 'email': 'bablu4@gmail.com',
                'password': 'bablu@123', 'first_name': 'bablu',
                'last_name': 'shiv', 'date_of_birth': '2023-01-01',
                'phone_number': 20657659, 'street': 'nigdi',
                'city': 'pune','zipcode':411044, 'state': 'maharashtra', 'country': 'india'}

        response = self.client.post( url,data, format='json')
        self.assertEqual( response.status_code ,status.HTTP_201_CREATED)
        print("POST method status code:", response.status_code)

    def test_admin_create(self):
        """ Admin User Test """

        url = reverse('user-list')
        data = {'username': 'admin1', 'email': 'admin1@gmail.com',
                'password': '1234', 'first_name': 'admin',
                'last_name': 'admin', 'date_of_birth': '2023-01-01',
                'phone_number': 213223, 'street': 'nigdi',
                'city': 'pune','zipcode':411044, 'state': 'maharashtra', 'country': 'india'}

        response = self.client.post( url,data, format='json')
        self.assertEqual( response.status_code ,status.HTTP_201_CREATED)
        print("POST method status code:", response.status_code)


class Read_User_Test(APITestCase):

    """ User Read Test """

    def setUp(self):


        self.user1 = User.objects.create(username='bablu1', email='bablu@gmail.com', password='bablu@123',
                                         first_name='bablu', last_name='shiv', date_of_birth='2023-01-01',
                                         phone_number='201233434', street='nigdi',zipcode='411044', city='pune',state='maharashtra',
                                        country='india')



        self.user3=User.objects.create(username='admin1', email='admin1@gmail.com', password='1234',
                                         first_name='admin', last_name='admin', date_of_birth='2023-01-01',
                                         phone_number='213223', street='nigdi', zipcode='411044', city='pune',state='Maharashtra',
                                         country='india')

    def test_user_read_user_list(self):

        """ User can read user list """


        url = reverse('user-detail')
        response  =self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("GET Method status code:", response.status_code)


    def test_superadmin_read_user_detail(self):
        """ Super Admin Read User Detail """
        self.client.force_authenticate(self.user3)
        url = reverse('user-detail',args=[self.user3.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        print("GET Method status code:",response.status_code)

    def test_Anonymous_user_can_read_user_detail(self):
        """ Anonymous User Test """

        url = reverse ( 'user-detail' , args=[self.user1.id] )
        response = self.client.get ( url )
        self.assertEqual ( response.status_code , status.HTTP_404_NOT_FOUND )
        print ( "GET Method status code:" , response.status_code )


class User_Update_Test ( APITestCase ):
    """ Update User Test Case"""

    def setUp(self):
        """ Test case init data """

        self.user3 = User.objects.create(username='rohan', email='rohan@gmail.com', password='bablu@123',
                                               first_name='rohan', last_name='deshmukh', date_of_birth='2023-01-01',
                                                phone_number='2013412', street='nigdi',zipcode='411042', city='pune',
                                               state='maharashtra',country='india')



        self.user13 = User.objects.create ( username='avinash' , email='avinash@gmail.com' , password='bablu@123' ,
                                           first_name='avi' , last_name='pawar' , date_of_birth='2023-01-01' ,
                                           phone_number='22223333' , street='nigdi' , zipcode='411043' , city='pune' ,
                                           state='maha' , country='india' )

        self.user15 = User.objects.create ( username='rushi' , email='rushi@gmail.com' , password='bablu@123' ,
                                            first_name='rushi' , last_name='chavan' , date_of_birth='2023-02-02' ,
                                            phone_number='2131122' , street='nigdi' , zipcode='33232' , city='pune' ,
                                            state='maha' , country='india' )


    def test_user_can_update(self):
        """ User can update """

        url = reverse ( 'user-detail' , args=[self.user3.id] )
        data = {'username': 'abc2', 'email': 'rohan@gmail.com',
                'password': 'bablu@123', 'first_name': 'bablu',
                'last_name': 'bablu', 'date_of_birth': '2023-01-07',
                'phone_number': 201212365, 'street': 'nigdi',
                'city': 'pune','zipcode':411044,'state': 'maharashtra', 'country': 'india'}
        self.client.force_authenticate ( self.user3 )
        response = self.client.put ( url , data , format='json' )
        self.assertEqual ( response.status_code , status.HTTP_200_OK )
        print ( "PUT method status code:" , response.status_code )


    def test_anonymous_user_can_update(self):
        """  Anonymous Update Test """

        url = reverse ( 'user-detail' , args=[self.user13.id] )
        data = {'username': 'pranav', 'email': 'avinash@gmail.com',
                'password': 'bablu@123', 'first_name': 'pranav',
                'last_name': 'pranav', 'date_of_birth': '2023-01-02',
                'phone_number': 223344, 'street': 'pimpri',
                'city': 'mumbai','zipcode':411044,'state': 'maha', 'country': 'up'}
        response = self.client.put ( url , data , format='json' )
        self.assertEqual ( response.status_code , status.HTTP_404_NOT_FOUND )
        print ( "PUT method status code:" , response.status_code )

    def test_admin_can_update_user_detail(self):
        """ User can update """

        url = reverse ( 'user-detail' , args=[self.user15.id] )
        data = {'username': 'abcde' , 'email': 'rushi@gmail.com' ,
                'password': 'bablu@123' , 'first_name': 'babluu' ,
                'last_name': 'babluu' , 'date_of_birth': '2023-01-07' ,
                'phone_number': 20121234 , 'street': 'pimpri' ,
                'city': 'punee' , 'zipcode': 411044 , 'state': 'maharashtra' , 'country': 'indiaa'}
        self.client.force_authenticate ( self.user15 )
        response = self.client.put ( url , data , format='json' )
        self.assertEqual ( response.status_code , status.HTTP_200_OK )
        print ( "PUT method status code:" , response.status_code )


class User_Delete_Test(APITestCase):
    """ User can Delete """

    def setUp(self):


        self.user6 = User.objects.create(username='bablu5', email='bablu5@gmail.com', password='bablu@123',
                                          first_name='puru', last_name='shiv', date_of_birth='2023-01-01',
                                          phone_number=2012343, street='nigdi', zipcode= 411044 , city='Pune',
                                           state='Maharashtra',country='India')

        self.user12 = User.objects.create ( username='xyz' , email='xyz1@gmail.com' , password='bablu@123' ,
                                           first_name='xyz' , last_name='xyz' , date_of_birth='2023-01-01' ,
                                           phone_number=2222222 , street='nigdi' , zipcode=411044 , city='pune' ,
                                           state='maharashtra' , country='india' )

        self.user14 = User.objects.create ( username='abcd' , email='abcd@gmail.com' , password='bablu@123' ,
                                            first_name='abcd' , last_name='abcd' , date_of_birth='2023-01-01' ,
                                            phone_number=22213232 , street='nigdi' , zipcode=411044 , city='pune' ,
                                            state='maharashtra' , country='india' )

    #user delete
    def test_user_delete(self):
        """ User Delete test"""
        self.client.force_authenticate(self.user12)
        url = reverse('user-detail', args=[self.user12.id])
        response = self.client.delete(url, self.user12.id, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print("DELETE method status code:", response.status_code)

    def test_Anonymous_user_can_delete(self):
        """ Anonymous User Test """

        url = reverse ( 'user-detail' , args=[self.user6.id] )
        response = self.client.delete ( url , self.user6.id , format='json' )
        self.assertEqual ( response.status_code , status.HTTP_404_NOT_FOUND )
        print ( "DELETE method status code:" , response.status_code )


    def test_admin_can_delete_user_detail(self):
        """ Admin Can Delete The User Detail """

        self.client.force_authenticate(self.user14)
        url = reverse('user-detail', args=[self.user14.id])
        response = self.client.delete(url, self.user14.id, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print("DELETE method status code:", response.status_code)


class Test_login_logout(APITestCase):
    def setUp(self):
        """ Login And Logout User """

        self.profile = User.objects.create_user(username="salman", password="bablu@123",
                                            date_of_birth="2023-02-02", phone_number="3233241",street="nigdi",
                                            zipcode="33232", first_name="salman", last_name="khan",
                                            email="salman@gmail.com", city="pune", state="maha", country="india")

    def test_login_User(self):
        """ login User Test"""

        user = User.objects.get()
        self.client.force_authenticate(user=user)
        response = self.client.post(
        reverse('login'),
        {"username": "salman", "password": "bablu@123", "email": "salman@gmail.com"}
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print ( "POST method status code:" , response.status_code )

    def test_logout(self):
        """ User Logout Test"""
        user = User.objects.get ()
        self.client.force_authenticate ( user=user )
        response = self.client.post (
        reverse ( 'logout' ))
        self.assertEqual ( response.status_code ,status.HTTP_200_OK )
        print ( "POST method status code:" , response.status_code)


































































































































































"""
class User_Login_Test ( APITestCase ):
   

    def setUp(self):
        

        self.user11 = User.objects.create(
            username="rushi", password="bablu@123", date_of_birth="2023-02-01", phone_number="1231122",
            street="nigdi", zipcode="33232", first_name="rushi", last_name="chavan",
            email="rushi@gmail.com", city="pune", state="maha", country="india"
        )

    def test_user_login(self):
      

        url = reverse ( 'user-list' , args=[self.user11.id] )
        data = {
            "key": "4bcc295fd0dac1fdea1ff99268c3f1de387a8e1c" ,
            "userid": 'id'

        }
        self.client.force_authenticate ( self.user11 )
        response = self.client.put ( url , data , format='json' )
        self.assertEqual ( response.status_code , 200 )
        print ( "Post method status code:" , response.status_code )

    def test_user_logout(self):
        url = reverse ( 'user-login' , args=[self.user11.id] )
        data = {'username': 'rushi', 'email': 'rushi@gmail.com',
                'password': 'bablu@123', 'first_name': 'rushi',
                'last_name': 'chavan', 'date_of_birth': '2023-02-01',
                'phone_number': 1231122, 'street': 'nigdi',
                'city': 'pune','zipcode':33232,'state': 'maha', 'country': 'india'}
        self.client.force_authenticate ( self.user11 )
        response = self.client.put ( url , data , format='json' )
        self.assertEqual ( response.status_code , 200 )
        print ( "Post method status code:" , response.status_code )"""




"""
class Test_login(APITestCase):
    def setUp(self):
        self.user = Create_User.objects.create_user(
            username="rushi", password="bablu@123", date_of_birth="2023-02-01", phone_number="1231122",
            street="nigdi", zip_code="33232", first_name="rushi", last_name="chavan",
            email="rushi@gmail.com", city="pune", state="maha", country="india"
        )

    def user_login(self):
        user = CustomUser.objects.get()
        self.client.force_authenticate(user=user)
        response = self.client.post(
            reverse('user-login'),
            {"username": "rushi", "password": "bablu@123", "email": "rushi@gmail.com"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)"""




















































