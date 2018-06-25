# Sphinx GraphiQL

This is a GraphiQL plugin for Sphinx that lets you make GraphQL queries from your docs.

We built this for documenting our [graphql engine](https://hasura.io/) queries. Check it out in action [here](https://docs.hasura.io/0.15/graphql/manual/queries/nested-object-queries.html).

![example](https://raw.githubusercontent.com/hasura/sphinx_graphiql/master/assets/sphinx-graphiql-example.png)


## Usage

To insert a GraphiQL component inside your `.rst` doc, use the declarative:

```
.. graphiql::
   :query:
        query {
            author(order_by: ["-name"]) {
            		name
            }
        }
```

### Read only

If you want to make GraphiQL read-only, you just have to add another option `:view_only:`. For example:

```
.. graphiql::
   :view_only:
   :query:
        query {
            author(order_by: ["-name"]) {
            		name
            }
        }
```

### Template with a dummy response

Sometimes you will want to show the response along with the query. You can do that by adding a `:response:` option. This is useful when you want syntax highlighting for GraphQL which is not yet supported by Sphinx.

```
.. graphiql::
   :view_only: true
   :query:
        mutation insert_article {
            insert_article (
                objects: [
                    {
                        title: "Article 1",
                        content: "Sample article content",
                        author_id: 3
                    }
                ]
            )
            {
                returning {
                  id
                  title
                }
            }
        }
   :response:
        {
            "data": {
                "insert_article": {
                    "affected_rows": 1,
                    "returning": [
                        {
                          "id": 102,
                          "title": "Article 1"
                        }
                    ]
                }
            }
        }

```

## Installation

### Step 1: Install the plugin

```bash
$ pip install sphinx_graphiql
```

### Step 2: Mention the plugin as an extension in `conf.py`

You might be using other extensions in your docs. Just append `sphinx_graphiql` to the list of extensions.

```
extension.append('sphinx_graphiql')
```

### Step 3: Add appropriate scripts to your template HTML

Just add the following tags inside the `<head></head>` of your template html file.

```html

<script src="//cdn.jsdelivr.net/react/15.4.2/react.min.js"></script>
<script src="//cdn.jsdelivr.net/react/15.4.2/react-dom.min.js"></script>
<script src="https://rawgit.com/hasura/sphinx_graphiql/master/static/graphiql/graphiql.min.js"></script>
<link href="https://rawgit.com/hasura/sphinx_graphiql/master/static/graphiql/graphiql.css" rel="stylesheet">
<link href="https://rawgit.com/hasura/sphinx_graphiql/master/static/styles.css" rel="stylesheet">
<script type="text/javascript">
  // graphiql
  // graphql query fetcher
  const graphQLFetcher = function(endpoint) {
    endpoint = endpoint || "{{ GRAPHIQL_DEFAULT_ENDPOINT }}";
    return function(graphQLParams) {
      const params = {
        method: 'post',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(graphQLParams),
        credentials: 'include'
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
      const query = target.getElementsByClassName("query")[0].innerHTML.trim();
      const response = target.getElementsByClassName("response")[0].innerHTML.trim();
      const graphiQLElement = React.createElement(GraphiQL, {
        fetcher: graphQLFetcher(endpoint),
        schema: null, // Introspects schema from endpoint by default. Pass schema if introspection not supported
        query: query,
        response: response
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

### GraphQL Endpoint

You have to set the GraphQL endpoint as an environment variable in your sphinx configuration file (typically `conf.py` at the root your your project).

For example:

```python
GRAPHIQL_DEFAULT_ENDPOINT = "https://graphql.accountat35.hasura-app.io/v1alpha1/graphql"
```

### Auto-completion

GraphiQL uses the GraphQL schema to auto complete as you type in queries and mutations.

If your GraphQL endpoint supports introspection, auto-completion will work out of the box. However, if your endpoint does not support introspection, you can pass the schema prop to the GraphiQL element in the [script](#add-appropriate-scripts-to-your-template-html).

```js

const graphiQLElement = React.createElement(GraphiQL, {
  fetcher: graphQLFetcher(endpoint),
  schema: schemaObj, // Required only if the endpoing does not support introspection
  query: query,
  response: response
});
```
