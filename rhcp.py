import abc, csv, re

class IRHCP(abc.ABC):
    methods: list = []
    response_codes: dict = {}

    def _validate_method(self, method: str) -> bool:
        return method in self.methods

    @abc.abstractmethod
    def format_request(self, request: str) -> None:
        pass

    @abc.abstractmethod
    def validate(self) -> str:
        pass

    @abc.abstractmethod
    def read_file(self, filename: str):
        pass

    @abc.abstractmethod
    def write_file(self, filename: str, rows):
        pass

    @abc.abstractmethod
    def response(self, status_code: str, obj: str|None = None, status: str|None = None) -> str:
        pass

    @abc.abstractmethod
    def process(self) -> str:
        pass


class RHCP1_0(IRHCP):
    '''
    Implementação do protocolo RHCP/1.0

    Para utilizar, crie uma instância da classe.
    Depois, passe a requisição para o método format_request.
    Após isso, chame o método process, que retornará a resposta da requisição.
    '''

    methods: list = ['GET', 'SET']
    response_codes: dict = {
        '200': '200 OK',
        '400': '400 Bad Request',
        '404': '404 Not Found',
        '405': '405 Method Not Allowed',
        '500': '500 Internal Server Error'
    }

    def format_request(self, request: str) -> None:
        '''
        Formata a requisição (self.request) para um dicionário com os seguintes campos:
        
            header: {
                method: <método>,
                object: <objeto>,
                version: <versão do protocolo>
            },
            body: [
                {field: <campo>, value: <valor>},
                ...
            ]

        Caso haja algum erro de sintaxe ou semântica, o atributo self.request é definido como None
        '''
        request_splitted: list[str] = request.split('\r\n')
        lines_number: int = len(request_splitted)
        if lines_number < 4:
            self.request = None
            return
        
        if (request_splitted[lines_number - 1] != ''
            or request_splitted[lines_number - 2] != ''):
            self.request = None
            return
        
        temp_header: list = request_splitted[0].split(' ')
        if len(temp_header) != 3:
            self.request = None
            return
        
        header: dict = {}
        header['method'] = temp_header[0]
        header['object'] = temp_header[1]
        header['version'] = temp_header[2]

        new_request: dict = {}

        new_request['header'] = header
        new_request['body'] = []

        fields: list = request_splitted[1:(lines_number - 2)]
        for field in fields:
            itens: list = field.split(': ')
            error: bool = (
                len(itens) <= 1
                or (itens[0] not in ['Request', 'Status'])
                or (itens[0] == 'Request' and itens[1] != 'status')
                or (itens[0] == 'Status' and itens[1] not in ['on', 'off'])
                or (new_request['header']['method'] == 'GET' and itens[0] == 'Status')
                or (new_request['header']['method'] == 'SET' and itens[0] == 'Request')
            )

            if error:
                self.request = None
                return
            
            body_item: dict = {'field': itens[0], 'value': itens[1]}
            new_request['body'].append(body_item)
        self.request = new_request
    
    def validate(self) -> str|None:
        '''
        Verifica se houve algum erro de sintaxe ou de método não permitido
        '''
        if self.request is None:
            return self.response('400')
        if not self._validate_method(self.request['header']['method']):
            return self.response('405')
        return None
        
    def read_file(self, filename):
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            return [row for row in reader]
        
    def write_file(self, filename, rows):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

            
    def response(self, status_code: str, obj: str|None = None, status: str|None = None) -> str:
        '''
        Formata a resposta do servidor.
        Caso tenha acontecido algum erro na requisição (status != 200), é retornado uma mensagem no formato:

        "RHCP/1.0 <Código e descrição do erro>\\r\\n\\r\\n"

        Se a requisição for status 200, o seguinte formato é retornado:
        
        "RHCP/1.0 200 OK\\r\\nObject: <objeto>\\r\\nStatus: <status>\\r\\n\\r\\n"
        '''
        if status_code != '200':
            return f'RHCP/1.0 {self.response_codes[status_code]}\r\n\r\n'
        return f'RHCP/1.0 200 OK\r\nObject: {obj}\r\nStatus: {status}\r\n\r\n'
    
    def process(self) -> str:
        '''
        Processa a requisição.
        
        Caso a requisição seja válida, realiza a operação do método GET ou SET.

        Retorna uma resposta formatada.
        '''
        response = self.validate()
        if response is not None: return response
        filename: str = 'status.csv'
        file_content: list = []
        try:
            file_content = self.read_file(filename)
        except:
            return self.response('500')
        for i, line in enumerate(file_content):
            if self.request['header']['object'] == line[0]:
                match self.request['header']['method']:
                    case 'GET':
                        return self.response('200', line[0], line[1])
                    case 'SET':
                        # Como só existe um campo nessa versão do protocolo
                        # Ele vai pegar o valor do primeiro campo inserido no body
                        new_status = self.request['body'][0]['value']
                        line[1] = new_status
                        file_content[i] = line
                        self.write_file(filename, file_content)
                        return self.response('200', line[0], line[1])
        return self.response('404')
    

def getRHCP(version: str) -> IRHCP:
    '''
    Retorna o protocolo RHCP correspondente a versão passada.
    Retorna None se não existir uma implementação para a versão passada.
    '''
    match version:
        case '1.0':
            return RHCP1_0()
        case _:
            return None


def find_version(texto: str) -> str | None:
    """
    Extrai a versão de um texto no formato RHCP/<versão>\r ou RHCP/<versão>\n.
    Retorna a versão como string, ou None se não encontrar.
    """
    padrao = re.compile(r"RHCP/([^\r\n]+)")
    match = padrao.search(texto)
    if match:
        return match.group(1)
    return None
