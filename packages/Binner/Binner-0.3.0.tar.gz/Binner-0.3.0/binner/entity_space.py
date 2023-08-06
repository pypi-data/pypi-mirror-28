from .entity_artifact import EntityArtifact
class Space(EntityArtifact):
  fields = frozenset(('x', 'y', 'z'))
  x = 0
  y = 0
  z = 0 
  def to_dict( self ):
	return dict(x=self.x,y=self.y,z=self.z)
  def compute_next_sequence(self):
      self.x += 1 
      self.y += 1
      self.z += 1

  def x_with_item(self, item):
      return ( self.x + item.w )

  def y_with_item(self, item):
      return ( self.x + item.h )

  def z_with_item(self, item):
      return ( self.z + item.d )


  def get_coords(self):
    return self.get_position()


