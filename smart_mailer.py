#!/usr/bin/python

import collections
import csv
import getopt
import sys
import smtplib
import time

from typing import List, Dict, Tuple

DEPT_ALL = "all"
ARG_MAP = (("d", "dept"), ("c", "contacts"), ("m", "message"))
USAGE_HELPER = "usage: smart_mailer.py --message email_message.txt --contact maildata.csv --dept all"

# Email message placeholders
NAME_PLACEHOLDER = "#name#"
DEPARTMENT_PLACEHOLDER = "#department#"
SENDER_PLACEHOLDER = "#sender#"
RECEIVER_PLACEHOLDER = "#receiver#"

# SMTP server configuration
SMTP_HOSTNAME = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_DELAY = 3
sender = ""  # TODO(FILL IN YOUR EMAIL ADDRESS)
password = ""  # TODO(FILL IN YOUR PASSWORD)

# CSV HEADERS
DEPT_HEADER = "dept"
NAME_HEADER = "names"
EMAIL_ID_HEADER = "email"


# https://stackabuse.com/how-to-send-emails-with-gmail-using-python/
def connect_to_smtp(username: str, password: str, smtp_hostname: str, smtp_port: int):
    """
    Connect to SMTP server
    """
    if username == "" or password == "":
        raise Exception("Username or password cannot be blank!")
    server_ssl = smtplib.SMTP_SSL(smtp_hostname, smtp_port)
    server_ssl.ehlo()
    server_ssl.login(username, password)
    return server_ssl


def disconnect_from_smtp(server_ssl):
    """
    Disconnect from SMTP server
    """
    server_ssl.close()


def send_mail(sender_email: str, receiver_email: str, message: str, smtp_conn) -> bool:
    """
    Send mail to the receiver
    """
    try:
        print(f"sending from <{sender_email}> to <{receiver_email}>")
        smtp_conn.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        print(f"failed to send mail from {sender_email} to {receiver_email}")
        return False
    print(f"message successfully sent from <{sender_email}> to <{receiver_email}>")
    print()
    return True


def send_mails(sender_email: str, receivers: Dict[str, str], placeholder_msg: str, smtp_conn) -> Dict[str, int]:
    """
    Send mails to each receivers.
    :param sender_email: The email addres of the sender
    :param receivers: The data of the receivers: Eg. {"email": "weineng@gmail.com", "name": "weineng", "dept": "HR"}
    :param placeholder_msg: Message (with placeholder) to send to each receiver
    :param smtp_conn: The smtp connection
    :return: The statistics of result to each dept.
    """
    stats = collections.defaultdict(int)
    for data in receivers:
        receiver_email = data[EMAIL_ID_HEADER]
        name = data[NAME_HEADER]
        dept = data[DEPT_HEADER]
        message = parse_message(name, dept, receiver_email, sender_email, placeholder_msg)
        if send_mail(sender_email, receiver_email, message, smtp_conn):
            stats[dept] += 1
        time.sleep(EMAIL_DELAY)  # to prevent spamming
    return stats


def parse_message(name: str, dept: str, receiver_email: str, sender_email: str,msg: str) -> str:
    """
    Replace message placeholder with actual data
    :param name: receiver's name
    :param dept: department of receiver
    :param receiver_email:
    :param sender_email:
    :param msg: message to send to receiver (with placeholders)
    :return: message with placeholder replaced
    """
    return msg\
        .replace(NAME_PLACEHOLDER, name)\
        .replace(DEPARTMENT_PLACEHOLDER, dept)\
        .replace(RECEIVER_PLACEHOLDER, receiver_email)\
        .replace(SENDER_PLACEHOLDER, sender_email)


def filter_by_key(key: str, key_value: str, lst: List[Dict[str, str]]) -> List[Tuple[str, str, str]]:
    """
    Given a header as key, and its key_value, filter from lst all matching values.
    """
    if key is None:
        return lst
    return list(filter(lambda x: key in x and x[key] == key_value, lst))


def read_contact_file(filename: str) -> List[Dict[str, str]]:
    """
    Parse the CSV file into dictionaries into [...{header_field1: value1, header_field2: value2, ...}]
    """
    result = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = None
        for row in csv_reader:
            if header is None:
                header = row
            else:
                result.append(dict(zip(header, row)))
    return result


def parse_args(argv: List[str]) -> Tuple[str, str, str]:
    """
    Helper method to parse arguments passed into the program
    """
    short_arg = (i + ":" for i, _ in ARG_MAP)
    long_arg = (i + "=" for _, i in ARG_MAP)

    # Next line may throw if argv is invalid!
    opts, args = getopt.getopt(argv, "".join(short_arg), list(long_arg))

    message_file = ""
    contacts_file = ""
    dept = ""
    # TODO: CHANGE IF NEEDED!
    for opt, arg in opts:
        if opt in ['-m', '--message']:
            message_file = arg
        elif opt in ['-c', '--contacts']:
            contacts_file = arg
        elif opt in ['-d', '--dept']:
            dept = arg
    return message_file, contacts_file, dept


def read_message(filename: str) -> str:
    """
    Read from file.
    :param filename: The file to be read
    :return: data in the file.
    """
    with open(filename) as f:
        data = f.read()
    return data


def print_stats(stats: Dict[str, int]) -> None:
    """
    Print out reports of emails sent
    :param stats: the number of emails sent per department
    """
    print("Email report:")
    print("---------------")
    for dept, count in stats.items():
        print(f"Send {count} mails to {dept}")


def main(argv: List[str]) -> None:
    try:
        message_file, contacts_file, dept = parse_args(argv)
    except Exception as e:
        print("Error:", e)
        print(USAGE_HELPER)
        return

    # the following calls may throw due to invalid/non-existent files.
    contacts = read_contact_file(contacts_file)
    message = read_message(message_file)

    # Filter by department
    # TODO: CHANGE IF NEEDED!
    if dept == DEPT_ALL:
        contact_to_mail = filter_by_key(None, None, contacts)
    else:
        contact_to_mail = filter_by_key(DEPT_HEADER, dept, contacts)

    # Connect to SMTP
    try:
        smtp_conn = connect_to_smtp(sender, password, SMTP_HOSTNAME, SMTP_PORT)
    except Exception as e:
        print(f"Failed to connect to SMTP: {e}")
        return

    stats = send_mails(sender, contact_to_mail, message, smtp_conn)
    disconnect_from_smtp(smtp_conn)
    print_stats(stats)
    return


if __name__ == "__main__":
    main(sys.argv[1:])
