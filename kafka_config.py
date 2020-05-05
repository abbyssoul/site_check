import os 

topic_name = 'site_status'

# Address of a bootstrap server
bootstrap_servers = os.getenv("KAFKA_SERVERS")

# Place your ssl sert in the keys directory and uncomment this lines
# to connect to Kafka using ssl auth.
#ssl_cafile = "keys/ca.pem"
#ssl_certfile = "keys/service.cert"
#ssl_keyfile = "keys/service.key"
