import streamlit as st
import paramiko
import os

def connect_to_runpod(ssh_private_key_path, hostname, port, username, passphrase=None):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        private_key = paramiko.Ed25519Key.from_private_key_file(ssh_private_key_path, password=passphrase)
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

# import streamlit as st
# import paramiko
# import os
# import base64
# from io import StringIO

# def connect_to_runpod(ssh_key_content, hostname, port, username, passphrase=None):
#     ssh_client = paramiko.SSHClient()
#     ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#     try:
#         # Decode the base64 encoded key content
#         private_key_file = StringIO(base64.b64decode(ssh_key_content).decode('utf-8'))
#         private_key = paramiko.Ed25519Key.from_private_key(private_key_file, password=passphrase)
        
#         ssh_client.connect(hostname=hostname, port=port, username=username, pkey=private_key)
#         st.write('Connection successful!')
#         return ssh_client
#     except Exception as e:
#         st.error(f"An error occurred: {e}")
#         paramiko.util.log_to_file('paramiko.log')
#         return None

# # Use environment variables or Streamlit secrets to store sensitive information
# ssh_key_content = os.environ.get('/root/.ssh/id_ed25519')
# hostname = os.environ.get('94.155.194.99')
# port = int(os.environ.get('10593', '22'))
# username = os.environ.get('root')

# if st.button('Connect to RunPod.io'):
#     if ssh_key_content and hostname and username:
#         ssh_client = connect_to_runpod(
#             ssh_key_content=ssh_key_content,
#             hostname=hostname,
#             port=port,
#             username=username,
#         )
#         # ... rest of your code to interact with RunPod instance
#         if ssh_client:
#             # Example command to check GPU status
#             output, error = execute_command_on_runpod(ssh_client, 'nvidia-smi')
#             if output:
#                 st.text_area('GPU Status:', output, height=300)
#             if error:
#                 st.error('Error: ' + error)
#             ssh_client.close()
