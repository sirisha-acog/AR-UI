from typing import List, Union, Any, TypeVar, Optional
from aganitha_parsing_utils.html import HTMLParsingUtils
from src.hocr.aganitha_hocr.object_model import Region, Block
from src.hocr.aganitha_hocr.step import Step

# TypeVar
CompiledQuery_t = TypeVar('CompiledQuery')


class QueryCompiler(object):
    def __init__(self, query: str):
        self.query = query

    def compile(self) -> CompiledQuery_t:
        query_list = self.query.split('/')
        print(query_list)
        scope = query_list[0]
        compiled_query = []
        for query in query_list[1:]:
            axis, argument = query.split(':')
            compiled_query.append(Step(axis, argument[:-1]))
        return compiled_query


class CompiledQuery(object):
    def __init__(self, parsed_query: List[Step]):
        self.parsed_query = parsed_query

    def execute_query(self, doc: HTMLParsingUtils, context: Optional[Union[Region, Block]]) -> Any:
        for query in self.parsed_query:
            # query.axis , query.argument
            if query.axis == 'TOP':
                print('calling StepTOP()')
            elif query.axis == 'BOT':
                print('calling StepBOT')
            elif query.axis == 'RIGHT':
                print('calling StepRIGHT')
            elif query.axis == 'LEFT':
                print('calling StepLEFT')
            elif query.axis == 'TEXT':
                print('calling StepTEXT')
        pass

cq = QueryCompiler('PAGE/TOP:20%/RIGHT:30%/TEXT:Date')
compiled = cq.compile()



