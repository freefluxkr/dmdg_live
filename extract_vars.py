import os
import json
import re
import io
import tokenize

def extract_korean_vars(ipynb_path):
    korean_vars = set()
    try:
        with open(ipynb_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except Exception as e:
        return korean_vars
        
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = "".join(cell.get('source', []))
            
            # Remove magics to avoid syntax errors in tokenize
            lines = source.split('\n')
            clean_lines = []
            for line in lines:
                if line.strip().startswith('%') or line.strip().startswith('!'):
                    clean_lines.append(f"# {line}")
                else:
                    clean_lines.append(line)
            clean_source = '\n'.join(clean_lines)
            
            try:
                tokens = tokenize.tokenize(io.BytesIO(clean_source.encode('utf-8')).readline)
                for tok in tokens:
                    if tok.type == tokenize.NAME:
                        if re.search(r'[가-힣]', tok.string):
                            korean_vars.add(tok.string)
            except tokenize.TokenError:
                pass
            except SyntaxError:
                pass
                
    return korean_vars

base_path = r"C:\Users\tuesv\Downloads\DMDG_LIVE_CODE\삼선AXI 심화2\ml-tensorflow-master\ml-tensorflow-master"
all_vars = set()

for root, _, files in os.walk(base_path):
    for f in files:
        if f.endswith('.ipynb') and not f.startswith('new_'):
            path = os.path.join(root, f)
            all_vars.update(extract_korean_vars(path))

print(json.dumps(list(all_vars), ensure_ascii=False))
