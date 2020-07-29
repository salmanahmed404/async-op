import csv
import sys

from faker import Faker

FIELD_NAMES = ['name', 'address', 'discipline', 'cgpa', 'date_recorded']

def create_csv(records):
    """
    Function which creates a csv file with dummy data
    """
    fake = Faker()
    with open('../data/dummy.csv', 'w', newline='') as dummy_csv:
        
        csvwriter = csv.DictWriter(dummy_csv, fieldnames=FIELD_NAMES)
        csvwriter.writeheader()
        for i in range(records):
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
    if (len(sys.argv) > 1):
        create_csv(int(sys.argv[1]))
    else:
        create_csv(20000)
