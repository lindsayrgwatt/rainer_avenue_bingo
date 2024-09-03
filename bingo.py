import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

CARD_SIZE = 5

pdfmetrics.registerFont(TTFont('OldLondon', 'OldLondon.ttf'))
pdfmetrics.registerFont(TTFont('Garamond', 'AppleGaramond.ttf'))

# Methods to Generate Bingo Card Elements

def create_item_list(items, num_items):
    if len(items) < num_items:
        raise ValueError("Not enough unique items provided")
    return items[:num_items]

def generate_bingo_card(items):
    if len(items) < CARD_SIZE * CARD_SIZE:
        raise ValueError("Not enough unique items provided for the desired card size")

    card = random.sample(items, CARD_SIZE * CARD_SIZE)
    return [card[i * CARD_SIZE:(i + 1) * CARD_SIZE] for i in range(CARD_SIZE)]

def generate_bingo_cards(items, num_cards):
    cards = []
    for _ in range(num_cards):
        card = generate_bingo_card(items)
        cards.append(card)
    return cards
    
def create_pdf_for_card(card, filename, items):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Header
    header_text = 'Rainier Avenue'
    
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(
        name='HeaderStyle',
        parent=styles['Normal'],
        fontName='OldLondon',
        fontSize=100,
        alignment=1,
        spaceBefore=0,
        spaceAfter=0,
        leading=120
    )
    
    x=0
    header_height = 120 # 1 inch

    y = height - header_height # 0.5 inches
    header_width = width

    header = Paragraph(header_text, header_style)

    header.wrapOn(c, header_width, header_height)
    header.drawOn(c, x, y)
    
    # Playing Grid
    c.setFont("Courier", 72)
    cell_width = 72
    cell_height = 72

    grid_offset_x = 126 # 1 3/4"
    grid_offset_y = 126 # 1 3/4"

    cell_body_style = ParagraphStyle(
        name='cellBodyStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        alignment=1
    )
    cell_title_style = ParagraphStyle(
        name='cellTitleStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=72,
        alignment=1,
        leading=100 # Found by trial & error to center in square
    )
    free_cell_style = ParagraphStyle(
        name='freeCellStyle',
        parent=styles['Normal'],
        fontName='OldLondon',
        fontSize=20,
        alignment=1,
        leading=32
    )
    
    b = Paragraph('B', cell_title_style)
    i = Paragraph('I', cell_title_style)
    n = Paragraph('N', cell_title_style)
    g = Paragraph('G', cell_title_style)
    o = Paragraph('O', cell_title_style)

    data = [
        [b,i,n,g,o]
    ]

    for ii in range(CARD_SIZE):
        row = []
        for jj in range(CARD_SIZE):
            if ii == 2 and jj == 2:
                text = 'Free'
                element = Paragraph(text, free_cell_style)
            else:
                text = str(card[ii][jj])
                element = Paragraph(text, cell_body_style)
            row.append(element)
        data.append(row)

    table = Table(data, colWidths=cell_width, rowHeights=cell_height)
    
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOX', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    x = grid_offset_x
    y = height - grid_offset_y
    width_table = 5 * cell_width
    height_table = 6 * cell_width

    table.wrapOn(c, width_table, height_table)
    table.drawOn(c, x, y - height_table)
    
    # Draw lines on the table
    for i in range(CARD_SIZE+1):
        for j in range(CARD_SIZE):
            x1, y1 = grid_offset_x + j * cell_width, height - (i + 1) * cell_height - grid_offset_y
            c.rect(x1, y1, cell_width, cell_height)    
    
    # Footer
    footer_text_1 = "<para>Celebrating the things that make the Valley, <i>the Valley</i>.</para>"
    footer_text_2 = """<para>Feedback // Tile ideas // Shade <font name="Courier">@rainier_valley_bingo</font> (IG)</para>"""

    footer_style = ParagraphStyle(
        name='FooterStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        alignment=0,
        spaceBefore=0,
        spaceAfter=0,
        leading=16
    )

    # Create a Paragraph object with the defined text and style
    footer_1 = Paragraph(footer_text_1, footer_style)    
    
    x = 126
    footer_height = 120 # 1 inch

    y = 180 # 8 inches down page
    footer_width = width - 2 * x

    footer_1.wrapOn(c, header_width, header_height)
    footer_1.drawOn(c, x, y)
    
    footer_2 = Paragraph(footer_text_2, footer_style)
    y = 160

    footer_2.wrapOn(c, header_width, header_height)
    footer_2.drawOn(c, x, y)
    
    # Unused tiles
    baseline_style = ParagraphStyle(
        name='FooterStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8,
        alignment=0,
        spaceBefore=0,
        spaceAfter=0,
        leading=10
    )
    
    
    used = []
    for i in range(CARD_SIZE):
        for j in range(CARD_SIZE):
            if i != 2 and j!=2:
                used.append(card[i][j])
    
    unused = [item for item in items if item not in used]
    
    unused_string = " | ".join(unused)
    baseline_text = """<para>Slow night? Here are some more tile ideas - or add your own: <font name="Courier">"""
    baseline_text += unused_string
    baseline_text += "</font></para>"
    baseline = Paragraph(baseline_text, baseline_style)
    
    x = 36
    baseline_height = 72
    y = 72
    baseline_width = width - 2 * x
    
    baseline.wrapOn(c, baseline_width, baseline_height)
    baseline.drawOn(c, x, y)
    
    c.save()

def main():
    items = [
        "Donk aka rims worth more than car",
        "American muscle car, pre-1980",
        "Honda touring bike with really loud music",
        "Pounding bass",
        "Driving in bus lane",
        "Driving with headlights off",
        "Driving over 60 miles an hour",
        "Person randomly wandering across road mid-block",
        "Ambulance with lights & siren",
        "Police car with lights & siren",
        "Fire truck with lights & siren",
        "Person wearing clogs",
        "Car with every window tinted",
        "Car with no license plate",
        "Friday evening. I've got my best sweatpants on",
        "Bollard/ building hit by vehicle in last 24 hours",
        "Outback, Tesla and Prius in a row - any order",
        "Car with no hubcaps",
        "Person wearing mask outdoors with no one around",
        "Someone brought their dog to the bar",
        "Two adjacent #7 buses. One full. One empty",
        "Car turning but no signal",
        "Two or more people riding a lime scooter on sidewalk",
        "Lost bicyclist going up rainier",
        "Stoplight is red but my car is still going",
        "Body panel different color from main car color",
        "Visibly damaged car driving down road",
        "Spoiler way too big for car"
    ]
    num_cards = 5

    item_list = create_item_list(items, CARD_SIZE * CARD_SIZE)
    cards = generate_bingo_cards(item_list, num_cards)

    for i, card in enumerate(cards):
        filename = f"bingo_card_{i + 1}.pdf"
        create_pdf_for_card(card, filename, items)
        print(f"Generated {filename}")
        
if __name__ == "__main__":
    main()