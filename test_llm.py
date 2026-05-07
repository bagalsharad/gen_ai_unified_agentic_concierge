import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI

try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    print("Flash:", llm.invoke("Say hi").content)
except Exception as e:
    print("Flash failed:", e)

try:
    llm2 = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
    print("Gemini-pro:", llm2.invoke("Say hi").content)
except Exception as e:
    print("Gemini-pro failed:", e)

