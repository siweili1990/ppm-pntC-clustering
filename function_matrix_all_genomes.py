import sys
import copy

PNGCS = set(('IspD', 'NTP_transferase', 'NTP_transf_3'))

with open(sys.argv[1], 'r') as fin:
  counts = {}
  order = {}
  i = 0
  current_gcf = None
  current_pos_start = None
  current_freqs = {}
  has_pep_mutase = False
  has_pngc = False
  last_pos = None

#  good_gcfs = set()
#  with open('/Vagabundo/monica/Desktop/Importance-tri_sign-0_03-0', 'r') as f:
#    for line in f:
#     good_gcfs.add(line.split()[0])

  for line in fin:
    parts = line.strip().split('\t')
    if parts[0] == 'GCF':
      continue
    gcf = parts[0]
    pos = int(parts[1])
    family = parts[3]
    if family == 'PEP_mutase':
      has_pep_mutase = True
    elif family in PNGCS:
      has_pngc = True
    if gcf != current_gcf or pos - last_pos > 11 or pos - last_pos < 0:
      if current_gcf is not None:
        if has_pngc and has_pep_mutase:
          if current_gcf not in counts:
            counts[current_gcf] = []
          counts[current_gcf].append((current_pos_start, last_pos, current_freqs))

      current_gcf = gcf
      current_pos_start = pos
      current_freqs = {}
      has_pep_mutase = False
      has_pngc = False

    if family not in current_freqs:
      current_freqs[family] = 0
    current_freqs[family] += 1

    if gcf not in order:
      order[gcf] = i
      i += 1

    last_pos = pos

  if has_pngc and has_pep_mutase:
    if current_gcf not in counts:
      counts[current_gcf] = []
    counts[current_gcf].append((current_pos_start, last_pos, current_freqs))

  sorted_counts = sorted(counts.items(), key=lambda x: order[x[0]])
  counts_list = []
  id_list = []
  for gcf, pos_and_family_counts in sorted_counts:
    for pos_start, pos_end, family_counts in pos_and_family_counts:
      counts_list.append(copy.deepcopy(family_counts))
      id_list.append((gcf, pos_start))

  jaccard_list = []
  for i, fam_counts_a in enumerate(counts_list):
    for j, fam_counts_b in enumerate(counts_list):
      if j > 0:
        pass

      if j <= i:
        pass
      else:
        a = set(fam_counts_a.keys())
        b = set(fam_counts_b.keys())
        if 'HYPOTHETICAL' in b:
          b.add('HYPOTHETICALLY_DIFFERENT')
          b.remove('HYPOTHETICAL')

        total_a = sum(fam_counts_a.values())
        total_b = sum(fam_counts_b.values())

        id_a = id_list[i][0] + '_n' + str(id_list[i][1])
        id_b = id_list[j][0] + '_n' + str(id_list[j][1])
        jaccard_list.append((id_a, id_b, total_a, total_b, '/'.join(a & b), len(a & b), '/'.join(a | b), len(a | b), 1 - float(len(a & b)) / len(a | b)))
  jaccard_list.sort(key=lambda x: x[8])

  with open(sys.argv[1] + '_jaccard_table', 'w') as fout:
    fout.write('N1,N2,N1_SIZE,N2_SIZE,INTERSECTION,INTERSECTION_SIZE,UNION,UNION_SIZE,JACCARD_DISTANCE\n')
    for x in jaccard_list:
      fout.write('{},{},{},{},{},{},{},{},{}\n'.format(*x))

  with open(sys.argv[1] + '_jaccard_matrix_all', 'w') as fout:
    fout.write('\t' + '\t'.join('{}_n{}'.format(*id_list_item) for id_list_item in id_list) + '\n')
    for i, fam_counts_a in enumerate(counts_list):
      fout.write('{}_n{}'.format(*id_list[i]) + '\t')
      row = []
      for j, fam_counts_b in enumerate(counts_list):
        if j == i:
          row.append(0)
        else:
          a = set(fam_counts_a.keys())
          b = set(fam_counts_b.keys())
          if 'HYPOTHETICAL' in b:
            b.add('HYPOTHETICALLY_DIFFERENT')
            b.remove('HYPOTHETICAL')
          row.append(1 - float(len(a & b)) / len(a | b))
      fout.write('\t'.join(str(x) for x in row) + '\n')

 # with open(sys.argv[1] + '_family_freq', 'w') as fout:
 #   for gcf, pos_and_family_counts in sorted_counts:
 #     for pos_start, pos_end, family_counts in pos_and_family_counts:
 #       if 'HYPOTHETICAL' in family_counts:
 #         del family_counts['HYPOTHETICAL']
 #       best_family = max(family_counts.items(), key=lambda x: x[1])
 #       all_best = []
 #       for k, v in family_counts.items():
 #         if v == best_family[1]:
 #           all_best.append(k)
 #       fout.write('{}\t{}\t{}\t{}\t{}\n'.format(gcf, pos_start, pos_end, ','.join(all_best), best_family[1]))




