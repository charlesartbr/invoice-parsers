import csv
import re
import glob
import fitz

def itau_creditcard_invoice_parser(pdf: str):

    text = ''

    with fitz.open(pdf) as doc:

        for page in doc:
            text += page.get_text()

    lines = text.split('\n')

    with open(pdf.replace('.pdf', '.csv'), 'w', newline='') as csvfile:

        fields = ['date', 'description', 'value']

        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fields)
        writer.writeheader()

        for i in range(len(lines)-1):

            if re.match(r'\d{2}/\d{2}$', lines[i]):

                date = lines[i]
                
                i += 1
                description = lines[i].replace('-CT', '').rstrip().lstrip()

                if re.match(r'.*\d{2}/\d{2}$', description):
                    d = description[-5:]
                    description = description[:-5].rstrip().lstrip() + ' - ' + d

                if '*' in description:
                    description = description.split('*').pop()

                i += 1
                value = lines[i]

                writer.writerow({ 'date': date, 'description': description, 'value': value })

files = glob.glob('*.pdf')

if len(files) == 0:
    pdf = input('PDF file: ')
    files.append(pdf)

for pdf in files:
    itau_creditcard_invoice_parser(pdf)