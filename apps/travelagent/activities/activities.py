from temporalio import activity


@activity.defn
def compose_hello_message(name: str) -> str:
    return f"Hello, {name}! Welcome to Temporal Travel Agent."
