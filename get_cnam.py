import requests
import csv
from datetime import datetime
import time
import sys
import os


SID = os.environ.get('SID', None)
TOKEN = os.environ.get('TOKEN', None)

now = datetime.now()

result_dict = {}
result_list = []


def get_input():
    print("Reading {}".format(input_filename))
    with open ( os.path.join(input_filename) ) as f:
        input_numbers = f.read().splitlines()
    return(input_numbers)


def get_ocn(phone_number):

    if len(phone_number) is not 10:
        print("***** NUMBER LENGTH IS {} {} *****".format(len(phone_number), phone_number))
        write_csv_error(phone_number, "CHECK LENGTH")
        return()

    url = 'https://api.everyoneapi.com/v1/phone/+{0}'.format(phone_number)
    payload = {'account_sid': SID,
               'auth_token': TOKEN,
               'data': 'carrier,carrier_o'
               }
    r = requests.get(url, params=payload)
    result = r.json()['data']
    price = r.json()['pricing']
    missed = r.json()['missed']

    if len(missed) is not 0:
        print("***** NO MATCH {} *****".format(phone_number))
        write_csv_error(phone_number, "NO MATCH")
        return()

    write_csv_carrier(phone_number, result, price)
    return()


def get_cnam(phone_number):
    if len(phone_number) is not 10:
        print("***** NUMBER LENGTH IS {} {} *****".format(len(phone_number), phone_number))
        write_csv_error(phone_number, "CHECK LENGTH")
        return()

    url = 'https://api.everyoneapi.com/v1/phone/+{0}'.format(phone_number)
    payload = {'account_sid': SID,
               'auth_token': TOKEN,
               'data': 'cnam,name,carrier,carrier_o,linetype,address,location'
               }

    try:
        r = requests.get(url, params=payload)
    except Exception, e:
        write_csv_error(phone_number)
        print(phone_number)
        print(e)
        return()

    print(r.json())
    try:
        result = r.json()['data']
        # print("RESULT")
        # print(result)
        price = r.json()['pricing']
        # print("PRICE")
        # print(price)
        write_csv(phone_number, result, price)
    except Exception, e:
        write_csv_error(phone_number)
        print(e)

    return()


def write_csv_headers():
    print("Writing to {}".format(output_filename))
    with open(output_filename, 'wb') as csvfile:
        my_file = csv.writer(csvfile)
        my_file.writerow([
            "Phone Number",
            "Carrier ID",
            "Carrier Name",
            "Original Carrier ID",
            "Original Carrier Name",
            "CNAM",
            "Derived Name",
            "Line Type",
            "Address",
            "City",
            "State",
            "ZIP",
            "latitude",
            "longitude",
            "Query Cost"
            ])


def write_csv_carrier_headers():
    print("Writing to {}".format(output_filename))
    with open(output_filename, 'wb') as csvfile:
        my_file = csv.writer(csvfile)
        my_file.writerow([
            "Phone Number",
            "Carrier ID",
            "Carrier Name",
            "Original Carrier ID",
            "Original Carrier Name",
            "Query Cost"
            ])



def write_csv(phone_number, data, price):
    with open(output_filename, 'a') as csvfile:
        my_file = csv.writer(csvfile)
        try:
            my_file.writerow([
                phone_number,
                data.get('carrier').get('id'),
                data.get('carrier').get('name'),
                data.get('carrier_o').get('id'),
                data.get('carrier_o').get('name'),
                data.get('cnam'),
                data.get('name'),
                data.get('linetype'),
                data.get('address'),
                data.get('location').get('city'),
                data.get('location').get('state'),
                data.get('location').get('zip'),
                data.get('location').get('geo').get('latitude'),
                data.get('location').get('geo').get('longitude'),
                price.get('total')
                ])
        except Exception, e:
            write_csv_partial(phone_number, data)
            print(e)
    return()


def write_csv_carrier(phone_number, data, price):
    with open(output_filename, 'a') as csvfile:
        my_file = csv.writer(csvfile)
        try:
            my_file.writerow([
                phone_number,
                data.get('carrier').get('id'),
                data.get('carrier').get('name'),
                data.get('carrier_o').get('id'),
                data.get('carrier_o').get('name'),
                price.get('total')
                ])
        except Exception, e:
            print(e)
    return()


def write_csv_error(phone_number):
    with open(output_filename, 'a') as csvfile:
        my_file = csv.writer(csvfile)
        try:
            my_file.writerow([
                phone_number,
                "ERROR",
                "##",
                "##",
                "##"
                ])
        except Exception, e:
            print(e)
    return()


def write_csv_partial(phone_number, data):
    with open(output_filename, 'a') as csvfile:
        my_file = csv.writer(csvfile)
        try:
            my_file.writerow([
                phone_number,
                "ERROR",
                data,
                "##",
                "##",
                "##"
                ])
        except Exception, e:
            print(e)
    return()



def run(numbers):
    start_time = time.time()
    n = 0
    print("Searching for {} numbers..".format(len(numbers)))
    print("Using {}".format(query_type))

    if query_type == "full":
        print("FULL LOOP")
        write_csv_headers()
        for number in numbers:
            stat_time = time.time()
            n = n+1
            print(" {} Lookup for {}... {}".format(n, number, stat_time - start_time))
            try:
                get_cnam(number)
            except Exception, e:
                write_csv_error(number)
                print(e)
        end_time = time.time()
        time.sleep(2)
        print("Batch complete, runtime {}".format(end_time - start_time))
        return()

    if query_type == "ocn":
        print("OCN LOOP")
        write_csv_carrier_headers()
        for number in numbers:
            stat_time = time.time()
            n = n+1
            print(" {} Lookup for {}... {}".format(n, number, stat_time - start_time))
            try:
                get_ocn(number)
            except Exception, e:
                write_csv_error(number)
                print(e)
        end_time = time.time()
        time.sleep(2)
        print("Batch complete, runtime {}".format(end_time - start_time))
        return()


if __name__ == '__main__':
    if len(sys.argv) is not 3:
        print("Input filename and Query type required")
        print("Query type is full or ocn")
        sys.exit()
    else:
        query_type = sys.argv[2]
        input_filename = sys.argv[1]
        print input_filename
        output_filename = "{}_res.csv".format(input_filename)
        print("\n{} Search for numbers in {} \nResults in {}".format(query_type, input_filename, output_filename))
        run(get_input())
