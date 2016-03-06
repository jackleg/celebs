#!/usr/bin/env python
# -*- coding: utf8 -*-


import sys
import os.path
import django


def import_django():
	"""django 설정을 외부에서도 사용할 수 있도록 import하는 과정"""

	# DJANGO_SETTINGS_MODUL 환경변수에 setting.py 위치 설정
	pkg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, 'django_server')
	sys.path.append(pkg_path)
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_server.settings')

	django.setup()
