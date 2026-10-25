import os

# ---------------- CLEAN FUNCTION ----------------
def clean_code(code):
    result = []
    i = 0
    n = len(code)

    in_single = False
    in_multi = False
    in_html = False
    in_string = False
    string_char = ''
    in_py_multi = False
    py_multi_char = ''

    while i < n:
        ch = code[i]
        next2 = code[i:i+2]
        next3 = code[i:i+3]
        next4 = code[i:i+4]

        # -------- HANDLE STATES --------
        if in_single:
            if ch == '\n':
                in_single = False
                result.append(ch)
            i += 1
            continue

        if in_multi:
            if next2 == '*/':
                in_multi = False
                i += 2
            else:
                i += 1
            continue

        if in_html:
            if next3 == '-->':
                in_html = False
                i += 3
            else:
                i += 1
            continue

        if in_py_multi:
            if code[i:i+3] == py_multi_char:
                in_py_multi = False
                i += 3
            else:
                i += 1
            continue

        if in_string:
            result.append(ch)
            if ch == '\\':
                if i + 1 < n:
                    result.append(code[i+1])
                    i += 2
                    continue
            elif ch == string_char:
                in_string = False
            i += 1
            continue

        # -------- START CONDITIONS --------
        if ch in ('"', "'", '`'):
            if code[i:i+3] in ("'''", '"""'):
                in_py_multi = True
                py_multi_char = code[i:i+3]
                i += 3
                continue
            else:
                in_string = True
                string_char = ch
                result.append(ch)
                i += 1
                continue

        if next2 == '//':
            in_single = True
            i += 2
            continue

        if ch == '#':
            in_single = True
            i += 1
            continue

        if next2 == '--':
            in_single = True
            i += 2
            continue

        if next2 == '/*':
            in_multi = True
            i += 2
            continue

        if next4 == '<!--':
            in_html = True
            i += 4
            continue

        result.append(ch)
        i += 1

    # -------- CLEAN WHITESPACE --------
    lines = ''.join(result).splitlines()
    cleaned = [line.strip() for line in lines if line.strip()]

    return '\n'.join(cleaned)


# ---------------- FILE FILTER ----------------
def get_valid_files():
    extensions = ('.c', '.cpp', '.java', '.py', '.js', '.html', '.sql', '.txt')
    valid_files = []

    current_file = os.path.basename(__file__)  # exact current file name

    for f in os.listdir():
        # Skip folders
        if not os.path.isfile(f):
            continue

        # 🔥 Skip main file (DOUBLE SAFETY)
        if f == current_file or f == "main.py":
            continue

        # 🔥 Skip cleaned files
        if f.startswith("cleaned_"):
            continue

        # Only valid extensions
        if f.endswith(extensions):
            valid_files.append(f)

    return valid_files

# ---------------- MAIN PROCESS ----------------
def process_files():
    files = get_valid_files()

    if not files:
        print("❌ No valid source files found!")
        return

    print("🔍 Processing files...\n")

    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                code = f.read()

            cleaned_code = clean_code(code)

            output_file = "cleaned_" + file

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(cleaned_code)

            print(f"✅ {file} → {output_file}")

        except Exception as e:
            print(f"❌ Error processing {file}: {e}")

    print("\n🎉 All files processed successfully!")


# ---------------- RUN ----------------
if __name__ == "__main__":
    process_files()