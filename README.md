# QuickVPN.py
Modifed async version of "[vpngate.py](https://gist.github.com/Lazza/bbc15561b65c16db8ca8)" script by "[Andrea Lazzarotto](https://andrealazzarotto.com/)" with threading option for Windows. <br>

# Usage
Import QuickVPN.py to your project. (Make sure to include *Exceptions.py* script and whole *bin* folder)

```python
import QuickVPN
```

Create a Connection object providing desired country name or code as a first argument.<br>Optionally you can also pass the async loop 

```python
connection = QuickVPN.Connection("Korea", loop=app_loop)
```

Start the connection by using one of three avaliable methods <br>

  - **run()** - loop.fun_forever()
  - **start()** - loop.create_task()
  - **start_background()** - Thread()

<br>

# Example of usage
**Async** <br>
```python
import QuickVPN
import asyncio
import keyboard


async def keyboard_op():
    def end_con():
        print("Ending")
        connection.end()
    keyboard.add_hotkey('ctrl+alt', end_con)
    keyboard.wait()
    
app_loop = asyncio.new_event_loop()
connection = QuickVPN.Connection("Korea", loop=app_loop)

connection.start()
app_loop.create_task(keyboard_op())
app_loop.run_forever()
```
<br>

```python
import QuickVPN
    
connection = QuickVPN.Connection("Korea")
connection.run()
```

<br>

**Threading** <br>

```python
import QuickVPN
import keyboard


def end_con():
    print("Ending")
    connection.end()

connection = QuickVPN.Connection("Korea")
connection.start_background()

keyboard.add_hotkey('ctrl+alt', end_con)
keyboard.wait()
```

# Exceptions
  - **NotAnAdmin** - raised when user ran script without admin privileges.
  - **NoAvailableServers** - raised when there isn't any available servers.
  - **NoServersInCountry** - raised when there isn't any available servers in desired country.
  - **InvalidCountryName** - raised when the country name is too short.

# Requirements
  - **requests** - 2.24.0
  - **keyboard** - 0.13.5 (Optional)
