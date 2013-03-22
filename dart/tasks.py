import httplib, re
from django.conf import settings
from dart.models import Zone, Zone_Position, DART_DOMAIN, Ad_Page
import settings, time


# String used to define a browser when making DART requests from a commandline
DEFAULT_BROWSER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:8.0.1) Gecko/20100101 Firefox/8.0.1"


def dart_sync(zones=None, debug_mode=False, clear_cache_command="", *args, **kwargs):
	""" 
	Loops through all zones and positions and get's their status in doubleclick
	then updates the local database with the result.
	
	If zone value is passed, then it only loops through that custom list of zones
	"""
	
	clear_cache_flag = False
	
	if not zones:
		zones = Zone.objects.all()

	for zone in zones:
		positions = zone.zone_position_set.filter(sync=True)
		for position in positions:
			clear_cache_flag = _dart_sync_zone_position(zone, position, debug_mode, clear_cache_command)
			
		time.sleep(1)
		
	if clear_cache_command and clear_cache_flag:
		exec clear_cache_command
		
	return True



def _dart_sync_zone_position(zone, position, debug_mode, clear_cache_command, *args, **kwargs):
	clear_cache_flag = False

	size = position.position.size_list_string
	pos = position.position.slug
	
	ad_page = Ad_Page(zone=zone.slug, *args, **kwargs)
	
	# Loop through all of the sites the zone is enabled for, and get the ad tag for each
	temp_site = ""
	
	for site in zone.site.all():
		if settings.DEBUG:
			site = site.slug_dev
		else:
			site = site.slug
		
		# A quick check to make sure the same site isn't being checked twice
		if site != temp_site:
			ad_page.site = site
			temp_site = site

			url = ad_page.js_url(pos, with_ord=True, size=size, ) 
			
			if debug_mode: print url
			
			res = dart_request(url, *args, **kwargs)
			
			#if settings.DEBUG: print u"Status:%s" % res.status
			if res.status == 200:
				response = res.read()
				
				previous_enabled = position.enabled
				
				if _dart_has_ad(response, debug_mode):
					position.enabled = True
				else:
					position.enabled = False

				# check if the value has changed
				if previous_enabled != position.enabled:
					position.save()
					clear_cache_flag = True
				else:
					clear_cache_flag = False
						
	return clear_cache_flag
	
def _dart_has_ad(response, debug_mode, *args, **kwargs):
	if re.search(r"grey\.gif", response) or response.strip() == "document.write('');":
		if debug_mode: print "Position: disabled"
		return False
	else:
		if debug_mode: print "Position: enabled"
		return True
			
		
def dart_request(url, user_agent=DEFAULT_BROWSER_AGENT, domain=DART_DOMAIN, *args, **kwargs):
	""" 
	Makes a single HTTP request of a DART tag to DART 
	server mimicking a browser request 
	"""
	conn = httplib.HTTPConnection(domain)
	conn.request(
		"GET",
		url,
		headers={
			"Referer": settings.SITE_URL, 
			"User-Agent": user_agent
		}
	)
	
	return conn.getresponse()
	
def dart_publish_scheduled_ads():
	"""
	Enables all ads set to publish in the future that aren't being synced with DART
	"""
	Zone_Position.objects.filter(enabled=False, date_published__lte=datetime.date.today(), sync=False).update(enabled=True)


