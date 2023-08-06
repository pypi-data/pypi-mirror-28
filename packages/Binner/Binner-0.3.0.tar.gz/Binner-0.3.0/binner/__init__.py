import logging
logging.basicConfig(
	 level=logging.DEBUG,
	 format="%(asctime)s %(message)s" )

log = logging.getLogger("")

def find_smallest(item_collection, packed_bins):
   smallest = packed_bins.first()
   for bin in packed_bins:
     if ( bin.get_size() < smallest.get_size() ) and ( len( bin.items ) == item_collection.count() ):
          smallest = bin
   return smallest


def show_adding_box_log(space, item):
  log.info("adding a box at: x: {0}, mx: {1}, y: {2}, my: {3}, z: {4}, mz: {5}".format(
     space.x, 
     space.x_with_item(item), 
     space.y, 
     space.y_with_item(item), 
     space.z, 
     space.z_with_item(item)))


