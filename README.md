# AI-Playbook-Generator
 This project focuses on leveraging an interactive AI model to generate Ansible playbooks for automating, deploying, and provisioning network infrastructures.


## Pre-requisites
1. Make sure you request for a Bridge IT key from [here](https://forms.office.com/pages/responsepage.aspx?id=Yq_hWgWVl0CmmsFVPveEDgC5krjn8p1FqwLnE5quaEZUNlNXTlZBS0xZQkFSMzYxN1ZMWlZYSjc1Vy4u)

2. Create an .env file with the following info you get from BridgeIT
```
CLIENT_ID=<CLIENT_ID>
CLIENT_SECRET=<CLIENT_SECRET>
CISCO_OPENAI_APP_KEY=<APP_KEY>
DEPLOYMENT_NAME=gpt-4o-mini
AZURE_ENDPOINT=https://chat-ai.cisco.com
API_VERSION=2024-07-01-preview
NUM_TOKENS=90000
TOKEN_URL=https://id.cisco.com/oauth2/default/v1/token
```

3. Make sure you have Python v3.10+ installed

## Installing dependencies
1. Create a new virtual environment
```
python3 -m venv .venv
```

2. Activate the environment
```
source .venv/bin/activate
```

3. Install all the dependencies: (from the BridgeIT directory)
```
pip install -r requirements.txt
```



# Chat UI

**main.py** A sample python script that shows how to create a chat assitant with UI using streamlit and BridgeIT in the backend.

To learn more about streamlit, check out this [link](https://streamlit.io/)

Other UI framework:
1. [Chainlit](https://docs.chainlit.io/get-started/overview)
2. [Gradio.app](https://www.gradio.app/)

