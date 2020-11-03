from typing import List, Union, Any, TypeVar, Optional
from aganitha_parsing_utils.html import HTMLParsingUtils
from src.hocr.aganitha_hocr.object_model import Region, Block, HOCRDoc
from src.hocr.aganitha_hocr.step import Step, StepTop, StepBottom, StepRight, StepLeft, StepText

# TypeVar
CompiledQuery_t = TypeVar('CompiledQuery')


class QueryCompiler(object):
    def __init__(self, query: str):
        self.query = query

    def compile(self) -> CompiledQuery_t:
        query_list = self.query.split('/')
        print(query_list)
        compiled_query = []
        for query in query_list[1:]:
            axis, argument = query.split(':')
            axis = axis.lower().strip()
            if axis == 'top':
                step = StepTop(axis, argument[:-1])
            elif axis == 'bot':
                step = StepBottom(axis, argument[:-1])
            elif axis == 'right':
                step = StepRight(axis, argument[:-1])
            elif axis == 'left':
                step = StepLeft(axis, argument[:-1])
            elif axis == 'text':
                step = StepText(axis, argument[:-1])
            compiled_query.append(step)
        return compiled_query


class CompiledQuery(object):
    def __init__(self, parsed_query: List[Step]):
        self.parsed_query = parsed_query

    def execute_query(self, context: Union[HOCRDoc, Region, Block]) -> Any:
        next_step_context = context
        for step in self.parsed_query:
            next_step_context = step.execute(next_step_context)

        return next_step_context


cq = QueryCompiler('PAGE/TOP:20%/RIGHT:30%/TEXT:Date')
compiled = cq.compile()
