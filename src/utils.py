import os
import sys
import requests
from dotenv import find_dotenv, load_dotenv
from transformers import pipeline
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from config import API_URL, MODEL

sys.path.append(".")
load_dotenv(dotenv_path="./.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HFACE_API_KEY = os.getenv("HFACE_API_KEY")

def get_caption(img_loc):
    """Creates a caption for the input image"""
    pl = pipeline("image-to-text", model=MODEL)
    caption = pl(img_loc)[0]["generated_text"]
    return caption


def generate_titles(img_descr):
    """Creates five title ideas based on the following image descriptions:"""
    template = """
    You are a creative title generator;
    You can suggest creative title ideas based on a set of phrases. Each title should capture as many concepts from all phrases as possible and it should be playful. Each title should have four words of less and it should contain no more than two relavant emojis.
    PHRASES: {img_descr}
    FIVE TITLE IDEAS:
    """
    prompt = PromptTemplate(template=template, input_variables=["img_descr"])

    llm_story = LLMChain(
        llm=ChatOpenAI(model_name="gpt-4-0613", temperature=1),
        prompt=prompt,
    )
    story = llm_story.predict(img_descr=img_descr)
    return story
