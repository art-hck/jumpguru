#!/usr/bin/env python3
"""Dependency-free bootstrap checks. These do not validate an Android application."""
from pathlib import Path
import hashlib
import json
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def check(root: Path) -> list[str]:
    errors = []
    required = (
        'README.md', 'AGENTS.md', 'docs/architecture.md', 'docs/measurement.md',
        'docs/hardware.md', 'docs/roadmap.md', 'docs/development.md',
        'docs/agent-workflow.md', 'docs/skills.md', '.github/ISSUE_TEMPLATE/task.md',
        '.github/workflows/bootstrap.yml', 'skills-lock.json',
    )
    for name in required:
        if not (root / name).is_file():
            errors.append(f'Missing required file: {name}')
    roles = list((root / '.codex/agents').glob('*.toml'))
    names = set()
    if not roles:
        errors.append('No agent roles found')
    for path in roles:
        try:
            role = tomllib.loads(path.read_text())
            for field in ('name', 'description', 'developer_instructions'):
                if not isinstance(role.get(field), str) or not role[field].strip():
                    errors.append(f'{path.name}: missing string {field}')
            if role.get('name') in names:
                errors.append(f'Duplicate agent name: {role.get("name")}')
            names.add(role.get('name'))
            if role.get('sandbox_mode') not in ('read-only', 'workspace-write'):
                errors.append(f'{path.name}: unexpected sandbox mode')
        except (ValueError, OSError) as exc:
            errors.append(f'{path.name}: {exc}')
    try:
        lock = json.loads((root / 'skills-lock.json').read_text())
        if lock['schema_version'] != 1:
            errors.append('Unsupported skills lock schema')
        upstream = lock['upstream']
        if not re.fullmatch(r'[0-9a-f]{40}', upstream['commit']):
            errors.append('Upstream skill commit must be a full SHA')
        if not upstream['files']:
            errors.append('Upstream file manifest is empty')
        for name, expected in upstream['files'].items():
            path = root / name
            if not path.resolve().is_relative_to(root.resolve()):
                errors.append(f'Unsafe manifest path: {name}')
                continue
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                errors.append(f'Skill missing or checksum mismatch: {name}')
        for name in (*upstream['paths'], *lock['local_skills']):
            path = root / '.agents/skills' / name / 'SKILL.md'
            if not path.is_file():
                errors.append(f'Missing skill: {name}')
                continue
            content = path.read_text()
            if not content.startswith('---\n') or '\n---\n' not in content[4:]:
                errors.append(f'Missing skill frontmatter: {name}')
            elif f'\nname: {name}\n' not in content or '\ndescription:' not in content:
                errors.append(f'Missing skill name/description: {name}')
        actual = {
            str(p.relative_to(root))
            for name in upstream['paths']
            for p in (root / '.agents/skills' / name).rglob('*') if p.is_file()
        }
        for extra in sorted(actual - set(upstream['files'])):
            errors.append(f'Unrecorded upstream skill file: {extra}')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f'Invalid skills-lock.json: {exc}')
    return errors


if __name__ == '__main__':
    failures = check(ROOT)
    for failure in failures:
        print(f'FAIL: {failure}', file=sys.stderr)
    if failures:
        sys.exit(1)
    print('PASS: repository infrastructure and pinned skills. Android/hardware: NOT TESTED.')
