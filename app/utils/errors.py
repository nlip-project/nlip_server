"""
This file defines some common types of exceptions in the code. 
They are defined as children of PrivateException class so that 
one can catch this particular execption and handle it as needed. 

"""


class PrivateException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class UnitializedConfigurationError(PrivateException):
    def __init__(self, parameter):
        super().__init__(f"Configuration parameter {parameter} needs to be defined")


class RethrownException(PrivateException):
    def __init__(self, message: str, e: Exception = None):
        if e is None:
            super().__init__(message)
        else:
            super().__init__(f"{message} generated exception {e}")


class UnImplementedError(PrivateException):
    def __init__(
        self,
        function_name: str,
        class_name: str = None,
    ):
        if class_name is None:
            message = f"function {function_name} is not implemented"
        else:
            message = (
                f"function {function_name} in class {class_name} is not implemented"
            )
        super().__init__(message)


class MissingFieldError(Exception):
    def __init__(self, field: str):
        super().__init__(f"Missing Expected field {field} in passed argument")


class DuplicateEntryError(Exception):
    def __init__(self, className: str, parameter: str):
        super().__init__(
            f"Tried to create a new instance of {className} but an instance with name {parameter} already exists"
        )


class MissingEntry(Exception):
    def __init__(self, objectType: str, name: str):
        super().__init__(
            f"There is no {objectType} with name of {name} in persistent store"
        )


class LLMInvocationError(RethrownException):
    def __init__(self, model_name: str, prompt: str, e: Exception = None):
        super().__init(f"Calling model {model_name} failed on prompt {prompt}", e)


class UnparseableInput(RethrownException):
    def __init__(self, message: str, input: str, e: Exception = None):
        super().__init(f"Error: {message} for input: {input} could not be parsed", e)


class MissingKeyError(Exception):
    def __init__(self, field_name: str, this_dict: dict):
        super().__init__(
            f"Error: Expected key {field_name} in dictionary but it is not present in dictionary {this_dict}"
        )


class MissingParameterError(Exception):
    def __init__(self, field_name: str, function_name: str, this_dict: dict):
        super().__init__(
            f"Error: Expected parameter {field_name} to be spcified when calling function {function_name} but it is not present in {this_dict}"
        )


class MissingCallableFunction(Exception):
    def __init__(self, function_name: str, class_name: str):
        super().__init__(
            f"Error: function {function_name} is not defined on objects of class {class_name}"
        )
