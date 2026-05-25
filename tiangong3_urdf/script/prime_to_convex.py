#!/usr/bin/env python3
"""从网格文件计算凸包并导出 STL（依赖 trimesh）。"""

import argparse
from pathlib import Path

import trimesh


def process_mesh(inp: Path, out_dir: Path) -> None:
    """处理单个网格文件，导出凸包到输出目录。"""
    mesh = trimesh.load(str(inp))
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(
            tuple(
                g.copy()
                for g in mesh.geometry.values()
                if isinstance(g, trimesh.Trimesh)
            )
        )
    if not isinstance(mesh, trimesh.Trimesh):
        print(f"  跳过（无法得到三角网格）: {inp.name}")
        return

    convex_hull = mesh.convex_hull
    out_path = out_dir / inp.name
    out_dir.mkdir(parents=True, exist_ok=True)
    convex_hull.export(str(out_path))
    print(f"  已导出凸包: {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="将网格转为凸包 STL")
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=None,
        help="输入文件夹（包含 stl 文件）；默认：meshes",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="输出文件夹；默认：meshes_convex",
    )
    args = parser.parse_args()

    # 默认路径
    in_dir = args.input if args.input is not None else Path("meshes")
    out_dir = args.output if args.output is not None else Path("meshes_convex")

    in_dir = in_dir.resolve()
    out_dir = out_dir.resolve()

    if not in_dir.is_dir():
        raise SystemExit(f"输入文件夹不存在: {in_dir}")

    # 查找所有 stl 文件（忽略大小写）
    stl_files = [f for f in in_dir.iterdir() if f.suffix.upper() == ".STL"]
    if not stl_files:
        raise SystemExit(f"输入文件夹中没有 stl 文件: {in_dir}")

    print(f"找到 {len(stl_files)} 个 stl 文件，开始处理...")
    for stl_file in sorted(stl_files):
        print(f"处理: {stl_file.name}")
        process_mesh(stl_file, out_dir)
    print(f"完成！凸包已导出到: {out_dir}")


if __name__ == "__main__":
    main()
