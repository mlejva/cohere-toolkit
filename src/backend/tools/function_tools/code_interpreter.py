import os
from typing import Any

from langchain_core.tools import Tool as LangchainTool
from pydantic.v1 import BaseModel, Field
from e2b_code_interpreter import CodeInterpreter, Result, Execution

from backend.tools.function_tools.base import BaseFunctionTool


class LangchainCodeInterpreterToolInput(BaseModel):
    code: str = Field(description="Python code to execute.")


class CodeInterpreterFunctionTool(BaseFunctionTool):
    """
    This class calls arbitrary code against a Python Jupyter notebook.
    It requires an E2B_API_KEY to create a sandbox.
    """

    def __init__(self):
        # Instantiate the E2B sandbox - this is a long lived object
        # that's pinging E2B cloud to keep the sandbox alive.
        if "E2B_API_KEY" not in os.environ:
            raise Exception(
                "Code Interpreter tool called while E2B_API_KEY environment variable is not set. Please get your E2B api key here https://e2b.dev/docs and set the E2B_API_KEY environment variable."
            )
        self.code_interpreter = CodeInterpreter()

    def call(self, parameters: dict, **kwargs: Any):
        # TODO: E2B supports generating and streaming charts and other rich data
        # because it has a full Jupyter server running inside the sandbox.
        # What's the best way to send this data back to frontend and render them in chat?

        code = parameters.get("code", "")
        print("Code to run", code)
        execution: Execution = self.code_interpreter.notebook.exec_cell(code)

        print("Result of code run", execution)

        artifacts = [
            {"type": mime_type, "data": data}
            for result in execution.results
            for mime_type, data in result.raw.items()
        ]

        artifact_list = ", ".join([a["type"] for a in artifacts])
        print("Artifacts", artifact_list)

        # TODO: We may need to serialize the fields so they can be streamed.
        # TODO: We should make it so that the info about results can be send to LLM too — just sending the Base64 encoding of the artifact is useless.
        return {
            "results": artifacts,
            "stdout": execution.logs.stdout,
            "stderr": execution.logs.stderr,
            "error": execution.error,
        }

    # langchain does not return a dict as a parameter, only a code string
    def langchain_call(self, code: str):
        return self.call({"code": code})

    def to_langchain_tool(self) -> LangchainTool:
        tool = LangchainTool(
            name="code_interpreter",
            description="Execute python code in a Jupyter notebook cell and returns any rich data (eg charts) as results, with stdout, stderr, and error. The rich results are shown to user automatically, so don't link them.",
            func=self.langchain_call,
        )
        tool.args_schema = LangchainCodeInterpreterToolInput
        return tool
