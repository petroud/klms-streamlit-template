import streamlit as st
import os
from utils.mclient import MinioClient


st.title("K8s-Launched Streamlit App")

qparams = st.query_params

access_key = qparams.get("access_key")
if access_key:
    st.session_state.access_key = access_key

secret_key = qparams.get("secret_key")
if secret_key:
    st.session_state.secret_key = secret_key

session_token = qparams.get("session_token")
if session_token:
    st.session_state.session_token = session_token

s3_endpoint = qparams.get("s3_endpoint")
if s3_endpoint:
    st.session_state.s3_endpoint = s3_endpoint

s3_path = qparams.get("s3_path")
if s3_path:
    st.session_state.s3_path = s3_path

# Check if all required credentials are provided
if not (st.session_state.get("access_key") and st.session_state.get("secret_key") and st.session_state.get("s3_endpoint") and st.session_state.get("s3_path")):
    st.write("Credentials not provided")
else:
    st.write("Access Key:", st.session_state.access_key)
    st.write("Secret Key:", st.session_state.secret_key)
    st.write("Session Token:", st.session_state.session_token)
    st.write("S3 Endpoint:", st.session_state.s3_endpoint)
    st.write("S3 Path:", st.session_state.s3_path)

    # Download the file from S3
    local_path = os.path.join(os.getcwd(), "profile_data.json")

    mc = MinioClient(
        endpoint=st.session_state.s3_endpoint,
        access_key=st.session_state.access_key,
        secret_key=st.session_state.secret_key,
        session_token=st.session_state.session_token,
        secure=True
    )

    mc.get_object(s3_path=st.session_state.s3_path, local_path=local_path)

    st.write("File downloaded successfully to:", local_path)
    # Display the content of the downloaded file
    with open(local_path, "r") as file:
        content = file.read()
        st.text_area("Content of the downloaded file:", content, height=300)