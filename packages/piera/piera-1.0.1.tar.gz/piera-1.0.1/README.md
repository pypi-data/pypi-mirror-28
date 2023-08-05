# Piera
Piera is a pure-Python [Hiera](http://docs.puppetlabs.com/hiera/) parser and toolkit. It's a nearly feature complete implementation that allows you to use your favorite systems data store, in your favorite systems language.

Piera was originally built at [Braintree](http://github.com/braintree) to help bridge a gap of emerging Python system scripts, and a historical storage of Puppet/Hiera data.

## Shortcomings
Right now Piera does not have a fully-complete deep-merge implementation, although it is planned.

## Install It

### PyPi
`pip install piera`

### Manual
```bash
git clone git@github.com:b1naryth1ef/piera.git
cd piera
python setup.py install
```

## Usage
```python
import piera

h = piera.Hiera("my_hiera.yaml")

# You can use piera to simply interact with your structured Hiera data

# key: 'value'
assert h.get("key") == "value"

# key_alias: '%{alias('key')}'
assert h.get("key_alias") == "value"

# key_hiera: 'OHAI %{hiera('key_alias')}'
assert h.get("key_hiera") == "OHAI value"

# Give piera context
assert h.get("my_context_based_key", name='test01', environment='qa') == "context is great!"

# Pass a fully compliant hiera object with enforced scope, useful for contextual templates/etc
newiera = h.scoped(name='test02', environment='staging')
assert newaiera.get("my_staging_overriden_key") == "ohai staging"
```
