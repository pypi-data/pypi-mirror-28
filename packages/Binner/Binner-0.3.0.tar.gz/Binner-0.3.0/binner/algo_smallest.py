from .algo import Algo
from .algo_code import AlgoCode
from .entity_slot import Slot
from .entity_space import Space
from . import log, show_adding_box_log, find_smallest
from .exception import DistributionException
import time
class AlgoSmallest(Algo):
  """
  find the smallest bin
  for a given amount of 
  bins.

  Output SHOULD try to have all
  the items. I.e 

  A bin smaller bin with less items is worse than 
  A bigger bin with more items

  @param item_collection: set of items

  @returns a Bin object
         whose size is smallest with the most
         amount of items 
  """
  
  def run(self):
    log.debug("Entering Algorithm SMALLEST")
    bin_collection = self.bins
    item_collection = self.items
    if not (bin_collection.size() > 0 and item_collection.size() > 0):
	    raise DistributionException("Please provide atleast one bin and item")
    def continue_fn( bin, space, item ):
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
      if space.z + item.d > bin.d:
        space.y += m_y.max_y
        space.x = m_y.min_x
        space.z = m_y.min_z
      """ if were at the top of the box """
      """ we cannot allocate any more space so we can move on """
      if int(space.y + item.h) > bin.h:
         return AlgoCode.LAST_ITEM

      return AlgoCode.FOUND_SPACE

    bin = bin_collection.next()
    while bin:
      log.info("Trying to allocate items for bin: {0}".format(bin.id))
      item_collection.reset()
      bin.start_time = time.time()
      item = item_collection.next()

      while item:
        item = item_collection.current()
        if not bin.can_fit( item ):
            item_collection.next()
            continue

        space = Space(x=0, y=0, z=0)
        can_continue = continue_fn(bin, space, item)
    
        """ if item.w > bin.w: """
        """ self.binner.add_lost(item) """
        while can_continue == AlgoCode.NO_SPACE:
            space.compute_next_sequence()
            can_continue = continue_fn(bin, space, item)
        if can_continue == AlgoCode.LAST_ITEM:
            continue

        show_adding_box_log(space, item)
        slot = Slot.from_space_and_item(space, item)
        bin.append(slot)
        item_collection.next()
      bin.end_time =time.time()
      bin = bin_collection.next()
    """
    to be the smallest bin we
    must allocate all space of the
    bin and be the smallest in size
    """
    smallest = find_smallest(item_collection, self.binner.packed_bins)
    self.binner.set_smallest(smallest)
    return self.binner
