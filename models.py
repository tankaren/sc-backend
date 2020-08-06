import datetime
import mongoengine as mongo
import mongoengine_goodjson as gj

class FutureUser(gj.Document):
    org_name = mongo.StringField()
    org_email = mongo.EmailField()

    poc_name = mongo.StringField()
    poc_email = mongo.EmailField()

class User(gj.Document):
    id = mongo.IntField(primary_key=True)
    email = mongo.EmailField(unique=True)
    password = mongo.StringField(max_length=256)
    admin = mongo.BooleanField(default=False)

    registered_on = mongo.DateTimeField(default=datetime.datetime.now)
    confirmed = mongo.BooleanField(default=False)
    confirmed_on = mongo.DateTimeField()

class Event(gj.EmbeddedDocument):
    title = mongo.StringField(required=True)
    description = mongo.StringField(required=True)
    start_datetime = mongo.DateTimeField(required=True)
    end_datetime = mongo.DateTimeField(required=True)
    link = mongo.URLField()

class Resource(gj.EmbeddedDocument):
    title = mongo.StringField(required=True, max_length=150)
    link = mongo.URLField(required=True)

class SocialMediaMap(gj.EmbeddedDocument):
    facebook = mongo.URLField()
    instagram = mongo.URLField()
    linkedin = mongo.URLField()
    twitter = mongo.URLField()
    youtube = mongo.URLField()

class Tag(gj.Document):
    name = mongo.StringField(required=True)
    id = mongo.IntField(required=True, primary_key=True)

class Club(gj.Document):
    name = mongo.StringField(required=True, max_length=100)
    owner = mongo.ReferenceField(User, required=True)

    tags = mongo.ListField(mongo.ReferenceField(Tag), default=[])
    app_required = mongo.BooleanField(required=True)
    accepting_members = mongo.BooleanField(required=True)
    
    profile_pic = mongo.ImageField(collection_name='profile', default=None)
    cover_pic = mongo.ImageField(collection_name='cover', default=None)

    description = mongo.StringField(default='')

    resources = mongo.EmbeddedDocumentListField(Resource, default=[])
    events = mongo.EmbeddedDocumentListField(Event, default=[])

    website = mongo.URLField(null=True)
    social_media_links = mongo.EmbeddedDocumentField(SocialMediaMap, default={})
    gcalendar = mongo.URLField(null=True)

    meta = {
        'indexes': [
            {
                'fields': ['$name', '$description'],
                'default_language': 'english',
                'weights': {'name': 8, 'description': 2}
            }
        ]
    }