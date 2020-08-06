import mongoengine as mongo
import mongoengine_goodjson as gj

from models.user import User

class Event(gj.EmbeddedDocument):
    id   = mongo.StringField(required=True, max_length=100)
    name = mongo.StringField(required=True, max_length=100)
    link = mongo.URLField(null=True)
    event_start = mongo.DateTimeField(db_field='event-start', required=True)
    event_end   = mongo.DateTimeField(db_field='event-end', required=True)
    description = mongo.StringField(required=True, max_length=500)

class Resource(gj.EmbeddedDocument):
    id   = mongo.StringField(required=True, max_length=100)
    name = mongo.StringField(required=True, max_length=100)
    link = mongo.URLField(required=True)

class SocialMediaLinks(gj.EmbeddedDocument):
    contact_email = mongo.EmailField(db_field='contact-email', null=True)
    website     = mongo.URLField(null=True)
    facebook    = mongo.URLField(null=True)
    instagram   = mongo.URLField(null=True)
    linkedin    = mongo.URLField(null=True)
    twitter     = mongo.URLField(null=True)
    youtube     = mongo.URLField(null=True)
    github      = mongo.URLField(null=True)
    behance     = mongo.URLField(null=True)
    medium      = mongo.URLField(null=True)
    gcalendar   = mongo.URLField(null=True) # TODO: ask if we're still integrating this

class Tag(gj.Document):
    id   = mongo.IntField(required=True, primary_key=True)
    name = mongo.StringField(required=True)

class Club(gj.Document):
    id    = mongo.StringField(required=True, primary_key=True)
    name  = mongo.StringField(required=True, max_length=100)
    owner = mongo.ReferenceField(User, required=True)

    tags         = mongo.ListField(mongo.ReferenceField(Tag), required=True, max_length=3)
    app_required = mongo.BooleanField(db_field='app-required', required=True)
    new_members  = mongo.BooleanField(db_field='new-members', required=True)
    
    logo_url   = mongo.URLField(db_field='logo-url', null=True, default=None)
    banner_url = mongo.URLField(db_field='banner-url', null=True, default=None)

    about_us     = mongo.StringField(db_field='about-us', default='', max_length=500)
    get_involved = mongo.StringField(db_field='get-involved', default='', max_length=500)

    resources = mongo.EmbeddedDocumentListField(Resource, default=[])
    events    = mongo.EmbeddedDocumentListField(Event, default=[])

    social_media_links = mongo.EmbeddedDocumentField(SocialMediaLinks, db_field='social-media-links', default=SocialMediaLinks())

    meta = {
        'indexes': [
            {
                'fields': ['$name', '$about_us'],
                'default_language': 'english',
                'weights': {'name': 8, 'about-us': 2}
            }
        ]
    }