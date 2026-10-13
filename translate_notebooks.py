import os
import json
import io
import tokenize
import subprocess

trans_dict = {
    "파일경로": "file_path",
    "독립": "independent",
    "종속": "dependent",
    "보스턴": "boston",
    "아이리스": "iris",
    "레모네이드": "lemonade",
    "인코딩": "encoding"
}

def translate_code(source):
    # We will use tokenize to safely replace names
    # But magics like % and ! break tokenize. 
    # We can temporarily hide them, tokenize, untokenize, then restore them.
    lines = source.split('\n')
    hidden_lines = {}
    clean_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('%') or stripped.startswith('!'):
            hidden_lines[i] = line
            clean_lines.append("") # Keep line numbers intact
        else:
            clean_lines.append(line)
            
    clean_source = '\n'.join(clean_lines)
    
    try:
        tokens = list(tokenize.tokenize(io.BytesIO(clean_source.encode('utf-8')).readline))
        new_tokens = []
        for tok in tokens:
            tok_type, tok_string, start, end, line = tok
            if tok_type == tokenize.NAME and tok_string in trans_dict:
                tok_string = trans_dict[tok_string]
            new_tokens.append((tok_type, tok_string))
        
        # untokenize
        translated_source = tokenize.untokenize(new_tokens).decode('utf-8')
    except Exception as e:
        # If tokenization fails, fallback to simple string replacement (risky but better than failing)
        translated_source = clean_source
        for k, v in trans_dict.items():
            # simple replacement
            translated_source = translated_source.replace(k, v)
            
    # Restore magics
    final_lines = translated_source.split('\n')
    for i, magic_line in hidden_lines.items():
        if i < len(final_lines):
            final_lines[i] = magic_line
            
    # Sometimes untokenize adds an extra newline at the end if it wasn't there
    if not source.endswith('\n') and translated_source.endswith('\n'):
        final_lines = final_lines[:-1]
        
    return '\n'.join(final_lines)

base_path = r"C:\Users\tuesv\Downloads\DMDG_LIVE_CODE\삼선AXI 심화2\ml-tensorflow-master\ml-tensorflow-master"

results = []

for root, _, files in os.walk(base_path):
    for f in files:
        if f.endswith('.ipynb') and not f.startswith('new_') and not '.ipynb_checkpoints' in root:
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as nb_file:
                    nb = json.load(nb_file)
                
                changed = False
                for cell in nb.get('cells', []):
                    if cell.get('cell_type') == 'code':
                        source = "".join(cell.get('source', []))
                        new_source = translate_code(source)
                        if source != new_source:
                            changed = True
                        
                        # cell['source'] expects a list of lines with newlines
                        # untokenize returns a single string.
                        # Let's re-split and add newlines
                        split_lines = new_source.splitlines(keepends=True)
                        cell['source'] = split_lines
                        
                new_f = f"new_{f}"
                new_path = os.path.join(root, new_f)
                
                with open(new_path, 'w', encoding='utf-8') as out_file:
                    json.dump(nb, out_file, ensure_ascii=False, indent=1)
                
                print(f"[SUCCESS] Saved {new_f}")
                results.append(new_path)
            except Exception as e:
                print(f"[ERROR] Failed to process {f}: {e}")

# Run tests
print("\n--- Running Tests with nbconvert ---")
for nb_path in results:
    nb_name = os.path.basename(nb_path)
    print(f"Testing {nb_name}...")
    try:
        # We run it inplace to test it. If it fails, nbconvert throws an error.
        # Use timeout to prevent hanging.
        cmd = ["jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", nb_path]
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=120)
        print(f"  -> {nb_name} executed successfully.")
    except subprocess.TimeoutExpired:
        print(f"  -> [TIMEOUT] {nb_name} took too long to execute.")
    except subprocess.CalledProcessError as e:
        print(f"  -> [FAILED] {nb_name} execution error.")
        # Print a short summary of the error
        err_out = e.stderr if e.stderr else e.stdout
        print("     " + "\n     ".join(err_out.splitlines()[-5:]))
    except FileNotFoundError:
        print("  -> [ERROR] jupyter nbconvert not found in PATH.")
        break
