# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Position'
        db.create_table('dart_position', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('size', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('width', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('height', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('dart', ['Position'])

        # Adding model 'Zone'
        db.create_table('dart_zone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('dart', ['Zone'])

        # Adding model 'Custom_Ad'
        db.create_table('dart_custom_ad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('embed', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
            ('text_version', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('dart', ['Custom_Ad'])

        # Adding model 'Zone_Position'
        db.create_table('dart_zone_position', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dart.Position'])),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dart.Zone'])),
            ('custom_ad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dart.Custom_Ad'], null=True, blank=True)),
        ))
        db.send_create_signal('dart', ['Zone_Position'])

    def backwards(self, orm):
        
        # Deleting model 'Position'
        db.delete_table('dart_position')

        # Deleting model 'Zone'
        db.delete_table('dart_zone')

        # Deleting model 'Custom_Ad'
        db.delete_table('dart_custom_ad')

        # Deleting model 'Custom_Ad_Template'
        db.delete_table('dart_custom_ad_template')

        # Deleting model 'Zone_Position'
        db.delete_table('dart_zone_position')

    models = {
        'dart.custom_ad': {
            'Meta': {'object_name': 'Custom_Ad'},
            'embed': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text_version': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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
