from Bio import SeqIO

def calculate_n50_l50(fasta_file):
    contig_lengths = [len(record.seq) for record in SeqIO.parse(fasta_file, "fasta")]
    contig_lengths.sort(reverse=True)  # Sort lengths in descending order
    
    total_length = sum(contig_lengths)
    half_length = total_length / 2
    
    cumulative_length = 0
    n50 = 0
    l50 = 0
    
    for i, length in enumerate(contig_lengths):
        cumulative_length += length
        if cumulative_length >= half_length:
            n50 = length
            l50 = i + 1  # 1-based index
            break
    
    return n50, l50

def print_contig_lengths(fasta_file):
    for record in SeqIO.parse(fasta_file, "fasta"):
        print(f"Contig: {record.id}, Length: {len(record.seq)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Calculate N50 and L50 and print contig lengths from a metaSPAdes FASTA file.")
    parser.add_argument("fasta", help="Path to the metaSPAdes output FASTA file (e.g., contigs.fasta)")
    args = parser.parse_args()
    
    print_contig_lengths(args.fasta)
    n50, l50 = calculate_n50_l50(args.fasta)
    print(f"N50: {n50}")
    print(f"L50: {l50}")
