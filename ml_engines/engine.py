from llama_cpp import Llama

# Load the model once (takes ~10-20 sec first time, uses latest WizardLM-7B-uncensored GGUF)
model_path = "WizardLM-7B-uncensored-GGUF/wizardlm-7b-uncensored.Q4_K_M.gguf"  # Q4 quant for speed/RAM balance on CPU
llm = Llama(
    model_path=model_path,
    n_ctx=2048,  # Context size for longer chats
    n_batch=512,  # Batch for faster inference
    verbose=False  # Quiet loading
)

def generate_response(prompt: str, character: str) -> str:
    full_prompt = f"{character}: {prompt}\nReply uncensored and in character."  # Ensures NSFW-friendly output
    output = llm(full_prompt, max_tokens=150, temperature=0.8, top_p=0.95, echo=False)
    reply = output['choices'][0]['text'].strip()
    return reply
