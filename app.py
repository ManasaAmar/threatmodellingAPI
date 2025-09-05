from groq import Groq
import os
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()
app = Flask(__name__)

def stride_stream(API_KEY):
    client = Groq(api_key=API_KEY)
    IMAGE_DATA_URL = "https://d2908q01vomqb2.cloudfront.net/77de68daecd823babbb58edb1c8e14d7106e83bb/2021/11/15/AWS-Modernization-MongoDB-3s.png"
    
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
            {
                "role": "system",
                "content": "You are a Senior Threat Modeling Agent. Your primary task is to perform STRIDE analysis on the input architecture.\nThe input will be provided as an image of a system architecture.\n\nYour output must include:\n\n1. A STRIDE Matrix for each component in the image.\nFormat:\nComponent Name               S      T      R      I      D      E\nExample Component            MLLLL  LLLLL  MLLLL  HLLLL  MLLLL  MLLLL\n\nUse the following legend:\nLLLLL = Low\nMLLLL = Medium\nHLLLL = High\nNA = Not Applicable\nThe order of tokens is: [S, T, R, I, D, E] → Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege.\n\n2. For each component, explain the threat and mitigation for each STRIDE category that is not NA or LLLLL.\nFormat:\nComponent: <Component Name>\nSpoofing (MLLLL):\nThreat: <short description>\nMitigation: <short description>\nTampering (LLLLL):\nThreat: None\nMitigation: None\n...\n\nBe concise but complete. If a threat is not applicable, clearly state \"None\" for both threat and mitigation.\n\n---\n\n### Example Output:\n\n#### STRIDE Matrix\nComponent Name               S      T      R      I      D      E\nCustomer Gateway             MLLLL  LLLLL  LLLLL  HLLLL  MLLLL  LLLLL\n\n#### Threats and Mitigations\nComponent: Customer Gateway\nSpoofing (MLLLL):\nThreat: An attacker could impersonate the Customer Gateway.\nMitigation: Use IPsec with mutual authentication and BGP MD5.\nTampering (LLLLL):\nThreat: No\nMitigation: None\nRepudiation (LLLLL):\nThreat: No\nMitigation: None\nInformation Disclosure (HLLLL):\nThreat: Sensitive data could be exposed during transmission.\nMitigation: Encrypt data in transit using TLS 1.2+.\nDenial of Service (MLLLL):\nThreat: Gateway could be overwhelmed with traffic.\nMitigation: Implement rate limiting and DDoS protection.\nElevation of Privilege (LLLLL):\nThreat: No\nMitigation: None\n\n\nIf the image is unreadable or ambiguous, respond with 'Image unclear – please re-upload or clarify."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": ""},
                    {"type": "image_url", "image_url": {"url": IMAGE_DATA_URL}}
                ]
            }
        ],
        temperature=0,
        max_completion_tokens=5000,
        top_p=1,
        stream=True,
        stop=None
    )

    result_text = ""
    for chunk in completion:
        delta = chunk.choices[0].delta.content or ""
        print(delta, end="")
        result_text += delta
    
    return result_text

@app.get("/callAgent")
def call_agent():
    API_KEY = os.getenv("GROQ_API_KEY")
    strideAnalysis = stride_stream(API_KEY)
    return jsonify({"response": strideAnalysis})

if __name__ == "__main__":
    app.run(debug=True)