
import streamlit as st
import hashlib
import json
import datetime
import pandas as pda
import os
import base64
from typing import Optional

# File to store the blockchain
BLOCKCHAIN_FILE = "blockchain_data.json"

# Supported file types
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}

# Initialize session state
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = []

# --- File Handling Functions ---
def is_allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(uploaded_file) -> Optional[str]:
    """Save uploaded file and return base64 encoded content"""
    if uploaded_file is not None and is_allowed_file(uploaded_file.name):
        file_content = uploaded_file.getvalue()
        return base64.b64encode(file_content).decode('utf-8')
    return None

def display_document(file_data: str, file_name: str):
    """Display document based on its type"""
    if not file_data:
        return

    decoded = base64.b64decode(file_data)
    file_ext = file_name.split('.')[-1].lower()

    if file_ext == 'pdf':
        # Display PDF
        base64_pdf = base64.b64encode(decoded).decode('utf-8')
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
        st.markdown(pdf_display, unsafe_allow_html=True)
    elif file_ext in {'png', 'jpg', 'jpeg'}:
        # Display image
        st.image(decoded, caption=file_name, use_column_width=True)
    else:
        # Download button for unsupported display types
        st.download_button(
            label="Download Document",
            data=decoded,
            file_name=file_name,
            mime="application/octet-stream"
        )

# --- Blockchain Functions ---
def load_blockchain():
    if os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, 'r') as f:
            return json.load(f)
    return []

def save_blockchain(blockchain):
    with open(BLOCKCHAIN_FILE, 'w') as f:
        json.dump(blockchain, f)

def calculate_hash(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def create_block(data, previous_hash=''):
    block = {
        'index': len(st.session_state.blockchain) + 1,
        'timestamp': str(datetime.datetime.now()),
        'data': data,
        'previous_hash': previous_hash,
        'hash': ''
    }
    block['hash'] = calculate_hash(block)
    return block

def add_block(data):
    previous_hash = st.session_state.blockchain[-1]['hash'] if st.session_state.blockchain else ''
    new_block = create_block(data, previous_hash)
    st.session_state.blockchain.append(new_block)
    save_blockchain(st.session_state.blockchain)
    return new_block['index']

# Initialize blockchain
st.session_state.blockchain = load_blockchain()

# --- Streamlit UI ---
st.title("📄🔗 Document Verification Blockchain")

menu = st.sidebar.selectbox("Menu", ["Register Document", "Verify Document", "View Blockchain"])

if menu == "Register Document":
    st.header("Register New Document")

    with st.form("registration_form"):
        name = st.text_input("Owner's Full Name*")
        document_type = st.selectbox("Document Type*",
                                   ["Educational Certificate",
                                    "Professional License",
                                    "Property Document",
                                    "Government ID",
                                    "Legal Contract",
                                    "Other"])

        # Document-specific fields
        doc_details = {}
        if document_type == "Educational Certificate":
            doc_details['institution'] = st.text_input("Institution Name*")
            doc_details['degree'] = st.text_input("Degree/Certificate Name*")
            doc_details['year'] = st.text_input("Year of Issue*")
        elif document_type == "Professional License":
            doc_details['license_name'] = st.text_input("License Name*")
            doc_details['issuing_authority'] = st.text_input("Issuing Authority*")
            doc_details['expiry_date'] = st.text_input("Expiry Date")
        elif document_type == "Property Document":
            doc_details['property_address'] = st.text_input("Property Address*")
            doc_details['document_purpose'] = st.selectbox("Document Purpose",
                                                         ["Ownership Proof",
                                                          "Sale Agreement",
                                                          "Lease Agreement",
                                                          "Other"])

        # File upload with type restrictions
        uploaded_file = st.file_uploader(
            "Upload Document* (PDF, PNG, JPG, DOC/DOCX)",
            type=list(ALLOWED_EXTENSIONS),
            accept_multiple_files=False
        )

        additional_notes = st.text_area("Additional Notes")

        submitted = st.form_submit_button("Register Document")

        if submitted:
            if not name:
                st.error("Please enter owner's name")
            elif uploaded_file is None:
                st.error("Please upload a document")
            else:
                # Prepare document data
                document_data = {
                    "record_type": document_type,
                    "owner_name": name,
                    "file_name": uploaded_file.name,
                    "file_content": save_uploaded_file(uploaded_file),
                    "file_type": uploaded_file.name.split('.')[-1].lower(),
                    "registration_date": str(datetime.date.today()),
                    "additional_notes": additional_notes,
                    **doc_details
                }

                block_index = add_block(document_data)
                st.success(f"Document successfully registered! Your unique ID is: {block_index}")
                st.info("Please save this ID securely for future verification.")

elif menu == "Verify Document":
    st.header("Verify Document")

    unique_id = st.text_input("Enter Unique Document ID")

    if unique_id:
        try:
            block_index = int(unique_id) - 1
            if 0 <= block_index < len(st.session_state.blockchain):
                block = st.session_state.blockchain[block_index]
                data = block['data']

                st.subheader(f"Document Verification - ID: {unique_id}")
                st.write(f"**Document Type:** {data['record_type']}")
                st.write(f"**Owner Name:** {data['owner_name']}")
                st.write(f"**Registered On:** {block['timestamp']}")

                # Display document-specific details
                if data['record_type'] == "Educational Certificate":
                    st.write(f"**Institution:** {data.get('institution', 'N/A')}")
                    st.write(f"**Degree/Certificate:** {data.get('degree', 'N/A')}")
                    st.write(f"**Year of Issue:** {data.get('year', 'N/A')}")
                elif data['record_type'] == "Professional License":
                    st.write(f"**License Name:** {data.get('license_name', 'N/A')}")
                    st.write(f"**Issuing Authority:** {data.get('issuing_authority', 'N/A')}")
                    st.write(f"**Expiry Date:** {data.get('expiry_date', 'N/A')}")

                # Document display section
                st.subheader("Document Preview")
                if data.get('file_content'):
                    display_document(data['file_content'], data['file_name'])
                else:
                    st.warning("No document attached to this record")

                # Blockchain verification
                st.subheader("Blockchain Verification")
                st.write(f"**Block Hash:** {block['hash']}")
                calculated_hash = calculate_hash(block)

                if calculated_hash == block['hash']:
                    st.success("✅ Document verified - This record has not been tampered with")
                    st.write(f"**Previous Block Hash:** {block.get('previous_hash', 'Genesis Block')}")
                else:
                    st.error("❌ Verification failed - This document may have been altered")
            else:
                st.error("Invalid ID. Please check and try again.")
        except ValueError:
            st.error("Please enter a valid numeric ID")

elif menu == "View Blockchain":
    st.header("Blockchain Explorer")

    if st.session_state.blockchain:
        st.write(f"Total blocks in chain: {len(st.session_state.blockchain)}")

        view_option = st.radio("View Options", ["All Records", "Search by Document Type", "View Specific Block"])

        if view_option == "All Records":
            simplified_blocks = []
            for block in st.session_state.blockchain:
                simplified_blocks.append({
                    "ID": block['index'],
                    "Type": block['data']['record_type'],
                    "Owner": block['data']['owner_name'],
                    "Date": block['timestamp'],
                    "File": block['data']['file_name']
                })
            st.dataframe(pd.DataFrame(simplified_blocks))

        elif view_option == "Search by Document Type":
            doc_type = st.selectbox("Select Document Type",
                                   ["Educational Certificate",
                                    "Professional License",
                                    "Property Document",
                                    "Government ID",
                                    "Legal Contract",
                                    "Other"])

            filtered_blocks = [block for block in st.session_state.blockchain
                             if block['data']['record_type'] == doc_type]

            if filtered_blocks:
                st.write(f"Found {len(filtered_blocks)} {doc_type} records")
                for block in filtered_blocks:
                    with st.expander(f"ID: {block['index']} - {block['data']['owner_name']}"):
                        st.json(block['data'])
            else:
                st.info(f"No {doc_type} records found")

        elif view_option == "View Specific Block":
            block_num = st.number_input("Enter block number",
                                      min_value=1,
                                      max_value=len(st.session_state.blockchain))
            block = st.session_state.blockchain[block_num - 1]
            st.json(block)
    else:
        st.info("The blockchain is currently empty. No documents have been registered yet.")
