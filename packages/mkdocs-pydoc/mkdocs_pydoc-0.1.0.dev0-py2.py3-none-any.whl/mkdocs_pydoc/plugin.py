import io
import logging

from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type
from mkdocs.utils import string_types

from .parser import parse

log = logging.getLogger('mkdocs.pydev')


class PydocPlugin(BasePlugin):
    '''
    A MkDocs plugin extracting Python documentation from docstrings
    '''
    EXTENSION = '.pydoc'

    config_scheme = (
        ('syntax', Type(string_types, default='sphinxdoc')),
    )

    def on_page_read_source(self, item, page=None, **kwargs):
        '''
        Extract markdown node listing a *.pydoc files
        '''
        if not page.input_path.endswith(self.EXTENSION):
            return
        log.info('read page: %s', page.input_path)
        with io.open(page.abs_input_path) as f:
            specs = f.readlines()

        return '\n'.join(parse(spec) for spec in specs)
