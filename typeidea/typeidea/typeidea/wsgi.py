"""
WSGI config for typeideas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

import sys


from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'typeidea.settings')

# 区分环境，即开发环境使用develop.py的配置，线上环境使用product.py的配置
profile = os.environ.get('TYPEIDEA_PROFILE', 'develop')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "typeidea.settings.%s" % profile)

application = get_wsgi_application()
