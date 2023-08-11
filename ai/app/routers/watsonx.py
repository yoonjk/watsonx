# general
import requests, os, json
# fastapi
from fastapi import APIRouter, File, UploadFile, Form
# ibm-generative-ai package
from genai.credentials import Credentials 
from genai.extensions.langchain import LangChainInterface
from genai.schemas import GenerateParams
from genai.model import Model
from genai.prompt_pattern import PromptPattern
# watson
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

""" 
	User Define
"""

# models
from schemas import Message, PromptMessage
from config import getConfig
from typing import Optional

api_key = os.getenv("GENAI_KEY", None) 
api_url = os.getenv("GENAI_URL", None)

print('api_key:', api_key)
creds = Credentials(api_key, api_endpoint=api_url)
router = APIRouter(prefix='/api/v1', tags = ["watsonx"])

@router.post('/qna', 
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
async def qna(message: str = Form(), uploadfile: Optional[UploadFile] = File(None)):
    if uploadfile:
        try:
            contents = await uploadfile.read()
            print(contents)
        finally:
            uploadfile.file.close()

    print(message)
    print("\n------------- Example (LangChain)-------------\n")

    #translate(body)
    params = GenerateParams(decoding_method="greedy", max_new_tokens=700)
    
    langchain_model = LangChainInterface(model="google/flan-ul2", params=params, credentials=creds)
    result = langchain_model('{}'.format(message))
    print("------------result:", result)
    transMessage = langTranslate(result, 'en', 'ko')
    voiceText = transMessage.get('translations')
    msg = voiceText[0] 
    print(msg.get('translation'))
    return msg
        # return result

@router.post('/summary')
async def summarize(message: str = Form(), upload_file: Optional[UploadFile] = File(None)):
    json_data = json.load(upload_file.file)

    if not message:
        message ='다음 본문은 뉴스 기사입니다. 본분을 새 문장으로 요약해주세요.'
        # ​The following document is a news article from Korea. Read the document and then write 3 sentences summary.           
    params = GenerateParams(
        decoding_method = 'sample',
        max_new_tokens=1024,
        min_new_tokens=100,
        repetition_penalty=2.0,
        top_k=50,
        temperature=0.7
    )
    # Prompt pattern
    prompt_str = """
        {0}
        
        본문:
        {1}
        요약:
    """.format(message, json_data['text'])  
    
    pattern = PromptPattern.from_str(prompt_str)
    model = Model(model="bigscience/mt0-xxl", params=params, credentials=creds)
    responses = model.generate_as_completed([str(pattern)])
    
    result = []
    
    for response in responses:
        print("Generated text:")
        result.append(response.generated_text)
        
    return {'result': '\n'.join(result)}
        

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