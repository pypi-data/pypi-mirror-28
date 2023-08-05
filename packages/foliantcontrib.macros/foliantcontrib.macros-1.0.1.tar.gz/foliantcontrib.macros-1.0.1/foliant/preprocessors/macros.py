import re

from foliant.preprocessors.base import BasePreprocessor


class Preprocessor(BasePreprocessor):
    defaults = {
        'macros': {}
    }
    tags = 'macro',

    _param_delimiters = r' |,\s*|;\s*'

    def process_macros(self, content: str) -> str:
        '''Replace macros with content defined in the config.

        :param content: Markdown content

        :returns: Markdown content without macros
        '''

        def _sub(macro):
            options = self.get_options(macro.group('options'))

            name = options['name']

            params = [
                param
                for param in re.split(self._param_delimiters, options.get('params', ''))
                if param
            ]

            return self.options['macros'].get(name, '').format(*params)

        return self.pattern.sub(_sub, content)

    def apply(self):
        for markdown_file_path in self.working_dir.rglob('*.md'):
            with open(markdown_file_path, encoding='utf8') as markdown_file:
                content = markdown_file.read()

            with open(markdown_file_path, 'w', encoding='utf8') as markdown_file:
                markdown_file.write(self.process_macros(content))
