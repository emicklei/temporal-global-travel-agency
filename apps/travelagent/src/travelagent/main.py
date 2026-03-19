import argparse
import asyncio

from .worker import DEFAULT_TASK_QUEUE, run_worker


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Temporal Travel Agent demo app")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    worker_parser = subparsers.add_parser("worker", help="Run Temporal worker")
    worker_parser.add_argument("--hostport", default="localhost:7233")
    worker_parser.add_argument("--namespace", default="default")
    worker_parser.add_argument("--task-queue", default=DEFAULT_TASK_QUEUE)

    return parser.parse_args()


async def run_from_args(args: argparse.Namespace) -> None:
    await run_worker(
        hostport=args.hostport,
        namespace=args.namespace,
        task_queue=args.task_queue,
    )


def main() -> None:
    asyncio.run(run_from_args(parse_args()))


if __name__ == "__main__":  # pragma: no cover
    main()
