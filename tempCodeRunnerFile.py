lymer':
                    if thiscomputer == 'DESKTOP-473QAMH':
                        base = r'C:\Users\tim\OneDrive\Documents\Python\charts'
                        quenchfile = PdfPages(base + f'\\{filedate}_{thischartlabel} Trend.pdf')
                    else:
                        quenchbase = r'K:\Quality - Records\8512 - Validation and Control of Special Processes\Heat Treat\Quench Tank'
                        quenchfile = PdfPages(quenchbase + f'\\{filedate}_{thischartlabel} Trend.pdf')   