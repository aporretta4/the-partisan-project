from pathlib import Path
from django import template
from django_project.settings import BASE_DIR
import os
from glob import glob

register = template.Library()

def get_directory_files(dir):
  found_files = []
  for path, subdirs, files in os.walk(dir):
    for name in files:
      found_files.append(os.path.join(path, name))
  return found_files

def cachebust_url(resource_path):
  cached_path = resource_path
  static_files = get_directory_files(str(BASE_DIR) + '/partisan/static/' + '/'.join(Path(resource_path[1:]).parts[:-1]))
  for static_file in static_files:
    if os.path.isfile(static_file):
      if static_file.find('___') != -1:
        path_without_cache = static_file[0:static_file.find('___')] + static_file[static_file.find('.'):]
        path_without_cache = path_without_cache.replace(str(BASE_DIR) + '/partisan/static', '')
        if resource_path == path_without_cache:
          cached_path = '/static/' + '/'.join(Path(resource_path[1:]).parts[:-1]) + '/' + Path(static_file).name
          break
  return cached_path

register.filter(name='cachebust_url', filter_func=cachebust_url)