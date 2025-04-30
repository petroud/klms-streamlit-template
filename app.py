import streamlit as st
import os
from utils.mclient import MinioClient
from utils.profile_functions import read_json_profile, profiler_visualization

layout = "wide"
page_title = "Profile - Visualizer"
st.set_page_config(page_title=page_title, layout=layout)

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

if 'content' not in st.session_state:
    st.session_state.content = None
else:
    st.session_state.content = st.session_state.content

# Check if all required credentials are provided
if not (st.session_state.get("access_key") and st.session_state.get("secret_key") and st.session_state.get("s3_endpoint") and st.session_state.get("s3_path")):
    st.write("Credentials not provided")
else:
    # Download the file from S3
    original_filename = os.path.basename(st.session_state.s3_path)
    local_path = os.path.join(os.getcwd(), original_filename)

    mc = MinioClient(
        endpoint=st.session_state.s3_endpoint,
        access_key=st.session_state.access_key,
        secret_key=st.session_state.secret_key,
        session_token=st.session_state.session_token,
        secure=True
    )

    if st.session_state.content is None:
       print('Fetching file from MinIO...')
       st.session_state.content = mc.get_object(s3_path=st.session_state.s3_path, local_path=local_path)

    profiler_visualization(st.session_state.content)