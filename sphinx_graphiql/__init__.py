from __future__ import absolute_import

from .sphinx_graphiql import SphinxGraphiQL

def setup(app):
    app.add_directive('graphiql', SphinxGraphiQL)

    return {'parallel_read_safe': True,
            'parallel_write_safe': True}
