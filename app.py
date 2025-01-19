from flask import Flask, request, render_template_string, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

# Initialize database with LC-related fields
def init_db():
    conn = sqlite3.connect('lc_management.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS lc_data (
                    id INTEGER PRIMARY KEY, 
                    lcType TEXT,
                    lcNumber TEXT, 
                    issueDate TEXT, 
                    expiryDate TEXT, 
                    expiryPlace TEXT, 
                    benificiaryDetails TEXT, 
                    amount TEXT, 
                    amountInWords TEXT, 
                    variations TEXT, 
                    bankName TEXT, 
                    bankAddress TEXT,
                    creditType TEXT,
                    usance TEXT, 
                    bank1 TEXT, 
                    bank1Address TEXT, 
                    bank2 TEXT, 
                    bank2Address TEXT, 
                    deferredPayment TEXT,
                    partialShipments TEXT,
                    transhipment TEXT,
                    shipmentFrom TEXT,
                    portDischarge TEXT,
                    latestShipmentDate TEXT,
                    goods_description TEXT,    -- Changed to TEXT (comma-separated values)
                    required_docs TEXT,        -- Changed to TEXT (comma-separated values)
                    additional_conditions TEXT, -- Changed to TEXT (comma-separated values)
                    reimbursing_bank TEXT
                )''')
    conn.commit()
    conn.close()



@app.route('/')
def index():
    return render_template_string(open('index.html').read())

@app.route('/choose', methods=['POST'])
def choose_action():
    action = request.form['action']
    if action == 'new_lc':
        return render_template('new_lc.html')
    elif action == 'show_lc':
        return redirect(url_for('show_lc'))
    elif action == 'edit_lc':
        return redirect(url_for('edit_lc'))

@app.route('/submit_lc', methods=['POST'])
def submit_lc():
    lc_data = {
        'lcType': request.form['lcType'],
        'lcNumber': request.form['lcNumber'],
        'issueDate': request.form['issueDate'],
        'expiryDate': request.form['expiryDate'],
        'expiryPlace': request.form['expiryPlace'],
        'benificiaryDetails': request.form['benificiaryDetails'],
        'amount': request.form['amount'],
        'amountInWords': request.form['amountInWords'],
        'variations': request.form['variations'],
        'bankName': request.form['bankName'],
        'bankAddress': request.form['bankAddress'],
        'creditType': request.form['creditType'],
        'usance': request.form["usance"],
        'bank1': request.form['bank1'],
        'bank1Address': request.form['bank1Address'],
        'bank2': request.form['bank2'],
        'bank2Address': request.form['bank2Address'],
        'deferredPayment': request.form['deferredPayment'],
        'partialShipments': request.form['partialShipments'],
        'transhipment': request.form['transhipment'],
        'shipmentFrom': request.form['shipmentFrom'],
        'portDischarge': request.form['portDischarge'],
        'latestShipmentDate': request.form['latestShipmentDate'],
        'goods_description': ', '.join(request.form.getlist('goods_description[]')),
        'required_docs': ', '.join(request.form.getlist('required_docs[]')),
        'additional_conditions': ', '.join(request.form.getlist('additional_conditions[]')),
        'reimbursing_bank': request.form['reimbursing_bank']
    }

    # Store in database
    conn = sqlite3.connect('lc_management.db')
    c = conn.cursor()
    c.execute('''INSERT INTO lc_data 
                (lcType, lcNumber, issueDate, expiryDate, expiryPlace, benificiaryDetails, amount, amountInWords, variations, bankName, bankAddress, creditType, usance, bank1, bank1Address, bank2, bank2Address, deferredPayment, partialShipments, transhipment, shipmentFrom, portDischarge, latestShipmentDate, goods_description, required_docs, additional_conditions ,reimbursing_bank)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              tuple(lc_data.values()))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/edit_lc')
def edit_lc():
    return render_template('drop.html')

@app.route('/show_lc')
def show_lc():
    return render_template('show_lc.html')

@app.route('/retrieve_lc', methods=['POST'])
def retrieve_lc():
    lcNumber = request.form['lcNumber']
    
    # Fetch LC details
    conn = sqlite3.connect('lc_management.db')
    c = conn.cursor()
    c.execute("SELECT * FROM lc_data WHERE lcNumber = ?", (lcNumber,))
    lc = c.fetchone()
    conn.close()
    
    if lc:
        return render_template('lc_details.html', lc=lc)
    else:
        return "<h1>LC not found!</h1><br><a href='/'>Go back to Home</a>"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)