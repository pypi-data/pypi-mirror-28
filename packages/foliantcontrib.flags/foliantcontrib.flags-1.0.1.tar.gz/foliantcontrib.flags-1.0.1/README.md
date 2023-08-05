# Conditional Blocks for Foliant

This preprocessors lets you exclude parts of the source based on flags defined in the project config and environment variables, as well as current target and backend.


## Installation

```shell
$ pip install foliantcontrib.flags
```


## Config

Enable the propressor by adding it to `preprocessors`:

```yaml
preprocessors:
  - flags
```

Enabled project flags are listed in `preprocessors.flags`:

```yaml
preprocessors:
  - flags:
    - foo
    - bar
```

To set flags for the current session, define `FOLIANT_FLAGS` environment variable:

```shell
$ FOLIANT_FLAGS="spam, eggs"
```

You can use commas, semicolons, or spaces to separate flags.

>   **Hint**
>
>   To emulate a particular target or backend with a flag, use the special flags `target:FLAG` and `backend:FLAG` where `FLAG` is your target or backend:
>       $ FOLIANT_FLAGS="target:pdf, backend:pandoc, spam"


## Usage

Conditional blocks are enclosed between `<<if>...</if>` tags:

```markdown
This paragraph is for everyone.

<<if flags="management">
This parapraph is for management only.
</if>
```

A block can depend on multiple flags. You can pick whether all tags must be present for the block to appear, or any of them (by default, `kind="all"` is assumed):

```markdown
<<if flags="spam, eggs" kind="all">
This is included only if both `spam` and `eggs` are set.
</if>

<<if flags="spam, eggs" kind="any">
This is included if both `spam` or `eggs` is set.
</if>
```

You can also list flags that must *not* be set for the block to be included:

```markdown
<<if flags="spam, eggs" kind="none">
This is included only if neither `spam` nor `eggs` are set.
</if>
```

You can check against the current target and backend instead of manually defined flags:

```markdown
<<if targets="pdf">This is for pdf output</if><<if targets="site">This is for the site</if>

<<if backends="mkdocs">This is only for MkDocs.</if>
```
