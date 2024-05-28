from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta, UTC
from cryptography.hazmat.primitives.serialization import pkcs12
import os

# Define paths
key_path = r"dev-misr-solera.key"
crt_path = r"dev-misr-solera.crt"
pem_path = r"no.pwd.dev-misr-solera.pem"
pfx_path = r"dev-misr-solera.pfx"

password = b'password' # secret key of your application
not_valid_before =  datetime.now(UTC)
not_valid_after = datetime.now(UTC) + timedelta(days=365 * 10) # 10 years
DNS_name = u"localhost"

COUNTRY_NAME = u"EG" #change these
STATE_OR_PROVINCE_NAME= u"Cairo" #change these
LOCALITY_NAME= u"Masr ElGdeda" #change these
ORGANIZATION_NAME= u"SETTEL" #change these
COMMON_NAME= u"dev.settel-payments.com"

# Generate RSA private key
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Write the private key to a file
with open(key_path, "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(password),  # Replace with your password
    ))

# Create a self-signed certificate
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, COUNTRY_NAME), #change these
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, STATE_OR_PROVINCE_NAME), #change these
    x509.NameAttribute(NameOID.LOCALITY_NAME, LOCALITY_NAME), #change these
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, ORGANIZATION_NAME), #change these
    x509.NameAttribute(NameOID.COMMON_NAME, COMMON_NAME), #change these
])
cert = (x509.CertificateBuilder()
.subject_name(subject)
.issuer_name(issuer)
.public_key(key.public_key())
.serial_number(x509.random_serial_number())
.not_valid_before(not_valid_before)
.not_valid_after(not_valid_after) # Certificate valid for 10 years
.add_extension(x509.SubjectAlternativeName([x509.DNSName(DNS_name)]),critical=False)
.sign(key, hashes.SHA256()) # replace that with SHA1
) 

# Write the certificate to a file
with open(crt_path, "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

# Create a PKCS#12 file (PFX)
pfx = pkcs12.serialize_key_and_certificates(
    b"mykey",
    key,
    cert,
    None,
    serialization.BestAvailableEncryption(password) 
)
with open(pfx_path, "wb") as f:
    f.write(pfx)


# Write the combined key and certificate to a PEM file
with open(pem_path, "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))
    f.write(cert.public_bytes(serialization.Encoding.PEM))