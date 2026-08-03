#!/usr/bin/env python3
"""
teamlore scarmap — Living Scar Map Generator
Generates an HTML force graph of lore entries.
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def parse_lore_files(lore_root: Path):
    nodes = []
    edges = []
    path_map = defaultdict(list)

    for md in lore_root.rglob("*.md"):
        content = md.read_text(encoding="utf-8")
        if not content.startswith("---"):
            continue
        match = re.match(r"---\n(.*?)\n---", content, re.DOTALL)
        if not match:
            continue
        fm = match.group(1)
        kind = re.search(r"kind:\s*(\w+)", fm)
        commit = re.search(r"commit:\s*(\w+)", fm)
        verify_by = re.search(r"verify_by:\s*([\d-]+)", fm)
        paths = re.findall(r"paths:\s*\n((?:\s+-\s+.*\n)+)", fm)
        if paths:
            path_list = re.findall(r"\s+-\s+(.+)", paths[0])
        else:
            path_list = []

        if kind and commit:
            node_id = commit.group(1)[:8]
            nodes.append({
                "id": node_id,
                "label": md.stem,
                "kind": kind.group(1),
                "verify_by": verify_by.group(1) if verify_by else "unknown",
                "paths": path_list
            })
            for p in path_list:
                path_map[p].append(node_id)

    for node in nodes:
        for p in node["paths"]:
            for target in path_map[p]:
                if target != node["id"]:
                    edges.append({"source": node["id"], "target": target})

    return nodes, edges

def generate_html(nodes, edges, output_path: Path):
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Scar Map — {datetime.now().strftime("%Y-%m-%d")}</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/vis-network.min.js"></script>
    <style>
        body {{ margin: 0; font-family: Arial, sans-serif; }}
        #mynetwork {{ width: 100vw; height: 100vh; }}
        #header {{ position: absolute; top: 10px; left: 10px; z-index: 100; background: rgba(255,255,255,0.9); padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div id="header">
        <h2>Scar Map</h2>
        <p>Nodes: {len(nodes)} | Edges: {len(edges)}</p>
    </div>
    <div id="mynetwork"></div>
    <script>
        const nodes = new vis.DataSet([
            {",".join(f'{{id: "{n["id"]}", label: "{n["label"]}", title: "{n["kind"]} — {n["verify_by"]}"}}' for n in nodes)}
        ]);
        const edges = new vis.DataSet([
            {",".join(f'{{from: "{e["source"]}", to: "{e["target"]}"}}' for e in edges)}
        ]);
        const container = document.getElementById("mynetwork");
        const data = {{ nodes, edges }};
        const options = {{
            physics: {{ stabilization: true }},
            nodes: {{ shape: "dot", size: 16 }},
            edges: {{ arrows: "to" }}
        }};
        new vis.Network(container, data, options);
    </script>
</body>
</html>
"""
    output_path.write_text(html, encoding="utf-8")
    print(f"Scar map generated: {output_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: teamlore scarmap <lore-root> [--output <file>]")
        sys.exit(1)

    lore_root = Path(sys.argv[1])
    output = Path("scar-map.html")
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output = Path(sys.argv[idx + 1])

    nodes, edges = parse_lore_files(lore_root)
    generate_html(nodes, edges, output)

if __name__ == "__main__":
    main()
