# thonny-black-formatter
Thonny plugin for source formatting with black (Thonny >= 4.x)

This plugin enables formatting with black tool inside Thonny python editor.
## History and rationale

Originally there was this plugin available:

https://pypi.org/project/thonny-black-format/

From Thonny release 4.0.0 the plugin stopped working and has been found in an abandoned project state (dead github project home page link) but still installable from PyPI repository.

This is an adptation built from the sources installes and modified in order to make it work for Thonny release 4.0.0 and - hopefully - subsequent.

## Credits

All credits go to the author "Franccisco" of the original plugin.

All information available to me related to the original plugin is in the following two links.

Github repo: https://github.com/Franccisco/thonny-black-code-format [dead link]
Docs: https://pypi.org/project/thonny-black-format/

## How the plugin works

### Install the plugin

The plugin must be installed using the Thonny menu:

```Tools -> Manage plug-ins... ```
 
### Format your code

The plugin adds the following menu entry:

```Tools -> Format with black... ```

Use this command to format the current source being edited in the active window.




