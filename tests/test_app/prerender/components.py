from time import sleep

import reactpy_django
from reactpy import component, html


@component
def prerender_string():
    scope = reactpy_django.hooks.use_scope()

    sleep(0.5)
    return (
        "prerender_string: Fully Rendered"
        if scope.get("type") == "websocket"
        else "prerender_string: Prerendered"
    )


@component
def prerender_vdom():
    scope = reactpy_django.hooks.use_scope()

    if scope.get("type") == "http":
        return html.div("prerender_vdom: Prerendered")

    return html.div("prerender_vdom: Fully Rendered")


@component
def prerender_component():
    scope = reactpy_django.hooks.use_scope()

    @component
    def inner(value):
        return html.div(value)

    if scope.get("type") == "http":
        return inner("prerender_component: Prerendered")

    return inner("prerender_component: Fully Rendered")
