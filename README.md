
# Project Title

This python script for creating SSL certificates need files and keys.


## Deployment

To deploy this project run

```bash
  pip install -r requirements.txt
```
Then run
```bash
  python index.py
```



## Variables

To Adjust the file as you needed or to fit your work change these variables

- These variables related to where the files should be saved
`key_path`
`crt_path`
`pem_path`
`pfx_path`

-These varaiable are fro personal preferences. 
`password`
`not_valid_before`
`not_valid_after`
`DNS_name`
`COUNTRY_NAME`
`STATE_OR_PROVINCE_NAME`
`LOCALITY_NAME`
`ORGANIZATION_NAME`
`COMMON_NAME`
## Features

files generated
- .key file contains the private key
- .crt file contains the certificate 
- .pfx file
- .pem file contains the pulbic and private key at the sametime. 

