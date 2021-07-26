
function changeMenu () {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/login/menu', true);
        // Envia a informação do cabeçalho junto com a requisição.
    
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.onreadystatechange = function() { // Chama a função quando o estado mudar.
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            var data = JSON.parse(this.responseText)
            if  (data.tipoUsuario === 'Administrador') {
                HidenMenuAdmn();
            } else if( data.tipoUsuario === 'Cliente'){
				HidenMenuClient();
            } else {
                HidenMenuFuncio();
            }
        }
    }
    xhr.send();
    // xhr.send(new Int8Array());
    // xhr.send(document);
}   

function HidenMenuClient () {
	document.getElementById('LiFornecedor').classList.add('display');
	document.getElementById('LiEmpresa').classList.add('display');
	document.getElementById('LiProduto').classList.add('display');
	document.getElementById('LiDevelopmen').classList.add('display');
}

function HidenMenuFuncio () {
	document.getElementById('LiFornecedor').classList.add('display');
	document.getElementById('LiEmpresa').classList.add('display');
	document.getElementById('LiProduto').classList.add('display');
	document.getElementById('LiUsuario').classList.add('display');
	document.getElementById('LiDevelopmen').classList.add('display');

}

function HidenMenuAdmn() {
	return  
}

changeMenu();