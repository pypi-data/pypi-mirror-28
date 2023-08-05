from pathlib import Path

import yaml
from django.utils.text import slugify

from drf_apitests.exception import ValidationError


class APITestSuite:
    def __init__(self, top_dir, start_dir, pattern='api/tests/*.yaml',
                 base_url='/api/v1'):
        self.top_dir = Path(top_dir)
        self.start_dir = Path(start_dir)
        self.pattern = pattern
        self.base_url = base_url

    def discover(self):
        path = self.top_dir.joinpath(self.start_dir)
        iterable = path.rglob(self.pattern)
        for file in sorted(iterable):
            yield APITestDocument.from_yaml(self, file, self.top_dir)


class APITestDocument:
    def __init__(self, parent, module, filename, name, auth, fixtures, skip):
        self.parent = parent
        self.module = module
        self.filename = filename
        self.name = name
        self.auth = auth
        self.fixtures = fixtures
        self.skip = skip
        self.tests = []

    def __repr__(self):
        return f'<APITestDocument: {self.module}.{self.filename}>'

    @classmethod
    def from_yaml(cls, parent, file, top_dir):
        file = Path(file)
        module = '.'.join(file.parent.relative_to(top_dir).parts)
        with file.open('rt') as f:
            mapping = yaml.load(f)
        return cls.validate(parent, module, file.stem, mapping)

    @classmethod
    def validate(cls, parent, module, filename, mapping):
        if 'name' not in mapping:
            raise ValidationError('name is required')
        if 'tests' not in mapping:
            raise ValidationError('tests is required')
        name = mapping['name']
        tests = mapping['tests']
        auth = mapping.get('auth')
        fixtures = mapping.get('fixtures', [])
        skip = mapping.get('skip', [])
        doc = cls(parent, module, filename, name, auth, fixtures, skip)
        doc.tests = [APITestCase.validate(doc, test) for test in tests]
        return doc


class APITestCase:
    def __init__(self, parent, name, url, url_vars, method, params, skip):
        self.parent = parent
        self.name = name
        self.url = url
        self.url_vars = url_vars
        self.method = method
        self.params = params
        self.skip = skip
        self.slug = slugify(name).replace('-', '_')
        assert self.method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE'), \
            f"invalid method '{self.method}'"

    def __repr__(self):
        if self.parent:
            module_filename = f'{self.parent.module}.{self.parent.filename}'
            return f'<APITestCase: {module_filename}:{self.slug}>'
        else:
            return f'<APITestCase: {self.slug}>'

    @classmethod
    def validate(cls, parent, mapping):
        if 'name' not in mapping:
            raise ValidationError('name is required')
        if 'url' not in mapping:
            raise ValidationError('url is required')
        if 'method' not in mapping:
            raise ValidationError('method is required')
        name = mapping['name']
        url = mapping['url']
        url_vars = mapping.get('url-vars', {})
        # TODO: test url_vars + url
        method = mapping['method']
        params = mapping.get('params', {})
        skip = mapping.get('skip', [])
        # TODO: test types
        return cls(parent, name, url, url_vars, method, params, skip)

    @property
    def full_url(self):
        return self.parent.parent.base_url + self.url

    @property
    def interpolated_url(self):
        url = self.full_url
        for key, value in self.url_vars.items():
            url = url.replace(':' + key, str(value))
        return url
