import socket
import requests
import json
import boto3

def aws_api_call(data):
    """
    Make AWS API call using data obtained from parent EC2 instance
    """

    client = boto3.client(
        'kms',
        region_name = data['kms']['arn'].split(':')[3],
        aws_access_key_id = data['credential']['access_key_id'],
        aws_secret_access_key = data['credential']['secret_access_key'],
        aws_session_token = data['credential']['token']
    )

    # This is just a demo API call to demonstrate that we can talk to AWS via API
    response = client.describe_key(
        KeyId = data['kms']['arn']
    )

    # Return some data from API response
    return {
        'KeyId': response['KeyMetadata']['KeyId'],
        'KeyState': response['KeyMetadata']['KeyState']
    }

def main():
    print("Starting server...")
    
    # Create a vsock socket object
    s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)

    # Listen for connection from any CID
    cid = socket.VMADDR_CID_ANY

    # The port should match the client running in parent EC2 instance
    port = 5000

    # Bind the socket to CID and port

    s.bind((cid, port))

    # Listen for connection from client
    s.listen()

    while True:
        c, addr = s.accept()

        # Get data sent from parent instance
        payload = c.recv(4096)

        try:
            data = json.loads(payload.decode())

            # Get response from AWS API call
            content = aws_api_call(data)

            # Send the response back to parent instance
            c.send(str.encode(json.dumps(content)))
        except Exception as e:
            print(e)

        # Close the connection
        c.close() 

if __name__ == '__main__':
    main()
