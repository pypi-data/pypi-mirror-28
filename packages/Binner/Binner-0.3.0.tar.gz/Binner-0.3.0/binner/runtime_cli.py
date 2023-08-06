from .runtime import Runtime
from .algo_smallest import AlgoSmallest
from .algo_multi import AlgoMulti
from .algo_single import AlgoSingle
from .collection_bin import BinCollection
from .collection_item import ItemCollection
from helpers import enumerate_json, get_a_binner_id
from uuid import uuid4
import json
import argparse
class RuntimeCLI(Runtime):
  def __init__(self,args):
	super(RuntimeCLI, self).__init__(args)
        self.initv2( self.args )
  def initv1(self, a):
    for _i in range(0, len(a)):
      i = a[_i]
      try:
        j = a[_i + 1]
      except:
        j = a[_i]
        
      if i in ['-bin', '--bins']:
        self.bins = j 
      if i in ['-i', '--items']:
        self.items = j 
      if i in ['-a', '--algorithm']:
        self.algorithm = j
      if i in ['-h', '--help']:
        self._help()
        return None
    self.run(self)
  def initv2( self, a ):
		
	 parser = argparse.ArgumentParser()
	 ##parser.add_argument("--mode", help="mode, cli or web", default="cli")
	 parser.add_argument("--algorithm", help="algorithm to use 'small' or 'multi' or 'single'", default="single")
	 parser.add_argument("--multi-use-smallest-bins",help="Use the smallest bins",action="store_true")
	 parser.add_argument("--bins", help="Bins to specify")
	 parser.add_argument("--items", help="Items to specify")
	 parser.add_argument("--id", help="A transaction ID defaults to a unique id", default=get_a_binner_id())
	 parser.add_argument("--host", help="Host to run API on", default="0.0.0.0")
	 parser.add_argument("--port", help="Port to run API on", default=9100)
	 result = parser.parse_args()
	 if len( a ) == 1:
		parser.print_help()
	 else:
	 	self.run( result )
        
  def _help(self):
    print """
usage: binner "{web|cli}" required_input required_input2
options:

SERVER SPECIFIC
--bins Bins to use
--items Items to pack
--algorithm What algorithm to use
"""
  
  def run(self, args):
      bins = BinCollection(json.loads(args.bins))
      items = ItemCollection(json.loads(args.items))
      id = args.id

      if args.algorithm == 'single':
        binner_algo = AlgoSingle(args,bins,items,id=id)
      elif args.algorithm == 'multi':
        binner_algo = AlgoMulti(args,bins,items, id=id)
      elif args.algorithm == "smallest":
        binner_algo = AlgoSmallest(args,bins,items, id=id)
      binner_algo.run()
      print binner_algo.binner.show()


