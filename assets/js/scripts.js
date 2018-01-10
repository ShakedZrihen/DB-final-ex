

function projects(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Typical action to be performed when the document is ready:
            document.getElementById("demo").innerHTML = xhttp.responseText;
        }
    };
    xhttp.open("GET", "filename", true);
    xhttp.send();
}

function deleteEngineer(id) {
    var toDelete = document.getElementById(id);
    var engineerId = toDelete.innerHTML
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Typical action to be performed when the document is ready:
            location.reload();
        }
    };
    xhttp.open("DELETE", "engineers", true);
    xhttp.send(engineerId);
}

function getPhones(){
    var phones = document.getElementsByClassName("new-phone-number");
    var phoneList = []
    for(var i=0; i< phones.length; i++){
        phoneList.push(phones[i].value);
    }
    return phoneList;
}

function showPhones(engineerId){
    var engineerIdStr = document.getElementById(engineerId).innerHTML;
    engineerIdStr = engineerIdStr.replace(".0", " ");

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Typical action to be performed when the document is ready:
            var phoneList = JSON.parse(xhttp.response);
             var form = document.getElementById("show-phone-list");
                while (form.firstChild) {
                    form.removeChild(form.firstChild);
                }
            for (phone in phoneList){
                var phoneNumber = phoneList[phone];
                var listTag =  document.createElement("li");
                var labelTag = document.createElement("label");
                labelTag.appendChild(document.createTextNode("Phone number: " + phoneNumber));
                listTag.appendChild(labelTag);
                form.appendChild(listTag);
            }
        }
    };
    var url = "/phones/" + engineerIdStr;
    xhttp.open("GET", url, true);
    xhttp.setRequestHeader("content-Type", "application/json");
    xhttp.send();
}

function addAnotherPhone(){
        var form = document.getElementById("phone-list");
        var listTag =  document.createElement("li");
        var labelTag = document.createElement("label");
        labelTag.appendChild(document.createTextNode("Phone number:     "));
        var inputTag = document.createElement("input");
        inputTag.setAttribute("class", "new-phone-number");
        inputTag.setAttribute("type", "tel");
        labelTag.appendChild(inputTag);
        var aTag = document.createElement("a");
        aTag.setAttribute("style", "margin: 0 0 3px 16px;");
        aTag.setAttribute("onclick", "addAnotherPhone()");
        aTag.setAttribute("class", "btn pmd-btn-fab pmd-btn-flat pmd-ripple-effect btn-default btn-sm");
        var iTag = document.createElement("i");
        iTag.setAttribute("class", "material-icons md-dark pmd-sm");
        iTag.appendChild(document.createTextNode("add"));
        aTag.appendChild(iTag);
        labelTag.appendChild(aTag);
        listTag.appendChild(labelTag);
        form.appendChild(listTag);
}

function addEngineer() {
    var addBtn = document.getElementById("add-engineer");
    addBtn.addEventListener("click", function(){
        var engineerTable = document.getElementById("engineer-table");
        var td = document.createElement("td");
        var tr = document.createElement("tr");
        tr.setAttribute("id", "new-row");
        var input = document.createElement("input");
        input.setAttribute("type", "text");
        input.setAttribute("style", "border: 1px solid rgba(0,0,0,0.02)");
        input.setAttribute("id", "first-name");
        td.appendChild(input);
        tr.appendChild(td);

        td = document.createElement("td");
        input = document.createElement("input");
        input.setAttribute("type", "text");
        input.setAttribute("style", "border: 1px solid rgba(0,0,0,0.02)");
        input.setAttribute("id", "last-name");
        td.appendChild(input);
        tr.appendChild(td);

        td = document.createElement("td");
        input = document.createElement("input");
        input.setAttribute("type", "text");
        input.setAttribute("style", "border: 1px solid rgba(0,0,0,0.02)");
        input.setAttribute("id", "id");
        td.appendChild(input);
        tr.appendChild(td);

        td = document.createElement("td");
        input = document.createElement("input");
        input.setAttribute("type", "text");
        input.setAttribute("style", "border: 1px solid rgba(0,0,0,0.02)");
        input.setAttribute("id", "field-id");
        td.appendChild(input);
        tr.appendChild(td);

        td = document.createElement("td");
        input = document.createElement("input");
        input.setAttribute("type", "text");
        input.setAttribute("style", "border: 1px solid rgba(0,0,0,0.02)");
        input.setAttribute("id", "address");
        td.appendChild(input);
        tr.appendChild(td);

        td = document.createElement("td");
        input = document.createElement("input");
        input.setAttribute("type", "text");
        input.setAttribute("style", "border: 1px solid rgba(0,0,0,0.02)");
        input.setAttribute("id", "birthday");
        td.appendChild(input);
        tr.appendChild(td);

        td = document.createElement("td");
        tr.appendChild(td);

        td = document.createElement("td");

        //  Add Phone Number
        var aTag = document.createElement('a');
        aTag.setAttribute("class", "btn pmd-btn-fab pmd-btn-flat pmd-ripple-effect btn-default btn-sm");
        var iTag = document.createElement("i");
        iTag.setAttribute("class", "material-icons md-dark pmd-sm");
        aTag.setAttribute("style", "margin-left: 38px");
        iTag.appendChild(document.createTextNode("phone"));
        aTag.appendChild(iTag);
        aTag.setAttribute("data-toggle", "modal");
        aTag.setAttribute("data-target", "#myModal");
        td.appendChild(aTag);
        tr.appendChild(td);

        td = document.createElement("td");
        aTag = document.createElement('a');
        aTag.setAttribute("class", "btn pmd-btn-fab pmd-btn-flat pmd-ripple-effect btn-default btn-sm");
        iTag = document.createElement("i");
        iTag.setAttribute("class", "material-icons md-dark pmd-sm");
        iTag.appendChild(document.createTextNode("done"));
        aTag.appendChild(iTag);
        aTag.addEventListener("click", function(){
            var phones = getPhones();
            var content = {
                "first_name": document.getElementById("first-name").value,
                "last_name": document.getElementById("last-name").value,
                "id": document.getElementById("id").value,
                "field_id": document.getElementById("field-id").value,
                "address": document.getElementById("address").value,
                "birthday": document.getElementById("birthday").value,
                "phones": phones
            };
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    // Typical action to be performed when the document is ready:
                    location.reload();
                }
            };
            xhttp.open("POST", "/engineers", true);
            xhttp.setRequestHeader("content-Type", "application/json");
            xhttp.send(JSON.stringify(content));
        });
        td.appendChild(aTag);
        aTag = document.createElement('a');
        aTag.setAttribute("class", "btn pmd-btn-fab pmd-btn-flat pmd-ripple-effect btn-default btn-sm");
        iTag = document.createElement("i");
        iTag.setAttribute("class", "material-icons md-dark pmd-sm");
        iTag.appendChild(document.createTextNode("close"));
        aTag.appendChild(iTag);
        aTag.addEventListener("click", function(){
            var toRemove = document.getElementById("new-row");
            toRemove.parentNode.removeChild(toRemove);
        });
        td.appendChild(aTag);
        tr.appendChild(td);
        engineerTable.appendChild(tr)
    });
}

addEngineer();
