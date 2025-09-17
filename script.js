// funcao para alterar o status exibido de um dispositivo
function changeStatus(id, txt) {
    let spanDevice = document.getElementById(id);
    spanDevice.innerText = txt;
    spanDevice.className = '';
    spanDevice.classList.add(txt);
}

// funcao para carregar o csv contendo o status dos dispositivos
async function loadCSV() {
    try {
        // carregando o arquivo
        var response = await fetch("status.csv");
        // obtendo o seu texto
        var text = await response.text();
        // quebrando por linhas
        var lines = text.split('\n');
        for (var i=0; i < lines.length; i++)
        {
            // quebrando por colunas
            var data = lines[i].split(',');
            if (data.length == 2)
            {
                changeStatus(data[0], data[1].toUpperCase())
            }
        }
        // adicionando este log para 'tentar' forçar as atualizações
        console.log("...")
    } catch (error) {
        console.error('Error loading CSV:', error);
    }
}

// carregando a funcao na inicializacao
loadCSV()
// chamando a funcao a cada 1s
setInterval(loadCSV, 1000);
