import os
import time
from dotenv import load_dotenv 
from selenium_scraper import Connection
from selenium.webdriver.common.by import By
from llama_cpp import Llama

MODEL_PATH_ENV_VAR = "PATH_TO_GGUF_FILE"

PINPOINT_URL = "https://www.linkedin.com/games/view/pinpoint/desktop/"
PINPOINT_GRID_CLASS = "pinpoint__board"
PINPOINT_INPUT_CLASS = "pinpoint__input"

GAME_CONTINUING_CLASS = "pinpoint__card__answer--empty"

def continue_to_guess(connection):
    try:
        connection.driver.find_element(By.CLASS_NAME, GAME_CONTINUING_CLASS)
        return True
    except Exception:
        return False

def gather_clue(connection):
    clues = []
    for i, div in connection.get_game_elements():
        spans = div.find_elements(By.TAG_NAME, 'span')
        if spans:
            clues.append(spans[0].text.strip())
    return clues

def solve_pinpoint():
    load_dotenv()
    model_path = os.getenv(MODEL_PATH_ENV_VAR)
    if not model_path:
        raise ValueError(f"Environment variable '{MODEL_PATH_ENV_VAR}' is not set.")
    
    connection = Connection(PINPOINT_URL, PINPOINT_GRID_CLASS).open()
    llm = Llama(model_path=os.getenv("PATH_TO_GGUF_FILE"), verbose=False, n_ctx=8192)

    guess = None
    while continue_to_guess(connection):
        clues = gather_clue(connection)
        prompt = f"Clues: '{"', '".join(clues)}'.\nCategory: '"
        output = llm.create_completion(prompt, max_tokens=5, temperature=0.1)
        guess = output['choices'][0]['text'].strip().split("'")[0]

        input_field = connection.driver.find_element(By.CLASS_NAME, PINPOINT_INPUT_CLASS)
        input_field.send_keys(guess)
        input_field.submit()
        time.sleep(1)

    connection.close()
    llm.close()

    print(f"Category: {guess}")