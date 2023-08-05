# Python SDK for Lucidtech AI Services API

## Installation

```bash
$ pip install lucidtech-las
```

## Usage Match Receipts

Supported file formats are
- jpeg
- png
- gif
- bmp
- pdf

```python
from las import Client, Receipt

api_key = '...'
client = Client(api_key)

transactions = {
    'transaction_1': {'total': '100.00', 'date': '2017-08-21'},
    'transaction_2': {'total': '340.90', 'date': '2016-03-08'},
    'transaction_3': {'total': '90.37', 'date': '2017-02-17'}
}

receipts = {
    'receipt_1': Receipt(url='https://example.com/receipt1.jpeg'),
    'receipt_2': Receipt(url='https://example.com/receipt2.jpeg'),
    'receipt_3': Receipt(filename='receipt3.jpeg')
}

matching_fields = [
    'total',
    'date'
]

# Optionally specify a matching strategy for respective fields.

matching_strategy = {
    'total': {
        'maximumDeviation': 1.0 # Total amount might differ with 1.0
    },
    'date': {
        'maximumDeviation': 1 # Date might differ with 1 day
    }
}

response = client.match_receipts(
    transactions=transactions,
    receipts=receipts,
    matching_fields=matching_fields,
    matching_strategy=matching_strategy
)

print(response['matchedTransactions'])

# {'transaction_1': 'receipt_2', 'transaction_3': 'receipt_1'}

print(response['unmatchedTransactions'])

# ['transaction_2']
```

## Usage Scan Receipt

Supported file formats are
- jpeg
- png
- gif
- bmp
- pdf

```python
from las import Client, Receipt

api_key = '...'
client = Client(api_key)

receipt = Receipt(url='https://example.com/img.jpeg')
fields = client.scan_receipt(receipt)
print(fields)

# [{'label': 'total', 'value': '157.00', 'confidence': '0.968395300'} ...]

with open('img.jpeg', 'rb') as fp:
    receipt = Receipt(fp=fp)
    fields = client.scan_receipt(receipt)
    print(fields)

# [{'label': 'total', 'value': '157.00', 'confidence': '0.968395300'} ...]

receipt = Receipt(filename='img.jpeg')
fields = client.scan_receipt(receipt)
print(fields)

# [{'label': 'total', 'value': '157.00', 'confidence': '0.968395300'} ...]
```
