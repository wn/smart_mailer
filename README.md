# Smart mailer

A python script to mass send emails to folks in different departments.

## To use

- Fill in credentials in `smtp_config.py`

```python
# usage python3 smart_mailer.py --message <email file> --contact <contacts file> --dept '<dept to filter>'

# To send to everyone in contact
python3 smart_mailer.py --message email_message.txt --contact maildata.csv --dept 'all'

# To send to dept "Team X"
python3 smart_mailer.py --message email_message.txt --contact maildata.csv --dept 'Team X'
```
