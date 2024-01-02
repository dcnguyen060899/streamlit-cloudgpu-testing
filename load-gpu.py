# import streamlit as st
# import paramiko

# def connect_to_runpod(ssh_private_key_path, hostname, port, username, passphrase=None):
#     ssh_client = paramiko.SSHClient()
#     ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#     try:
#         private_key = paramiko.Ed25519Key.from_private_key_file(ssh_private_key_path, password=passphrase)
#         ssh_client.connect(hostname=hostname, port=port, username=username, pkey=private_key)
#         st.write('Connection successful!')
#         return ssh_client
#     except Exception as e:
#         st.error(f"An error occurred: {e}")
#         # Log the full traceback for debugging purposes
#         paramiko.util.log_to_file('paramiko.log')
#         return None

# def execute_command_on_runpod(ssh_client, command):
#     if ssh_client is None:
#         st.error('SSH Client is not connected.')
#         return None
#     else:
#         stdin, stdout, stderr = ssh_client.exec_command(command)
#         return stdout.read().decode('utf-8')

# if st.button('Connect to RunPod.io'):
#     ssh_client = connect_to_runpod(
#         ssh_private_key_path='/root/.ssh/id_ed25519',  # Adjust if necessary
#         hostname='94.155.194.99',  # The IP address of the RunPod.io instance
#         port=10573,  # The external port number provided by RunPod.io
#         username='dcnguyen060899',  # Replace with the correct username
#     )
#     if ssh_client:
#         output = execute_command_on_runpod(ssh_client, 'nvidia-smi')
#         if output:
#             st.text_area('GPU Status:', output, height=300)
#         ssh_client.close()

import streamlit as st
import getpass

# Get the username of the user running the Streamlit app
streamlituser = getpass.getuser()

# Write the username to the Streamlit app
st.write(f"The Streamlit app is running as: {streamlituser}")


