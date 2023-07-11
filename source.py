#Importing boto3
import boto3

# Importing the psycopg2 library for PostgreSQL database connectivity
import psycopg2

#Importing json library
import json

# Establishing a connection to the PostgreSQL database
conn = psycopg2.connect(
   host="0.0.0.0",
   port= 5432,
   database="postgres",
   user="postgres",
   password="postgres"
)

# Creating a cursor object to interact with the database
cursor = conn.cursor()

# Creating an SQS client with AWS access key and secret access key
sqs = boto3.client('sqs',
                   region_name='us-east-1',
                   endpoint_url='http://localhost:4566',
                   aws_access_key_id='YOUR_ACCESS_KEY',
                   aws_secret_access_key='YOUR_SECRET_ACCESS_KEY')

# Specifying the queue URL
queue_url = 'http://localhost:4566/000000000000/login-queue'

#Retrieving queue attributes using the SQS client
#sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['All'])

# Defining a function to retrieve message from the queue
def get_messages():
    # Receiving messages from the queue with a maximum count of 5
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=5)
    return response

# Rollback the transaction in case of an error
conn.rollback()

# SQL statement to alter the column "app_version" type in the "user_logins" table
sql = "ALTER TABLE user_logins ALTER COLUMN app_version TYPE varchar"

# Execute the SQL statement
cursor.execute(sql)

# Commit the changes to the database
conn.commit()

# Define a function that replaces all but the last four characters of a string with asterisks
def replace_with_asterisks(field):
    """
    Replaces all but the last four characters of a given string with asterisks.
    
    Args:
        field (str): The input string to be processed.
    
    Returns:
        str: The processed string with asterisks.
    """
    return len(field[:-4]) * '*' + field[-4:]

# Function to insert data into the database
def insert_data(data):
    sql = "INSERT INTO user_logins(user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date) VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)"
    conn.rollback()
    cursor.executemany(sql, data)
    conn.commit()
    print(f"inserted {len(data)} records in the database")

# Initialize variables for tracking total messages and total insertions
total_messages, total_insert = 0, 0

# Define the batch size for processing messages
batch_size = 20

# Continuously process messages in batches
while 1:
    messages = []
    
    done = False
    while len(messages) < batch_size:
        # Get messages from a source (not shown here)
        response = get_messages()
        
        # Check if there are no messages in the response
        if 'Messages' not in response:
            done = True
            print(f"No messages in response {response}")
            break
            #continue
            
        # Check if the response is empty
        if len(response['Messages']) == 0:
            done = True
            break
        
        messages += response['Messages']
    
    if done: break
    
    data = []
    total_messages += len(messages)
    for item in messages:
        message = item['Body']
    
        message_dict = json.loads(message)
        
        #sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=item['ReceiptHandle'])

        # Masking device_id field
        if 'device_id' in message_dict:
            message_dict['device_id'] = replace_with_asterisks(message_dict['device_id'])

        # Masking ip field
        if 'ip' in message_dict:
            message_dict['ip'] = replace_with_asterisks(message_dict['ip'])
        print(message_dict)
        try:
            user_id = message_dict['user_id']
            device_type = message_dict['device_type']
            masked_ip = message_dict['ip']
            masked_device_id = message_dict['device_id']
            locale = message_dict['locale'] # if message_dict['locale'] else "EN"
            app_version = message_dict['app_version']
        except KeyError as ke:
            print(f"received KeyError {ke}")
            continue
            
        row = (user_id, device_type, masked_ip, masked_device_id, locale, app_version)
        print(user_id)
        data.append(row)

    # Insert data into the database
    insert_data(data)
    total_insert += len(data)

# Print the total insertions and total messages processed
print(f"totals {total_insert} {total_messages}")


conn.close()
