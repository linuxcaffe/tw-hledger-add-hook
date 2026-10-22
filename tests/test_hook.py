"""on-modify_hledger-add: only a transaction needs a terminal. Runs the hook as Taskwarrior does
(two JSON lines on stdin) in a fake home, so ~/.task and the real journal are never touched."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parent.parent / 'on-modify_hledger-add.py'


def run(original, modified, home, **env):
    e = {'HOME': str(home), 'PATH': '/usr/bin:/bin', **env}
    r = subprocess.run([sys.executable, str(HOOK)], input=f'{json.dumps(original)}\n{json.dumps(modified)}\n',
                       capture_output=True, text=True, env=e, timeout=20)
    return r


def task(**kw):
    t = {'uuid': '00000000-0000-0000-0000-000000000001', 'description': 'water the plants',
         'status': 'pending', 'entry': '20261022T000000Z'}
    t.update(kw)
    return t


@pytest.fixture
def home(tmp_path):
    return tmp_path


def test_a_plain_completion_goes_through_under_tw_noninteract(home):
    """The bug (0.1.0–0.1.1): TW_NOINTERACT was checked before the trigger, so tw-web's every Done was refused."""
    done = task(status='completed', end='20261022T120000Z')
    r = run(task(), done, home, TW_NOINTERACT='1')
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout.strip().splitlines()[-1])['status'] == 'completed'
    assert 'tw_needs_pty' not in r.stderr


def test_a_transaction_under_tw_noninteract_asks_for_a_terminal(home):
    done = task(status='completed', end='20261022T120000Z', tags=['txn'], description='pay hydro')
    r = run(task(tags=['txn'], description='pay hydro'), done, home, TW_NOINTERACT='1', TW_PREFLIGHT_CMD='12 done')
    assert r.returncode == 1
    sig = json.loads([l for l in r.stderr.splitlines() if l.startswith('{')][0])
    assert sig == {'type': 'tw_needs_pty', 'cmd': '12 done'}


def test_a_modify_that_is_not_a_completion_goes_through(home):
    r = run(task(), task(description='water the plants twice'), home, TW_NOINTERACT='1')
    assert r.returncode == 0
    assert json.loads(r.stdout.strip().splitlines()[-1])['description'] == 'water the plants twice'
