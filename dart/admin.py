from django.contrib import admin
from settings import STATIC_URL
from dart.models import Zone, Position, Custom_Ad, Custom_Ad_Template, Zone_Position, Size, Site
from settings import STATIC_URL
		
class Zone_PositionInline(admin.TabularInline):
	model = Zone.position.through
	ordering = ("position__name",)
	fields = ("position", "custom_ad", "enabled", "date_published")

	
class Zone_Admin(admin.ModelAdmin):
	ordering = ("name",)
	prepopulated_fields = {"slug" : ("name",)}
	
	ct_field = "content_type"
	ct_fk_field = "object_id"
	css = {
		"all": (
			STATIC_URL + "blog/css/autocomplete.css",
		)
	}
	
	fieldsets = (
		(None, {
			"fields": ("name", "slug", "site"),
		}),
	)
	inlines = [
		Zone_PositionInline,	
	]

class Size_Admin(admin.ModelAdmin):
	ordering = ("name",)
	
	
	
class Zone_Position_Admin(admin.ModelAdmin):
	ordering = ("zone", "position")
	
	list_display = ("zone", "position", "custom_ad", "enabled", "default_dart_tag")
	
	fieldsets = (
		(None, {
			"fields": ("zone", "position", "custom_ad", "enabled", "date_published", "sync", )
		}),
	)
	class Media:
		
		js = (
			STATIC_URL + "admin/dart/js/zone_position.js",
		)	


class Zone_Inline(admin.TabularInline):
	model = Zone.position.through
	verbose_name = "Enabled Zones"
	verbose_name_plural = "Enabled Zones"
	fields = ("zone", "custom_ad", "enabled", "date_published")

class Position_Admin(admin.ModelAdmin):
	prepopulated_fields = {"slug" : ("name",)}
	ordering = ("name",)
	class Media:
		
		js = (
			STATIC_URL + "admin/dart/js/position.js",
		)
	
	fieldsets = (
		(None, {
			"fields": ("name", "slug", "sizes", )
		}),
	)
	
	inlines = [
		Zone_Inline,
	]
	
class Site_Admin(admin.ModelAdmin):
	ordering = ("slug",)


class Custom_Ad_Template_Admin(admin.ModelAdmin):
	pass	
	
class Custom_Ad_Admin(admin.ModelAdmin):
	prepopulated_fields = {"slug" : ("name",)}
	search_fields = ["name", ]
	
	class Media:
		
		js = (
			STATIC_URL + "admin/dart/js/custom_ad.js",
		)
	fieldsets = (
		(None, {
			"fields": ("name", "slug", "type" )
		}),
		("Custom Code", {
			"description": "Use this section to write custom HTML. Overrides anything set in the Image/URL section.",
			"classes": ("collapse closed sizes custom-code",),
			"fields": ("load_template", "embed",)
		}),
		("Image/URL", {
			"description": "Upload an image and a URL for a simple linked image ad unit",
			"classes": ("collapse closed sizes image-url",),
			"fields": ("url", "image")
		}),
		("Text Version", {
			"description": "Text version of the ad for non-HTML/JS browsers and newsletters",
			"classes": ("sizes",),
			"fields": ("text_version",)
		}),
	)

admin.site.register(Site, Site_Admin)
admin.site.register(Zone_Position, Zone_Position_Admin)
admin.site.register(Zone, Zone_Admin)
admin.site.register(Custom_Ad, Custom_Ad_Admin)
admin.site.register(Custom_Ad_Template, Custom_Ad_Template_Admin)
admin.site.register(Position, Position_Admin)
admin.site.register(Size, Size_Admin)