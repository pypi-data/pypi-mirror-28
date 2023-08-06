
from .algo import Algo 
from .entity_slot import Slot
from .entity_space import Space
from .algo_code import AlgoCode
from . import log, show_adding_box_log
from .exception import DistributionException

import time
class AlgoMulti(Algo):
  """
  pack items into multiple
  bins. Bins should follow FIFO
        algorithm

	
  @param item_collection: set of items
  @returns bins with items
  """ 
  def run(self):
    log.debug("Entering Algorithm MULTI")
    item_collection = self.items
    bin_collection = self.bins
    if not item_collection.size() >= bin_collection.size():
	 raise DistributionException("Bins should be less than items")

    def continue_fn(bin, space, item):
      if bin.occupied_space(space, item):
         return AlgoCode.NO_SPACE

      m_y = bin.get_min_y_pos(space.y)

      if (space.x + item.w) > bin.w:
        """ try z now """
        space.z += item.d 
        space.x = 0
      else: 
        space.x += 1

      """ if space.z fails and so does  space.x """
      """ go up in height make sure y  """
      """ is at the proper juxtaposition """
      if (space.z + item.d) > bin.d:
        space.y += m_y.max_y
        space.x = m_y.min_x
        space.z = m_y.min_z

      """ if were at the top of the box """
      """ we cannot allocate any more space so we can move on """
      if int(space.y + item.h) > bin.h:
	      return AlgoCode.LAST_ITEM

      return AlgoCode.FOUND_SPACE
 	



    bin = bin_collection.next()
    first = True
    while bin:
      log.info("Packing Bin #{0}".format(bin.id))
      bin.start_time = time.time() 
      item_collection.reset()
      item = item_collection.next()
      while item:
        item = item_collection.current()
        """ using heuristics, rotate and see if we occupy less room """
        #item.rotate()
        if not bin.can_fit( item ):
           item_collection.nextlargest()
           continue

        space = Space(x=0, y=0, z=0)
       
        """ if item.w > bin.w: """
        """ self.binner.add_lost(item) """
        can_continue = continue_fn(bin, space, item)
        while can_continue == AlgoCode.NO_SPACE:
           space.compute_next_sequence()
           can_continue = continue_fn(bin, space, item)

        if can_continue == AlgoCode.LAST_ITEM:
           continue

        show_adding_box_log(space, item)

        slot = Slot.from_space_and_item(space, item)
        bin.append(slot)
        item = item_collection.nextlargest()

      bin.end_time = time.time()
      bin = bin_collection.next()
    return self.binner


	   
