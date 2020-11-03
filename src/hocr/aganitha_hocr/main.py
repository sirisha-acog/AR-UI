from src.hocr.aganitha_hocr.query_engine import QueryCompiler, CompiledQuery
from src.hocr.aganitha_hocr.object_model import HOCRDoc, Region, BlockSet, Block

if __name__ == "__main__":
    hocr = HOCRDoc('/home/adarsh/ar-automation/tmp/07.06.20-lb83197-1-10-addl-doc-01.jpg.hocr')
    qc = QueryCompiler('PAGE/TOP:70%/BOT:45%/RIGHT:90%/TEXT:KATZ')
    compiled_query = qc.compile()
    cq = CompiledQuery(compiled_query)
    region = cq.execute_query(hocr)
    #print(region.x_top_left, region.y_top_left, region.x_bot_right, region.y_bot_right)  # should be 0.5*0.5*1468 = 367
