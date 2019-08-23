#!/usr/bin/python3

from subprocess import Popen, PIPE
import pandas as pd


def check_ip(ip_addr, test_origin):
    test_origin = 'AS' + test_origin

    # Query on AfriNIC

    # grep origin
    database = 'AfriNIC'
    p = Popen(["whois", "-h" "whois.afrinic.net", '{}'.format(ip_addr)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    asn = Popen(["grep", "origin"], stdin=p.stdout, stdout=PIPE, stderr=PIPE)

    (db_origin, err) = asn.communicate()

    if db_origin == b'':
        report = 'Ip has no route object'
    else:
        db_origin = db_origin[16:].decode("utf-8").rstrip()

    if db_origin == test_origin:
        report = '{} matched with {} on database'.format(test_origin, db_origin)
    elif db_origin != b'' and db_origin != test_origin:
        report = '{} did not match with {} on database'.format(test_origin, db_origin)

    if db_origin == test_origin:
        match = 'True'
    else:
        match = 'False'

    return ip_addr, test_origin, database, match, report


if __name__ == '__main__':
    path = input("Enter file name: ")
    df = pd.read_excel('{}'.format(path), index_col=[0, 1])
    df_out = pd.DataFrame({'Prefix': [], 'Origin ASN': [], 'Database': [], 'Match': [], 'Report': []})

    for index, row in df.iterrows():
        results = check_ip('{}'.format(index[0]), '{}'.format(index[1]))

        new_df = pd.DataFrame({
            "Prefix": [results[0]],
            "Origin ASN": [results[1]],
            "Database": [results[2]],
            "Match": [results[3]],
            "Report": [results[4]],
        })

        df_out = df_out.append(new_df, ignore_index=True)

    #     Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('Results-{}'.format(path), engine='xlsxwriter')

    #     Convert the dataframe to an XlsxWriter Excel object.
    df_out.to_excel(writer, sheet_name='Sheet1')

    #     Close the Pandas Excel writer and output the Excel file.
    writer.save()

    print("Success! ")

