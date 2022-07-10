import os
from django.http import JsonResponse
from pandas import read_csv
from Contacts.models.contacts import Contact



class ProcessCSV:
    '''
    Function to populate DB with CSV records.
    This function takes a CSV file, reads it and populates the database with it's values.
    It takes away duplicat records based on phone numbers.
    '''
    def csv_record_upload(self, csv_file, user):
        # Read the CSV file using pandas
        df = read_csv(csv_file)
        df.dropna(subset="phone_number", inplace=True)
        # Drops phone number duplicates
        data = df.drop_duplicates(subset=["phone_number"], keep="first")

        # Empty list to accept valid data from CSV
        valid_data = []

        # Iterate over each row to check if phone number doesn't exist already
        for row in data.iterrows():
            try:
                Contact.objects.get(
                    phone_number=row[1]['phone_number'],
                )
            except Contact.DoesNotExist:
                # If phone number does not exist already, create an item in the empty array
                valid_data.append(
                    Contact(
                        first_name=row[1]["first_name"],
                        middle_name=row[1]["middle_name"],
                        last_name=row[1]["last_name"],
                        phone_number=row[1]["phone_number"],
                        address=row[1]["address"],
                        user=user
                    )
                )
        log_msg = '========= Uploading ' + str(len(valid_data)) + ' records ============'
        print(log_msg)
        # Bulk create records in the database
        Contact.objects.bulk_create(valid_data, batch_size=10000, ignore_conflicts=True)

        # Return a success message
        return JsonResponse({'status': 'Success','message': "Data uploaded to db successfully"}, safe=False)

