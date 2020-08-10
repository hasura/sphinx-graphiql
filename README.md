# Sphinx GraphiQL

This is a GraphiQL plugin for Sphinx that lets you make GraphQL queries from your docs.


## Build

```bash
python3 setup.py sdist
```

## Publish

Make sure you have installed twine

```bash
python3 -m pip install --user --upgrade twine
```

Make suer you have a ~/.pypirc config setup

```bash
[distutils]
 index-servers =
   nexus
 
 [nexus]
 repository: http://docker-registry.ontotext.com/repository/pypi-repo/
 username: kim-user
 password: ************
```

```bash
twine upload -r nexus dist/ontotext_sphinx_graphiql-0.0.4.tar.gz --verbose  
```

## Usage

To insert a GraphiQL component inside your `.rst` doc, use the declarative:

```rst
.. graphiql::
   :query:
      query {
         author {
            id
            name
         }
      }
```

### View only

If you want to make GraphiQL view-only (ie: disable execution), you just have to add another option `:view_only:`. For example:

```rst
.. graphiql::
   :view_only:
   :query:
      query {
         author {
            id
            name
         }
      }
```

### Show a dummy response

Sometimes you will want to show the response along with the query without executing it. You can do that by adding a `:response:` option.

```rst
.. graphiql::
   :view_only:
   :query:
      query {
         author {
            id
            name
         }
      }
   :response:
      {
         "data": {
            "author": [
               {
                  "id": 1
                  "name": "Justin",
               },
               {
                  "id": 2
                  "name": "Beltran",
               },
               {
                  "id": 3
                  "name": "Sidney",
               }
           ]
        }
     }
```

### Custom endpoint

By default, the GraphQL endpoint is picked up from an environment variable as described [here](#default-graphql-endpoint). 
In case you want to explicitly set an endpoint for a query, you can do so by adding an `:endpoint:` option.

```rst
.. graphiql::
   :endpoint: http://localhost:8080/v1/graphql
   :query:
      query {
         author {
            id
            name
         }
      }
```

### JWT Token

It is possible to add a JWT token to the Authorization header used within GraphQL requests
from the GraphiQL widget

```rst
.. graphiql::
   :token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFCcFNNSzJNdENTck0zS3FxWERnTWhNMVhVY0V3ZDNLIn0.eyJhdWQiOiI2NzJjYTdiMy1jMzcyLTRkZjMtODJkOC05YTFhMGQ3ZDY4YzEiLCJleHAiOjE2NTA1OTUwNzksImlhdCI6MTU4NzQ4MTE3NSwiaXNzIjoic3dhcGktcGxhdGZvcm0ub250b3RleHQuY29tIiwic3ViIjoiNDAwZmNjODAtZGZhZS00NmQ3LWFiNWMtNjQ1NzQ3OTk4MWRmIiwiYXV0aGVudGljYXRpb25UeXBlIjoiUEFTU1dPUkQiLCJlbWFpbCI6ImRyb2lkaHV0dHJlYWRAZXhhbXBsZS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicHJlZmVycmVkX3VzZXJuYW1lIjoiZHJvaWRodXR0cmVhZCIsImFwcGxpY2F0aW9uSWQiOiI2NzJjYTdiMy1jMzcyLTRkZjMtODJkOC05YTFhMGQ3ZDY4YzEiLCJyb2xlcyI6WyJEcm9pZEh1dHRSZWFkIiwiU2NoZW1hUkJBQ0FkbWluIl19.GO1PYegUgc1u79l2jBK1_fqK-jcxDLxjo8A2F7IH-qE
   :query:
      query {
         author {
            id
            name
         }
      }
```

## Installation

### Step 1: Install the plugin

```bash
$ pip install sphinx_graphiql
```

### Step 2: Mention the plugin as an extension in `conf.py`

You might be using other extensions in your docs. Append `sphinx_graphiql` to the list of extensions.

```
extensions.append('sphinx_graphiql')
```

### Step 3: Add the required scripts to your template HTML

Add the following tags inside the `<head></head>` of your template html file (typically `layout.html`).

```html

<!-- GraphiQL -->
<script src="https://cdn.jsdelivr.net/react/15.4.2/react.min.js"></script>
<script src="https://cdn.jsdelivr.net/react/15.4.2/react-dom.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/jazzyray/sphinx-graphiql@master/static/graphiql/graphiql.min.js"></script>
<link href="https://cdn.jsdelivr.net/gh/jazzyray/sphinx-graphiql@master/static/graphiql/graphiql.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/gh/jazzyray/sphinx-graphiql@master/static/styles.css" rel="stylesheet">
<script type="text/javascript">
  // graphql query fetcher
  const graphQLFetcher = function(endpoint, token, insecure) {
    endpoint = endpoint || "https://swapi-platform.ontotext.com/graphql";
    insecure = insecure || false
    return function(graphQLParams) {
      const params = {
        method: 'post',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(graphQLParams),
        credentials: 'include',
        insecure: true,
      };
      return fetch(endpoint, params)
        .then(function (response) {
          return response.text();
        })
        .then(function (responseBody) {
          try {
            return JSON.parse(responseBody);
          } catch (error) {
            return responseBody;
          }
        });
    }
  };
  // create GraphiQL components and embed into HTML
  const setupGraphiQL = function() {
    if (typeof(React) === 'undefined' || typeof(ReactDOM) === 'undefined' || typeof(GraphiQL) === 'undefined') {
      return;
    }
    const targets = document.getElementsByClassName('graphiql');
    for (let i = 0; i < targets.length; i++) {
      const target = targets[i];
      const endpoint = target.getElementsByClassName("endpoint")[0].innerHTML.trim();
      const token = target.getElementsByClassName("token")[0].innerHTML.trim();
      const insecure = target.getElementsByClassName("insecure")[0].innerHTML.trim();
      const query = target.getElementsByClassName("query")[0].innerHTML.trim();
      const response = target.getElementsByClassName("response")[0].innerHTML.trim();
      const graphiQLElement = React.createElement(GraphiQL, {
        fetcher: graphQLFetcher(endpoint, token, insecure),
        schema: undefined,
        query: query,
        response: response,
        token: token
      });
      ReactDOM.render(graphiQLElement, target);
    }
  };
                                       
  // if graphiql elements present, setup graphiql
  if (document.getElementsByClassName('graphiql').length > 0) {
    setupGraphiQL();
  }
</script>
```

> You can find these tags at `static/static.html` of the root directory.

## Configuration

### Default GraphQL Endpoint

You have to set the GraphQL endpoint as an environment variable in your sphinx configuration file (typically `conf.py` at the root your your project).

For example:

```python
GRAPHIQL_DEFAULT_ENDPOINT = "https://graphql.my-graphql-app.io/v1/graphql"
```

### Auto-completion

GraphiQL uses the GraphQL schema to auto complete as you type in queries and mutations.

If your GraphQL endpoint supports introspection, just pass `undefined` as the schema variable and 
auto-completion will work out of the box.

```js

const graphiQLElement = React.createElement(GraphiQL, {
  fetcher: graphQLFetcher(endpoint),
  schema: undefined, // the schema will be fetched using introspection
  query: query,
  response: response
});
```