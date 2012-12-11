from django.db import models
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from coffin.template import Context, loader
from django.conf import settings
from settings import UPLOAD_PATH
from time import mktime
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site as Django_Site


# DART-related constants that can be adjusted in site settings

DART_DOMAIN = getattr(settings, "DART_DOMAIN", "ad.doubleclick.net")

# Dictionary that sets defaults for ad settings
DART_AD_DEFAULTS = getattr(settings, "DART_AD_DEFAULTS", settings.DART_AD_DEFAULTS)

# If using ad network codes
DART_NETWORK_CODE = getattr(settings, "DART_NETWORK_CODE", "")

# If enabled shows cats from placekitten.com instead of ads for testing
DART_PLACEHOLDER_MODE = getattr(settings, "DART_PLACEHOLDER_MODE", False)


class Size(models.Model):
	"""
	Handles list of ad sizes that be allowed in a position.  Default list based on IAB standards is set in fixture
	"""
	name = models.CharField(max_length=255, null=False, blank=False) 
	
	width = models.PositiveSmallIntegerField(default=0, null=False, blank=False, help_text="Use zero for unknown/variable values")
	
	height = models.PositiveSmallIntegerField(default=0, null=False, blank=False, help_text="Use zero for unknown/variable values")
	
	def __unicode__(self):
		return u"%s - %s" % (self.name, self.dart_formatted_size)
	
	@property
	def dart_formatted_size(self):
		return u"%sx%s" % (self.width, self.height)

class Site(models.Model):
	""" DART site value that can be associated with a Django Site """

	slug = models.CharField("DART site handle", help_text="This is the same field passed to DART as the site", max_length=255, null=False, blank=False)
	
	slug_dev = models.CharField("DART development site handle", help_text="Development DART site handle to be used when DEBUG is enabled", max_length=255, null=False, blank=True)
	
	site = models.ForeignKey(Django_Site, blank=True)
	
	class Meta:
		verbose_name_plural = "Sites"
		verbose_name = "Site"
		
	def __unicode__(self, *args, **kwargs):
		return self.slug

class Position(models.Model):
	""" 
	Model for handling ad positions that map to placements on the page
	and the allowable sizes designated
	"""

	name = models.CharField(max_length=255, null=False, blank=False) 

	slug = models.CharField(help_text="This will be the same field passed to DART as the position", max_length=255, null=False, blank=False)
	
	sizes = models.ManyToManyField("Size", null=False, blank=False)

	class Meta:
		verbose_name_plural = "Ad Positions"
		
	def __unicode__(self):
		return u"%s" % self.name
		
	@property
	def size_list_string(self):
		return ",".join([size.dart_formatted_size for size in self.sizes.all()])
		
	@property
	def size_list(self):
		return [(size.width, size.height) for size in self.sizes.all()]

		
class Zone(models.Model):
	"""
	Model for handling ad zones for the site and the allowable positions enabled for that position
	"""

	name = models.CharField(max_length=255)

	slug = models.CharField(help_text="This will be the same field passed to DART as the zone", max_length=255)
	
	site = models.ManyToManyField(Site, blank=True)
	
	position = models.ManyToManyField(Position, through="Zone_Position")
	
	class Meta:
		verbose_name_plural = "Ad Zones"
		ordering = ["name"]
		
	def __unicode__(self):
		return u"%s" % self.name		


class Custom_Ad(models.Model):
	"""
	Custom ads served from the database, not DART, as either HTML, image/link, and/or plain text (for newsletters)
	"""

	name = models.CharField(max_length=255, default="")
	
	slug = models.CharField(max_length=255)
	
	type =  models.IntegerField(choices=((0, "Custom HTML"), (1, "Image/URL")), default=0)
	
	url = models.URLField(null=True, blank=True, help_text="Click tag URL")
	
	image = models.ImageField(null=True, blank=True, upload_to=UPLOAD_PATH + "custom_ads", help_text="Image for custom ad")
	
	embed = RichTextField(null=True, blank=True)
	
	load_template = models.ForeignKey("Custom_Ad_Template", null=True, blank=True, default=None, help_text="Load HTML code into the embed field from a pre-defined template")
	
	text_version = models.TextField(blank=True, help_text="Text version of ad for newsletters or Javascript disabled browsers")

	class Meta:
		verbose_name = "Custom Ad"
		verbose_name_plural = "Custom Ads"
		
	def __unicode__(self):
		return u"%s" % self.name
		
class Custom_Ad_Template(models.Model):
	""" 
	Templates for pre-defined HTML that can be loaded into a Custom Ad
	"""
	class Meta:
		verbose_name = "Custom Ad Template"
		verbose_name_plural = "Custom Ad Templates"
		
	name = models.CharField(max_length=255, default="")
	
	template = RichTextField(null=True, blank=True)

	def __unicode__(self):
		return u"%s" % self.name

	

class Zone_Position(models.Model):
	""" 
	Through model that goes between Zone and Position to enable positions for a zone,
	and set a Custom Ad for a Zone-Position
	"""

	position = models.ForeignKey(Position)
	
	zone = models.ForeignKey(Zone)
	
	custom_ad = models.ForeignKey(Custom_Ad, blank=True, null=True,)
	
	enabled = models.BooleanField(default=True)
	
	sync = models.BooleanField(default=True, help_text="Determines whether the position is synced with DART when sync task is run.  Otherwise enabled manually.")
	
	def default_dart_tag(self):
		
		return Ad_Page(zone=self.zone.slug).js_url(self.position.slug, size=self.position.sizes.all()[0].dart_formatted_size)
	
	def __unicode__(self):
		return u"%s: %s" % (self.zone, self.position)

	class Meta:
		verbose_name = "Enabled Position"
		verbose_name_plural = "Enabled Positions"
        ordering = ["zone__name"]

class Ad_Page(object):
	""" 
	Base class for ad settings on a page and rendering ad tag HTML 
	"""
	
	ad_attributes = {}
	_tile = 0
	site = None
	zone = None
	network_code = None
	default_render_js = True
	disable_ad_manager = True
	page_ads = {}

	def __init__(self, settings={}, site=None, zone=None, network_code="", default_render_js=None, disable_ad_manager=None, ad_attributes={}, ad_settings={}, *args, **kwargs):
		""" 
		Ad page attributes that are configured here:
			site - DART site - string
			zone - DART zone - string
			network_code - DART network code - numerical string
			default_render_js - render DART javascript by default, otherwise blank - boolean
			disable_ad_manager - Turn off ad management - boolean
			ad_attributes - dict of name/value pairs passed to all dart tags
			Kwargs are passed to DART string. Can be any key, value pair - dict
			
		"""
		temp_default = DART_AD_DEFAULTS.copy() if DART_AD_DEFAULTS else {}
		if settings:
			temp_default.update(settings)
		
		for setting in temp_default:
			self.__setattr__(setting, temp_default[setting])
		
		
		if site: self.site = site
		if zone: self.zone = zone

		self.network_code = DART_NETWORK_CODE if DART_NETWORK_CODE else network_code

		if default_render_js: self.default_render_js = default_render_js
		if disable_ad_manager: self.disable_ad_manager = disable_ad_manager
	
		
		if ad_attributes:
			self.ad_attributes.update(ad_attributes)
			
		# Support for legacy 'ad_settings' variable name
		if ad_settings:
			self.ad_attributes.update(ad_settings)
		
		# Preloader commented out because of possible caching conflicts
		# Pre-load all of the ads for the page into a dict
		#if not self.disable_ad_manager:
		#	page_ads = Zone_Position.objects.all().filter(zone__slug__in=(self.zone,"ros"), enabled=True)
		#	for ad in page_ads:
		#		self.page_ads[ad.position.slug] = ad

	@property
	def tile(self):
		""" Gets and increments the tile position for the page """
		self._tile = self._tile + 1
		return self._tile
		
	def _query_ad(self, pos, site=None, custom_zone=None, custom_ad=False, **kwargs):
		""" Creates queryset for an ad in ad_manager. Used by has_ad and get_ad """
		zone = custom_zone if custom_zone else self.zone
		
		qs = Zone_Position.objects.all().filter(position__slug=pos, zone__slug__in=(zone, "ros"), enabled=True)
		
		if site:
			qs = qs.filter(zone__site__slug=site)
		
		if custom_ad:
			qs = qs.filter(custom_ad__isnull=False)
			
		return qs

	def get_ad(self, *args, **kwargs):
		""" Gets ad from ad_manager, None otherwise """
		qs = self._query_ad(*args, **kwargs)
		if qs.exists():
			return qs[0]
		else:
			return None
			
	def has_ad(self, *args, **kwargs):
		
		""" Doesn't render an ad, just checks for existence in ad manager """
		return self._query_ad(*args, **kwargs).exists()

			
	def get_custom_ad(self, slug, pos, **kwargs):
		""" Gets custom ad code if it exists """
		try:
			custom_ad = Custom_Ad.objects.get(slug=slug)
			return render_custom_ad(pos, custom_ad, **kwargs)
			
		except Custom_Ad.DoesNotExist:
			return ""
			
	
	def render_custom_ad(self, pos, custom_ad, template="dart/embed.html", text_version=False, desc_text="", omit_noscript=False, **kwargs):
		""" Renders the custom ad, determining which template to use based on custom ad settings """
	
		if text_version:
			return custom_ad.text_version
			
		elif custom_ad.embed:
			return custom_ad.embed
		
		elif custom_ad.url:
			t = loader.get_template(template)
			c = Context({
				"pos": pos,
				"link_url": custom_ad.url,
				"image": custom_ad.image,
				"desc_text": desc_text,
                "omit_noscript": omit_noscript,
			})
			return t.render(c)
		else:
			return ""
			
	def render_js_ad(self, pos, template="dart/ad.html", desc_text="", omit_noscript=False, **kwargs):
		""" 
			Renders a DART JS tag to the ad HTML template 
		"""
		
		context_vars = {
			"js_url": self.js_url(pos, **kwargs),
			"link_url": self.link_url(pos, **kwargs),
			"image_url": self.image_url(pos, **kwargs),
			"tile": self.tile,
			"desc_text": desc_text,
			"pos": pos,
            "omit_noscript": omit_noscript,
            "kwargs": kwargs,
		}

		t = loader.get_template(template)
		c = Context(context_vars)
		return t.render(c)
		
		
		
	def render_default(self, pos, custom_only=False, omit_noscript=False, **kwargs):
		"""  
			Renders default ad content, blank or DART javascript,
			depending on settings 
		"""
	
		if self.default_render_js and not custom_only:
			return self.render_js_ad(pos, omit_noscript=omit_noscript, **kwargs)
		else:
			return ""
	
	def render_placeholder(self, ad, **kwargs):
		""" 
			Renders an image placeholder to test ad placements
		"""
		size = ad.position.size_list[0]
		
		context_vars = {
			"js_url": self.js_url(ad.position.slug, **kwargs),
			"pos": ad.position.slug,
			"width": size[0],
			"height": size[1],
            "kwargs": kwargs,
		}

		t = loader.get_template("dart/placeholder.html")
		c = Context(context_vars)
		return t.render(c)
		
	

	def get(self, pos, ad=None, enable_ad_manager=None, omit_noscript=False, **kwargs):
		return self.render_ad(pos, ad, enable_ad_manager, omit_noscript=omit_noscript, **kwargs)
		
	def render_ad(self, pos, ad=None, enable_ad_manager=None, omit_noscript=False, **kwargs):
		""" 
		Main method to display ad code
		
		Configuration variables used in this function
		
			Required:
				pos -- Ad position slug as defined in Zone_Position - string
			
			Optional:
				ad -- A predefined ad, if needed - Ad object
				custom_only -- Only deliver a custom ad, don't use DART - boolean
				enable_ad_manager -- Override Page settings and use the ad manager - boolean
				omit_noscript -- Option to omit noscript tag (for ads without backup images)
	
			
			Standard keywords passed on to template and other functions:
				size -- Limit ads by size, 0x0 is a wildcard - string
				template -- Template used to render the ad, defaults to basic JS embed - filename string
				desc_text -- Text that comes before ad, declaring who the sponsor is - string
				text_version -- Only deliver text version for a custom ad - boolean
		
		"""

		# If kitten mode, just show those ads
		if DART_PLACEHOLDER_MODE:
			ad = self.get_ad(pos, **kwargs)
			if ad:
				return self.render_placeholder(ad, **kwargs)
			else:
				return ""
				
		# If ad manager is disabled, it goes straight to displaying the iframe/js code
		if self.disable_ad_manager and not enable_ad_manager:
			return self.render_default(pos, omit_noscript=omit_noscript, **kwargs)
		else:
		# using the ad manager
			
			# if no ad info, get ad info
			if not ad:
				if enable_ad_manager and not self.page_ads:
					# if ad is not pre-loaded, get the ad from the DB
					ad = self.get_ad(pos, **kwargs)
				elif pos in self.page_ads:
					# get pre-loaded ad
					ad = self.page_ads[pos]
				
			if ad and ad.custom_ad:
				# if we have an ad, and its a custom one
				return self.render_custom_ad(pos, ad.custom_ad, omit_noscript=omit_noscript, **kwargs)
				
			elif ad and not ad.custom_ad:
				# if we have an ad
				if "size" not in kwargs:
					kwargs["size"] = ad.position.size_list_string
				return self.render_js_ad(pos, omit_noscript=omit_noscript, **kwargs)
			else:
				return self.render_default(pos, omit_noscript=omit_noscript, **kwargs)
	
	
	# Methods to format DART URLs
	
	def param_string(self, pos, **kwargs):
		""" 
			Formats the DART URL from a set of keyword arguments and settings 
		
			Attributes are defined in order of explicity
				More explicit overrides more general
				default -> zone attributes -> kwargs

				ad_attributes -- dict of name, value pairs to be passed to DART parameters
				with_ord -- add ord for instances where its not passed by javascript
		"""
		
		attrs = {"size":"0x0"}
		attrs.update(self.ad_attributes)
		if "ad_attributes" in kwargs:
			attrs.update(kwargs["ad_attributes"])
		attrs.update({
			"pos": pos,
		})
		
		# legacy catch in now that size is in ad_attributes
		if "size" in kwargs:
			attrs["size"] = kwargs["size"]
		
		
		zone = kwargs["custom_zone"] if "custom_zone" in kwargs else self.zone
	
		url = "%s/%s;" % (self.site, zone)

		for attr, val in attrs.items():
			if attr == "title":
				continue
			
			elif attr == "size":
			# DART needs size var explicitly spelled 'sz'
				attr = "sz"

			# if it is a non-string iteratible object
			if hasattr(val, "__iter__"):
				val = ",".join(val)
			if attr not in ["size", "sz"]:
				val = slugify(val)
				
			url += "%s=%s;" % (attr, val)
		
		if "with_ord" in kwargs:
			url = u"%sord=%s;" % (url, int(mktime(datetime.now().timetuple())))
		
		return url
		
	def format_path(self, pos, ad_type, **kwargs):
		""" Formats the DART path, without domain, for those instances where that's useful.  Passed to format URL to create the whole ad tag """
		url = self.param_string(pos, **kwargs)

		if self.network_code:
			return "/N%s/%s/%stile=%s;" % (self.network_code, ad_type, url, self.tile)
		else:
			return "/%s/%stile=%s;" % (ad_type, url, self.tile)
			
	def format_url(self, pos, ad_type, **kwargs):
		""" Formats the DART URL from a set of keyword arguments and settings """
		
		path = self.format_path(pos, ad_type, **kwargs)
		
		return "http://%s%s" % (DART_DOMAIN, path)
	
	def js_path(self, pos, **kwargs):
		return self.format_path(pos, "adj", **kwargs)
	
	def js_url(self, pos, **kwargs):
		""" Gets the DART URL for a Javascript ad """
		
		url = self.format_url(pos, "adj", **kwargs)
		
		return url

	def iframe_url(self, pos, **kwargs):
		""" Gets the DART URL for an Iframe ad """
		return self.format_url(pos, "ad", **kwargs)
		
	def image_url(self, pos, **kwargs):
		""" Gets the DART URL for an image src """
		return self.format_url(pos, "ad", **kwargs)
		
	def link_url(self, pos, **kwargs):
		""" Gets the DART URL for a link used in HTML ads """
		return self.format_url(pos, "jump", **kwargs)


