from os import path
import os
from django.utils.datastructures import MultiValueDictKeyError
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models.contacts import Contact
from helpers.status_codes import ContactAlreadyExists, RecordDoesNotExist, KeyError
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from helpers.validations import check_parameters
from ..views.csv_upload import ProcessCSV
from django.core.files.storage import FileSystemStorage
from config.keys import CSV_PATH

class AddNewContact(APIView):
    # Authenticate the incoming request
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request, *args, **kwargs):
        '''
        Recieve all or some input from user request. 
        Only phone_number is required, the rest are optional
        '''
        phone_number = request.data.get('phone_number')
        first_name = request.data.get('first_name')
        middle_name = request.data.get('middle_name')
        address = request.data.get('address')
        last_name = request.data.get('last_name')
        user = self.request.user
        email = user.email

        # Check if request contains phone_number
        check_parameters(phone_number, 'phone_number')

        try:
            '''
            Retrieve record from database with phone entered.
            If phone number already exists, return appropriate error message
            '''
            Contact.objects.get(phone_number = phone_number)
            raise ContactAlreadyExists()
        except Contact.DoesNotExist:
            # If contact does not exist, save the request data
            details = {
                'phone_number' : phone_number,
                'first_name' : first_name,
                'middle_name' : middle_name,
                'address' : address,
                'last_name' : last_name,
                'user':user
            }
            # Create a record in the database
            Contact.objects.create(**details)
            # Return success message to user
            return JsonResponse({'status': 'Success', 'message': 'Record created successfully'}, status=status.HTTP_201_CREATED, safe=False) 


class RetrieveSingleRecord(APIView):
    # Authenticate the incoming request
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        # Get record ID from request url
        record_id = self.kwargs['record_id']

        # Check if record ID is empty or not in url
        check_parameters(record_id, 'record_id')

        try:
            # Retrieve record by record ID
            contact = Contact.objects.filter(pk=record_id).values()

            # Return record data and success message
            return JsonResponse({'status': 'Success', 'message': 'Record retrieved successfully', 'data':contact[0] }, safe=False)
        except IndexError:
            # If record does not exist, raise an exception
            raise RecordDoesNotExist()
             

class UpdateSingleRecord(APIView):
    # Authenticate the incoming request
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def put(self, request, *args, **kwargs):
        # Get record ID from request url
        record_id = self.kwargs['record_id']

        # Check if record ID is empty or not in url
        check_parameters(record_id, 'record_id')

        try:
            # Retrieve record by ID
            contact = Contact.objects.get(pk = record_id)

            # Update record based on the request data received
            if 'first_name' in request.data:
                contact.first_name = request.data['first_name']
            if 'middle_name' in request.data:
                contact.middle_name = request.data['middle_name']
            if 'last_name' in request.data:
                contact.last_name = request.data['last_name']
            if 'phone_number' in request.data:
                contact.phone_number = request.data['phone_number']
            if 'address' in request.data:
                contact.address = request.data['address']
            # Save record
            contact.save()
            # Return a success message
            return JsonResponse({'status': 'Success', 'message': 'Record updated successfully'}, safe=False)
        except Contact.DoesNotExist:
            # Raise exception if record does not exist
            raise RecordDoesNotExist()


class DeleteSingleRecord(APIView):
    # Authenticate the incoming request
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def delete(self, request, *args, **kwargs):
        record_id = self.kwargs['record_id']

        # Check if record ID is empty or not in url
        check_parameters(record_id, 'record_id')

        try:
            # Retrieve record by ID
            contact = Contact.objects.get(pk = record_id)
            print(contact)
            # Delete record
            contact.delete()
            # Return success message
            return JsonResponse({'status': 'Success', 'message': 'Record deleted successfully'}, safe=False)
        except Contact.DoesNotExist:
            # Raise exception if record does not exist
            raise RecordDoesNotExist()

class RetrieveAllRecords(APIView):
    # Authenticate the incoming request
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        '''
        Get page number from url
        '''
        page_number = self.kwargs['page_number']

        # Check if page number is empty or not in url
        check_parameters(page_number, 'page_number')

        # Retrieve all records, ordering by date they were added
        records = Contact.objects.filter().order_by('date_added').values()

        # A general response
        response = 'Retrieved records successfully'

        # Creating a paginator object by 20 items each
        data = Paginator(records, 20) 
        try:
            # Returns the desired page object
            page = data.get_page(page_number)  
            total = data.count  
            total_pages = data.num_pages  
       
            data = list(page)
            # Return the paginated data, with the necessary accompanied data and success message
            return JsonResponse({'status': 'Success', 'message': response, "current_page": page_number,
            "total_records": total, "total_pages": total_pages , "data" :data}, safe=False)
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page = data.get_page(1)  # returns the desired page object
            total = data.count  
            total_pages = data.num_pages  

            data = list(page)
            # Return the paginated data, with the necessary accompanied data and success message
            return JsonResponse({'status': 'Success', 'message': response, "current_page": 1,
            "total_records": total, "total_pages": total_pages , "data" :data}, safe=False)
        except EmptyPage:
            # if page is empty then return last page
            page = data.page(data.num_pages)
            total = data.count  
            total_pages = data.num_pages  

            data = list(page)
            # Return the paginated data, with the necessary accompanied data and success message
            return JsonResponse({'status': 'Success', 'message': response, "current_page": data.num_pages,
            "total_records": total, "total_pages": total_pages , "data" :data}, safe=False)

class UploadCSV(APIView):
    # Authenticate the incoming request
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        email = user.email
        try:
            csv_file = request.FILES['csv']
        except MultiValueDictKeyError:
            raise KeyError()

        # Save the uploaded file locally
        fs = FileSystemStorage(location=CSV_PATH)
        filename = csv_file.name
        fs.save(str(filename), csv_file)

        filepath = CSV_PATH+str(filename)

        # Call function to upload records from CSV file
        csv_function = ProcessCSV()
        csv_function.csv_record_upload(filepath, user)

        # Delete CSV file after successful upload
        if path.exists(filepath):
            os.remove(filepath)

        return JsonResponse({'status': 'Success','message': "Data uploaded to database successfully"}, safe=False)
