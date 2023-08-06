from binner.entity import Entity

class EntityObject(Entity):
   def __init__(self, *args, **kwargs):
      super(EntityObject,self).__init__(*args, **kwargs)
      self.initial = dict(
         w=kwargs['w'],
         h=kwargs['h'],
         d=kwargs['d']
  	  )
   def get_size(self):
     return dict(w=self.w, h=self.h)
   def to_dict(self):
     return dict(w=self.w, h=self.h, d=self.d, id=self.id)



