/*function procurar2pessoas(){
var nomeBase1 = document.getElementById("pessoa1");
var nomeBase2 = document.getElementById("pessoa1");

var percentage = 98;

var output = "Podemos garantir com"  + percentage + "que" + nomeBase1 + " e " +nomeBase2 + "são a mesma pessoa nas bases de dados informadas.";
}

function selecionarOpcao(){

}
function verificar2bases(){
    var nomeBase1 = document.getElementById("pessoa1");
    var nomeBase2 = document.getElementById("pessoa1");
    var Base1;
    var Base2;
    
    var percentage = 98;
    
    var output = "As pessoas com maior similidaridade a pessoa informada são:";
}*/
function GetOption(){
    var select = document.getElementById('TipoConsulta');
    var value = select.options[select.selectedIndex].value;
    console.log(value);
    //buttonPage = document.getElementById('submit');
//BasesCruzadas, SaoAMesma
    switch (value) {
        case "Existe":
         // buttonPage.href="";
        document.getElementById('submit').href="bases-cruzadas.html";
        case "BasesCruzadas":
        document.getElementById('submit').href="bases-cruzadas.html";
          break;
        case "SaoAMesma":
            console.log("Comparacao");
          //  buttonPage.href="comparacao.html";
          document.getElementById('submit').href="comparacao.html";
            break;
    }
}

