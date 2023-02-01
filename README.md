### Invoice-Processing-API

## Invoice Processing API Documentation

# Introduction:
The Invoice Processing API allows users to extract data from invoices and convert it into structured data. It supports PDF, image and text formats. The API can be integrated into an application or a system to automate the process of invoice data extraction.

# Functionalities:

Extraction of invoice data such as vendor name, invoice number, invoice date, total amount, and line item details.
Support for different invoice formats including PDF, image and text.
Ability to handle multiple invoices in a batch.
Endpoints:
The API has the following endpoints:

/invoices/upload
This endpoint is used to upload an invoice to the API. The endpoint supports file formats including PDF, image and text.
Request:

```
POST /invoices/upload
Content-Type: multipart/form-data
```

/invoices/extract
This endpoint is used to extract the data from an uploaded invoice. The extracted data includes vendor name, invoice number, invoice date, total amount, and line item details.
Request:

```
GET /invoices/extract
Content-Type: application/json
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/json
{
    "vendor_name": "ABC Ltd.",
    "invoice_number": "INV-123",
    "invoice_date": "2022-12-01",
    "total_amount": "$1000",
    "line_items": [
        {
            "item_name": "Item 1",
            "quantity": 10,
            "unit_price": "$100"
        },
        {
            "item_name": "Item 2",
            "quantity": 5,
            "unit_price": "$200"
        }
    ]
}
```

Usage:
To use the API, follow the below steps:

Upload an invoice to the API using the /invoices/upload endpoint.
Extract the data from the uploaded invoice using the /invoices/extract endpoint.
Example:
Here is an example of how to extract data from an invoice using the API:

python

```
import requests

# Step 1: Upload an invoice to the API
url = "https://api.example.com/invoices/upload"
files = {'invoice': ('invoice.pdf', open('invoice.pdf', 'rb'), 'application/pdf')}
response = requests.post(url, files=files)

# Step 2: Extract data from the uploaded invoice
url = "https://api.example.com/invoices/extract"
response = requests.get(url)
data = response.json()
print(data)
```
Note: Replace "https://api.example.com" with the actual API endpoint.
