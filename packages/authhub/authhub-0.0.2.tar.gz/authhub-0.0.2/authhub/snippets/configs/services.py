''' Services Configuration File '''

import os

AUTH_PROVIDERS = {
    'github': {
        'client': os.environ.get('GITHUB_CLIENT'),
        'secret': os.environ.get('GITHUB_SECRET'),
        'redirect': os.environ.get('GITHUB_REDIRECT'),
        'driver': 'authhub.providers.GitHubDriver.GitHubDriver'
    }
}
