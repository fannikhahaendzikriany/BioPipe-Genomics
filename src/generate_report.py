"""
Script pembuatan laporan PDF mini project BIF1223
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image, PageBreak
)
from reportlab.platypus import KeepTogether

# ── Path setup ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'output')
DOCS_DIR   = os.path.join(BASE_DIR, '..', 'docs')
VIZ_PATH   = os.path.join(OUTPUT_DIR, 'gc_analysis_visualization.png')

os.makedirs(DOCS_DIR, exist_ok=True)
PDF_PATH = os.path.join(DOCS_DIR, 'laporan_mini_project.pdf')

# ── Warna tema ──
DARK_BLUE   = colors.HexColor('#1a3a5c')
MID_BLUE    = colors.HexColor('#2980b9')
LIGHT_BLUE  = colors.HexColor('#d6eaf8')
ACCENT      = colors.HexColor('#27ae60')
LIGHT_GRAY  = colors.HexColor('#f2f3f4')
DARK_GRAY   = colors.HexColor('#5d6d7e')
RED_ACCENT  = colors.HexColor('#c0392b')

def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle('CoverTitle',
        fontSize=20, fontName='Helvetica-Bold',
        textColor=DARK_BLUE, alignment=TA_CENTER,
        leading=26, spaceAfter=6))

    styles.add(ParagraphStyle('CoverSubtitle',
        fontSize=13, fontName='Helvetica',
        textColor=MID_BLUE, alignment=TA_CENTER,
        leading=18, spaceAfter=4))

    styles.add(ParagraphStyle('CoverInfo',
        fontSize=10, fontName='Helvetica',
        textColor=DARK_GRAY, alignment=TA_CENTER,
        leading=14, spaceAfter=2))

    styles.add(ParagraphStyle('SectionHead',
        fontSize=13, fontName='Helvetica-Bold',
        textColor=DARK_BLUE, spaceBefore=14, spaceAfter=6,
        borderPad=4))

    styles.add(ParagraphStyle('SubHead',
        fontSize=11, fontName='Helvetica-Bold',
        textColor=MID_BLUE, spaceBefore=8, spaceAfter=4))

    styles.add(ParagraphStyle('BodyJ',
        fontSize=10, fontName='Helvetica',
        leading=16, alignment=TA_JUSTIFY,
        textColor=colors.black, spaceAfter=6))

    styles.add(ParagraphStyle('CodeBlock',
        fontSize=8.5, fontName='Courier',
        leading=13, textColor=colors.HexColor('#2c3e50'),
        backColor=LIGHT_GRAY, leftIndent=10, rightIndent=10,
        spaceBefore=4, spaceAfter=4, borderPad=6))

    styles.add(ParagraphStyle('Caption',
        fontSize=9, fontName='Helvetica-Oblique',
        textColor=DARK_GRAY, alignment=TA_CENTER, spaceAfter=6))

    styles.add(ParagraphStyle('BulletBody',
        fontSize=10, fontName='Helvetica',
        leading=15, leftIndent=16, spaceAfter=3,
        textColor=colors.black, bulletIndent=4))

    return styles


def make_section_header(title, styles):
    """Membuat header seksi dengan garis biru."""
    return [
        Paragraph(title, styles['SectionHead']),
        HRFlowable(width='100%', thickness=2, color=MID_BLUE, spaceAfter=6)
    ]


def make_info_table(data_rows, col_widths=None):
    """Tabel info berstruktur (label: value)."""
    if col_widths is None:
        col_widths = [5*cm, 11*cm]
    tbl = Table(data_rows, colWidths=col_widths)
    tbl.setStyle(TableStyle([
        ('BACKGROUND',  (0, 0), (0, -1), LIGHT_BLUE),
        ('FONTNAME',    (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE',    (0, 0), (-1, -1), 9.5),
        ('TEXTCOLOR',   (0, 0), (0, -1), DARK_BLUE),
        ('TEXTCOLOR',   (1, 0), (1, -1), colors.black),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, LIGHT_GRAY]),
        ('GRID',        (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',(0, 0), (-1, -1), 8),
        ('TOPPADDING',  (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 5),
        ('VALIGN',      (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return tbl


def build_pdf():
    styles = build_styles()
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.2*cm, bottomMargin=2.2*cm,
        title='Laporan Mini Project BIF1223',
        author='Mahasiswa Bioinformatika IPB'
    )

    story = []
    W = A4[0] - 5*cm   # usable width

    # ════════════════════════════════════════════════════
    # COVER PAGE
    # ════════════════════════════════════════════════════
    cover_header = Table(
        [['LAPORAN MINI PROJECT\nSTRUKTUR DATA BIOINFORMATIKA']],
        colWidths=[W]
    )
    cover_header.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), DARK_BLUE),
        ('TEXTCOLOR',     (0,0), (-1,-1), colors.white),
        ('FONTNAME',      (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 16),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 18),
        ('BOTTOMPADDING', (0,0), (-1,-1), 18),
        ('ROWBACKGROUNDS',(0,0), (-1,-1), [DARK_BLUE]),
    ]))
    story.append(cover_header)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph(
        'BioPipe-Genomics: Pipeline Analisis Komposisi Nukleotida<br/>dan Visualisasi GC Content pada Sekuens Genomik',
        styles['CoverTitle']
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width='60%', thickness=1.5, color=ACCENT, hAlign='CENTER'))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph(
        '<i>Mycobacterium tuberculosis</i> H37Rv<br/>'
        'Sumber: NCBI Nucleotide Database (NC_000962.3)',
        styles['CoverSubtitle']
    ))
    story.append(Spacer(1, 0.8*cm))

    identity_data = [
        ['Mata Kuliah',  'Struktur Data Bioinformatika (BIF1223)'],
        ['Pertemuan',    '#15 – Integrasi Struktur Data untuk Pipeline Analisis'],
        ['Dosen',        'Toto Haryanto'],
        ['Institusi',    'IPB University, Bogor, Indonesia'],
        ['Tanggal',      '27 Juni 2026'],
        ['GitHub',       'https://github.com/<username>/BioPipe-Genomics'],
    ]
    story.append(make_info_table(identity_data))
    story.append(Spacer(1, 0.6*cm))

    story.append(HRFlowable(width='100%', thickness=1, color=LIGHT_BLUE))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '<b>Abstrak.</b> Laporan ini menyajikan implementasi pipeline bioinformatika sederhana '
        'yang mengintegrasikan struktur data List dan Dictionary dalam bahasa Python untuk '
        'menganalisis komposisi nukleotida sekuens genomik <i>Mycobacterium tuberculosis</i> H37Rv. '
        'Pipeline mencakup pembacaan file FASTA, penghitungan frekuensi basa, perhitungan '
        'GC Content dan GC Skew, pengurutan sekuens, visualisasi multi-panel dengan Matplotlib, '
        'serta ekspor hasil ke file CSV. Hasil menunjukkan rata-rata GC Content sebesar 83,36% '
        'yang konsisten dengan karakter genomik <i>M. tuberculosis</i> sebagai organisme kaya-GC.',
        styles['BodyJ']
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════
    # BAB 1 – PENDAHULUAN
    # ════════════════════════════════════════════════════
    story += make_section_header('1. Pendahuluan', styles)

    story.append(Paragraph(
        '<b>1.1 Latar Belakang</b>',
        styles['SubHead']
    ))
    story.append(Paragraph(
        '<i>Mycobacterium tuberculosis</i> (Mtb) H37Rv adalah agen penyebab tuberkulosis (TB) '
        'yang menjadi salah satu penyakit infeksi paling mematikan di dunia. Secara genomik, '
        'Mtb memiliki karakteristik yang sangat khas: kandungan G+C (GC Content) yang sangat '
        'tinggi, berkisar antara 65–67% pada genom lengkapnya. Tingginya GC Content ini '
        'berkorelasi dengan stabilitas termal DNA yang lebih besar dan kompleksitas ekspresi '
        'gen, menjadikan Mtb subjek yang menarik untuk analisis komposisi nukleotida.',
        styles['BodyJ']
    ))
    story.append(Paragraph(
        'Dalam konteks pembelajaran Struktur Data Bioinformatika, analisis pipeline berbasis '
        'Python memberikan kesempatan untuk mengaplikasikan struktur data fundamental — '
        'khususnya List dan Dictionary — dalam konteks biologis yang nyata. Pipeline ini '
        'mencerminkan alur kerja bioinformatika standar: dari pembacaan data mentah (FASTA) '
        'hingga visualisasi dan pelaporan hasil.',
        styles['BodyJ']
    ))

    story.append(Paragraph('<b>1.2 Tujuan</b>', styles['SubHead']))
    tujuan_items = [
        'Membaca dan memproses file FASTA menggunakan struktur data List dalam Python.',
        'Menghitung frekuensi setiap nukleotida (A, T, G, C) dengan menggunakan Dictionary.',
        'Menghitung GC Content dan GC Skew untuk setiap sekuens.',
        'Mengurutkan sekuens berdasarkan GC Content secara descending.',
        'Menampilkan 3 sekuens dengan GC Content tertinggi.',
        'Menghasilkan visualisasi multi-panel menggunakan Matplotlib.',
        'Mengekspor hasil analisis ke file CSV.',
    ]
    for item in tujuan_items:
        story.append(Paragraph(f'• {item}', styles['BulletBody']))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('<b>1.3 Organisme dan Sumber Data</b>', styles['SubHead']))
    org_data = [
        ['Nama Organisme', 'Mycobacterium tuberculosis H37Rv'],
        ['Accession NCBI', 'NC_000962.3'],
        ['Tipe Data',      'File FASTA (sekuens DNA double-stranded)'],
        ['Ukuran Genom',   '~4.41 Mb (4.411.532 bp)'],
        ['GC Content Ref', '~65.6% (literatur Cole et al. 1998)'],
        ['Relevansi',      'Patogen TB; organisme kaya-GC; model genomik bakteri'],
    ]
    story.append(make_info_table(org_data))
    story.append(Spacer(1, 0.4*cm))

    # ════════════════════════════════════════════════════
    # BAB 2 – METODOLOGI
    # ════════════════════════════════════════════════════
    story.append(PageBreak())
    story += make_section_header('2. Metodologi', styles)

    story.append(Paragraph('<b>2.1 Alur Pipeline</b>', styles['SubHead']))
    story.append(Paragraph(
        'Pipeline diimplementasikan sebagai skrip Python modular dengan enam tahap utama yang '
        'dieksekusi secara sekuensial. Setiap tahap dirancang dengan fungsi terpisah untuk '
        'memastikan keterbacaan (readability) dan kemudahan pengujian (testability).',
        styles['BodyJ']
    ))

    pipeline_data = [
        ['Tahap', 'Fungsi', 'Struktur Data', 'Output'],
        ['1', 'read_fasta()', 'List of Dict', 'List sekuens'],
        ['2', 'calculate_nucleotide_frequency()', 'Dictionary', 'Frekuensi A/T/G/C'],
        ['3', 'calculate_gc_content() / gc_skew()', 'Float', 'GC%, GC Skew'],
        ['4', 'sort_by_gc_content()', 'sorted() + List', 'List terurut'],
        ['5', 'get_top_sequences()', 'List slicing', 'Top-3 sekuens'],
        ['6a', 'visualize_results()', 'Matplotlib', 'PNG 3-panel'],
        ['6b', 'write_to_csv()', 'csv.DictWriter', 'File CSV'],
    ]
    tbl2 = Table(pipeline_data, colWidths=[1.5*cm, 5.5*cm, 4*cm, 5*cm])
    tbl2.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), DARK_BLUE),
        ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
        ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 8.5),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.white, LIGHT_GRAY]),
        ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#bdc3c7')),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('TOPPADDING',    (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ALIGN',         (0,0), (-1,-1), 'LEFT'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(tbl2)
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph('<b>2.2 Struktur Data List</b>', styles['SubHead']))
    story.append(Paragraph(
        'List Python digunakan sebagai wadah utama untuk menyimpan seluruh sekuens yang '
        'dibaca dari file FASTA. Setiap elemen list adalah sebuah Dictionary yang berisi '
        'atribut: <i>id</i> (identifier sekuens), <i>description</i> (deskripsi header), '
        'dan <i>sequence</i> (string basa nukleotida). Pemilihan List memungkinkan '
        'pengindeksan O(1), iterasi O(n), dan operasi sorting in-place atau menggunakan '
        '<i>sorted()</i> untuk menghasilkan salinan terurut.',
        styles['BodyJ']
    ))

    story.append(Paragraph(
        'Contoh deklarasi dan pengisian List:',
        styles['BodyJ']
    ))
    story.append(Paragraph(
        'sequences: list[dict] = []<br/>'
        'sequences.append({\'id\': current_id,<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;\'description\': current_desc,<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;\'sequence\': \'\'.join(current_seq).upper()})',
        styles['CodeBlock']
    ))

    story.append(Paragraph('<b>2.3 Struktur Data Dictionary</b>', styles['SubHead']))
    story.append(Paragraph(
        'Dictionary Python digunakan untuk menghitung frekuensi nukleotida karena '
        'memberikan akses O(1) untuk operasi baca dan tulis. Setiap nukleotida ('
        'A, T, G, C, dan karakter lain) menjadi kunci, sedangkan jumlah kemunculannya '
        'menjadi nilai. Pendekatan ini lebih efisien dibandingkan menggunakan empat '
        'variabel integer terpisah karena memungkinkan ekstensibilitas ke alfabet '
        'nukleotida yang lebih luas (misal: U untuk RNA).',
        styles['BodyJ']
    ))
    story.append(Paragraph(
        'freq: dict = {\'A\': 0, \'T\': 0, \'G\': 0, \'C\': 0, \'other\': 0}<br/>'
        'for nucleotide in sequence:<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;if nucleotide in freq:<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;freq[nucleotide] += 1',
        styles['CodeBlock']
    ))

    story.append(Paragraph('<b>2.4 Rumus GC Content dan GC Skew</b>', styles['SubHead']))
    story.append(Paragraph(
        'GC Content dihitung menggunakan rumus standar:',
        styles['BodyJ']
    ))
    story.append(Paragraph(
        'GC% = (G + C) / (A + T + G + C) x 100%',
        styles['CodeBlock']
    ))
    story.append(Paragraph(
        'GC Skew merupakan metrik tambahan untuk mendeteksi asimetri komposisi '
        'antara dua untai DNA, yang berguna untuk mengidentifikasi ori (origin of replication):',
        styles['BodyJ']
    ))
    story.append(Paragraph(
        'GC Skew = (G - C) / (G + C)',
        styles['CodeBlock']
    ))
    story.append(Paragraph(
        'Nilai GC Skew positif mengindikasikan leading strand (G > C), sedangkan '
        'nilai negatif mengindikasikan lagging strand. Transisi antara positif dan '
        'negatif menandai lokasi ori dan ter pada kromosom bakteri (Lobry, 1996).',
        styles['BodyJ']
    ))

    story.append(Paragraph('<b>2.5 Algoritma Sorting</b>', styles['SubHead']))
    story.append(Paragraph(
        'Pengurutan list hasil analisis dilakukan menggunakan fungsi built-in '
        '<i>sorted()</i> Python yang mengimplementasikan algoritma Timsort (kompleksitas '
        'O(n log n) worst-case, O(n) best-case). Key function mengekstrak nilai '
        '<i>gc_content</i> dari setiap dictionary, dan parameter <i>reverse=True</i> '
        'menghasilkan urutan descending (GC tertinggi di posisi pertama):',
        styles['BodyJ']
    ))
    story.append(Paragraph(
        'sorted_results = sorted(results,<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;key=lambda x: x[\'gc_content\'],<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;reverse=True)',
        styles['CodeBlock']
    ))

    # ════════════════════════════════════════════════════
    # BAB 3 – HASIL
    # ════════════════════════════════════════════════════
    story.append(PageBreak())
    story += make_section_header('3. Hasil dan Analisis', styles)

    story.append(Paragraph('<b>3.1 Statistik Keseluruhan</b>', styles['SubHead']))
    stat_data = [
        ['Parameter', 'Nilai'],
        ['Total sekuens dianalisis', '10 sekuens'],
        ['Total panjang sekuens', '3.507 bp (10 region)'],
        ['GC Content tertinggi', '89,43% (NC_000962.3_1, _2, _5)'],
        ['GC Content terendah', '33,05% (NC_000962.3_9 – region kaya-AT)'],
        ['Rata-rata GC Content', '83,36%'],
        ['Rata-rata GC Skew', '+0,109 (predominan leading strand)'],
    ]
    story.append(make_info_table(stat_data))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph('<b>3.2 Tabel Hasil Analisis (Semua Sekuens – Terurut Descending)</b>', styles['SubHead']))

    result_header = ['Rank', 'Sequence ID', 'Length', 'A', 'T', 'G', 'C', 'GC%', 'AT%', 'GC Skew']
    result_rows = [
        ['1', 'NC_000962.3_1', '350', '28', '9',  '170','143','89.43','10.57','0.0863'],
        ['2', 'NC_000962.3_2', '350', '27', '10', '172','141','89.43','10.57','0.0990'],
        ['3', 'NC_000962.3_5', '350', '28', '9',  '172','141','89.43','10.57','0.0990'],
        ['4', 'NC_000962.3_3', '350', '28', '10', '171','141','89.14','10.86','0.0897'],
        ['5', 'NC_000962.3_10','350', '27', '10', '170','143','89.14','10.86','0.1026'],
        ['6', 'NC_000962.3_4', '350', '28', '11', '171','140','88.86','11.14','0.0932'],
        ['7', 'NC_000962.3_8', '350', '28', '11', '171','140','88.86','11.14','0.0932'],
        ['8', 'NC_000962.3_7', '350', '28', '12', '171','139','88.57','11.43','0.0968'],
        ['9', 'NC_000962.3_6', '350', '27', '16', '171','136','87.71','12.29','0.1010'],
        ['10','NC_000962.3_9', '357', '138','101','58', '60', '33.05','66.95','0.2542'],
    ]

    tbl3 = Table([result_header] + result_rows,
                 colWidths=[1*cm, 4.2*cm, 1.5*cm, 1*cm, 1*cm,
                            1*cm, 1*cm, 1.5*cm, 1.5*cm, 2.3*cm])
    tbl3.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), DARK_BLUE),
        ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
        ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
        ('BACKGROUND',    (0,1), (-1,3), colors.HexColor('#d5f5e3')),
        ('FONTNAME',      (0,1), (-1,3), 'Helvetica-Bold'),
        ('BACKGROUND',    (0,10), (-1,10), colors.HexColor('#fde8e8')),
        ('ROWBACKGROUNDS',(0,4), (-1,9), [colors.white, LIGHT_GRAY]),
        ('FONTSIZE',      (0,0), (-1,-1), 8),
        ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#bdc3c7')),
        ('LEFTPADDING',   (0,0), (-1,-1), 5),
        ('RIGHTPADDING',  (0,0), (-1,-1), 5),
        ('TOPPADDING',    (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(tbl3)
    story.append(Paragraph(
        '<i>Catatan: Hijau = Top 3 sekuens terbaik (GC tertinggi). '
        'Merah = sekuens kaya-AT (region kontrol/intergenik).</i>',
        styles['Caption']
    ))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph('<b>3.3 Visualisasi Hasil</b>', styles['SubHead']))
    if os.path.exists(VIZ_PATH):
        img = Image(VIZ_PATH, width=W, height=W * 0.38)
        story.append(img)
        story.append(Paragraph(
            '<b>Gambar 1.</b> Visualisasi multi-panel hasil analisis GC Content. '
            '(a) Bar chart GC Content per sekuens dengan garis rata-rata. '
            '(b) Komposisi nukleotida A/T/G/C dalam persen (stacked bar). '
            '(c) Scatter plot GC Content vs GC Skew untuk identifikasi bias replikasi.',
            styles['Caption']
        ))
    story.append(Spacer(1, 0.3*cm))

    # ════════════════════════════════════════════════════
    # BAB 4 – PEMBAHASAN
    # ════════════════════════════════════════════════════
    story += make_section_header('4. Pembahasan', styles)

    story.append(Paragraph('<b>4.1 Interpretasi GC Content</b>', styles['SubHead']))
    story.append(Paragraph(
        'Rata-rata GC Content sebesar 83,36% pada 10 region yang dianalisis '
        'melampaui nilai referensi genom lengkap Mtb (~65,6%). Hal ini dapat '
        'dijelaskan oleh fakta bahwa region yang dipilih merupakan sekuens '
        'coding yang kaya akan kodon GCC (Alanin) dan GCG (Alanin), '
        'mencerminkan preferensi kodon yang umum dijumpai pada organisme '
        'dengan GC Content tinggi. Temuan ini konsisten dengan karakteristik '
        'genomik Mtb sebagai salah satu patogen dengan bias GC paling tinggi '
        'di antara bakteri patogen manusia.',
        styles['BodyJ']
    ))
    story.append(Paragraph(
        'Satu-satunya outlier adalah region NC_000962.3_9 dengan GC Content '
        '33,05% — jauh di bawah rata-rata. Region ini kemungkinan merupakan '
        'sekuens intergenik, IS element (insertion sequence), atau repeat '
        'region yang memiliki komposisi kaya-AT. Daerah kaya-AT pada Mtb '
        'sering dikaitkan dengan promoter dan elemen regulatori yang '
        'membutuhkan fleksibilitas lokal DNA untuk pengikatan protein.',
        styles['BodyJ']
    ))

    story.append(Paragraph('<b>4.2 Interpretasi GC Skew</b>', styles['SubHead']))
    story.append(Paragraph(
        'Nilai GC Skew yang konsisten positif (+0,08 hingga +0,10) pada '
        'sebagian besar region menunjukkan bahwa G lebih sering muncul '
        'daripada C pada untai yang dianalisis. Ini mengindikasikan bahwa '
        'region-region tersebut terletak predominantly pada leading strand '
        'replikasi. Nilai GC Skew yang lebih tinggi pada region_9 (+0,2542) '
        'merupakan artefak dari GC Content yang rendah, bukan indikasi '
        'aktual tentang posisi origin of replication.',
        styles['BodyJ']
    ))

    story.append(Paragraph('<b>4.3 Signifikansi Biologis dan Klinis</b>', styles['SubHead']))
    story.append(Paragraph(
        'Tingginya GC Content pada <i>M. tuberculosis</i> memiliki implikasi biologis '
        'dan klinis yang signifikan: (1) <b>Stabilitas Termal:</b> Pasangan basa G-C '
        'membentuk tiga ikatan hidrogen (vs dua pada A-T), memberikan DNA '
        'stabilitas termal yang lebih tinggi — menguntungkan bagi bakteri yang '
        'hidup dalam lingkungan dengan suhu bervariasi. (2) <b>Resistensi Antibiotik:</b> '
        'Region kaya GC sering mengandung gen yang mengkode enzim modifikasi '
        'antibiotik, berkontribusi pada resistensi multi-obat (MDR-TB). '
        '(3) <b>Diagnostik:</b> GC Content yang tinggi memengaruhi kondisi PCR '
        '(suhu annealing lebih tinggi), penting untuk desain primer diagnostik TB.',
        styles['BodyJ']
    ))

    # ════════════════════════════════════════════════════
    # BAB 5 – KESIMPULAN
    # ════════════════════════════════════════════════════
    story += make_section_header('5. Kesimpulan', styles)

    story.append(Paragraph(
        'Pipeline BioPipe-Genomics berhasil mengimplementasikan analisis komposisi '
        'nukleotida secara end-to-end menggunakan struktur data List dan Dictionary '
        'dalam Python. Dari 10 sekuens <i>Mycobacterium tuberculosis</i> H37Rv yang '
        'dianalisis, diperoleh rata-rata GC Content sebesar 83,36% dengan tiga '
        'sekuens terbaik (NC_000962.3_1, _2, _5) mencapai 89,43%. Nilai GC Skew '
        'yang predominan positif mengkonfirmasi lokasi region pada leading strand '
        'replikasi. Pipeline ini mendemonstrasikan bagaimana struktur data fundamental '
        '— List untuk penyimpanan sekuensial dan Dictionary untuk penghitungan '
        'frekuensi — dapat diintegrasikan secara efektif dalam alur kerja '
        'bioinformatika berbasis Python yang lengkap.',
        styles['BodyJ']
    ))
    story.append(Spacer(1, 0.3*cm))

    # ════════════════════════════════════════════════════
    # REFERENSI
    # ════════════════════════════════════════════════════
    story += make_section_header('Referensi', styles)

    refs = [
        'Cole, S.T., et al. (1998). Deciphering the biology of <i>Mycobacterium tuberculosis</i> '
        'from the complete genome sequence. <i>Nature</i>, 393, 537–544. '
        'https://doi.org/10.1038/31159',
        'Lobry, J.R. (1996). Asymmetric substitution patterns in the two DNA strands of bacteria. '
        '<i>Molecular Biology and Evolution</i>, 13(5), 660–665.',
        'NCBI Nucleotide Database. <i>Mycobacterium tuberculosis</i> H37Rv, complete genome. '
        'Accession: NC_000962.3. https://www.ncbi.nlm.nih.gov/nuccore/NC_000962.3',
        'Hunter, J.D. (2007). Matplotlib: A 2D graphics environment. '
        '<i>Computing in Science and Engineering</i>, 9(3), 90–95.',
        'Haryanto, T. (2026). Integrasi Struktur Data untuk Pipeline Analisis Sederhana. '
        'Bahan Ajar Pertemuan #15, BIF1223 – IPB University.',
    ]
    for i, ref in enumerate(refs, 1):
        story.append(Paragraph(f'[{i}] {ref}', styles['BulletBody']))
        story.append(Spacer(1, 0.15*cm))

    # ── Build ──
    doc.build(story)
    print(f"[OK] Laporan PDF berhasil dibuat: {PDF_PATH}")
    return PDF_PATH


if __name__ == '__main__':
    build_pdf()
