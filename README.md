# Sublime Finanse

Sublime Text 3 plugin for expenses and transactions tracking in plain text using [finanse](https://github.com/bevesce/finanse).

![sublime finanse icon](icon.png) ![finanse icon](https://github.com/bevesce/finanse/raw/master/icon.png)

## Installation

As long as I'm the only person using this, I don't want to pollute Package Control. So installation is manual:

```
git clone --recursive https://github.com/bevesce/SublimeFinanse.git Finanse
mv Finanse "path/to/Sublime Text 3/Packages/"
```

There's one git submodule here so you need to use `--recursive` flag.

## Features
### Syntax highlighting

Highlighting should work with every color scheme:

![Syntax highlighting](screenshots/syntax.png)

### Filter & sum

You can filter (by folding) transactions with *finanse* queries:

![filter](screenshots/filter.png)

Pressing enter will show quick panel with the total amount of resulting transactions:

![sum](screenshots/sum.png)


## License

Copyright 2016 Piotr Wilczyński. Licensed under the MIT License.