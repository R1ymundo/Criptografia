from fpdf import FPDF

with open('runaway.txt', 'r') as f:
    texto = f.read()

pdf = FPDF(orientation = 'P', unit = 'mm', format = 'A4')
pdf.add_page()

pdf.set_font('Arial', '', 12)

pdf.set_text_color(255, 255, 255)  # Establece el color del texto en blanco
pdf.cell(0, 10, 'Texto invisible', 0, 1)  # Imprime texto en blanco
pdf.set_text_color(0, 0, 0)  # Restaura el color del texto a negro

pdf.multi_cell(w = 0, h = 5, txt = texto, border = 0, align = 'J', fill = 0)
pdf.ln()

pdf.multi_cell(w = 0, h = 5, txt = 'Aqui va la firma', border = 0, align = 'J', fill = 0)
pdf.ln()

pdf.output('hoja.pdf')