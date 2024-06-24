from reportlab.platypus     import Table, Image

def genHeaderTable(width, height):

    widthList = [
        width * 55 / 100, # col 1 - left image
        width * 45 / 100, # col 2 - right image
        0
    ]

    leftImgPath = 'resources\paradiseHotel.jpg'
    leftImgWidth = widthList[0]
    leftImg = Image(leftImgPath, leftImgWidth, height)

    rightImgPath = 'resources\logoParadise.png'
    rightImgWidth = widthList[1]
    rightImg = Image(
        rightImgPath, rightImgWidth, height, kind='proportional')    

    rightText = 'HOTEL'

    res = Table([
        [leftImg, rightImg, rightText]
    ],
    widthList,
    height)

    res.setStyle([
        #('GRID', (0,0), (-1,-1), 1, 'red'),

        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),

        ('ALIGN', (1,0), (1,0), 'CENTER'), # horizontal        
        ('VALIGN', (1,0), (1,0), 'MIDDLE'), # vertical   

        ('FONTSIZE', (2,0), (2,0), 20),
        ('LEFTPADDING', (2,0), (2,0), -widthList[1] + 98),     
        ('BOTTOMPADDING', (2,0), (2,0), 40),     
    ])

    return res