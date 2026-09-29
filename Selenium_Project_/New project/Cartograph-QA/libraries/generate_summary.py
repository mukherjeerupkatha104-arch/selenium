"""Create a lightweight, local execution dashboard from Robot output.xml."""
from __future__ import annotations

import argparse
import html
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="Robot output.xml")
    parser.add_argument("--result-dir", required=True)
    parser.add_argument("--browser", default="unknown")
    parser.add_argument("--environment", default="unknown")
    parser.add_argument("--build", default="local")
    args = parser.parse_args()
    root = ET.parse(args.output).getroot()
    tests = root.findall(".//test")
    rows = []
    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    for test in tests:
        status = test.find("status")
        state = status.attrib.get("status", "UNKNOWN") if status is not None else "UNKNOWN"
        counts[state] = counts.get(state, 0) + 1
        message = status.text.strip() if status is not None and status.text else ""
        rows.append(f"<tr><td>{html.escape(test.attrib.get('name', ''))}</td><td class='{state}'>{state}</td><td>{html.escape(message[:240])}</td></tr>")
    screenshots = sorted(Path(args.result_dir).glob("screenshots/*.png"))
    links = " ".join(f'<a href="{html.escape(str(p.relative_to(args.result_dir)).replace(chr(92), "/"))}">{html.escape(p.name)}</a>' for p in screenshots) or "No failure screenshots captured."
    total = len(tests)
    document = f"""<!doctype html><html><head><meta charset='utf-8'><title>Cartograph QA Summary</title>
<style>body{{font:16px Arial;margin:36px;color:#152238}}.cards{{display:flex;gap:12px}}.card{{padding:16px;background:#edf3f8;border-radius:8px;min-width:100px}}table{{border-collapse:collapse;width:100%;margin-top:24px}}td,th{{padding:10px;border-bottom:1px solid #d7e0e8;text-align:left}}.PASS{{color:#147a42;font-weight:bold}}.FAIL{{color:#b42318;font-weight:bold}}.SKIP{{color:#9a6700;font-weight:bold}}a{{margin-right:12px}}</style></head><body>
<h1>Cartograph QA Execution Summary</h1><p>Generated {datetime.now(timezone.utc).isoformat()} | Browser: {html.escape(args.browser)} | Environment: {html.escape(args.environment)} | Build: {html.escape(args.build)}</p>
<div class='cards'><div class='card'>Total<br><b>{total}</b></div><div class='card'>Passed<br><b>{counts.get('PASS',0)}</b></div><div class='card'>Failed<br><b>{counts.get('FAIL',0)}</b></div><div class='card'>Skipped<br><b>{counts.get('SKIP',0)}</b></div></div>
<h2>Failure evidence</h2><p>{links}</p><h2>Test results</h2><table><tr><th>Test</th><th>Result</th><th>Message</th></tr>{''.join(rows)}</table><p>For keyword-level detail, open <a href='log.html'>log.html</a> or <a href='report.html'>report.html</a>.</p></body></html>"""
    Path(args.result_dir, "summary.html").write_text(document, encoding="utf-8")


if __name__ == "__main__":
    main()
