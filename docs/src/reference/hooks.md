## Overview

<p class="intro" markdown>

Prefabricated hooks can be used within your `components.py` to help simplify development.

</p>

!!! abstract "Note"

    Looking for standard React hooks?

    This package only contains Django specific hooks. Standard hooks can be found within [`reactive-python/reactpy`](https://reactpy.dev/docs/reference/hooks-api.html#basic-hooks).

---

## Use Query

This hook is used to execute functions in the background and return the result, typically to [read](https://www.sumologic.com/glossary/crud/) data the Django ORM.

The [default postprocessor](../reference/utils.md#django-query-postprocessor) expects your query function to `#!python return` a Django `#!python Model` or `#!python QuerySet`. The postprocessor needs to be changed to execute other types of queries. Query functions can be sync or async.

=== "components.py"

    ```python
    {% include "../../python/use-query.py" %}
    ```

=== "models.py"

    ```python
    {% include "../../python/example/models.py" %}
    ```

??? example "See Interface"

    <font size="4">**Parameters**</font>

    | Name | Type | Description | Default |
    | --- | --- | --- | --- |
    | `#!python options` | `#!python QueryOptions | None` | An optional `#!python QueryOptions` object that can modify how the query is executed. | `#!python None` |
    | `#!python query` | `#!python Callable[_Params, _Result | None]` | A callable that returns a Django `#!python Model` or `#!python QuerySet`. | N/A |
    | `#!python *args` | `#!python _Params.args` | Positional arguments to pass into `#!python query`. | N/A |
    | `#!python **kwargs` | `#!python _Params.kwargs` | Keyword arguments to pass into `#!python query`. | N/A |

    <font size="4">**Returns**</font>

    | Type | Description |
    | --- | --- |
    | `#!python Query[_Result | None]` | An object containing `#!python loading`/`#!python error` states, your `#!python data` (if the query has successfully executed), and a `#!python refetch` callable that can be used to re-run the query. |

??? question "How can I provide arguments to my query function?"

    `#!python *args` and `#!python **kwargs` can be provided to your query function via `#!python use_query` parameters.

    === "components.py"

        ```python
        {% include "../../python/use-query-args.py" %}
        ```

??? question "How can I customize this hook's behavior?"

    This hook accepts a `#!python options: QueryOptions` parameter that can be used to customize behavior.

    Below are the settings that can be modified via these `#!python QueryOptions`.

    ---

    <font size="4">**`#!python thread_sensitive`**</font>

    Whether to run your synchronous query function in thread-sensitive mode. Thread-sensitive mode is turned on by default due to Django ORM limitations. See Django's [`sync_to_async` docs](https://docs.djangoproject.com/en/dev/topics/async/#sync-to-async) docs for more information.

    This setting only applies to sync query functions, and will be ignored for async functions.

    === "components.py"

        ```python
        {% include "../../python/use-query-thread-sensitive.py" %}
        ```

    ---

    <font size="4">**`#!python postprocessor`**</font>

    {% include-markdown "../../includes/orm.md" start="<!--orm-fetch-start-->" end="<!--orm-fetch-end-->" %}

    However, if you...

    1. Want to use this hook to defer IO intensive tasks to be computed in the background
    2. Want to to utilize `#!python use_query` with a different ORM

    ... then you can either set a custom `#!python postprocessor`, or disable all postprocessing behavior by modifying the `#!python QueryOptions.postprocessor` parameter. In the example below, we will set the `#!python postprocessor` to `#!python None` to disable postprocessing behavior.

    === "components.py"

        ```python
        {% include "../../python/use-query-postprocessor-disable.py" %}
        ```

    If you wish to create a custom `#!python postprocessor`, you will need to create a callable.

    The first argument of `#!python postprocessor` must be the query `#!python data`. All proceeding arguments
    are optional `#!python postprocessor_kwargs` (see below). This `#!python postprocessor` must return
    the modified `#!python data`.

    === "components.py"

        ```python
        {% include "../../python/use-query-postprocessor-change.py" %}
        ```

    ---

    <font size="4">**`#!python postprocessor_kwargs`**</font>

    {% include-markdown "../../includes/orm.md" start="<!--orm-fetch-start-->" end="<!--orm-fetch-end-->" %}

    However, if you have deep nested trees of relational data, this may not be a desirable behavior. In these scenarios, you may prefer to manually fetch these relational fields using a second `#!python use_query` hook.

    You can disable the prefetching behavior of the default `#!python postprocessor` (located at `#!python reactpy_django.utils.django_query_postprocessor`) via the `#!python QueryOptions.postprocessor_kwargs` parameter.

    === "components.py"

        ```python
        {% include "../../python/use-query-postprocessor-kwargs.py" %}
        ```

    _Note: In Django's ORM design, the field name to access foreign keys is [postfixed with `_set`](https://docs.djangoproject.com/en/dev/topics/db/examples/many_to_one/) by default._

??? question "Can I make ORM calls without hooks?"

    {% include-markdown "../../includes/orm.md" start="<!--orm-excp-start-->" end="<!--orm-excp-end-->" %}

??? question "Can I make a failed query try again?"

    Yes, a `#!python use_mutation` can be re-performed by calling `#!python reset()` on your `#!python use_mutation` instance.

    For example, take a look at `#!python reset_event` below.

    === "components.py"

        ```python
        {% include "../../python/use-mutation-reset.py" %}
        ```

    === "models.py"

        ```python
        {% include "../../python/example/models.py" %}
        ```

??? question "Why does the example query function return `#!python TodoItem.objects.all()`?"

    This design decision was based on [Apollo's `#!javascript useQuery` hook](https://www.apollographql.com/docs/react/data/queries/), but ultimately helps avoid Django's `#!python SynchronousOnlyOperation` exceptions.

    With the `#!python Model` or `#!python QuerySet` your function returns, this hook uses the [default postprocessor](../reference/utils.md#django-query-postprocessor) to ensure that all [deferred](https://docs.djangoproject.com/en/dev/ref/models/instances/#django.db.models.Model.get_deferred_fields) or [lazy](https://docs.djangoproject.com/en/dev/topics/db/queries/#querysets-are-lazy) fields are executed.

---

## Use Mutation

This hook is used to modify data in the background, typically to [create/update/delete](https://www.sumologic.com/glossary/crud/) data from the Django ORM.

Mutation functions can `#!python return False` to prevent executing your `#!python refetch` function. All other returns are ignored. Mutation functions can be sync or async.

=== "components.py"

    ```python
    {% include "../../python/use-mutation.py" %}
    ```

=== "models.py"

    ```python
    {% include "../../python/example/models.py" %}
    ```

??? example "See Interface"

    <font size="4">**Parameters**</font>

    | Name | Type | Description | Default |
    | --- | --- | --- | --- |
    | `#!python mutate` | `#!python Callable[_Params, bool | None]` | A callable that performs Django ORM create, update, or delete functionality. If this function returns `#!python False`, then your `#!python refetch` function will not be used. | N/A |
    | `#!python refetch` | `#!python Callable[..., Any] | Sequence[Callable[..., Any]] | None` | A query function (the function you provide to your `#!python use_query` hook) or a sequence of query functions that need a `refetch` if the mutation succeeds. This is useful for refreshing data after a mutation has been performed. | `#!python None` |

    <font size="4">**Returns**</font>

    | Type | Description |
    | --- | --- |
    | `#!python Mutation[_Params]` | An object containing `#!python loading`/`#!python error` states, a `#!python reset` callable that will set `#!python loading`/`#!python error` states to defaults, and a `#!python execute` callable that will run the query. |

??? question "How can I provide arguments to my mutation function?"

    `#!python *args` and `#!python **kwargs` can be provided to your mutation function via #!python mutation.execute` parameters.

    === "components.py"

        ```python
        {% include "../../python/use-mutation-args-kwargs.py" %}
        ```

??? question "How can I customize this hook's behavior?"

    This hook accepts a `#!python options: MutationOptions` parameter that can be used to customize behavior.

    Below are the settings that can be modified via these `#!python MutationOptions`.

    ---

    <font size="4">**`#!python thread_sensitive`**</font>

    Whether to run your synchronous mutation function in thread-sensitive mode. Thread-sensitive mode is turned on by default due to Django ORM limitations. See Django's [`sync_to_async` docs](https://docs.djangoproject.com/en/dev/topics/async/#sync-to-async) docs for more information.

    This setting only applies to sync query functions, and will be ignored for async functions.

    === "components.py"

        ```python
        {% include "../../python/use-mutation-thread-sensitive.py" %}
        ```

??? question "Can I make ORM calls without hooks?"

    {% include-markdown "../../includes/orm.md" start="<!--orm-excp-start-->" end="<!--orm-excp-end-->" %}

??? question "Can I make a failed mutation try again?"

    Yes, a `#!python use_mutation` can be re-performed by calling `#!python reset()` on your `#!python use_mutation` instance.

    For example, take a look at `#!python reset_event` below.

    === "components.py"

        ```python
        {% include "../../python/use-mutation-reset.py" %}
        ```

    === "models.py"

        ```python
        {% include "../../python/example/models.py" %}
        ```

??? question "Can `#!python use_mutation` trigger a refetch of `#!python use_query`?"

    Yes, `#!python use_mutation` can queue a refetch of a `#!python use_query` via the `#!python refetch=...` argument.

    The example below is a merge of the `#!python use_query` and `#!python use_mutation` examples above with the addition of a `#!python use_mutation(refetch=...)` argument.

    Please note that `refetch` will cause all `#!python use_query` hooks that use `#!python get_items` in the current component tree will be refetched.

    === "components.py"

        ```python
        {% include "../../python/use-mutation-query-refetch.py" %}
        ```

    === "models.py"

        ```python
        {% include "../../python/example/models.py" %}
        ```

---

## Use Connection

This hook is used to fetch the active connection, which is either a Django [WebSocket](https://channels.readthedocs.io/en/stable/topics/consumers.html#asyncjsonwebsocketconsumer) or a [HTTP Request](https://docs.djangoproject.com/en/4.2/ref/request-response/#django.http.HttpRequest).

=== "components.py"

    ```python
    {% include "../../python/use-connection.py" %}
    ```

??? example "See Interface"

    <font size="4">**Parameters**</font>

    `#!python None`

    <font size="4">**Returns**</font>

    | Type | Description |
    | --- | --- |
    | `#!python Connection` | The component's `WebSocket` or `HttpRequest`. |

---

## Use Scope

This is a shortcut that returns the WebSocket or HTTP [scope](https://channels.readthedocs.io/en/stable/topics/consumers.html#scope).

=== "components.py"

    ```python
    {% include "../../python/use-scope.py" %}
    ```

??? example "See Interface"

    <font size="4">**Parameters**</font>

    `#!python None`

    <font size="4">**Returns**</font>

    | Type | Description |
    | --- | --- |
    | `#!python MutableMapping[str, Any]` | The WebSocket's `#!python scope`. |

---

## Use Location

This is a shortcut that returns the client's URL `#!python path`.

You can expect this hook to provide strings such as `/reactpy/my_path`.

=== "components.py"

    ```python
    {% include "../../python/use-location.py" %}
    ```

??? example "See Interface"

    <font size="4">**Parameters**</font>

    `#!python None`

    <font size="4">**Returns**</font>

    | Type | Description |
    | --- | --- |
    | `#!python Location` | An object containing the current URL's `#!python pathname` and `#!python search` query. |

??? info "This hook's behavior will be changed in a future update"

    This hook will be updated to return the browser's currently active HTTP path. This change will come in alongside ReactPy URL routing support.

    Check out [reactive-python/reactpy-django#147](https://github.com/reactive-python/reactpy-django/issues/147) for more information.

---

## Use Origin

This is a shortcut that returns the client's `#!python origin`.

You can expect this hook to provide strings such as `http://example.com`.

=== "components.py"

    ```python
    {% include "../../python/use-origin.py" %}
    ```

??? example "See Interface"

    <font size="4">**Parameters**</font>

    `#!python None`

    <font size="4">**Returns**</font>

    | Type | Description |
    | --- | --- |
    | `#!python str | None` | A string containing the browser's current origin, obtained from WebSocket or HTTP headers (if available). |
