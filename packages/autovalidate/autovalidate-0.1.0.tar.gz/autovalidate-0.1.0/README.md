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

## Supported formats

- json
- yaml

## Why would I use this?

Say you've got a repository full of configuration files. You use pull requests to submit configuration changes. You'd like to at least have some lightweight automated tests in place to guard against dumb mistakes like adding an extra comma or forgetting a curly brace. You don't feel like writing actual code to do any of this.

That's basically the scenario I have in mind for this tool.
