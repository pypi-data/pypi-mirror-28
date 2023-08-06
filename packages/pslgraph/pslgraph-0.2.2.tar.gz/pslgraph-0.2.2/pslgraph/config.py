import d3m_metadata.metadata

D3M_API_VERSION = '2018.1.26'
VERSION = '0.2.2'
TAG_NAME = ''

REPOSITORY = 'https://gitlab.datadrivendiscovery.org/dhartnett/psl'
PACAKGE_NAME = 'pslgraph'

# D3M_PERFORMER_TEAM = 'SRI-UCSC'
D3M_PERFORMER_TEAM = 'SRI'

PACKAGE_URI = ''
if TAG_NAME:
    PACKAGE_URI = "git+%s@%s" % (REPOSITORY, TAG_NAME)
else:
    PACKAGE_URI = "git+%s" % (REPOSITORY)

PACKAGE_URI = "%s#egg=%s" % (PACKAGE_URI, PACAKGE_NAME)

INSTALLATION = {
    'type' : d3m_metadata.metadata.PrimitiveInstallationType.PIP,
    'package': PACAKGE_NAME,
    'version': VERSION
}
