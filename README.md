# Mojang-Login-API
An unofficial wrapper for Mojang's services

### How to use it ###

```python
import Mojang

print Mojang.login("email","password") # Params= email/username,password

# It'll return a list, containing [False,"Dead"] if the account is dead
# or [True,"Working, non full-access"] if it is alive but not full-access
# or [True,"Working, full access"] if it's alive and full-access

```
