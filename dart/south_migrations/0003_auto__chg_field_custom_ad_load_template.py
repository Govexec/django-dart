# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Custom_Ad.load_template'
        db.alter_column('dart_custom_ad', 'load_template_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dart.Custom_Ad_Template'], null=True))


    def backwards(self, orm):
        
        # Changing field 'Custom_Ad.load_template'
        db.alter_column('dart_custom_ad', 'load_template_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['dart.Custom_Ad_Template']))


    models = {
        'dart.custom_ad': {
            'Meta': {'object_name': 'Custom_Ad'},
            'embed': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'load_template': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['dart.Custom_Ad_Template']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text_version': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'dart.custom_ad_template': {
            'Meta': {'object_name': 'Custom_Ad_Template'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'template': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'})
        },
        'dart.position': {
            'Meta': {'object_name': 'Position'},
            'height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'dart.zone': {
            'Meta': {'object_name': 'Zone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dart.Position']", 'through': "orm['dart.Zone_Position']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'dart.zone_position': {
            'Meta': {'object_name': 'Zone_Position'},
            'custom_ad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dart.Custom_Ad']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dart.Position']"}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dart.Zone']"})
        }
    }

    complete_apps = ['dart']
