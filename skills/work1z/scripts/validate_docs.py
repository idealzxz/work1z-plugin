"""Read-only checks for work1z PRD and technical documents (Python 3.9+)."""

import argparse
import datetime
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


VERSION = re.compile(r"v1\.(?:0|[1-9][0-9]*)\Z")
LINK = re.compile(r'!?\[[^\]\n]*\]\((<[^>\n]+>|[^\s()]+(?:\([^()]*\)[^\s()]*)*)(?:\s+"[^"\n]*")?\)')
HISTORY = ["文档版本", "修改日期", "修改人", "影响章节", "变更摘要"]
INDEX = ["PRD 文档版本", "涉及模块及主要变化", "本次技术方案及附件", "需回看的既有设计"]
PRD_HEADINGS = ["1. 背景与目标", "2. 需求范围", "3. 能力边界", "4. 异常处理", "5. 非功能需求", "6. 验收标准"]
PLAN_HEADINGS = ["1. 技术栈与选型", "2. 架构设计", "3. 项目目录", "4. 业务模块设计", "5. 关键交互", "6. 性能设计", "7. 实施与验证"]


def prose_lines(text):
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            token, rest = marker.groups()
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not rest.strip():
                fence = None
            continue
        if fence is None:
            yield number, line


def targets(line):
    return [match.group(1).strip("<>") for match in LINK.finditer(line)]


def local_target(source, target):
    parts = urlsplit(target)
    if parts.scheme or parts.netloc:
        return None
    return (source.parent / unquote(parts.path)).resolve() if parts.path else source


class Validator:
    def __init__(self):
        self.errors = 0
        self.warnings = 0
        self.documents = {}

    def report(self, path, line, rule, message, warning=False):
        if warning:
            self.warnings += 1
        else:
            self.errors += 1
        print(f"{path}:{line}: {'提醒' if warning else '错误'} [{rule}] {message}")

    def read(self, path):
        if path not in self.documents:
            self.documents[path] = path.read_text(encoding="utf-8-sig")
        return self.documents[path]

    def table(self, path, header):
        lines = list(prose_lines(self.read(path)))
        active = False
        rows = []
        for number, line in lines:
            if not line.strip().startswith("|"):
                if active:
                    break
                continue
            cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
            if cells == header:
                active = True
                continue
            if not active or all(re.fullmatch(r":?-+:?", cell) for cell in cells):
                continue
            if len(cells) != len(header):
                self.report(path, number, "table", f"应有 {len(header)} 列，实际 {len(cells)} 列")
            else:
                rows.append((number, cells))
        if not active or not rows:
            self.report(path, 1, "table", f"缺少表头或数据行：{' / '.join(header)}")
        return rows

    def structure(self, path, headings, required):
        found = []
        for number, line in prose_lines(self.read(path)):
            if not line.startswith("## "):
                continue
            title = line[3:].strip().rstrip("#").strip()
            if title not in headings:
                self.report(path, number, "heading", f"不在模板中的二级标题，请核对：{title}", True)
            else:
                found.append(headings.index(title))
        if found != sorted(set(found)):
            self.report(path, 1, "heading", "模板章节重复或顺序不正确")
        for title in required:
            if headings.index(title) not in found:
                self.report(path, 1, "heading", f"缺少章节：{title}")

    def common(self, path):
        text = self.read(path)
        for number, line in prose_lines(text):
            plain = re.sub(r"`+[^`]*`+", "", line)
            if re.search(r"\[(?:项目名(?:称)?|项目或需求名称|版本号|姓名|YYYY-MM-DD|模块名称)\](?![([])", plain):
                self.report(path, number, "placeholder", "存在未替换的模板占位符")
            if re.search(r"<!--\s*(?:编写提示|初版写本项目|本文件命名为)", line):
                self.report(path, number, "template", "存在模板填写说明")
            if line.startswith("#") and re.search(r"（(?:可选|必填|按需填写)）", line):
                self.report(path, number, "template", "标题仍带模板提示")
            if re.search(r"\b(?:TODO|TBD)\b|\[待填写\]", plain):
                self.report(path, number, "placeholder", "请核对待填写内容", True)
            if re.search(r"\[[^\]]+\]\[[^\]]*\]|^\s*\[[^\]]+\]:|<(?:a|img)\b", plain):
                self.report(path, number, "link-manual", "引用式或 HTML 链接需人工核对", True)
            for target in targets(plain):
                self.check_link(path, number, target)

    def check_link(self, path, number, target):
        destination = local_target(path, target)
        if destination is None:
            self.report(path, number, "link-external", f"外部链接未联网检查：{target}", True)
            return
        if not destination.exists():
            self.report(path, number, "link", f"目标不存在：{target}")
            return
        fragment = unquote(urlsplit(target).fragment)
        if not fragment:
            return
        if destination.suffix.lower() != ".md":
            self.report(path, number, "anchor", f"非 Markdown 锚点需人工核对：{target}", True)
            return
        anchors = set()
        for _, line in prose_lines(self.read(destination)):
            heading = re.match(r"^#{1,6}\s+(.+?)(?:\s+#+)?$", line)
            if heading:
                title = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading.group(1))
                slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
                candidate = slug
                suffix = 0
                while candidate in anchors:
                    suffix += 1
                    candidate = f"{slug}-{suffix}"
                anchors.add(candidate)
            anchors.update(re.findall(r'\b(?:id|name)=[\'"]([^\'"]+)[\'"]', line))
        if fragment not in anchors:
            self.report(path, number, "anchor", f"未匹配标题锚点，请在目标渲染器确认：{target}", True)

    def prd(self, path, expected):
        self.common(path)
        self.structure(path, PRD_HEADINGS, [title for title in PRD_HEADINGS if not title.startswith("5.")])
        text = self.read(path)
        lines = list(prose_lines(text))
        for field in ("所属项目", "目标版本", "负责人", "最近更新"):
            if not any(re.search(rf"{field}[：:]\s*[^\s｜|]", line) for _, line in lines):
                self.report(path, 1, "field", f"缺少或为空：{field}")
        if not any(re.fullmatch(r"### 用例图\s*", line) for _, line in lines):
            self.report(path, 1, "heading", "缺少用例图章节")
        rows = self.table(path, HISTORY)
        versions = []
        for offset, (number, cells) in enumerate(rows):
            version, date, author, chapters, summary = cells
            versions.append(version)
            if version != f"v1.{offset}":
                self.report(path, number, "version", f"历史版本应连续排列，此行为 v1.{offset}")
            try:
                if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", date):
                    raise ValueError
                datetime.date.fromisoformat(date)
            except ValueError:
                self.report(path, number, "date", "修改日期须为有效 YYYY-MM-DD")
            if not all((author, chapters, summary)):
                self.report(path, number, "history", "修改人、影响章节和变更摘要不能为空")
            if offset == 0 and summary != "初版":
                self.report(path, number, "history", "初版摘要应为“初版”")
            if offset and summary:
                items = re.split(r"<br\s*/?>", summary)
                if any(not re.match(rf"\s*{position}\.\s*\S", item) for position, item in enumerate(items, 1)):
                    self.report(path, number, "history", "摘要须从 1. 连续编号，用 <br> 分行")
        current = versions[-1] if versions else None
        if expected and current != expected:
            self.report(path, 1, "version", f"最新修改记录为 {current}，预期 {expected}")
        for number, line in lines:
            for version in re.findall(r"\b(v1\.[0-9]+)[：:]", line):
                if version not in versions:
                    self.report(path, number, "version", f"正文标注 {version} 没有对应修改记录")
        return versions

    def plan(self, path, prd, version):
        self.common(path)
        self.structure(path, PLAN_HEADINGS, PLAN_HEADINGS if version == "v1.0" else [])
        headers = [(number, line) for number, line in prose_lines(self.read(path)) if line.startswith("对应 PRD：")]
        if len(headers) != 1:
            self.report(path, 1, "plan", "须有一行“对应 PRD：链接、版本｜本次范围：…”")
            return
        number, header = headers[0]
        if version not in re.findall(r"\bv[0-9]+\.[0-9]+\b", header):
            self.report(path, number, "version", f"对应 PRD 须标明版本 {version}")
        if not any(local_target(path, target) == prd for target in targets(header)):
            self.report(path, number, "plan", "对应 PRD 未链接到指定的 PRD 文件")
        if not re.search(r"本次范围[：:]\s*(?:前端|后端|全栈|两端)", header):
            self.report(path, number, "plan", "本次范围须标明前端、后端或两端")

    def archive(self, path, prd, versions):
        self.common(path)
        rows = self.table(path, INDEX)
        if [cells[0] for _, cells in rows] != versions:
            self.report(path, 1, "archive", "清单版本及顺序须与 PRD 修改记录一致")
        current = [line for _, line in prose_lines(self.read(path)) if line.startswith("当前 PRD：")]
        if len(current) != 1 or not any(local_target(path, target) == prd for target in targets(current[0])):
            self.report(path, 1, "archive", "当前 PRD 须链接到指定的 PRD 文件")
        for number, cells in rows:
            version, modules, design, previous = cells
            if not VERSION.fullmatch(version):
                self.report(path, number, "version", f"无效版本：{version}")
                continue
            if not modules:
                self.report(path, number, "archive", "涉及模块及主要变化不能为空")
            directory = prd.parent / version
            if design == "无技术变更":
                if directory.exists():
                    self.report(path, number, "archive", f"标为无技术变更却存在 {version} 目录")
                continue
            main = directory / "技术方案.md"
            if not main.is_file():
                self.report(path, number, "archive", f"缺少 {version}/技术方案.md")
                continue
            if not any(local_target(path, target) == main for target in targets(design)):
                self.report(path, number, "archive", f"本次技术方案未链接到 {version}/技术方案.md")
            for target in targets(design):
                destination = local_target(path, target)
                if destination and directory not in destination.parents:
                    self.report(path, number, "archive", "本次技术附件应位于同号目录，旧设计放在需回看列")
            self.plan(main, prd, version)


def markdown_file(value):
    try:
        path = Path(value).expanduser().resolve()
        if not value.strip() or not path.is_file() or path.suffix.lower() != ".md":
            raise argparse.ArgumentTypeError("必须指定存在的 Markdown 文件（.md）")
        path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError, ValueError, RuntimeError) as error:
        raise argparse.ArgumentTypeError(f"文件须可读且为 UTF-8：{error}") from error
    return path


def version_value(value):
    if not VERSION.fullmatch(value):
        raise argparse.ArgumentTypeError("版本须为 v1.0、v1.1 等格式，不允许前导零")
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--prd", required=True, type=markdown_file, help="PRD 文件")
    parser.add_argument("--plan", type=markdown_file, help="本次技术方案；省略则不检查")
    parser.add_argument("--index", type=markdown_file, help="归档时使用的项目文档清单")
    parser.add_argument("--version", type=version_value, help="预期的最新文档版本；默认取 PRD 修改记录末行")
    parser.add_argument("--stage", choices=("draft", "archived"), default="draft")
    args = parser.parse_args(argv)
    if (args.stage == "archived") != bool(args.index):
        parser.error("--index 与 --stage archived 必须一起提供")
    paths = [path for path in (args.prd, args.plan, args.index) if path]
    if len(paths) != len(set(paths)):
        parser.error("PRD、技术方案和文档清单不能是同一个文件")
    if args.index and args.index.parent != args.prd.parent:
        parser.error("项目文档清单必须与 PRD 同级")
    validator = Validator()
    try:
        versions = validator.prd(args.prd, args.version)
        current = versions[-1] if versions else args.version
        if args.plan:
            if args.stage == "archived" and args.plan != args.prd.parent / str(current) / "技术方案.md":
                parser.error("归档模式的 --plan 必须是最新版本目录下的技术方案.md")
            if args.stage == "draft":
                validator.plan(args.plan, args.prd, current)
        if args.index:
            validator.archive(args.index, args.prd, versions)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"读取或解析失败：{error}", file=sys.stderr)
        return 2
    print(f"检查完成：{validator.errors} 个错误，{validator.warnings} 个提醒。仅覆盖文档机械规则，不代表业务审查或验收通过。")
    return 1 if validator.errors else 0


if __name__ == "__main__":
    sys.exit(main())
