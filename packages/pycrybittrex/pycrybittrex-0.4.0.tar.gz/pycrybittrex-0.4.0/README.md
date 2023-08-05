How to install

```

pip3 install pycrybittrex

```

Usage example:

```python

from pycrybittrex import bittrex, ApiVersion
client = bittrex.create_client(ApiVersion.V1_1, api_key='<api_key>', api_secret='<api_secret>')
order_history = client.get_order_history("ETH-XRP")

```

To setup development environment using conda:

```bash

conda create --name pycrybittrex --file requirements.txt

```






