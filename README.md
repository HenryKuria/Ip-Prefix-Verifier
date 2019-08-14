**AfriNIC prefix Verifier**

inputs:
    excel document containing:

        col A has the ips in the form ip/mask
        col B has the ASN in the format AS..
        

**How it works**

The script uses the whois command to check the AfriNIC database

You should modify the path in the script to point to your spreadsheet

**Installation** 

clone the script, make it executable

pip install -r requirements.txt

run script



