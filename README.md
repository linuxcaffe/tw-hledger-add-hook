# tw-hledger-add-hook

Taskwarrior on-modify hook: launches `hledger add` interactively when a
transaction-related task is completed.

## What it does

When you complete a task tagged `+txn`, `+acct`, or whose description starts
with a trigger verb (`pay`, `buy`), the hook fires `hledger add` with the date
and payee pre-filled from the task. You fill in the posting lines interactively,
then the hook annotates the task with a `ledger: Payee DATE` reference.

## Payee extraction

| Description | Payee | Comment |
|-------------|-------|---------|
| `pay Koodo Mobile cel phone bill` | `Koodo Mobile` | `cel phone bill` |
| `pay Claude subscription` | `Claude` | `subscription` |
| `buy rechargeable hand-warmers` (+Amazon tag) | `Amazon` | — |
| `pay koodo mobile cel phone bill` | `koodo mobile cel phone bill` | — |

**Strategy cascade:**
1. Consecutive capitalised word(s) after the trigger verb → payee; remainder → comment
2. First capitalised tag → payee (fallback when no caps in description)
3. All words after the trigger verb → payee (last resort)

## hledger add pre-fill

```
hledger [-f FILE] add DATE 'Payee Name  ;comment amount'
```

If the `amount` UDA is set on the task (e.g. `task <id> modify amount:$42.50`),
it is included in the comment so you can see it while filling in postings.

## Installation

```bash
bash hledger-add.install
```

Edit `~/.task/config/hledger-add.rc`.

Optionally define an amount UDA in `.taskrc`:
```
uda.amount.type=string
uda.amount.label=Amount
```

## Config (`~/.task/config/hledger-add.rc`)

```ini
hledger.journal         =        # blank = hledger default ($LEDGER_FILE or ~/.hledger.journal)
hledger.trigger_tags    = txn,acct
hledger.trigger_verbs   = pay,buy
hledger.amount_uda      = amount  # blank to disable
```

## Usage

```bash
task add pay Koodo Mobile cel phone bill +txn
task <id> done
# → hledger add fires interactively, pre-filled with date and "Koodo Mobile  ;cel phone bill"
# → on completion: task annotated with "ledger: Koodo Mobile 2026-03-04"
```

## Requirements

- Taskwarrior 2.6.x
- hledger (any version supporting `hledger add`)
- Python 3.8+

## Files

| File | Installed to |
|------|-------------|
| `on-modify_hledger-add.py` | `~/.task/hooks/` |
| `hledger-add.rc` | `~/.task/config/` |
