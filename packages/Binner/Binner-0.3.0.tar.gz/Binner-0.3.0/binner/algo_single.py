from .algo import Algo
from .algo_code import AlgoCode
from .entity_slot import Slot
from .entity_space import Space
from  . import log, show_adding_box_log
from .exception import DistributionException
import time
class AlgoSingle(Algo):
  """
  pack items into a single
  bin

  for single bin packing we merely
  need to operate on one bin. Don't
  accept input bins larger than size one

  @param item_collection: set of items
  @returns one bin packed with items
  """
  def run(self):
    log.debug("Entering algorithm SINGLE")
    bin_collection = self.bins
    item_collection =self.items
    if len(bin_collection.items) == 0 or len(bin_collection.items) > 1:
	    raise DistributionException("Single takes only one item")

    bin = bin_collection.next()
    """
    checks with the bin can continue within the space
    for single algo
    """
    def continue_fn(bin, space, item):
        if bin.occupied_space(space, item):
           return AlgoCode.NO_SPACE
        m_y = bin.get_min_y_pos(space.y)

        if space.x + (item.w > bin.w):
            """ try z now """
            space.z += item.d 
            space.x = 0
        else: 
            space.x += 1


        """ if space.z fails and so does space.x """
        """ go up in height make sure y  """
        """ is at the proper juxtaposition """
        if space.z + item.d > bin.d:
            space.y += m_y.max_y
            space.x = m_y.min_x
            space.z = m_y.min_z
        if int(space.y + item.h) > bin.h:
            return AlgoCode.LAST_ITEM
        return AlgoCode.FOUND_SPACE

    while bin:
      log.info("Trying to allocate items for bin: {0}".format(bin.id))

      item_collection.reset()
      bin.start_time = time.time()
      item = item_collection.next()

      while item:
        item = item_collection.current()
        if not bin.can_fit( item ) :
            item_collection.next()
            continue

        space = Space(x=0, y=0, z=0)
        """ if item.w > bin.w: """
        """ self.binner.add_lost(item) """
        can_continue = continue_fn(bin, space, item)
        while can_continue == AlgoCode.NO_SPACE:
          """ if were at the top of the box """
          """ we cannot allocate any more space so we can move on """
          space.compute_next_sequence()
          can_continue = continue_fn(bin, space, item)
        if can_continue == AlgoCode.LAST_ITEM:
           continue
        show_adding_box_log(space, item) 

        slot = Slot.from_space_and_item(space, item)
        bin.append(slot)
        item = item_collection.next()
	
      bin.end_time = time.time()
      bin = bin_collection.next()
    return self.binner

