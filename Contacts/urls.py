from django.urls import path
from .views.contacts_view import AddNewContact, RetrieveSingleRecord, UpdateSingleRecord, DeleteSingleRecord, RetrieveAllRecords, UploadCSV



urlpatterns = [
    path('add-new-record/', AddNewContact.as_view(), name="Add New Record"),
    path('get-record/<int:record_id>', RetrieveSingleRecord.as_view(), name="Get Record"),
    path('update-record/<int:record_id>', UpdateSingleRecord.as_view(), name="Update Record"),
    path('delete-record/<int:record_id>', DeleteSingleRecord.as_view(), name="Delete Record"),
    path('get-all-records/<int:page_number>', RetrieveAllRecords.as_view(), name="Retrieve All Records"),
    path('upload-csv/', UploadCSV.as_view(), name="Upload CSV"),
    
    
]
