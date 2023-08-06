# taptogo
A python interface to the LA Metro TAP To Go site

## Install
Taptogo can be installed from pypi using pip :

```
pip install taptogo
```

## Usage

``` python
from taptogo import TapToGo

tap = TapToGo()

# Log in with email and password
tap.login(email, password)

# List cards associated with account
for card in tap.describe_tap_cards():
    print(card)

# Add stored value to a tap card
tap.add_stored_value(
    5.00, 
    tap_card_id='9999990123456789', 
    card_name='Bruce Wayne',
    card_num='4444000000000000',
    card_exp_month='01',
    card_exp_year='20',
    card_cvv=123
)
```

## Tests
To run the test suite, export your TAP user and password and auto-run:

```
$ env TAPTOGO_EMAIL="<your-email>" TAPTOGO_PASSWORD="<your-password>" python -m unittest discover tests/
```

## Contributing
There are many functions of the TAP To Go site that are missing from this
library. I built this to automatically reload my TAP card, so I will 
maintain it to keep the current functionality working. If it is missing 
something you need, feel free to add it and contribute back to this project. 
Pull requests and bug reports welcome!
