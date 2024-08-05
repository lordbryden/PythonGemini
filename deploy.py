import google.auth
import google.generativeai as genai

# Authenticate using the service account file
credentials, _ = google.auth.load_credentials_from_file('client_secret.json')

# Configure the library with the credentials
genai.configure(credentials=credentials)

# List available models
print("Available models:")
for model in genai.list_models():
    print(model.name)

# Access the text-bison-001 model
model_name = 'models/text-bison-001'

# Use the model to generate content
input_text = "what is 3 plus 2"  # Example input
try:
    response = genai.generate_text(
        model=model_name,
        prompt=input_text
    )
    # Accessing the generated text correctly
    result_text = response.candidates[0].output
    print(f"Input: {input_text}")
    print(f"Model output: {result_text}")
except Exception as e:
    print(f"An error occurred: {e}")
