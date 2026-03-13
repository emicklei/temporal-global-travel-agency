try:
    from temporalio import activity  # pants: no-infer-dep
except ModuleNotFoundError:
    class _ActivityShim:
        @staticmethod
        def defn(fn):
            return fn

    activity = _ActivityShim()


@activity.defn
def compose_hello_message(name: str) -> str:
    return f"Hello, {name}! Welcome to Temporal Travel Agent."
