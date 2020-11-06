from src.hocr.aganitha_hocr.query_engine import QueryCompiler, CompiledQuery
from src.hocr.aganitha_hocr.object_model import HOCRDoc, Region, BlockSet, Block

if __name__ == "__main__":

"""
list of functions available
- top(BlockSet, argument=100, type="percentage")
- bottom(BlockSet, argument=10, type="percentage")
- left (BlockSet, argument=10, type="percentage")
- right(BlockSet, argument=10, type="percentage")
- nearest(BlockSet, axis="top") 
- farthest(BlockSet, axis="top")
- Intersection(List[BlockSet])
- Union(List[BlockSet]

data storage

"""
    hocr = HOCRDoc('/home/adarsh/ar-automation/tmp/07.06.20-lb83197-1-10-addl-doc-01.jpg.hocr')
