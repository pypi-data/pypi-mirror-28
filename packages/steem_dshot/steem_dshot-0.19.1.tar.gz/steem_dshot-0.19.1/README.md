# Fork of Python STEEM Library

`steem-python` is the official STEEM library for Python. Due to inactivity and lack of response to pull requests in the official repo, I will maintain a seperate fork.


## Installation
You can install `steem-python-dshot` with `pip`:

```
pip install -U steem_dshot
```
## Differences

1. Beneficiaries

TODO

2. Default Node

Default node is jussi (api.steemit.com) now instead of the deprecated steemd.steemit.com.

3. Current voting Power

Account class has a new helper method to get current voting power. It also takes into account the regenerated
VP after the last vote cast.

```python
from steem.account import Account
print(Account('emrebeyler').get_current_voting_voting_power())
```

4. Propagation of custom steemd instance to internal constructors 

Account, Post, Blockchain, Converter, Block classes now obeys the custom node. [Thanks @crokkon]

5. Fix custom node selection on steempy cli. [Thanks @crokkon]

6. Fix the version of TOML in dependencies.

7. Implement DeleteComment operation.


## Documentation
Documentation of the main package is available at **http://steem.readthedocs.io**
