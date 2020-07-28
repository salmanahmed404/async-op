import csv

from faker import Faker

RECORDS = 10000
FIELD_NAMES = ['name', 'address', 'discipline', 'cgpa', 'date_recorded']

def create_csv():
    """
    Function which creates a csv file with dummy data
    """
    fake = Faker()
    with open('../data/dummy_med.csv', 'w', newline='') as dummy_csv:
        
        csvwriter = csv.DictWriter(dummy_csv, fieldnames=FIELD_NAMES)
        csvwriter.writeheader()
        for i in range(RECORDS):
            csvwriter.writerow({
                'name': fake.name(),
                'address': fake.street_address(),
                'discipline': fake.word(ext_word_list=[
                    'Mechanical', 'Computer', 'Electrical', 'Electronics', 'Civil'
                ]),
                'cgpa': fake.random_digit_not_null(),
                'date_recorded': fake.date_this_decade(before_today=True, after_today=False)
            })
    
    print ('File creation complete')


if __name__ == '__main__':
    create_csv()
