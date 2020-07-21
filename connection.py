import ibm_db

dsn_driver = "IBM DB2 ODBC DRIVER"
dsn_database = "BLUDB"           
dsn_hostname = "dashdb-txn-sbox-yp-lon02-07.services.eu-gb.bluemix.net"
dsn_port = "50000"             
dsn_protocol = "TCPIP" 
dsn_uid = "lps30376" 
dsn_pwd = "9m88-tjmx1p3c1zz" 

dsn = (
    "DRIVER={{IBM DB2 ODBC DRIVER}};"
    "DATABASE={0};"
    "HOSTNAME={1};"
    "PORT={2};"
    "PROTOCOL=TCPIP;"
    "UID={3};"
    "PWD={4};").format(dsn_database, dsn_hostname, dsn_port, dsn_uid, dsn_pwd)

conn = ibm_db.connect(dsn, "", "")

