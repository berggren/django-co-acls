'''
Created on Apr 5, 2011

@author: leifj
'''

from django.db import models
from django.db.models.fields import CharField, DateTimeField
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class AccessControlEntry(models.Model):
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    permission = CharField(max_length=256)
    modify_time = DateTimeField(auto_now=True)
    create_time = DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        if self.user:
            return "%s is allowed to %s %s" % (self.user.username,self.permission,self.content_object)
        elif self.group:
            return "%s is allowed to %s %s" % (self.group.name,self.permission,self.content_object)
        else:
            return "%s is allowed to %s %s" % ('anyone',self.permission,self.content_object)

    class Meta:
        unique_together = (('group','permission'),('user','permission'))

def allow(object,ug,permission):
    if isinstance(ug, Group):
        return allow_group(object,ug,permission)
    elif isinstance(ug,User):
        return allow_user(object,ug,permission)
    elif ug == 'anyone' or ug == '':
            type = ContentType.objects.get_for_model(object)
            ace,created = AccessControlEntry.objects.get_or_create(object_id=object.id,content_type=type,permission=permission,user=None,group=None)
            return ace
    else:
        raise Exception,"Don't know how to allow %s to do stuff" % repr(ug)

def deny(object,ug,permission):
    if isinstance(ug, Group):
        return deny_group(object,ug,permission)
    elif isinstance(ug,User):
        return deny_user(object,ug,permission)
    elif ug == 'anyone' or ug == '':
            type = ContentType.objects.get_for_model(object)
            acl = AccessControlEntry.objects.filter(object_id=object.id,content_type=type,user=None,group=None,permission=permission)
            for ace in acl: # just in case we grew duplicates
                ace.delete()
            return None
    else:
        raise Exception,"Don't know how to allow %s to do stuff" % repr(ug)

def acl(object,permission=None):
    type = ContentType.objects.get_for_model(object)
    qs = AccessControlEntry.objects.filter(object_id=object.id,content_type=type)
    if permission != None:
        return qs.filter(permission=permission)
    else:
        return qs

def allow_user(object,user,permission):
    type = ContentType.objects.get_for_model(object)
    ace,created = AccessControlEntry.objects.get_or_create(object_id=object.id,content_type=type,user=user,permission=permission)
    return ace

def deny_user(object,user,permission):
    type = ContentType.objects.get_for_model(object)
    acl = AccessControlEntry.objects.filter(object_id=object.id,content_type=type,user=user,permission=permission)
    for ace in acl:
        ace.delete()
    return None

def allow_group(object,group,permission):
    type = ContentType.objects.get_for_model(object)
    ace,created = AccessControlEntry.objects.get_or_create(object_id=object.id,content_type=type,group=group,permission=permission)
    return ace

def deny_group(object,group,permission):
    type = ContentType.objects.get_for_model(object)
    acl = AccessControlEntry.objects.filter(object_id=object.id,content_type=type,group=group,permission=permission)
    for ace in acl:
        ace.delete()
    return None

def clear_acl(object):
    type = ContentType.objects.get_for_model(object)
    for ace in AccessControlEntry.objects.filter(object_id=object.id,content_type=type):
        ace.delete()
        
def remove_permission(id):
    for ace in AccessControlEntry.objects.filter(pk=id):
        ace.delete()

def is_allowed(object,user,permission):
    type = ContentType.objects.get_for_model(object)
    for ace in AccessControlEntry.objects.filter(object_id=object.id,content_type=type,permission=permission):
        if (not ace.group and not ace.user) or (ace.group in user.groups.all()) or (user == ace.user):
            return True
            
    return False

def is_anyone_allowed(object,permission):
    type = ContentType.objects.get_for_model(object)
    for ace in AccessControlEntry.objects.filter(object_id=object.id,content_type=type,user=None,group=None,permission=permission):
        if not ace.group and not ace.user: #probably redundant but you never know what the db layer does...
            return True
    return False