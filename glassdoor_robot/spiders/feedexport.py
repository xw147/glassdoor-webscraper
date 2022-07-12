'''
Created on 12 Jul 2022

@author: haha
'''


"""
The standard CSVItemExporter class does not pass the kwargs through to the
CSV writer, resulting in EXPORT_FIELDS and EXPORT_ENCODING being ignored
(EXPORT_EMPTY is not used by CSV).
"""

from scrapy.utils.project import get_project_settings
SETTINGS = get_project_settings()

from scrapy.exporters import CsvItemExporter

class CSVkwItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        kwargs['fields_to_export'] = SETTINGS.getlist('EXPORT_FIELDS') or None
        kwargs['encoding'] = SETTINGS.get('EXPORT_ENCODING', 'utf-8')

        super(CSVkwItemExporter, self).__init__(*args, **kwargs)