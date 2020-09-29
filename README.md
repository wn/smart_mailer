# Smart mailer

A python script to mass send emails to folks in different departments.

## To use

- Fill in credentials in `smtp_config.py`
- Set email message in email_message.txt
- Set contact list in maildata.csv

```python
# usage python3 smart_mailer.py --message <email file> --contact <contacts file> --dept '<dept to filter>'

# To send to everyone in contact
python3 smart_mailer.py --message email_message.txt --contact maildata.csv --dept 'all'

# To send to dept "Team X"
python3 smart_mailer.py --message email_message.txt --contact maildata.csv --dept 'Team X'
```

## Notes

To use the app with gmail, it is necessary to set ["Less secure app access"](https://support.google.com/accounts/answer/6010255?authuser=2&p=lsa_blocked&hl=en-GB&authuser=2&visit_id=637369444787376366-3108823837&rd=1)
