import re
from os import getenv

from foliant.preprocessors.base import BasePreprocessor


class Preprocessor(BasePreprocessor):
    defaults = {
        'flags': []
    }
    tags = 'if',

    _flags_envvar = 'FOLIANT_FLAGS'
    _flag_delimiters = r' |,\s*|;\s*'

    def process_flagged_blocks(self, content: str) -> str:
        '''Replace flagged blocks either with their contents or nothing, depending on the value
        of ``FOLIANT_FLAGS`` environment variable and ``flags`` config value.

        :param content: Markdown content

        :returns: Markdown content without flagged blocks
        '''

        def _sub(flagged_block):
            options = self.get_options(flagged_block.group('options'))

            required_flags = {
                flag.lower()
                for flag in re.split(self._flag_delimiters, options.get('flags', ''))
                if flag
            } | {
                f'target:{target.lower()}'
                for target in re.split(self._flag_delimiters, options.get('targets', ''))
                if target
            } | {
                f'backend:{backend.lower()}'
                for backend in re.split(self._flag_delimiters, options.get('backends', ''))
                if backend
            }

            env_flags = {
                flag.lower()
                for flag in re.split(self._flag_delimiters, getenv(self._flags_envvar, ''))
                if flag
            }

            config_flags = {flag.lower() for flag in self.options['flags']}

            set_flags = env_flags \
                | config_flags \
                | {f'target:{self.context["target"]}', f'backend:{self.context["backend"]}'}

            kind = options.get('kind', 'all')

            if (kind == 'all' and required_flags <= set_flags) \
                or (kind == 'any' and required_flags & set_flags) \
                or (kind == 'none' and not required_flags & set_flags):
                return flagged_block.group('body').strip()

            else:
                return ''

        return self.pattern.sub(_sub, content)

    def apply(self):
        for markdown_file_path in self.working_dir.rglob('*.md'):
            with open(markdown_file_path, encoding='utf8') as markdown_file:
                content = markdown_file.read()

            with open(markdown_file_path, 'w', encoding='utf8') as markdown_file:
                markdown_file.write(self.process_flagged_blocks(content))
