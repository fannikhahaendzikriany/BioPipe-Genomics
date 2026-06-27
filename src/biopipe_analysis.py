"""
BioPipe-Genomics: Pipeline Analisis Komposisi Nukleotida dan Visualisasi GC Content
====================================================================================
Mata Kuliah : Struktur Data Bioinformatika (BIF1223)
Organisme   : Mycobacterium tuberculosis H37Rv
Sumber Data : NCBI (https://www.ncbi.nlm.nih.gov/nuccore/NC_000962.3)

Struktur Data yang Digunakan:
  - List    : Menyimpan seluruh sekuens hasil pembacaan file FASTA
  - Dictionary : Menghitung frekuensi nukleotida per sekuens
  - Sorting : Mengurutkan sekuens berdasarkan nilai GC Content (descending)
"""

import csv
import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime


# ─────────────────────────────────────────────
# 1. MEMBACA FILE FASTA → MENYIMPAN DALAM LIST
# ─────────────────────────────────────────────

def read_fasta(filepath: str) -> list[dict]:
    """
    Membaca file FASTA dan menyimpan setiap sekuens ke dalam List of Dictionary.
    Setiap elemen list berisi: {'id': str, 'description': str, 'sequence': str}

    Parameter:
        filepath (str): Path ke file FASTA

    Return:
        sequences (list): List berisi dictionary tiap sekuens
    """
    sequences: list[dict] = []  # ← Struktur Data: LIST

    if not os.path.exists(filepath):
        print(f"[ERROR] File tidak ditemukan: {filepath}")
        sys.exit(1)

    with open(filepath, 'r') as fasta_file:
        current_id = None
        current_desc = ""
        current_seq = []

        for line in fasta_file:
            line = line.strip()
            if not line:
                continue

            if line.startswith('>'):
                # Simpan sekuens sebelumnya jika ada
                if current_id is not None:
                    sequences.append({
                        'id': current_id,
                        'description': current_desc,
                        'sequence': ''.join(current_seq).upper()
                    })
                # Parse header baru
                header = line[1:]
                parts = header.split(' ', 1)
                current_id = parts[0]
                current_desc = parts[1] if len(parts) > 1 else ""
                current_seq = []
            else:
                current_seq.append(line)

        # Simpan sekuens terakhir
        if current_id is not None:
            sequences.append({
                'id': current_id,
                'description': current_desc,
                'sequence': ''.join(current_seq).upper()
            })

    print(f"[INFO] Berhasil membaca {len(sequences)} sekuens dari file FASTA.")
    return sequences


# ────────────────────────────────────────────────────────────────
# 2. MENGHITUNG FREKUENSI NUKLEOTIDA MENGGUNAKAN DICTIONARY
# ────────────────────────────────────────────────────────────────

def calculate_nucleotide_frequency(sequence: str) -> dict:
    """
    Menghitung frekuensi setiap nukleotida (A, T, G, C) menggunakan Dictionary.

    Parameter:
        sequence (str): String sekuens DNA

    Return:
        freq (dict): Dictionary {'A': int, 'T': int, 'G': int, 'C': int, 'other': int}
    """
    freq: dict = {'A': 0, 'T': 0, 'G': 0, 'C': 0, 'other': 0}  # ← Struktur Data: DICTIONARY

    for nucleotide in sequence:
        if nucleotide in freq:
            freq[nucleotide] += 1
        else:
            freq['other'] += 1

    return freq


def calculate_gc_content(freq: dict) -> float:
    """
    Menghitung persentase GC Content dari dictionary frekuensi nukleotida.
    Formula: GC% = (G + C) / (A + T + G + C) × 100

    Parameter:
        freq (dict): Dictionary frekuensi nukleotida

    Return:
        gc_percent (float): Persentase GC Content
    """
    total = freq['A'] + freq['T'] + freq['G'] + freq['C']
    if total == 0:
        return 0.0
    gc_percent = (freq['G'] + freq['C']) / total * 100
    return round(gc_percent, 2)


def calculate_gc_skew(freq: dict) -> float:
    """
    Menghitung GC Skew: (G - C) / (G + C)
    Berguna untuk mengidentifikasi asal replikasi pada genom bakteri.

    Parameter:
        freq (dict): Dictionary frekuensi nukleotida

    Return:
        gc_skew (float): Nilai GC Skew
    """
    g_plus_c = freq['G'] + freq['C']
    if g_plus_c == 0:
        return 0.0
    gc_skew = (freq['G'] - freq['C']) / g_plus_c
    return round(gc_skew, 4)


# ────────────────────────────────────────────────────────────────
# 3. ANALISIS LENGKAP PER SEKUENS (INTEGRASI LIST + DICTIONARY)
# ────────────────────────────────────────────────────────────────

def analyze_sequences(sequences: list[dict]) -> list[dict]:
    """
    Melakukan analisis lengkap untuk setiap sekuens:
    menghitung frekuensi nukleotida, GC Content, GC Skew, dan panjang sekuens.

    Parameter:
        sequences (list): List sekuens hasil read_fasta()

    Return:
        results (list): List berisi hasil analisis lengkap
    """
    results: list[dict] = []  # ← Struktur Data: LIST

    for seq_record in sequences:
        seq_id = seq_record['id']
        description = seq_record['description']
        sequence = seq_record['sequence']

        # Hitung frekuensi menggunakan Dictionary
        freq = calculate_nucleotide_frequency(sequence)

        # Hitung GC Content dan GC Skew
        gc_content = calculate_gc_content(freq)
        gc_skew = calculate_gc_skew(freq)
        length = len(sequence)

        results.append({
            'id': seq_id,
            'description': description,
            'length': length,
            'A': freq['A'],
            'T': freq['T'],
            'G': freq['G'],
            'C': freq['C'],
            'gc_content': gc_content,
            'gc_skew': gc_skew,
            'at_content': round(100 - gc_content, 2)
        })

        print(f"  → {seq_id}: GC={gc_content}% | len={length} bp | GC Skew={gc_skew}")

    return results


# ────────────────────────────────────────────────────────────────
# 4. MENGURUTKAN SEKUENS BERDASARKAN GC CONTENT (SORTING)
# ────────────────────────────────────────────────────────────────

def sort_by_gc_content(results: list[dict], ascending: bool = False) -> list[dict]:
    """
    Mengurutkan list hasil analisis berdasarkan nilai GC Content.
    Menggunakan built-in sorted() dengan key function (Timsort – O(n log n)).

    Parameter:
        results (list)  : List hasil analisis
        ascending (bool): True = ascending, False = descending (default)

    Return:
        sorted_results (list): List terurut
    """
    sorted_results = sorted(results, key=lambda x: x['gc_content'], reverse=not ascending)
    print(f"\n[INFO] Sekuens telah diurutkan berdasarkan GC Content ({'ascending' if ascending else 'descending'}).")
    return sorted_results


# ────────────────────────────────────────────────────────────────
# 5. MENAMPILKAN 3 SEKUENS TERBAIK (GC CONTENT TERTINGGI)
# ────────────────────────────────────────────────────────────────

def get_top_sequences(sorted_results: list[dict], n: int = 3) -> list[dict]:
    """
    Mengambil n sekuens teratas berdasarkan GC Content tertinggi.

    Parameter:
        sorted_results (list): List terurut (descending by GC)
        n (int): Jumlah sekuens terbaik (default = 3)

    Return:
        top_n (list): List berisi n sekuens terbaik
    """
    top_n = sorted_results[:n]

    print(f"\n{'='*60}")
    print(f"  TOP {n} SEKUENS BERDASARKAN GC CONTENT TERTINGGI")
    print(f"{'='*60}")
    for rank, seq in enumerate(top_n, start=1):
        print(f"  #{rank}  ID      : {seq['id']}")
        print(f"       Desc    : {seq['description'][:60]}...")
        print(f"       Length  : {seq['length']} bp")
        print(f"       GC (%)  : {seq['gc_content']}%")
        print(f"       AT (%)  : {seq['at_content']}%")
        print(f"       GC Skew : {seq['gc_skew']}")
        print(f"       A={seq['A']} | T={seq['T']} | G={seq['G']} | C={seq['C']}")
        print(f"  {'-'*55}")

    return top_n


# ────────────────────────────────────────────────────────────────
# 6. VISUALISASI GRAFIK GC CONTENT (MATPLOTLIB)
# ────────────────────────────────────────────────────────────────

def visualize_results(sorted_results: list[dict], output_dir: str) -> str:
    """
    Membuat 3 panel visualisasi:
      (a) Bar Chart GC Content semua sekuens
      (b) Stacked Bar komposisi nukleotida (A/T/G/C) per sekuens
      (c) Scatter plot GC Content vs GC Skew

    Parameter:
        sorted_results (list): List hasil analisis (terurut)
        output_dir (str)     : Direktori output untuk menyimpan gambar

    Return:
        output_path (str): Path file gambar yang dihasilkan
    """
    os.makedirs(output_dir, exist_ok=True)

    ids = [s['id'].replace('NC_000962.3_', 'Seq_') for s in sorted_results]
    gc_vals = [s['gc_content'] for s in sorted_results]
    at_vals = [s['at_content'] for s in sorted_results]
    a_vals = [s['A'] for s in sorted_results]
    t_vals = [s['T'] for s in sorted_results]
    g_vals = [s['G'] for s in sorted_results]
    c_vals = [s['C'] for s in sorted_results]
    skew_vals = [s['gc_skew'] for s in sorted_results]

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(
        'BioPipe-Genomics: Analisis GC Content\nMycobacterium tuberculosis H37Rv',
        fontsize=14, fontweight='bold', y=1.01
    )

    # ── Panel A: Bar Chart GC Content ──
    ax1 = axes[0]
    colors = ['#c0392b' if v == max(gc_vals) else '#2980b9' for v in gc_vals]
    bars = ax1.bar(ids, gc_vals, color=colors, edgecolor='white', linewidth=0.8)
    ax1.axhline(y=sum(gc_vals)/len(gc_vals), color='orange', linestyle='--',
                linewidth=1.5, label=f'Rata-rata: {sum(gc_vals)/len(gc_vals):.1f}%')
    ax1.set_title('(a) GC Content per Sekuens', fontweight='bold', fontsize=11)
    ax1.set_ylabel('GC Content (%)')
    ax1.set_ylim(0, 100)
    ax1.set_xticks(range(len(ids)))
    ax1.set_xticklabels(ids, rotation=45, ha='right', fontsize=8)
    ax1.legend(fontsize=9)
    ax1.grid(axis='y', alpha=0.3)
    # Tambahkan nilai di atas bar
    for bar, val in zip(bars, gc_vals):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f'{val}%', ha='center', va='bottom', fontsize=7.5, fontweight='bold')

    # ── Panel B: Stacked Bar Komposisi Nukleotida ──
    ax2 = axes[1]
    x = range(len(ids))
    total_per_seq = [a + t + g + c for a, t, g, c in zip(a_vals, t_vals, g_vals, c_vals)]
    # Normalisasi ke persen
    a_pct = [a/tot*100 for a, tot in zip(a_vals, total_per_seq)]
    t_pct = [t/tot*100 for t, tot in zip(t_vals, total_per_seq)]
    g_pct = [g/tot*100 for g, tot in zip(g_vals, total_per_seq)]
    c_pct = [c/tot*100 for c, tot in zip(c_vals, total_per_seq)]

    ax2.bar(x, a_pct, label='A', color='#27ae60')
    ax2.bar(x, t_pct, bottom=a_pct, label='T', color='#e74c3c')
    ax2.bar(x, g_pct, bottom=[a+t for a, t in zip(a_pct, t_pct)], label='G', color='#2980b9')
    ax2.bar(x, c_pct,
            bottom=[a+t+g for a, t, g in zip(a_pct, t_pct, g_pct)], label='C', color='#f39c12')
    ax2.set_title('(b) Komposisi Nukleotida (%)', fontweight='bold', fontsize=11)
    ax2.set_ylabel('Persentase (%)')
    ax2.set_ylim(0, 100)
    ax2.set_xticks(list(x))
    ax2.set_xticklabels(ids, rotation=45, ha='right', fontsize=8)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.grid(axis='y', alpha=0.3)

    # ── Panel C: Scatter GC Content vs GC Skew ──
    ax3 = axes[2]
    sc = ax3.scatter(gc_vals, skew_vals, c=gc_vals, cmap='RdYlGn',
                     s=120, edgecolors='gray', linewidth=0.5, zorder=5)
    for i, label in enumerate(ids):
        ax3.annotate(label, (gc_vals[i], skew_vals[i]),
                     textcoords='offset points', xytext=(5, 3), fontsize=7.5)
    ax3.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    ax3.set_title('(c) GC Content vs GC Skew', fontweight='bold', fontsize=11)
    ax3.set_xlabel('GC Content (%)')
    ax3.set_ylabel('GC Skew  [(G-C)/(G+C)]')
    ax3.grid(alpha=0.3)
    cbar = plt.colorbar(sc, ax=ax3, shrink=0.8)
    cbar.set_label('GC Content (%)', fontsize=9)

    plt.tight_layout()
    output_path = os.path.join(output_dir, 'gc_analysis_visualization.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n[INFO] Visualisasi disimpan di: {output_path}")
    return output_path


# ────────────────────────────────────────────────────────────────
# 7. MENULIS HASIL KE FILE CSV
# ────────────────────────────────────────────────────────────────

def write_to_csv(sorted_results: list[dict], output_dir: str) -> str:
    """
    Menulis hasil analisis seluruh sekuens ke file CSV.

    Parameter:
        sorted_results (list): List hasil analisis (terurut)
        output_dir (str)     : Direktori output

    Return:
        csv_path (str): Path file CSV yang dihasilkan
    """
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, 'nucleotide_analysis_results.csv')

    fieldnames = ['Rank', 'Sequence_ID', 'Description', 'Length_bp',
                  'A', 'T', 'G', 'C', 'GC_Content_%', 'AT_Content_%', 'GC_Skew']

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for rank, seq in enumerate(sorted_results, start=1):
            writer.writerow({
                'Rank': rank,
                'Sequence_ID': seq['id'],
                'Description': seq['description'],
                'Length_bp': seq['length'],
                'A': seq['A'],
                'T': seq['T'],
                'G': seq['G'],
                'C': seq['C'],
                'GC_Content_%': seq['gc_content'],
                'AT_Content_%': seq['at_content'],
                'GC_Skew': seq['gc_skew']
            })

    print(f"[INFO] Hasil CSV disimpan di: {csv_path}")
    return csv_path


# ────────────────────────────────────────────────────────────────
# MAIN PIPELINE
# ────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  BioPipe-Genomics: Pipeline Analisis Nukleotida")
    print("  Organisme: Mycobacterium tuberculosis H37Rv")
    print(f"  Dijalankan: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Konfigurasi path
    FASTA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'sequences.fasta')
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')

    # ── TAHAP 1: Baca FASTA → simpan dalam List ──
    print("\n[TAHAP 1] Membaca file FASTA...")
    sequences = read_fasta(FASTA_FILE)

    # ── TAHAP 2: Analisis nukleotida dengan Dictionary ──
    print("\n[TAHAP 2] Menghitung frekuensi nukleotida (Dictionary)...")
    results = analyze_sequences(sequences)

    # ── TAHAP 3: Sorting berdasarkan GC Content ──
    print("\n[TAHAP 3] Mengurutkan sekuens berdasarkan GC Content...")
    sorted_results = sort_by_gc_content(results, ascending=False)

    # ── TAHAP 4: Tampilkan 3 sekuens terbaik ──
    print("\n[TAHAP 4] Menampilkan 3 sekuens terbaik...")
    top3 = get_top_sequences(sorted_results, n=3)

    # ── TAHAP 5: Visualisasi ──
    print("\n[TAHAP 5] Membuat visualisasi grafik...")
    img_path = visualize_results(sorted_results, OUTPUT_DIR)

    # ── TAHAP 6: Simpan CSV ──
    print("\n[TAHAP 6] Menyimpan hasil ke file CSV...")
    csv_path = write_to_csv(sorted_results, OUTPUT_DIR)

    # ── Ringkasan Akhir ──
    print(f"\n{'='*60}")
    print(f"  PIPELINE SELESAI – RINGKASAN")
    print(f"{'='*60}")
    print(f"  Total sekuens dianalisis : {len(sequences)}")
    print(f"  GC Content tertinggi     : {sorted_results[0]['gc_content']}% ({sorted_results[0]['id']})")
    print(f"  GC Content terendah      : {sorted_results[-1]['gc_content']}% ({sorted_results[-1]['id']})")
    avg_gc = sum(r['gc_content'] for r in results) / len(results)
    print(f"  Rata-rata GC Content     : {avg_gc:.2f}%")
    print(f"  File visualisasi         : {img_path}")
    print(f"  File CSV                 : {csv_path}")
    print(f"{'='*60}\n")

    return sorted_results, top3


if __name__ == '__main__':
    main()
