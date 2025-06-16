REST = 0

NOTES = {
    'B3': 247, 'C4': 262, 'CS4': 277, 'D4': 294, 'DS4': 311, 'E4': 330, 'F4': 349,
    'FS4': 370, 'G4': 392, 'GS4': 415, 'A4': 440, 'AS4': 466, 'B4': 494,
    'C5': 523, 'CS5': 554, 'D5': 587, 'DS5': 622, 'E5': 659, 'F5': 698,
    'FS5': 740, 'G5': 784, 'GS5': 831, 'A5': 880, 'AS5': 932, 'B5': 988,
    'A3': 220
}

melody = [
    (NOTES['A3'], 4), (NOTES['D4'], 8), (NOTES['D4'], 4), (NOTES['FS4'], 8),
    (NOTES['B4'], 4), (NOTES['FS4'], 8), (NOTES['A4'], 4), (REST, 8),
    (NOTES['A4'], 4), (NOTES['B4'], 8), (NOTES['A4'], 4), (NOTES['FS4'], 8),
    (NOTES['G4'], 4), (NOTES['FS4'], 8), (NOTES['E4'], 4), (REST, 8),
    (NOTES['B3'], 4),
    (NOTES['E4'], 8), (NOTES['E4'], 4),
    (NOTES['G4'], 8), (NOTES['CS5'], 4),
    (NOTES['CS5'], 8), (NOTES['B4'], 4),
    (NOTES['A4'], 8),
    (NOTES['G4'], -4),
    (NOTES['G4'], 4),
    (NOTES['FS4'], 8), (NOTES['B3'], 4),
    (NOTES['CS4'], 4), (NOTES['D4'], 4), (NOTES['E4'], 4),

    (REST, 4),

    (NOTES['A3'], 4), (NOTES['D4'], 8), (NOTES['D4'], 4), (NOTES['FS4'], 8),
    (NOTES['B4'], 4), (NOTES['FS4'], 8), (NOTES['A4'], 4), (REST, 8),
    (NOTES['A4'], 4), (NOTES['B4'], 8), (NOTES['A4'], 4), (NOTES['FS4'], 8),
    (NOTES['G4'], 4), (NOTES['FS4'], 8), (NOTES['E4'], 4), (REST, 8),
    (NOTES['B3'], 4),
    (NOTES['E4'], 8), (NOTES['E4'], 4),
    (NOTES['G4'], 8), (NOTES['CS5'], 4),
    (NOTES['CS5'], 8), (NOTES['B4'], 4),
    (NOTES['A4'], 8),
    (NOTES['G4'], -4),
    (NOTES['G4'], 4),
    (NOTES['FS4'], 8), (NOTES['E4'], 8),
    (NOTES['CS4'], 4), (NOTES['E4'], 4), (NOTES['D4'], 4),
    (REST, 4),

    (NOTES['B4'], 4), (REST, 8), (NOTES['B4'], 4), (NOTES['A4'], 8), (NOTES['G4'], 8),
    (NOTES['A4'], 8), (NOTES['B4'], 8), (NOTES['A4'], 8), (REST, 4), (NOTES['E4'], 4),
    (NOTES['FS4'], 8), (NOTES['GS4'], 4), (NOTES['E4'], 8), (NOTES['A4'], 4),
    (REST, 2),

    (NOTES['B4'], 4), (REST, 8),
    (NOTES['A4'], 4), (REST, 8),
    (NOTES['G4'], 4), (REST, 2),
    (NOTES['E4'], 4), (NOTES['E4'], 8), (NOTES['CS5'], 8), (REST, 8),
    (NOTES['B4'], 8), (NOTES['A4'], 8), (REST, 8),
    (NOTES['B4'], 8), (NOTES['A4'], 8), (REST, 8),
    (NOTES['G4'], 8), (REST, -4),

    (NOTES['A4'], 8), (REST, 8), (NOTES['B4'], 8), (NOTES['FS4'], 2),
    (NOTES['E4'], 8), (NOTES['D4'], 2),
]

tempo = 180
