import paramiko
import streamlit as st

# Adjusted function to include hostname and port parameters
def connect_to_runpod(ssh_private_key_path, hostname, port, username, passphrase=None):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        private_key = paramiko.Ed25519Key.from_private_key_file(ssh_private_key_path, password=passphrase)
        # Use hostname and port in the connect call
        ssh_client.connect(hostname=hostname, port=port, username=username, pkey=private_key)
        st.write('Connection successful!')
    except Exception as e:
        st.error(f"An error occurred: {e}")
        # Log the full traceback for debugging purposes
        paramiko.util.log_to_file('paramiko.log')

    return ssh_client

# Function to execute a command on RunPod.io and return the output
def execute_command_on_runpod(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    return stdout.read().decode('utf-8')

# Call the function with correct parameters
if st.button('Connect to RunPod.io'):
    ssh_client = connect_to_runpod(
        ssh_private_key_path='/root/.ssh/id_ed25519',  # Adjust if necessary
        hostname='94.155.194.99',  # The IP address of the RunPod.io instance
        port=10573,  # The external port number provided by RunPod.io
        username='dcnguyen060899',  # Replace with the correct username
    )
    
    # Example command to run on RunPod.io
    output = execute_command_on_runpod(ssh_client, 'nvidia-smi')  # Command to check GPU status
    ssh_client.close()  # Don't forget to close the client after you're done
    st.text_area('GPU Status:', output, height=300)

paramiko.util.log_to_file('paramiko.log')

import paramiko

