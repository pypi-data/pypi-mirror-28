# Gnome Shell Install Extension
Install Gnome Shell extension from zip files.
This project provides a CLI to manually install downloaded Gnome Shell extensions.

For a list of Gnome Shell extensions, see https://extensions.gnome.org.

## Installation

### From PyPI
```
pip3 install --user gnome-shell-install-extension
```

### Manually
Clone the git repository or download it as an archive, then:
```
pip3 install --user .
```

## Usage
After having downloaded an extension, for example `myextension.zip`, use the following command to install it:
```
gnome-shell-install-extension myextension.zip
```

You can also provide multiple extensions to install:
```
gnome-shell-install-extension extension1.zip extension2.zip extension3.zip
```


