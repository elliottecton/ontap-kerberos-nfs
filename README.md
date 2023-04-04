This script should work on RHEL/CentOS 7 and 8.

I haven't got around to creating a web frontend for it, so you are going to have to rough it.
The only file you have to modify is `kerberos_config.py`. The dictionary keys should remain the same, but the values need modified to the environments variables. And remember, CASE MATTERS in UNIX land.

After you have modified `kerberos_config.py` to match the environment you are setting up, just run `custom_commands.py`

If you have questions on how to use this, hit me up on Teams.

