"""
Funções auxiliares para processar dados JSON nas migrations.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any


def parse_date(date_str: str) -> datetime:
    """
    Converte string de data para datetime.
    Formatos suportados: "2024-4-23", "2-1", "2024-5-29"
    """
    try:
        parts = date_str.split('-')
        if len(parts) == 3:
            # Formato: "2024-4-23"
            year, month, day = map(int, parts)
            return datetime(year, month, day)
        elif len(parts) == 2:
            # Formato: "2-1" (assumindo ano atual)
            month, day = map(int, parts)
            current_year = datetime.now().year
            return datetime(current_year, month, day)
        else:
            # Fallback para data atual
            return datetime.now()
    except (ValueError, AttributeError):
        return datetime.now()


def parse_number(value: Any) -> int:
    """Converte string numérica (ex: "42.6K", "3864") para inteiro."""
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        value = value.strip()
        if value.lower() in ['n/a', 'na', '', 'compartilhar', '0']:
            return 0
        # Remove "K", "M" e converte
        if 'k' in value.lower():
            return int(float(value.lower().replace('k', '')) * 1000)
        if 'm' in value.lower():
            return int(float(value.lower().replace('m', '')) * 1000000)
        try:
            return int(value)
        except ValueError:
            return 0
    return 0


def process_json_file(file_path: Path) -> List[Dict[str, Any]]:
    """Processa um arquivo JSON e retorna lista de publicações."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    publications = []
    
    for item in data:
        # Processa publicação
        pub = {
            'publicacao_n': item.get('publicacao_n', 0),
            'url': item.get('url', ''),
            'description': item.get('description', ''),
            'date': parse_date(item.get('date', '')),
            'views': item.get('views', ''),
            'likes': item.get('likes', ''),
            'comments_count': item.get('comments_count', item.get('comments', 0)),
            'shares': item.get('shares', ''),
            'bookmarks': item.get('bookmarks', ''),
            'music_title': item.get('musicTitle', ''),
            'tags': item.get('tags', []),
            'comments': []
        }
        
        # Processa comentários
        comments_data = item.get('comments', []) or item.get('comments_usernames', [])
        
        for comment_data in comments_data:
            # Ignora comentários N/A
            if comment_data.get('username') == 'N/A' or comment_data.get('text') == 'N/A':
                continue
                
            comment = {
                'username': comment_data.get('username', ''),
                'text': comment_data.get('text', ''),
                'likes': parse_number(comment_data.get('likes', 0)),
                'replies': []
            }
            
            # Processa respostas
            replies_data = comment_data.get('replies', [])
            for reply_data in replies_data:
                reply = {
                    'username': reply_data.get('username', ''),
                    'text': reply_data.get('text', ''),
                    'likes': parse_number(reply_data.get('likes', 0))
                }
                comment['replies'].append(reply)
            
            pub['comments'].append(comment)
        
        publications.append(pub)
    
    return publications


def load_all_publications() -> List[Dict[str, Any]]:
    """
    Carrega todas as publicações dos arquivos JSON.
    Retorna lista de publicações únicas (por publicacao_n).
    
    Procura os arquivos JSON na pasta 'json' dentro do diretório do backend.
    O caminho é relativo ao arquivo helpers.py:
    - helpers.py está em: scrapping-backend/alembic/helpers.py
    - json/ está em: scrapping-backend/json/
    - Caminho: Path(__file__).parent.parent / "json"
      (alembic/helpers.py -> alembic/ -> scrapping-backend/ -> json/)
    """
    # Caminho relativo: alembic/helpers.py -> alembic/ -> scrapping-backend/ -> json/
    json_dir = Path(__file__).parent.parent / "json"
    
    if not json_dir.exists():
        raise FileNotFoundError(
            f"Diretório de JSONs não encontrado em: {json_dir.absolute()}\n"
            f"Certifique-se de que a pasta 'json' existe em: {Path(__file__).parent.parent.absolute()}"
        )
    
    all_publications = []
    
    for json_file in json_dir.glob('*.json'):
        try:
            publications = process_json_file(json_file)
            all_publications.extend(publications)
        except Exception as e:
            print(f"Erro ao processar {json_file.name}: {e}")
    
    # Remove duplicatas por publicacao_n, mantendo a que tem mais comentários
    seen_pubs = {}
    for pub in all_publications:
        pub_n = pub['publicacao_n']
        if pub_n not in seen_pubs or len(pub['comments']) > len(seen_pubs[pub_n]['comments']):
            seen_pubs[pub_n] = pub
    
    unique_publications = list(seen_pubs.values())
    unique_publications.sort(key=lambda x: x['publicacao_n'])
    
    return unique_publications

