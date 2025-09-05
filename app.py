from groq import Groq
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
app = Flask(__name__)

def stride_stream(sysName,sysDescp,AdditonalContext,imageUrl):
    client = Groq(api_key=GROQ_API_KEY)
    #IMAGE_DATA_URL = "https://d2908q01vomqb2.cloudfront.net/77de68daecd823babbb58edb1c8e14d7106e83bb/2021/11/15/AWS-Modernization-MongoDB-3s.png"
    IMAGE_DATA_URL= imageUrl
    with open("systemPrompt.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read().strip()
    
    user_prompt = sysName + ','+ sysDescp +','+  AdditonalContext
    

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": IMAGE_DATA_URL}}
                ]
            }
        ],
        temperature=0,
        max_completion_tokens=7000,
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

@app.post("/callAgent")
def call_agent():
    sysName = request.args.get("sysName", "")
    sysDescp = request.args.get("sysDescp", "")
    AdditonalContext = request.args.get("AdditonalContext", "")
    imageUrl = request.args.get("imageUrl", "")
    strideAnalysis = stride_stream(sysName, sysDescp, AdditonalContext, imageUrl)

    return strideAnalysis

@app.get("/")
def check_call():
    return "Threat Modelling API"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)