# autovalidate

Discover and validate static files in a project automatically

## Installation

```
pip install autovalidate
```

## Usage

```
autovalidate
```

This will recursively scan your project and identify any files that are invalid according to their expected format. For example, if a file has the extension .json but its content is not well-formed JSON, an error will be raised.

### Supported formats

- json
- yaml

### Options

```
-r, --reporter=<dot,list>
```

How validation results should be reported.

The dot reporter prints a `'.'` character for ever file successfully validated, and an `'F'` for files that are invalid.

The list reporter prints the full path of every file validated, with a green checkmark for valid files and a red X for invalid files.

```
-x, --exclude=<patterns>
```

Any patterns that should be excluded from validation.

For example, specify `'node_modules/*'` to not validate any data files belonging to your installed npm dependencies.

## Why would I use this?

Say you've got a repository full of configuration files. You use pull requests to submit configuration changes. You'd like to at least have some lightweight automated tests in place to guard against dumb mistakes like adding an extra comma or forgetting a curly brace. You don't feel like writing actual code to do any of this.

That's basically the scenario I have in mind for this tool.
