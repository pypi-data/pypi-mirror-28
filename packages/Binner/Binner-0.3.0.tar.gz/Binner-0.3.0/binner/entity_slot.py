from .entity_artifact import EntityArtifact
class Slot(EntityArtifact):
  fields = frozenset(('x', 'y', 'z'))
  min_x = 0
  max_x = 0
  min_y = 0
  max_y = 0
  min_z = 0 
  max_z = 0

  def to_dict( self ):
	return dict(
		id=self.id,
		min_x=self.min_x,
		max_x=self.max_x,
		min_y=self.min_y,
		max_y=self.max_y,
		min_z=self.min_z,
		max_z=self.max_z )
  @classmethod
  def from_space_and_item(cls, space, item):
	return Slot(
      item=item,
	  min_x=space.x,
	  min_y=space.y,
	  min_z=space.z,
	  max_x=space.x_with_item(item),
	  max_y=space.y_with_item(item),
	  max_z=space.z_with_item(item))
  def get_coords(self):
    return self.get_position()


