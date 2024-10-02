from django.db import models

class PermissionsModel(models.Model):
    """
    Auxiliary model to manage permissions without a database model.
    """
            
    class Meta:  # https://stackoverflow.com/a/37988537/2299448
        
        managed = False  # No database table creation or deletion  \
                         # operations will be performed for this model. 
                
        permissions = ( 
            ("can_trigger_inference", "Can Trigger AI Inference",),
        )