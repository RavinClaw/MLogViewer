# MLogViewer
A program designed to easily extract player mentions and commands from minecraft logs


## FAQ
### What files are supported?
`.log` and `.log.gz` files are both supported

### How do I add logs?
Place the logs into `logs` and they will be auto-read

### How do I add more commands and / or players?
All of that is handled by the `config.yml` and they can be added by simply adding it to their respective area


#### Example for players
```yml
player_match:
- exampleusername
- anotherexampleusername
- .anexamplebedrockusername
- anyUsernameISSUpPOtTEd
```

#### Example for commands
```yml
command_match:
- /give
- /gamemode
- /all_plugin_commands_are_supported
```
