from django.db import models
from django.contrib.auth import models as auth_models

from datetime import datetime, timedelta

class Message(models.Model):
    author = models.ForeignKey(auth_models.User)
    date = models.DateTimeField(null=True)
    title = models.CharField(max_length=50)
    text = models.TextField()



class Person(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(auth_models.User, blank=True, null=True)
    relationships = models.ManyToManyField('self', through='Relationship',
                                           symmetrical=False,
                                           related_name='related_to')

    def __unicode__(self):
        return self.name

    def add_relationship(self, person, status):
        relationship, created = Relationship.objects.get_or_create(
            from_person=self,
            to_person=person,
            status=status
        )
        return relationship

    def remowe_relationship(self, person, status):
        Relationship.objects.filter(
            from_person=self,
            to_person=person,
            status=status,
        ).delete()
        return

    def get_relationships(self, status):
        return self.relationships.filter(
            to_people__status=status,
            to_people__from_person=self,
        )

    def get_related_to(self, status):
        return self.related_to.filter(
            from_people__status=status,
            from_people__to_person=self,
        )

    def get_following(self):
        return self.get_relationships(RELATIONSHIP_FOLLOWING)

    def get_followers(self):
        return self.get_related_to(RELATIONSHIP_FOLLOWING)

    def get_friends(self):
        return self.relationships.filter(
            to_people__status=RELATIONSHIP_FOLLOWING,
            to_people__from_person=self,
            from_people__status=RELATIONSHIP_FOLLOWING,
            from_people__to_person=self,
        )


RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING,'Following'),
    (RELATIONSHIP_BLOCKED,'Blocked'),
)

class Relationship(models.Model):
    from_person = models.ForeignKey(Person, related_name='from_people')
    to_person = models.ForeignKey(Person, related_name='to_people')
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)