# general
import requests, os
# fastapi
from fastapi import APIRouter 
# ibm-generative-ai package
from genai.credentials import Credentials 
from genai.extensions.langchain import LangChainInterface
from genai.schemas import GenerateParams
# watson
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

""" 
	User Define
"""
from config import getConfig
# models
from schemas import Message, PromptMessage, BOOKS, Book


api_key = os.getenv("GENAI_KEY", None) 
api_url = os.getenv("GENAI_URL", None)

creds = Credentials(api_key, api_endpoint=api_url)
api = APIRouter(prefix='/api/v1')

@api.post('/message', tags = ["watsonx"], 
          description="prompt message",     
          responses={
            404: {"model": Message, "description": "The item was not found"},
            200: {
                "description": "Item requested by ID",
                "content": {
                    "application/json": {
                        "example": {"id": "bar", "value": "The bar tenders"}
                    }
            },
        },
    })
async def callWatson(body: PromptMessage):
        print(body)
        print("\n------------- Example (LangChain)-------------\n")
    
        #translate(body)
        params = GenerateParams(decoding_method="greedy", max_new_tokens=700)
        
        langchain_model = LangChainInterface(model="google/flan-ul2", params=params, credentials=creds)
        result = langchain_model('{}'.format(body.message))
        print("------------result:", result)
        transMessage = langTranslate(result, 'en', 'ko')
        voiceText = transMessage.get('translations')
        msg = voiceText[0] 
        print(msg.get('translation'))

        return msg
        # return result

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

    return translation 