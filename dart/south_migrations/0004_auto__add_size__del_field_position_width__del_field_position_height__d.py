# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Size'
        db.create_table('dart_size', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal('dart', ['Size'])

        # Deleting field 'Position.width'
        db.delete_column('dart_position', 'width')

        # Deleting field 'Position.height'
        db.delete_column('dart_position', 'height')

        # Deleting field 'Position.size'
        db.delete_column('dart_position', 'size')

        # Adding M2M table for field sizes on 'Position'
        db.create_table('dart_position_sizes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('position', models.ForeignKey(orm['dart.position'], null=False)),
            ('size', models.ForeignKey(orm['dart.size'], null=False))
        ))
        db.create_unique('dart_position_sizes', ['position_id', 'size_id'])

        # Adding field 'Zone_Position.enabled'
        db.add_column('dart_zone_position', 'enabled', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'Size'
        db.delete_table('dart_size')

        # Adding field 'Position.width'
        db.add_column('dart_position', 'width', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Position.height'
        db.add_column('dart_position', 'height', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Position.size'
        db.add_column('dart_position', 'size', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Removing M2M table for field sizes on 'Position'
        db.delete_table('dart_position_sizes')

        # Deleting field 'Zone_Position.enabled'
        db.delete_column('dart_zone_position', 'enabled')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sizes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dart.Size']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'dart.size': {
            'Meta': {'object_name': 'Size'},
            'height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
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
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dart.Position']"}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dart.Zone']"})
        }
    }

    complete_apps = ['dart']
