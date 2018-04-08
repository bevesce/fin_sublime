# Fin Sublime

Sublime Text 3 plugin for expenses and transactions tracking, in plain text, using [fin](https://github.com/bevesce/fin).

![sublime fin icon](icon.png)

## Installation

Installation is manual:

```
git clone --recursive https://github.com/bevesce/fin_sublime.git fin_sublime
mv fin_sublime "path/to/Sublime Text 3/Packages/"
```

There's one git submodule here so you need to use `--recursive` flag.

## Features
### Syntax highlighting

Highlighting should work with every color scheme:

![Syntax highlighting](screenshots/syntax.png)

### Filter & sum

You can filter (by folding) transactions with *fin* queries:

![filter](screenshots/filter.png)

Pressing enter will show quick panel with the total amount of resulting transactions:

![sum](screenshots/sum.png)


## License

Copyright 2016 Piotr Wilczyński. Licensed under the MIT License.
