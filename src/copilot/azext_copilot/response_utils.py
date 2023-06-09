from ._constants import DELIMITER, SYSTEM_PROMPT
from .log_utils import log_sub_prompts
from .template_utils import get_template
import openai
import json
from time import time
from .resource_utils import create_resource
from knack.prompting import prompt, prompt_y_n
from knack.log import get_logger
from knack.util import CLIError

logger = get_logger(__name__)

def get_completion_from_messages(messages, 
                                 model="gpt-35-turbo", 
                                 temperature=0, max_tokens=4000):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
        engine="gpt-35-turbo",
        
    )
    return response.choices[0].message["content"]

def get_sub_prompts(user_prompt):
    messages =  [  
        {
            'role':'system', 
            'content': SYSTEM_PROMPT
        },    
        {
            'role':'user', 
            'content': f"{DELIMITER}{user_prompt}{DELIMITER}"
        },  
    ] 
    sub_prompts = get_completion_from_messages(messages)
    sub_prompts = json.loads(sub_prompts)
    return sub_prompts

def fill_in_templates(sub_prompt, subscription_id):
    action = sub_prompt['action']
    if action == "create resource":
      return get_template[action][sub_prompt['resource_type']](subscription_id)
    elif action == "connect resources":
      return get_template[action](sub_prompt['source_resource_type'], sub_prompt['target_resource_type'], subscription_id)
    else:
       print("waiting for future release")
       return None

def get_payload(assistant_template, user_prompt):
    messages =  [  
        {
            'role':'system', 
            'content': assistant_template
        },    
        {
            'role':'user', 
            'content': f"{DELIMITER}{user_prompt}{DELIMITER}"
        },  
    ] 
    payload = get_completion_from_messages(messages)
    return payload

def process_prompt(prompt, subscription_id):
    logger.warning("Analyzing your prompt...")
    sub_prompts = get_sub_prompts(prompt)
    
    logger.warning(f"Finish analyzing your prompt.")
    log_sub_prompts(sub_prompts)

    payloads = []
    
    # generate payload for each sub_prompt and call rest apis
    for i, sub_prompt in enumerate(sub_prompts):
        logger.warning(f"Waking your copilot for Action {i + 1}...")
        assistant_template = fill_in_templates(sub_prompt, subscription_id)
        
        logger.warning("Start generating payload...")
        payload = get_payload(assistant_template, sub_prompt['sub_prompt'])
        logger.warning("Sucess. Operations will be done according to the payload below:")
        print(payload)

        if prompt_y_n("Do you want to continue?", default="n"):
            create_resource(payload)
            payloads.append(payload)
            logger.warning(f"Job {i + 1} done.")
            print('\n')
        else:
            raise CLIError('Stopping execution upon user input.')
    
    logger.warning("All jobs done. AZ Copilot is happy working with you.")
    return payloads
