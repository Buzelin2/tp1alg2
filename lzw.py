import sys
import time
import os
import struct

# Classe que representa um nó em uma Trie
class TrieNode:
    def __init__(self):
        self.children = {}
        self.code = None

# Classe que representa a Trie utilizada para a compressão LZW
class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.next_code = 256

    def insert(self, key, code):
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.code = code

    def search(self, key):
        node = self.root
        for char in key:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node.code

    def get_next_code(self):
        code = self.next_code
        self.next_code += 1
        return code

# Classe para escrever bits em um arquivo binário
class BitWriter:
    def __init__(self, file):
        self.file = file
        self.buffer = 0
        self.buffer_length = 0

    def write_bits(self, bits, length):
        self.buffer = (self.buffer << length) | bits
        self.buffer_length += length
        while self.buffer_length >= 8:
            self.buffer_length -= 8
            byte = (self.buffer >> self.buffer_length) & 0xFF
            self.file.write(bytes([byte]))
        # Mantém os bits restantes no buffer

    def flush(self):
        if self.buffer_length > 0:
            byte = (self.buffer << (8 - self.buffer_length)) & 0xFF
            self.file.write(bytes([byte]))
            self.buffer = 0
            self.buffer_length = 0

# Classe para ler bits de um arquivo binário
class BitReader:
    def __init__(self, file):
        self.file = file
        self.buffer = 0
        self.buffer_length = 0

    def read_bits(self, length):
        while self.buffer_length < length:
            byte = self.file.read(1)
            if not byte:
                if self.buffer_length == 0:
                    return None  # Fim do arquivo
                else:
                    # Preenche com zeros se faltar bits
                    self.buffer <<= (length - self.buffer_length)
                    self.buffer_length = length
                    break
            self.buffer = (self.buffer << 8) | byte[0]
            self.buffer_length += 8
        if self.buffer_length < length:
            return None  # Não há bits suficientes
        self.buffer_length -= length
        bits = (self.buffer >> self.buffer_length) & ((1 << length) - 1)
        self.buffer &= (1 << self.buffer_length) - 1
        return bits

# Função para comprimir dados usando o algoritmo LZW
def lzw_compress(input_bytes, max_bits=12, variable_bits=False):
    if max_bits < 9:
        raise ValueError("max_bits deve ser pelo menos 9 para acomodar 256 códigos iniciais.")

    trie = Trie()

    for i in range(256):
        trie.insert(bytes([i]), i)

    current_bytes = b""
    compressed_data = []

    code_size = 9 if variable_bits else max_bits
    max_table_size_current = 2 ** code_size

    for byte in input_bytes:
        new_bytes = current_bytes + bytes([byte])
        if trie.search(new_bytes) is not None:
            current_bytes = new_bytes
        else:
            compressed_data.append(trie.search(current_bytes))
            if trie.next_code < 2 ** max_bits:
                trie.insert(new_bytes, trie.next_code)
                trie.next_code += 1
                # Atualiza o code_size se necessário
                if variable_bits and trie.next_code >= max_table_size_current and code_size < max_bits:
                    code_size += 1
                    max_table_size_current = 2 ** code_size
            current_bytes = bytes([byte])

    if current_bytes:
        compressed_data.append(trie.search(current_bytes))

    return compressed_data, code_size

# Função para descomprimir dados comprimidos com LZW
def lzw_decompress(compressed_data, max_bits=12, variable_bits=False):
    if max_bits < 9:
        raise ValueError("max_bits deve ser pelo menos 9 para acomodar 256 códigos iniciais.")

    table = {i: bytes([i]) for i in range(256)}
    next_code = 256

    code_size = 9 if variable_bits else max_bits
    max_table_size_current = 2 ** code_size

    if not compressed_data:
        return b""

    current_code = compressed_data.pop(0)
    if current_code not in table:
        raise ValueError(f"Erro na descompressão: código inválido {current_code}.")
    current_bytes = table[current_code]
    decompressed_data = [current_bytes]

    for code in compressed_data:
        if variable_bits and next_code >= max_table_size_current and code_size < max_bits:
            code_size += 1
            max_table_size_current = 2 ** code_size

        if code in table:
            entry = table[code]
        elif code == next_code:
            entry = current_bytes + current_bytes[:1]
        else:
            raise ValueError(f"Erro na descompressão: código inválido {code}.")

        decompressed_data.append(entry)

        if next_code < 2 ** max_bits:
            table[next_code] = current_bytes + entry[:1]
            next_code += 1

        current_bytes = entry

    return b''.join(decompressed_data)

# Função para limpar os diretórios compressed e decompressed
def clear_directories():
    directories = ["compressed/", "decompressed/"]
    for directory in directories:
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Erro ao apagar o arquivo {file_path}: {e}")

# Ponto de entrada do script
if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "clear":
        clear_directories()
        print("Diretórios 'compressed' e 'decompressed' limpos com sucesso.")
        sys.exit(0)

    if len(sys.argv) < 4:
        print("Uso: python lzw.py <compress|decompress> <arquivo> <f|v> [max_bits]")
        sys.exit(1)

    mode = sys.argv[1]
    file_path = sys.argv[2]
    version = sys.argv[3].lower()
    max_bits = int(sys.argv[4]) if len(sys.argv) > 4 else 12

    if max_bits < 9:
        print("Erro: max_bits deve ser pelo menos 9 para acomodar 256 códigos iniciais.")
        sys.exit(1)

    variable_bits = version == 'v'

    base_dir = "original/"
    compressed_dir = "compressed/"
    decompressed_dir = "decompressed/"

    file_name = os.path.basename(file_path)
    file_base_name, file_extension = os.path.splitext(file_name)

    start_time = time.time()

    if mode == "compress":
        input_path = os.path.join(base_dir, file_name)
        output_path = os.path.join(compressed_dir, f"{file_base_name}.bin")  # Alterado para .bin

        # Obter a extensão sem o ponto
        extension = file_extension[1:] if file_extension.startswith('.') else file_extension
        extension_bytes = extension.encode('utf-8')
        extension_length = len(extension_bytes)

        with open(input_path, 'rb') as file:
            data = file.read()

        try:
            compressed, final_code_size = lzw_compress(data, max_bits, variable_bits)
        except ValueError as ve:
            print(f"Erro durante a compressão: {ve}")
            sys.exit(1)

        with open(output_path, 'wb') as file:
            # Escreve o modo e o tamanho máximo dos bits no cabeçalho
            # Modo: 1 byte (0 para fixo, 1 para variável)
            mode_byte = 1 if variable_bits else 0
            file.write(struct.pack('B', mode_byte))
            # Escreve o tamanho máximo dos bits (1 byte)
            file.write(struct.pack('B', max_bits))
            # Escreve o comprimento da extensão (1 byte)
            file.write(struct.pack('B', extension_length))
            # Escreve a extensão em bytes
            file.write(extension_bytes)
            # Escreve os códigos comprimidos usando BitWriter
            writer = BitWriter(file)
            code_size = 9 if variable_bits else max_bits
            max_table_size_current = 2 ** code_size
            next_code = 256

            for code in compressed:
                # Atualiza o code_size se necessário antes de escrever
                if variable_bits and next_code >= max_table_size_current and code_size < max_bits:
                    code_size += 1
                    max_table_size_current = 2 ** code_size
                writer.write_bits(code, code_size)
                next_code += 1

            writer.flush()

        print(f"Arquivo comprimido salvo como {output_path}")

        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        compression_ratio = original_size / compressed_size if compressed_size != 0 else 0
        print(f"Taxa de compressão: {compression_ratio:.2f}")
        print(f"Bits utilizados: {max_bits}")
        print(f"Tempo de execução: {time.time() - start_time:.2f} segundos")

    elif mode == "decompress":
        input_path = os.path.join(compressed_dir, file_name)

        with open(input_path, 'rb') as file:
            # Lê o cabeçalho
            mode_byte = file.read(1)
            if not mode_byte:
                print("Erro: Arquivo de compressão vazio ou inválido.")
                sys.exit(1)
            variable_bits = bool(struct.unpack('B', mode_byte)[0])

            max_bits_data = file.read(1)
            if not max_bits_data:
                print("Erro: Arquivo de compressão vazio ou inválido.")
                sys.exit(1)
            max_bits = struct.unpack('B', max_bits_data)[0]

            if max_bits < 9:
                print("Erro: max_bits no arquivo comprimido é menor que 9, o que é inválido.")
                sys.exit(1)

            # Lê o comprimento da extensão
            extension_length_data = file.read(1)
            if not extension_length_data:
                print("Erro: Arquivo de compressão vazio ou inválido.")
                sys.exit(1)
            extension_length = struct.unpack('B', extension_length_data)[0]

            # Lê a extensão
            extension_data = file.read(extension_length)
            if len(extension_data) != extension_length:
                print("Erro: Arquivo de compressão vazio ou inválido.")
                sys.exit(1)
            extension = extension_data.decode('utf-8')

            # Lê os dados comprimidos usando BitReader
            reader = BitReader(file)
            code_size = 9 if variable_bits else max_bits
            max_table_size_current = 2 ** code_size
            next_code = 256
            compressed = []

            while True:
                # Atualiza o code_size se necessário antes de ler
                if variable_bits and next_code >= max_table_size_current and code_size < max_bits:
                    code_size += 1
                    max_table_size_current = 2 ** code_size

                code = reader.read_bits(code_size)
                if code is None:
                    break
                compressed.append(code)
                next_code += 1

        # Definir o caminho do arquivo descomprimido com a extensão correta
        output_path = os.path.join(decompressed_dir, f"{file_base_name}.{extension}")

        try:
            decompressed = lzw_decompress(compressed, max_bits, variable_bits)
        except ValueError as ve:
            print(f"Erro durante a descompressão: {ve}")
            sys.exit(1)

        with open(output_path, 'wb') as file:
            file.write(decompressed)
        print(f"Arquivo descomprimido salvo como {output_path}")

        compressed_size = os.path.getsize(input_path)
        decompressed_size = os.path.getsize(output_path)
        compression_ratio = decompressed_size / compressed_size if compressed_size != 0 else 0
        print(f"Taxa de descompressão: {compression_ratio:.2f}")
        print(f"Bits utilizados: {max_bits}")
        print(f"Tempo de execução: {time.time() - start_time:.2f} segundos")

    else:
        print("Modo desconhecido. Use 'compress' ou 'decompress'.")
