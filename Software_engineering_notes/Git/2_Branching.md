# Branches

Commits are identified by hash values, and are not human-readable. Hence, a **branch**, which references a series of snapshots (commits). They are *mutable* because each commit is *immutable*.

When you make commits, Git stores a commit object that contains a *pointer* to the snapshot of the content you staged. This also contains details of the author (name and email), commit message, and pointers to the commit(s) that directly came before it.

A branch is simply a lightweight movable pointer to one of the commits. As you start making commits, you're given a branch (usually `main`) that points to the last commit you amde. Every time you commit, `main` pointer moves forward automatically.

## Creating Branches

`git branch [name]` 

If a commit is created in `main`, and you create a branch named `feature`, the commit has both branches tagged to it. 

Git keeps a special pointer called `HEAD` to track the current branch in your local. When you create a new branch, you are still on the first branch `main`.

Run `git log --oneline --decprate` to show you where the branch pointers are pointing.

```
1e425cb (HEAD -> main) Replaced old CLAUDE.md with symbolic link to AGENTS.md
3ea30b5 (origin/main) Added more test scripts and modification to current training and tuning scripts
```
## Switching Branches

To switch, run `git checkout [name]`. Now `HEAD` is pointed to `feature`. When you checkout to `main` after commiting to `feature`, the file you committed will not reflect on the branch you swithced into. This also means the changes you make from this point forward will diverge from an older version of the project.

A newer syntax is `git switch`:

- Switch to an existing branch: `git switch feature`.

- Create a new branch and switch to it: `git switch -c new-branch`. The `-c` flag stands for create, you can also use the full flag: `--create`.

- Return to your previously checked out branch: `git switch -`.

## Divergent History

Running `git log --oneline --decorate --graph --all` will show the history of your commits. It shows where your branch pointers are and how your history has diverged.

```bash
*   4a9908a Merge branch 'main' of 192.168.98.180:toni/CervAI-Plus
|\ (end of branch divergence) via git merge
| * 6b9b00c Added data privacy flow chart (tentative)
| * 2a4930d Updated pyproject.toml to reflect previous commit changes
| * dcbb8fc Changed src to cervai_plus for pip importing
| * 2c00377 Added changes in metrics and mode defining inside the tune script
| * e03fabf Changed tune report such that it report via a dictionary instead of parameters, in compliance with Ray 2.x changes
| * 32bdfbe Chnaged filename from ray_hpo to tune for storing tuning results in run_hpo
| * 737e049 Changed local_dir to storage_path in run_hpo due to DepreciationWarning
| * 68a0778 Refactored scripts for any error and unused libraries
| * 3f9e996 Moved checkpoint utils to main src
| * a974602 Moved save_checkpoint and load_checkpoint into checkpoint_utils
| * 20da660 Added ModelAdapter class inside models to handle model-agnostic training harness
* | 66dba77 Added AGENTS.md for agents analysis and CLAUDE.md for Claude specifically
|/ (start of branch divergence)
* 030a152 Unfinished tuning_retinanet.py and tuning_faster_rcnn.py scripts
```

# Managing Branches

- By using `--staged` or `--unstaged` in the `git branch`, you can display branches that have or have not yet merged respectively.
- `-d` deletes a branch. 
- `git checkout -b [name]` is a shorthand version of `git branch [name]` then `git checkout [name]`

It is generally advised to never rename a branch, especially when it is used collaboratively.

`git push --set-upstream origin main` allows others to see the branch you created. In this case, it is `origin/main`.

# Branching Workflows
