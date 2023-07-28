import sys
import socket
import requests
import json

def get_aws_session_token():
    """
    Get the AWS credential from EC2 instance metadata
    """
    r = requests.get("http://169.254.169.254/latest/meta-data/iam/security-credentials/")
    instance_profile_name = r.text

    r = requests.get("http://169.254.169.254/latest/meta-data/iam/security-credentials/%s" % instance_profile_name)
    response = r.json()

    credential = {
        'access_key_id' : response['AccessKeyId'],
        'secret_access_key' : response['SecretAccessKey'],
        'token' : response['Token']
    }

    return credential

def get_data(kms_arn):
    """
    Get the data
    """
    credential = get_aws_session_token()

    data = {
        'credential': credential,
        'kms': {
            "arn": kms_arn
        }
    }

    return data

def main():
    # Create a vsock socket object
    s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
    
    # Get CID from command line parameter
    cid = int(sys.argv[1])

    # Get KMS ARN from command line parameter
    kms_arn = sys.argv[2]

    data = get_data(kms_arn)

    # The port should match the server running in enclave
    port = 5000

    # Connect to the server
    s.connect((cid, port))

    # Send AWS credential to the server running in enclave
    s.send(str.encode(json.dumps(data)))
    
    # receive data from the server
    print(s.recv(1024).decode())

    # close the connection 
    s.close()

if __name__ == '__main__':
    main()
