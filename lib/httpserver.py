# Python standard library modules
import os

# 3rd party modules
from Cheetah.Template import Template
from twisted.internet import reactor
from twisted.web import server, resource


class RootHandler(resource.Resource):
    isLeaf = True

    def __init__(self, results, config):
        self.results = results
        self.config = config
        resource.Resource.__init__(self)

    def render_GET(self, request):
        template_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'templates',
            'status_page.tmpl',
        )
        rendered_data = Template(
            file=template_path,
            searchList=[{'results': self.results}],
        )

        request.setResponseCode(200 if self.results['all_ok'] else 500)
        request.setHeader('server', 'HealthReporter')

        return str(rendered_data)


def run_server(results, config):
    root = resource.Resource()
    root.putChild('', RootHandler(results, config))

    site = server.Site(root)
    reactor.listenTCP(
        port=config['bind_port'],
        factory=site,
        interface=config['bind_address'],
    )
    reactor.run()
