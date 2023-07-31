from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from message import Message, PromptMessage
from config import getConfig

from genai.extensions.langchain import LangChainInterface
from genai.credentials import Credentials
from genai.schemas import GenerateParams

import requests, os, json
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator



tags_metadata = [
    {
        "name": "watsonx",
        "description": "Users Operations with Watsonx.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)

def langTranslate(message: str, source: str, target: str):
    apikey=os.environ['LANG_TRANSLATOR_APIKEY']
    url = os.environ['LANG_TRANSLATOR_URL']
    print(f'url:{url}')
    
    authenticator = IAMAuthenticator(apikey)
    language_translator = LanguageTranslatorV3(
        version='2018-05-01',
        authenticator=authenticator
    )

    language_translator.set_service_url(url)
    
    print(message)
    
    translation = language_translator.translate(
        text=message,
        source=source,
        target=target
        ).get_result()
    

    print(json.dumps(translation, indent=2, ensure_ascii=False))    

    return translation 

@app.post('/translate')
async def translate(body: Message):
    print(body) 
    return langTranslate(body.message, body.source, body.target)
    
@app.post('/message', tags = ["watsonx"])
async def callWatson(body: PromptMessage):
        print(body)
        print("\n------------- Example (LangChain)-------------\n")
        print(getConfig())
        #translate(body)
        api_key=os.environ['GENAI_KEY']
        api_endpoint=os.environ['GENAI_URL']
        credentials = Credentials(api_key, api_endpoint)
        params = GenerateParams(decoding_method="greedy")


        langchain_model = LangChainInterface(model="google/flan-ul2", params=params, credentials=credentials)
        result = langchain_model('Answer this question:{}'.format(body.message))

        transMessage = langTranslate(result, 'en', 'ko')
        
        return transMessage


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Watsonx Challenge Korea Team",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
