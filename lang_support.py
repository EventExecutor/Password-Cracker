import sys
import os
import itertools
import multiprocessing as mp
from colorama import init, Fore, Style
import mmap
import string

init(autoreset=True)

TRANSLATIONS = {
    'it': {
        'title': "=== Password Cracker Ottimizzato ===",
        'subtitle': "Supporto per file di grandi dimensioni e case-insensitive matching",
        'enter_password': "Inserisci password da craccare: ",
        'password_length': "Password length: {}",
        'variations_created': "Variazioni create: {}",
        'dict_file_prompt': "File dizionario (default: common_passwords.txt): ",
        'dict_not_found': "File dizionario {} non trovato",
        'loading_dict': "Caricamento dizionario: {:.1f} MB...",
        'processed_lines': "Processate {:,} righe...",
        'dict_loaded': "Dizionario caricato: {:,} parole uniche da {:,} righe",
        'dict_error': "Errore nel caricamento del dizionario: {}",
        'searching_exact': "Cerco password esatta nel dizionario...",
        'found_direct': "✓ Trovata corrispondenza diretta!",
        'searching_suffix': "Cercare con suffissi numerici...",
        'progress': "Progresso: {:.1f}% ({:,}/{:,})",
        'found_suffix': "✓ Trovata con suffisso numerico!",
        'dict_complete': "Completato controllo dizionario (100%)        ",
        'starting_dict': "Avvio attacco dizionario ottimizzato...",
        'password_found': "✓ Password trovata: '{}' in {:,} tentativi",
        'dict_failed': "Dizionario fallito. Avvio brute force ottimizzato...",
        'password_too_long': "✗ Password troppo lunga per brute force.",
        'password_not_found_dict': "✗ Password non trovata nel dizionario.",
        'password_not_found_keyspace': "✗ Password non trovata nel keyspace.",
        'total_attempts': "Tentativi totali: {:,}",
        'another_password': "\nVuoi craccare un'altra password? (si/no): ",
        'program_terminated': "Programma terminato.",
        'program_interrupted': "\nProgramma interrotto dall'utente.",
        'error': "Errore: {}",
        'brute_force_info': "Brute force: {} processi, keyspace {}^{} = {:,}",
        'brute_force_progress': "Brute force: {:.1f}% (Worker principale)"
    },
    'en': {
        'title': "=== Optimized Password Cracker ===",
        'subtitle': "Support for large files and case-insensitive matching",
        'enter_password': "Enter password to crack: ",
        'password_length': "Password length: {}",
        'variations_created': "Variations created: {}",
        'dict_file_prompt': "Dictionary file (default: common_passwords.txt): ",
        'dict_not_found': "Dictionary file {} not found",
        'loading_dict': "Loading dictionary: {:.1f} MB...",
        'processed_lines': "Processed {:,} lines...",
        'dict_loaded': "Dictionary loaded: {:,} unique words from {:,} lines",
        'dict_error': "Error loading dictionary: {}",
        'searching_exact': "Searching for exact password in dictionary...",
        'found_direct': "✓ Found direct match!",
        'searching_suffix': "Searching with numeric suffixes...",
        'progress': "Progress: {:.1f}% ({:,}/{:,})",
        'found_suffix': "✓ Found with numeric suffix!",
        'dict_complete': "Completed dictionary check (100%)        ",
        'starting_dict': "Starting optimized dictionary attack...",
        'password_found': "✓ Password found: '{}' in {:,} attempts",
        'dict_failed': "Dictionary failed. Starting optimized brute force...",
        'password_too_long': "✗ Password too long for brute force.",
        'password_not_found_dict': "✗ Password not found in dictionary.",
        'password_not_found_keyspace': "✗ Password not found in keyspace.",
        'total_attempts': "Total attempts: {:,}",
        'another_password': "\nDo you want to crack another password? (yes/no): ",
        'program_terminated': "Program terminated.",
        'program_interrupted': "\nProgram interrupted by user.",
        'error': "Error: {}",
        'brute_force_info': "Brute force: {} processes, keyspace {}^{} = {:,}",
        'brute_force_progress': "Brute force: {:.1f}% (Main worker)"
    }
}

selected_language = 'en'

def get_text(key, *args):
    """Ottiene il testo tradotto per la chiave specificata"""
    text = TRANSLATIONS[selected_language].get(key, key)
    if args:
        return text.format(*args)
    return text

def select_language():
    """Seleziona la lingua dell'interfaccia"""
    global selected_language
    
    print(Fore.MAGENTA + "Lingua/Language" + Style.RESET_ALL)
    print("1. IT (Italiano)")
    print("2. EN (English)")
    print()
    
    while True:
        choice = input("Choice: ").strip()
        if choice == '1':
            selected_language = 'it'
            break
        elif choice == '2':
            selected_language = 'en'
            break
        else:
            print(Fore.RED + "Invalid choice. Please select 1 or 2." + Style.RESET_ALL)
    
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def try_guess(guess, password_variations, attempts, found, result):
    with attempts.get_lock():
        attempts.value += 1
    
    if guess in password_variations:
        with found.get_lock():
            found.value = True
        result.passwd = guess
        return True
    return False


def generate_case_variations(word):
    if len(word) <= 1:
        return {word.lower(), word.upper()}
    
    variations = {
        word.lower(),
        word.upper(), 
        word.capitalize(),
        word[0].upper() + word[1:].lower()
    }
    
    if len(word) <= 8:
        variations.add(word.title())
        if len(word) > 1:
            variations.add(word[:-1].lower() + word[-1].upper())
    
    return variations


def load_dictionary_chunked(filepath, max_length, chunk_size=8192):
    words = set()
    
    if not os.path.exists(filepath):
        print(Fore.YELLOW + get_text('dict_not_found', filepath) + Style.RESET_ALL)
        return words
    
    try:
        file_size = os.path.getsize(filepath)
        print(Fore.CYAN + get_text('loading_dict', file_size / (1024*1024)) + Style.RESET_ALL)
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                buffer = ""
                processed_lines = 0
                
                for chunk in iter(lambda: mmapped_file.read(chunk_size), b""):
                    chunk_str = chunk.decode('utf-8', errors='ignore')
                    buffer += chunk_str
                    
                    lines = buffer.split('\n')
                    buffer = lines[-1]
                    
                    for line in lines[:-1]:
                        word = line.strip()
                        if word and len(word) <= max_length:
                            words.add(word)
                            words.update(generate_case_variations(word))
                        
                        processed_lines += 1
                        if processed_lines % 100000 == 0:
                            print(f"\r{Fore.BLUE}{get_text('processed_lines', processed_lines)}{Style.RESET_ALL}", end='', flush=True)
                
                if buffer.strip():
                    word = buffer.strip()
                    if len(word) <= max_length:
                        words.add(word)
                        words.update(generate_case_variations(word))
        
        print(f"\r{Fore.GREEN}{get_text('dict_loaded', len(words), processed_lines)}{Style.RESET_ALL}")
        
    except Exception as e:
        print(Fore.RED + get_text('dict_error', e) + Style.RESET_ALL)
    
    return words


def dict_attack_fast(common_words, password_variations, length, attempts, found, result, max_suffix=4):
    print(f"{Fore.CYAN}{get_text('searching_exact')}{Style.RESET_ALL}")

    for password_var in password_variations:
        attempts.value += 1
        if password_var in common_words:
            found.value = True
            result.passwd = password_var
            print(f"\r{Fore.GREEN}{get_text('found_direct')}{Style.RESET_ALL}")
            return True
    
    print(f"{Fore.CYAN}{get_text('searching_suffix')}{Style.RESET_ALL}")

    words_list = list(common_words)
    total_words = len(words_list)
    
    for i, word in enumerate(words_list):
        if found.value:
            return True

        if i % 50000 == 0 and i > 0:
            percentage = (i / total_words) * 100
            print(f"\r{Fore.BLUE}{get_text('progress', percentage, i, total_words)}{Style.RESET_ALL}", end='', flush=True)
        
        for digits in range(1, max_suffix + 1):
            if found.value:
                return True
                
            for num in range(10**digits):
                attempts.value += 1
                guess = word + str(num).zfill(digits)
                
                if len(guess) == length and guess in password_variations:
                    found.value = True
                    result.passwd = guess
                    print(f"\r{Fore.GREEN}{get_text('found_suffix')}{Style.RESET_ALL}")
                    return True
                
                if digits > 1:
                    attempts.value += 1
                    guess_no_pad = word + str(num)
                    if len(guess_no_pad) == length and guess_no_pad in password_variations:
                        found.value = True
                        result.passwd = guess_no_pad
                        print(f"\r{Fore.GREEN}{get_text('found_suffix')}{Style.RESET_ALL}")
                        return True
    
    print(f"\r{Fore.YELLOW}{get_text('dict_complete')}{Style.RESET_ALL}")
    return False


def dict_attack_worker(word_chunk, password_variations, length, attempts, found, result, max_suffix):
    for word in word_chunk:
        if found.value:
            return

        if try_guess(word, password_variations, attempts, found, result):
            return
        
        for digits in range(1, max_suffix + 1):
            if found.value:
                return
                
            for num in range(10**digits):
                guess = word + str(num).zfill(digits)
                if len(guess) == length:
                    if try_guess(guess, password_variations, attempts, found, result):
                        return
                
                if digits > 1:
                    guess = word + str(num)
                    if len(guess) == length:
                        if try_guess(guess, password_variations, attempts, found, result):
                            return


def brute_force_chunk(start, end, keys, password_variations, length, attempts, found, result):
    total = len(keys) ** length
    for idx in range(start, min(end, total)):
        if found.value:
            return
        combo = []
        i = idx
        for _ in range(length):
            combo.append(keys[i % len(keys)])
            i //= len(keys)
        guess = ''.join(reversed(combo))
        if try_guess(guess, password_variations, attempts, found, result):
            return


def parallel_bruteforce_optimized(password_variations, length, attempts, found, result):
    if length <= 4:
        keys = '0123456789abcdefghijklmnopqrstuvwxyz'
    elif length <= 6:
        keys = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    else:
        keys = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#'
    
    workers = min(mp.cpu_count(), 12)
    total = len(keys) ** length
    chunk = total // workers + 1
    
    print(Fore.YELLOW + get_text('brute_force_info', workers, len(keys), length, total) + Style.RESET_ALL)
    
    processes = []
    for i in range(workers):
        start = i * chunk
        end = start + chunk
        p = mp.Process(
            target=brute_force_chunk_optimized,
            args=(start, end, keys, password_variations, length, attempts, found, result, i)
        )
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()


def brute_force_chunk_optimized(start, end, keys, password_variations, length, attempts, found, result, worker_id):
    total = len(keys) ** length
    keys_len = len(keys)
    progress_interval = max(1000, (end - start) // 100)
    
    for idx in range(start, min(end, total)):
        if found.value:
            return
            
        if idx % progress_interval == 0 and worker_id == 0:
            percentage = ((idx - start) / (end - start)) * 100
            print(f"\r{Fore.BLUE}{get_text('brute_force_progress', percentage)}{Style.RESET_ALL}", end='', flush=True)
        
        combo = []
        i = idx
        for _ in range(length):
            combo.append(keys[i % keys_len])
            i //= keys_len
        
        guess = ''.join(reversed(combo))
        
        with attempts.get_lock():
            attempts.value += 1
        
        if guess in password_variations:
            with found.get_lock():
                found.value = True
            result.passwd = guess
            return


def create_password_variations(password):
    variations = set()
    variations.update(generate_case_variations(password))
    return variations


def main():
    select_language()
    
    print(Fore.MAGENTA + get_text('title') + Style.RESET_ALL)
    print(Fore.CYAN + get_text('subtitle') + Style.RESET_ALL)
    print()
    
    while True:
        password = input(Fore.LIGHTRED_EX + get_text('enter_password') + Style.RESET_ALL)
        if not password:
            continue
            
        length = len(password)
        password_variations = create_password_variations(password)
        
        print(Fore.BLUE + get_text('password_length', length) + Style.RESET_ALL)
        print(Fore.BLUE + get_text('variations_created', len(password_variations)) + Style.RESET_ALL)

        DICT_FILE = input(Fore.CYAN + get_text('dict_file_prompt') + Style.RESET_ALL).strip()
        if not DICT_FILE:
            DICT_FILE = "common_passwords.txt"
        
        common_words = load_dictionary_chunked(DICT_FILE, length + 4)

        attempts = mp.Value('i', 0)
        found = mp.Value('b', False)
        manager = mp.Manager()
        result = manager.Namespace()
        result.passwd = None

        print(Fore.YELLOW + get_text('starting_dict') + Style.RESET_ALL)
        
        if common_words:
            dict_attack_fast(common_words, password_variations, length, attempts, found, result)
        
        if found.value:
            print(Fore.GREEN + get_text('password_found', result.passwd, attempts.value) + Style.RESET_ALL)
        elif length <= 8:
            print(Fore.YELLOW + get_text('dict_failed') + Style.RESET_ALL)
            parallel_bruteforce_optimized(password_variations, length, attempts, found, result)
            if found.value:
                print(Fore.GREEN + get_text('password_found', result.passwd, attempts.value) + Style.RESET_ALL)
            else:
                print(Fore.RED + get_text('password_not_found_keyspace') + Style.RESET_ALL)
        else:
            print(Fore.RED + get_text('password_too_long') + Style.RESET_ALL)
            if not found.value:
                print(Fore.RED + get_text('password_not_found_dict') + Style.RESET_ALL)

        print(Fore.BLUE + get_text('total_attempts', attempts.value) + Style.RESET_ALL)

        continue_options = ['si', 's', 'yes', 'y'] if selected_language == 'it' else ['yes', 'y', 'si', 's']
        risposta = input(Fore.CYAN + get_text('another_password') + Style.RESET_ALL).strip().lower()
        if risposta not in continue_options:
            print(Fore.MAGENTA + get_text('program_terminated') + Style.RESET_ALL)
            break
        
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')


if __name__ == '__main__':
    mp.freeze_support()
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + get_text('program_interrupted') + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + get_text('error', e) + Style.RESET_ALL)