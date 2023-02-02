# Invoice-Processing-API

## Invoice Processing API Documentation

### Introduction:
The Invoice Processing API allows users to extract data from invoices and convert it into structured data. It supports PDF, image and text formats. The API can be integrated into an application or a system to automate the process of invoice data extraction. This RESTful API built with Flask that allows you to process invoices and perform CRUD operations on them. It is built with Flask and uses SQLAlchemy as the ORM. The API also includes an email sending feature and token-based authentication.

### Requirements
```
Flask
Flask-SQLAlchemy
PyJWT
Flask-Marshmallow
```
### Setup
Clone the repository
```
$ git clone https://github.com/<username>/invoice-processing-api.git
```
Change into the repository directory

```
$ cd invoice-processing-api
```
Create a virtual environment and install the required packages

```
$ python -m venv env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
```
Set the environment variables for the email sending feature

```
$ export SENDER_EMAIL='you@example.com'
$ export SENDER_PASSWORD='your_email_password'
$ export RECIPIENT_EMAIL='recipient@example.com'
```

Run the API
```
(env) $ python app.py
```

### Endpoints
Get Invoices
Retrieve a paginated list of invoices.

```
GET /invoices
```

Query Parameters
```
page: The page number to retrieve. Default is 1.
processed: A boolean indicating whether to retrieve processed or unprocessed invoices.
search: A search string to filter the invoices by invoice number.
```
### Example Request
```
GET /invoices?page=2&processed=true&search=INV-100
```
Example Response
```
HTTP 200 OK

{
    "invoices": [
        {
            "id": 1,
            "invoice_number": "INV-100",
            "processed": true,
            "amount": 100.0,
            "custom_field_1": "Value 1",
            "custom_field_2": "Value 2"
        }
    ],
    "total_pages": 10
}
```
Create Invoice
Create a new invoice.

```
POST /invoices
```
Request Body

```
{
    "invoice_number": "INV-100",
    "processed": false,
    "amount": 100.0,
    "custom_field_1": "Value 1",
    "custom_field_2": "Value 2"
}
```
Example Request
```
POST /invoices
Authorization: Bearer <token>
Content-Type: application/json

{
    "invoice_number": "INV-100",
    "processed": false,
    "amount": 100.0,
    "custom_field_1": "Value 1",
    "custom_field_2": "Value 2"
}
```
