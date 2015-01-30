# taskwarrior-hledger-add-hook
Taskwarrior (http://taskwarrior.org) is great for tracking all kinds of tasks, and many of those tasks will be "transactional", having something to do with accounting. "pay Hydro Electric bill", "invoice Random Productions for video shoot", "buy new furnace gaskets", tracking these, and doing these, is great, but it's HALF the job! If you are completing these tasks but not recording the transactions in some accounting system, you are missing an opportunity to get your sh#t together.

Luckily, there are a few excellent accounting packages for people who use taskwarrior. If you use TW then you probably like things at the command-line, and you probably appreciate having all of your data in human readable (and editable) text files. For that sort of user (you) there exists *ledger. That's http://ledger-cli.org and it's haskell cousin http://hledger.org. Both of these programs work the same way, and (to a large extent) are file-compatible, that is, you can create a file in one, and read it with the other, and either of them will help you track all sorts of accounting transactions, and generate detailed and accurate reports. 

This tw hook script will use hledger (http://hledger.org) and it's interactive add function (http://hledger.org/manual.html#add) taking all of the details of the accounting-related task you just completed, and piping it through the interactive "add" command, into a properly formatted *ledger file. The object here is to tie the act of marking such a task "done" to the ledger-process, so you don't have to do it later, because it will take only seconds to do, it will establish a regular pattern of accurate bookkeeping, and if you don't do it right then, you'll forget!

### Requirements
- taskwarrior (http://taskwarrior.org/download/)
- hledger (http://hledger.org/download.html)
- tasklib (https://github.com/tbabej/tasklib/tree/develop) note: must use develop branch



