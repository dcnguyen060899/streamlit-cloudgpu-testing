import streamlit as st
import paramiko
import os

def connect_to_runpod(ssh_private_key_base64, hostname, port, username, passphrase=None):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Decode the base64-encoded SSH private key
        private_key_decoded = b64decode(ssh_private_key_base64)
        
        # Convert the decoded key into a file-like object
        private_key_fileobj = StringIO(private_key_decoded.decode("utf-8"))
        
        # Load the private key from the file-like object
        private_key = paramiko.Ed25519Key.from_private_key(private_key_fileobj, password=passphrase)
        
        ssh_client.connect(hostname=hostname, port=port, username=username, pkey=private_key)
        st.write('Connection successful!')
        return ssh_client
    except Exception as e:
        st.error(f"An error occurred: {e}")
        # Log the full traceback for debugging purposes
        paramiko.util.log_to_file('paramiko.log')
        return None

def execute_command_on_runpod(ssh_client, command):
    if ssh_client is None:
        st.error('SSH Client is not connected.')
        return None
    else:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        return stdout.read().decode('utf-8')

ssh_key_content = os.environ.get('/root/.ssh/id_ed25519')
hostname = os.environ.get('94.155.194.99')
port = int(os.environ.get('10593', '22'))
username = os.environ.get('root')

if st.button('Connect to RunPod.io'):
    ssh_client = connect_to_runpod(
        ssh_private_key_path=ssh_key_content,  # Adjust if necessary
        hostname=hostname,  # The IP address of the RunPod.io instance
        port=port,  # The external port number provided by RunPod.io
        username='username',  # Replace with the correct username
    )
    if ssh_client:
        output = execute_command_on_runpod(ssh_client, 'nvidia-smi')
        if output:
            st.text_area('GPU Status:', output, height=300)
        ssh_client.close()



