from DocQnA.logging import logger
from transformers import AutoTokenizer
from datasets import Dataset
from entity import DataTransformationConfig
from utils import read_yaml

# Load the configuration using the utility function
config = read_yaml('config.yaml')

# Create an instance of DataTransformationConfig
data_transformation_config = DataTransformationConfig(**config['data_transformation'])

class DataTransformation(Dataset):
    def __init__(self, data):
        super().__init__(data)
        self.config = data_transformation_config
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_name)
        logger.info("DataTransformation initialized")
        
    def __len__(self):
        # logger.info("Getting length of the dataset")
        return len(self.data)
    
    def formatting_prompts_func(examples):
        # logger.info("Formatting prompts")
        # Define a function to format each example in the dataset
        alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

        ### Instruction:
        {}

        ### Input:
        {}

        ### Response:
        {}"""

        instructions = examples["instruction"]
        inputs       = examples["input"]
        outputs      = examples["output"]
        # Get instructions, inputs, and outputs

        texts = []
        for instruction, input, output in zip(instructions, inputs, outputs):
            # Generate text by combining instructions, inputs, and outputs

            text = alpaca_prompt.format(instruction, input, output)
            # Format the text according to the prompt format

            texts.append(text)
        logger.info("Prompts formatted")
        return { "text" : texts, }
    # Return a list of formatted texts