from functools import wraps
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import jwt
import smtplib
import os
from email.mime.text import MIMEText


app = Flask(__name__)
app.config['SECRET_KEY'] = 'karios_254'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invoice.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(100), unique=True)
    processed = db.Column(db.Boolean)
    amount = db.Column(db.Float)
    custom_field_1 = db.Column(db.String(100))
    custom_field_2 = db.Column(db.String(100))
    
    def __init__(self, invoice_number, processed, amount, custom_field_1, custom_field_2):
        self.invoice_number = invoice_number
        self.processed = processed
        self.amount = amount
        self.custom_field_1 = custom_field_1
        self.custom_field_2 = custom_field_2

class InvoiceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'invoice_number', 'processed', 'amount', 'custom_field_1', 'custom_field_2')

invoice_schema = InvoiceSchema()
invoices_schema = InvoiceSchema(many=True)

def send_email(subject, message):
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    recipient_email = os.environ.get("RECIPIENT_EMAIL")

    if not all([sender_email, sender_password, recipient_email]):
        raise ValueError("Please set the SENDER_EMAIL, SENDER_PASSWORD, and RECIPIENT_EMAIL environment variables.")

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print("Error sending email: {}".format(e))
    finally:
        server.quit()


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except jwt.DecodeError:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return func(*args, **kwargs)
    
    return wrapper

@app.route('/invoices', methods=['GET'])
@token_required
def get_invoices():
    page = request.args.get('page', default=1, type=int)
    processed = request.args.get('processed', type=bool)
    search = request.args.get('search', type=str)
    invoices = Invoice.query

    if processed is not None:
        invoices = invoices.filter_by(processed=processed)
    
    if search:
        invoices = invoices.filter(Invoice.invoice_number.like("%" + search + "%"))

    paginated_invoices = invoices.paginate(page=page, per_page=25)
    result = invoices_schema.dump(paginated_invoices.items)

    return jsonify({'invoices': result, 'total_pages': paginated_invoices.pages})


@app.route('/invoices', methods=['POST'])
@token_required
def create_invoice():
    data = request.get_json()
    invoice_number = data.get('invoice_number')
    processed = data.get('processed', False)
    amount = data.get('amount')
    custom_field_1 = data.get('custom_field_1')
    custom_field_2 = data.get('custom_field_2')
    
    invoice = Invoice(invoice_number=invoice_number,
                      processed=processed,
                      amount=amount,
                      custom_field_1=custom_field_1,
                      custom_field_2=custom_field_2)

    db.session.add(invoice)
    db.session.commit()

    # send email notification
    if processed:
        send_email(to='user@example.com', subject='Invoice Processed',
                   body=f'Invoice {invoice_number} has been processed.')
    
    return invoice_schema.jsonify(invoice)

@app.route('/invoices/<int:id>', methods=['PUT'])
@token_required
def update_invoice(id):
    invoice = Invoice.query.get(id)

    if not invoice:
        return jsonify({'message': 'Invoice not found'}), 404

    data = request.get_json()
    invoice_number = data.get('invoice_number')
    processed = data.get('processed', False)
    amount = data.get('amount')
    custom_field_1 = data.get('custom_field_1')
    custom_field_2 = data.get('custom_field_2')

    invoice.invoice_number = invoice_number
    invoice.processed = processed
    invoice.amount = amount
    invoice.custom_field_1 = custom_field_1
    invoice.custom_field_2 = custom_field_2

    db.session.commit()

    return invoice_schema.jsonify(invoice)

@app.route('/invoices/<id>', methods=['DELETE'])
@token_required
def delete_invoice(id):
    invoice = Invoice.query.get(id)
    
    if not invoice:
        return jsonify({'message': 'Invoice not found'}), 404
    
    db.session.delete(invoice)
    db.session.commit()
    
    # send email notification
    send_email(to='user@example.com', subject='Invoice Deleted',
               body=f'Invoice {invoice.invoice_number} has been deleted.')
    
    return jsonify({'message': 'Invoice deleted'})


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    