import os
from typing import Any, Callable, List
from modules.custom_types import Segment
import re

class Validators:
    """
    A utility class for validating user inputs.
    """

    @staticmethod
    def prompt(validator:Callable, prompt:str, **kwargs:Any)->Any:
        """
        Prompts the user for input and validates it using the provided
        validator function.

        Args:
            validator (function): The validation function to use.
            prompt (str): The prompt message to display.

        Returns:
            Any: The validated input.
        """
        while True:
            try:
                user_input = input(prompt + '\n input: ').strip().lower()
                if not user_input:
                    raise ValueError('Input cannot be empty.')
                if validator is None:
                    return user_input 
                return validator(user_input, **kwargs)
            
            except ValueError as e:
                print(e)
    
    @staticmethod
    def validate_options(user_input:str, options:List[str])->str:
        """
        Validates that the input is one of the provided options.

        Args:
            user_input (str): The input from the user.
            options (list): A list of valid options.

        Returns:
            str: The validated option.
        """
        if user_input in options:
            return user_input
        raise ValueError('Invalid option.')
        
    
    @staticmethod
    def validate_integer(user_input:str, lower_bound:int=None, upper_bound:int=None)->int:
        """
        Validates that the input is an integer within specified bounds.
        Remark: this truncates floats to integers.

        Args:
            user_input (str): The input from the user.
            lower_bound (int, optional): The minimum value.
            upper_bound (int, optional): The maximum value.

        Returns:
            int: The validated integer.
        
        Raises:
            ValueError: If the input is not an integer or is out of bounds.
        """
        
        try:
            user_input = int(user_input)
        except Exception:
            raise ValueError('Please enter an integer.')
        if lower_bound is not None and user_input < lower_bound:
            raise ValueError(f'Please enter an integer greater than {lower_bound}.')
        
        if upper_bound is not None and user_input > upper_bound:
            raise ValueError(f'Please enter an integer less than {upper_bound}.')
        
        return user_input
        
    @staticmethod
    def validate_float(user_input:str, lower_bound:float=None, upper_bound:float=None)->float:
        """
        Validates that the input is a float within specified bounds.

        Args:
            user_input (str): The input from the user.
            lower_bound (float, optional): The minimum value.
            upper_bound (float, optional): The maximum value.

        Returns:
            float: The validated float.
        
        Raises:
            ValueError: If the input is not a float or is out of bounds.
        """
        
        try:
            user_input = float(user_input)
        except Exception:
            raise ValueError('Please enter a float.')
        if lower_bound is not None and user_input < lower_bound:
            raise ValueError(f'Please enter a float greater than {lower_bound}.')
        
        if upper_bound is not None and user_input > upper_bound:
            raise ValueError(f'Please enter a float less than {upper_bound}.')
        
        return user_input
    
    def validate_path(user_input:str)->str:
        """
        Validates that the input is a valid file path.

        Args:
            user_input (str): The input from the user.

        Returns:
            str: The path.

        Raises:
            ValueError: If the path does not exist.
        """
        if not os.path.exists(user_input):
            raise ValueError(f"Path '{user_input}' does not exist.")
        return user_input

    @staticmethod
    def extract_file_data(path: str) -> List[Segment]:
        """
        Extracts file data for road segments. Validates the file contents to
        ensure proper formatting.

        Args:
            path (str): The path to the file.

        Returns:
            List[Segment]: A list of road segments extracted from the file.

        Raises:
            ValueError: If the file contains invalid data.
            IOError: If the file cannot be read.
        """
        pattern = re.compile(r"^(-?[0-9]+),(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)$")
        append_fn = lambda match: ((int(match.group(1)), int(match.group(2))),
                                    (int(match.group(3)), int(match.group(4))))
        whitespace_pattern = re.compile(r'\s*,\s*')

        items = []
        try:
            with open(path, 'r') as file:
                for line in file:
                    line = whitespace_pattern.sub(',', line.strip())
                    if line and (match := pattern.match(line)):
                        items.append(append_fn(match))
                    elif line:
                        raise ValueError(f"Error: Invalid line: {line} in '{path}'")
            return items
        
        except IOError:
            raise IOError(f"Error: Could not read file: '{path}'")
        

