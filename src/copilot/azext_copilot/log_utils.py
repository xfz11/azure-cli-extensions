from knack.log import get_logger
from ._constants import COLUMN_WIDTH

logger = get_logger(__name__)

def log_sub_prompts(sub_prompts):
    logger.warning(f"{len(sub_prompts)} actions will be done accordingly.")
    print('\n')

    logger.warning("No.".ljust(10) + "Action".ljust(COLUMN_WIDTH) + "Resource Type".ljust(COLUMN_WIDTH) + "Prompt".ljust(COLUMN_WIDTH * 2))
    logger.warning("-" * (COLUMN_WIDTH * 4 + 10))

    for i, sub_prompt in enumerate(list(sub_prompts)):
        action = sub_prompt['action']
        if "resource_type" in sub_prompt:
           resource_type = sub_prompt["resource_type"]
        elif "source_resource_type" in sub_prompt and "target_resource_type" in sub_prompt:
           resource_type = f"{sub_prompt['source_resource_type']} + {sub_prompt['target_resource_type']}"
        prompt = sub_prompt['sub_prompt']
        logger.warning(f"{(i+1):<{10}}{action:<{COLUMN_WIDTH}}{resource_type:<{COLUMN_WIDTH}}{prompt:<{COLUMN_WIDTH * 2}}")
    logger.warning("-" * (COLUMN_WIDTH * 4))
    print('\n')