import csvkit


def load_table(f, skip_header):
    instr_ref_array = []
    instr_sub_table = []

    try:
        reader = csvkit.reader(f)
        i = 0
        for row in reader:

            # Skip header if required
            if skip_header == 1 and i == 0:
                i += 1
                continue

            instr_ref_array.append(row[0])

            instr_sub_array = []

            for j in range(1, len(row)):

                # Skip empty rows
                if not row[j]:
                    break

                instr_sub_array.append(row[j])

            instr_sub_table.append(instr_sub_array)
            i += 1

    finally:
        f.close()

    return instr_ref_array, instr_sub_table
