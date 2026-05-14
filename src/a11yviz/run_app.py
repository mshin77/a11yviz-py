"""Launch the local accessibility playground."""

from pathlib import Path

from a11yviz._utils import require_pkg


def run_app(host: str = "127.0.0.1", port: int = 8000,
            launch_browser: bool = True) -> None:
    shiny = require_pkg("shiny", "run_app")
    require_pkg("plotnine", "run_app")
    app_path = Path(__file__).parent / "playground" / "app.py"
    shiny.run_app(str(app_path), host=host, port=port,
                  launch_browser=launch_browser)


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser(prog="a11yviz-playground",
                                 description=run_app.__doc__)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()
    run_app(host=args.host, port=args.port,
            launch_browser=not args.no_browser)
