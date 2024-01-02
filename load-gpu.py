import paramiko
import streamlit as st

# Function to create an SSH client and connect to RunPod.io
def connect_to_runpod(ssh_private_key_path, passphrase=None):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # If the key is encrypted with a passphrase, provide it here
        private_key = paramiko.Ed25519Key.from_private_key_file(ssh_private_key_path, password=passphrase)
        ssh_client.connect(hostname='94.155.194.99', username='dcnguyen060899', pkey=private_key)
        # Proceed with your operations...
        st.write('it works')
    except Exception as e:
        st.write(f"An error occurred: {e}")
        # Handle exceptions or errors

    return ssh_client

# Function to execute a command on RunPod.io and return the output
def execute_command_on_runpod(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    return stdout.read().decode('utf-8')

# Streamlit interface to trigger the SSH command
if st.button('Connect to RunPod.io'):
    ssh_client = connect_to_runpod(
        ssh_private_key_path='/root/.ssh/id_ed25519',  # Securely provide your SSH private key path here
        public_ip='94.155.194.99',
        external_port=10573
    )
    # Example command to run on RunPod.io
    output = execute_command_on_runpod(ssh_client, 'nvidia-smi')  # Command to check GPU status
    ssh_client.close()  # Don't forget to close the client after you're done
    st.text_area('GPU Status:', output, height=300)

paramiko.util.log_to_file('paramiko.log')

import paramiko

