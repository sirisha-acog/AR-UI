from src.hocr.aganitha_hocr.query_engine import QueryCompiler, CompiledQuery
from src.hocr.aganitha_hocr.object_model import HOCRDoc, Region, BlockSet, Block

if __name__ == "__main__":
    hocr = HOCRDoc('/home/adarsh/ar-automation/tmp/07.06.20-lb83197-1-10-addl-doc-01.jpg.hocr')
    query_list = ['PAGE/TOP:70%/BOT:45%/RIGHT:90%/TEXT:KATZ', 'PAGE/BOT:70%/BOT:45%/LEFT:50%/TEXT:GROUP',
                  'PAGE/RIGHT:70%/BOT:45%/TOP:90%/TEXT:IPG', 'PAGE/TOP:10%/TEXT:IPG', 'PAGE/BOT:98%/TEXT:IPG']
    for query in query_list:
        qc = QueryCompiler(query)
        compiled_query = qc.compile()
        cq = CompiledQuery(compiled_query)
        region = cq.execute_query(hocr)
        print(region.x_top_left, region.y_top_left, region.x_bot_right, region.y_bot_right)  # should be 0.5*0.5*1468 = 367
"""
Current implementation to strip the query is very crude. Need to improve. Do try catch so that user does not
input invalid cases. ('TOP/150%') is invalid.
Need to find a better way to strip '%' symbol from str.
Can we use FUNCTION as a keyword in our language? Limit the search scope to block.
"""