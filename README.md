![LOGO](https://github.com/ctadel/linux_/assets/46838148/3022bb69-8cc5-484b-ab62-d7ed8dc535cd)

In the realm of customization, managing dotfiles – *those hidden configuration files that govern the behavior of various applications* – is a common practice among us developers. 

However, while many have their own dotfiles repositories, there's often a lack of efficient synchronization tools. This realization inspired the development of **teer**, a python program designed to streamline the synchronization process and ensure that your configurations are always up-to-date across different systems.

**teer** makes it incredibly easy to add the configuration of any application and include additional scripts to run post-syncing, providing a seamless and customizable experience.

![Demo](https://github.com/ctadel/linux_/assets/46838148/dbc1ff8f-7246-43cb-892d-3e56185133a7)

# Operating System Compatibility
| **Operating System** | **Status** |
| -------------------- | ---------- |
| Linux                | ✅          |
| MacOS                | ✅          |
| Windows              | ❌          |



# Getting Started

1. **Fork the Repository**: Fork the **teer** repository to your own github account.
2. **Add Your dotfiles**: Add your dotfiles and configurations to the forked repository.
3. **Make your Configuration File**: Create a *conf.json* file and specify the applications and their configurations to be synced. (See Reference: #configuration)
4. **Start Syncing**: Utilize the *sync.py* script to synchronize your dotfiles across different systems effortlessly.
```shell
python sync.py
```
5. **Sit Back and Relax**: Based on the instructions written in the configuration file, **teer** will start the synchronization process.


# Features

- **Interactive Syncing**: Use the (*--interactive / -i*) flag to run the script and sync dotfiles for each application one at a time
- **Executable Commands**: Execute commands after syncing configurations, allowing for additional customization or sourcing dotfiles.
- **Effortless Integration**: Create your own config file and easily integrate your dotfiles into your existing dotfiles repository workflow for seamless management.


# Configuration

The configuration file **conf.json** follows a structured format to define the source and destination paths for the dotfiles, along with additional instructions for post-syncing operations. Below is an explanation of each property:

- **local_path** (string/path):
	This property specifies the directory within the repository where the application's backup of dotfiles or folders is stored. If not specified, it defaults to the repository's root directory.

- **remote_path** (string/path):
	This property indicates the directory on the user's system where the dotfiles should be synced to. If not specified, it defaults to the user's home directory.

- **files** (object/dict):
	This property contains key-value pairs, where each key is a file in the local_path directory and it's corresponding value is the path where the file should be linked on the user's system. This allows for selective syncing of specific files.

- **exec** (string/shell command):
	This property specifies a script or command to be executed after the dotfiles have been synced. It is useful for any post-sync operations that need to be performed, such as reloading configurations or running setup scripts.

- **launch_file** (string/path):
	This property is used to link *.desktop* files, which are typically used to create entries in the application's launcher menu. The *.desktop* file will be linked inside the ***~/.local/share/applications/*** directory, making the application accessible from the system's application launcher.

Each entry in the configuration file ensures that the corresponding dotfiles are accurately synced from the specified local paths to the designated remote paths, with optional commands executed post-syncing to finalize the setup. This flexible configuration approach makes managing and syncing dotfiles efficient and tailored to individual application needs.


## Sample Configurations

Below are sample entries in the **conf.json** file illustrating various use cases:

```json
{
  "Shell Scripts"   :  {
    "local_path"      : "shell",
    "exec"            : "bash shell/add_source.sh",
    "files"           : {
          "bashpd.sh"   : ".bashpd"
        }
    },

  "Git"       : {
    "files"    : {
        "gitconfig"  : ".gitconfig"
      }
  },

  "Kitty Terminal"   : {
    "local_path"      : "kitty",
    "remote_path"     : "~/.config/kitty"
  },

  "Yazi File Manager"    : {
    "local_path"      : "yazi",
    "remote_path"     : "~/.config/yazi"
  },

  "Lunar Vim"    : {
    "local_path"      : "lvim",
    "remote_path"     : "~/.config/lvim"
  },

  "Postgresql"       : {
    "files"    : {
        "psqlrc"  : ".psqlrc"
      }
  },

  "Tig"       : {
    "files"    : {
        "tigrc"  : ".tigrc"
      }
  },

  "Byobu"       : {
    "local_path"  : "byobu",
    "remote_path" : "~/.byobu"
  },

  "FZF Script"       : {
    "local_path"  : "shell",
    "remote_path" : "~/usr/bin/",
    "files"    : {
        "fzf_script.sh"  : "f"
      }
  },

  "Spotify TUI"       : {
    "local_path"  : "ncspot",
    "remote_path" : "~/.config/ncspot"
  }
}

```


# Conclusion

With **teer**, managing your dotfiles across different systems becomes a breeze. Say goodbye to manual copy-pasting and *rsync* headaches – embrace a streamlined synchronization process and ensure your configurations are always in sync, no matter where you go. The ease of adding new application configurations and executing additional scripts post-syncing makes **teer** an indispensable tool for every developer.