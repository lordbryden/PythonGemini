import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models


def multiturn_generate_content():
  vertexai.init(project="721266053844", location="us-central1")
  model = GenerativeModel(
    "projects/721266053844/locations/us-central1/endpoints/4466548284537700352",
  )
  chat = model.start_chat()
  print(chat.send_message(
      ["""TRANSCRIPT: \\nMANNER OF DEATH: , Homicide.,CAUSE OF DEATH:,\\n\\n LABEL:"""],
      generation_config=generation_config,
      safety_settings=safety_settings
  ))


generation_config = {
    "max_output_tokens": 1024,
    "temperature": 1,
    "top_p": 1,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

multiturn_generate_content()

