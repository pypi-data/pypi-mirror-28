# -*- coding: utf-8 -*-

import time
from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings
from django.utils.html import mark_safe
from django.core.exceptions import ImproperlyConfigured
from cent.core import generate_token
from instant.apps import HANDLERS

DEBUG = False

try:
    SECRET_KEY = getattr(settings, 'CENTRIFUGO_SECRET_KEY')
except ImportError:
    raise ImproperlyConfigured(
        u"The Centrifugo secret key must be set in settings.py with CENTRIFUGO_SECRET_KEY")
SITE_SLUG = getattr(settings, 'SITE_SLUG', 'site')
CENTRIFUGO_HOST = getattr(settings, 'CENTRIFUGO_HOST', 'http://localhost')
CENTRIFUGO_PORT = getattr(settings, 'CENTRIFUGO_PORT', 8001)

APPS = getattr(settings, 'INSTANT_APPS', [])

public_channel = SITE_SLUG + '_public'
PUBLIC_CHANNEL = getattr(settings, 'INSTANT_PUBLIC_CHANNEL', public_channel)
ENABLE_PUBLIC_CHANNEL = getattr(
    settings, 'INSTANT_ENABLE_PUBLIC_CHANNEL', True)
ENABLE_STAFF_CHANNEL = getattr(settings, 'INSTANT_ENABLE_STAFF_CHANNEL', False)
ENABLE_USERS_CHANNEL = getattr(settings, 'INSTANT_ENABLE_USERS_CHANNEL', False)
ENABLE_SUPERUSER_CHANNEL = getattr(
    settings, 'INSTANT_ENABLE_SUPERUSER_CHANNEL', False)
EXCLUDE = getattr(settings, 'INSTANT_EXCLUDE', ["__presence__"])

PUBLIC_CHANNELS = getattr(settings, 'INSTANT_PUBLIC_CHANNELS', ())
USERS_CHANNELS = getattr(
    settings, 'INSTANT_USERS_CHANNELS', ())
STAFF_CHANNELS = getattr(settings, 'INSTANT_STAFF_CHANNELS', ())
SUPERUSER_CHANNELS = getattr(settings, 'INSTANT_SUPERUSER_CHANNELS', ())
USERS_CHANNELS = getattr(settings, 'INSTANT_USERS_CHANNELS', ())

# javascript debug messages
debug_mode = getattr(settings, 'INSTANT_DEBUG', False)
if debug_mode is True:
    DEBUG_MODE = "true"
else:
    DEBUG_MODE = "false"

register = template.Library()


@register.simple_tag
def get_centrifugo_url():
    return CENTRIFUGO_HOST + ":" + str(CENTRIFUGO_PORT)


@register.simple_tag
def debug_mode():
    return DEBUG_MODE


@register.simple_tag
def get_timestamp():
    return str(int(time.time()))


@register.simple_tag
def mq_generate_token(user, timestamp, info=""):
    token = generate_token(SECRET_KEY, user, timestamp, info)
    return token


@register.simple_tag
def public_channel_is_on():
    return ENABLE_PUBLIC_CHANNEL


@register.simple_tag
def get_public_channel():
    return PUBLIC_CHANNEL


@register.simple_tag
def is_users_channel():
    return ENABLE_USERS_CHANNEL


@register.simple_tag
def get_users_channel():
    return '$' + SITE_SLUG + '_users'


@register.simple_tag
def is_staff_channel():
    return ENABLE_STAFF_CHANNEL


@register.simple_tag
def get_staff_channel():
    return '$' + SITE_SLUG + '_staff'


@register.simple_tag
def is_superuser_channel():
    return ENABLE_SUPERUSER_CHANNEL


@register.simple_tag
def get_superuser_channel():
    return '$' + SITE_SLUG + '_admin'


@register.simple_tag
def get_channels(path, level):
    chanconf = []
    if level == "superuser":
        chanconf = SUPERUSER_CHANNELS
    elif level == "staff":
        chanconf = STAFF_CHANNELS
    elif level == "users":
        chanconf = USERS_CHANNELS
    elif level == "public":
        chanconf = PUBLIC_CHANNELS
    lastchar = path[-1:]
    if lastchar == "/":
        path = path[:-1]
    chans = []
    for chantup in chanconf:
        print(chantup)
        chan = chantup[0]
        chanpaths = []
        if len(chantup) == 1:
            chans.append(chan)
            continue
        else:
            chanpaths = chantup[1]
            for chanpath in chanpaths:
                if chanpath == path:
                    chans.append(chan)
    return chans


@register.simple_tag
def get_handlers_url(chan):
    global HANDLERS
    if chan in HANDLERS:
        url = "instant/handlers/" + chan + ".js"
    else:
        url = "instant/handlers/default.js"
    name = chan.replace("$", "")
    return [url, name]


@register.simple_tag
def get_apps():
    return APPS


@register.filter
@stringfilter
def is_in_apps(app):
    if app in APPS:
        return True
    else:
        return False


@register.simple_tag
def get_default_channels():
    channels = []
    if ENABLE_PUBLIC_CHANNEL is True:
        channels.append(PUBLIC_CHANNEL)
    if ENABLE_STAFF_CHANNEL is True:
        c = '$' + SITE_SLUG + '_staff'
        channels.append(c)
    if ENABLE_USERS_CHANNEL is True:
        c = '$' + SITE_SLUG + '_users'
        channels.append(c)
    if ENABLE_SUPERUSER_CHANNEL is True:
        c = '$' + SITE_SLUG + '_admin'
        channels.append(c)
    return channels


@register.simple_tag
def exclude_chans():
    chans = []
    for chan in EXCLUDE:
        chans.append('"' + chan + '"')
    return mark_safe(",".join(chans))


@register.simple_tag
def num_excluded_chans():
    return len(EXCLUDE)
