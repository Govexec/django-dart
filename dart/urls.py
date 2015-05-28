from coffin.conf.urls import patterns, url

urlpatterns = patterns("dart.views",

	url(r"template/(?P<template_id>\d+)/?$", "custom_ad_template_ajax"),

	url(r'^(?P<ad_url>\S+)$', 'ad'),	

)
