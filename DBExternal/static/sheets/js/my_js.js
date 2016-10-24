

function Addtab(){
	var lightbox = document.getElementById("lightbox");
    var dimmer = document.createElement("div");
	dimmer.style.width =  window.innerWidth + 'px';
	dimmer.style.height = "200%";
	dimmer.className = 'dimmer';
	dimmer.id = "dimmer";

	dimmer.onclick = function(){
    	document.body.removeChild(this);   
    	lightbox.style.visibility = 'hidden';
	}

	document.body.appendChild(dimmer);
	$('html, body').animate({scrollTop:0}, 'slow');
    lightbox.style.visibility = 'visible';
    lightbox.style.top = window.innerHeight/3 - 50 + 'px';
    lightbox.style.left = "30%";
    return false;
}

function AddTabButton(i){
	window.tabs.push('tab'+i.toString());
 	GenerateMyTabs();
}
function AddDocform(){
	var lightbox = document.getElementById("lightbox");
    var dimmer = document.createElement("div");
	dimmer.style.width =  window.innerWidth + 'px';
	dimmer.style.height = "200%";
	dimmer.className = 'dimmer';
	dimmer.id = "dimmer";

	dimmer.onclick = function(){
    	document.body.removeChild(this);   
    	lightbox.style.visibility = 'hidden';
	}

	document.body.appendChild(dimmer);
	$('html, body').animate({scrollTop:0}, 'slow');
    lightbox.style.visibility = 'visible';
    lightbox.style.top = window.innerHeight/2 - 50 + 'px';
    lightbox.style.left = "30%";
    return false;
}

function Shareform(){
	var lightbox = document.getElementById("sharebox");
    var dimmer = document.createElement("div");
	dimmer.style.width =  window.innerWidth + 'px';
	dimmer.style.height = "200%";
	dimmer.className = 'dimmer';
	dimmer.id = "dimmer1";

	dimmer.onclick = function(){
    	document.body.removeChild(this);   
    	lightbox.style.visibility = 'hidden';
	}

	document.body.appendChild(dimmer);
	$('html, body').animate({scrollTop:0}, 'slow');
    lightbox.style.visibility = 'visible';
    lightbox.style.top = window.innerHeight/3 - 50 + 'px';
    lightbox.style.left = "30%";
    return false;
}

function ImageForm(){
	var lightbox = document.getElementById("imagebox");
	console.log(lightbox.innerHTML);
    var dimmer = document.createElement("div");
	dimmer.style.width =  window.innerWidth + 'px';
	dimmer.style.height = "200%";
	dimmer.className = 'dimmer';
	dimmer.id = "dimmer2";

	dimmer.onclick = function(){
    	document.body.removeChild(this);   
    	lightbox.style.visibility = 'hidden';
	}

	document.body.appendChild(dimmer);
	$('html, body').animate({scrollTop:0}, 'slow');
    lightbox.style.visibility = 'visible';
    lightbox.style.top = window.innerHeight/3 - 50 + 'px';
    lightbox.style.left = "30%";
    return false;
}

function hideimageform(){
	var lightbox = document.getElementById("imagebox");
    var dimmer = document.createElement("div");
	dimmer.style.width =  window.innerWidth + 'px';
	dimmer.style.height = "200%";
	dimmer.className = 'dimmer';
	dimmer.id = "dimmer1";

	dimmer.onclick = function(){
    	document.body.removeChild(this);   
    	lightbox.style.visibility = 'hidden';
	}

	document.body.appendChild(dimmer);
	$('html, body').animate({scrollTop:0}, 'slow');
    lightbox.style.visibility = 'visible';
    lightbox.style.top = window.innerHeight/3 - 50 + 'px';
    lightbox.style.left = "30%";
    return false;
}


function hideshareform(){
	var lightbox = document.getElementById("sharebox");
	document.getElementById("dimmer1").remove();
	lightbox.style.visibility = 'hidden';
}


// function Adddoc () {
// 	var table1 = document.getElementById("doc_table");
// 	    table1.border = "1";
// 	    table1.style.padding = "15px";
// 	    table1.className = "highlight responsive-table";
// 	    table1.innerHTML = "";
// 	    //Get the count of columns.
// 	    var columnCount1 = window.tabs[0].length;
// 	    //Add the header row.
// 	    var row1 = table1.insertRow(-1);
// 	    for (var i = 0; i < columnCount1; i++) {
// 	        var headerCell = document.createElement("TH");
// 	        headerCell.innerHTML = window.tabs[0][i];
// 	        if(i==0){
// 	        	headerCell.className = "waves-effect waves-light btn";
	        	
// 	        }
// 	        else{
// 	        	headerCell.className = "btn disabled";
	        	
// 	        }
// 	        headerCell.style.padding = "5px";
// 	        headerCell.style.width = "25px";

// 	        row1.appendChild(headerCell);
// 	    }

// }

function refreshtabs(){
	var tab_name = document.getElementById("table_name").value;
	var lightbox = document.getElementById("lightbox");
	document.getElementById("dimmer").remove();
	tabs.push(tab_name);
	lightbox.style.visibility = 'hidden';
	GenerateTabs();
}

function refreshdocs(){
	var doc_name = document.getElementById("doc_name").value;
	var lightbox = document.getElementById("lightbox");
	document.getElementById("dimmer").remove();
	var index = docs.length;
	if(docs[index-1].length < 1)
		{docs[index-1].push(doc_name);}
	else{
		window.docs.push([doc_name]);
	}
	lightbox.style.visibility = 'hidden';
	GenerateDocs();
}

function GenerateMyTabs(tabs){
	var my_tabs = document.getElementById("tab_table");
	var tuple_tabs=[];
   	var temp_tab=[];
	for(var j=0;j<tabs.length;j++){
		temp_tab.push(tabs[j]);
		if((j+1)%3==0){
			tuple_tabs.push(temp_tab);
			temp_tab=[];
		}
	}
	if(temp_tab.length!=0){
		tuple_tabs.push(temp_tab);
	}
	for( var i=0; i<tuple_tabs.length; i++){
		if(i==0){
			data="";
		}
		data = data + '<div class="row">\
										    <div class="col s12">\
										      <ul class="tabs">';
	    for( var j=0; j < tuple_tabs[i].length; j++){
	    	console.log(JSON.stringify(tuple_tabs[i][j].fields));
	    	var num=(i*3+j).toString();
	    	if(i*3+j==active_tab){ 
		    	data=data+'<a id="tabs'+(i*3+j).toString()+'" class="waves-effect waves-light btn-large col s4" onclick="display_table('+(i*3+j).toString()+')" >     '+tuple_tabs[i][j].fields.sheet_name+'</a>';
		    }
		    else{
		    	data=data+'<a id="tabs'+(i*3+j).toString()+'"class="waves-effect waves-light btn col s4" onclick="display_table('+(i*3+j).toString()+')">'+tuple_tabs[i][j].fields.sheet_name+'</a>';
		    }
	    }
		    data=data+'</ul>\
					    </div>\
					 </div>';	

	}
	my_tabs.innerHTML=data;


}

function GenerateTabs() {

	    //Build an array containing Customer records.
	    //var tabs = new Array();
	   // 

	    //Create a HTML Table element.
	    var table1 = document.getElementById("tab_table");
	    table1.border = "1";
	    table1.style.padding = "15px";
	    table1.className = "highlight responsive-table";
	    table1.innerHTML = "";
	    //Get the count of columns.
	    var columnCount1 = tabs[0].length;
	
	    //Add the header row.
	    var row1 = table1.insertRow(-1);
	    for (var i = 0; i < columnCount1; i++) {
	        var headerCell = document.createElement("TH");
	        headerCell.innerHTML = window.tabs[0][i];
	        if(i==0){
	        	headerCell.className = "waves-effect waves-light btn";
	        	
	        }
	        else{
	        	headerCell.className = "btn disabled";
	        	
	        }
	        headerCell.style.padding = "5px";
	        headerCell.style.width = "25px";

	        row1.appendChild(headerCell);
	    }

	    // var dvTable1 = document.getElementById("sheet_tab");
	    // dvTable1.innerHTML = "";
	    // dvTable1.appendChild(table1);
	}

function sheet_name_before_card(doc){
	    var win = '<div class="card small">\
									    <div class="card-image waves-effect waves-block waves-light">\
									      <img class="activator" src="/static/sheets/css/5.png">\
									    </div>\
									    <div class="card-content">\
									      <span class="card-title activator grey-text text-darken-4">';
		return win;
}

function sheet_name_after_card(doc,sign,i,permission){
		var win1;
		if(permission=="edit"){
			win1 = '<i class="material-icons right">more_vert</i></span>\
										      <p><a href="'+sign+'">Click to open sheet</a></p>\
										    </div>\
										    <div class="card-reveal">\
										      <span class="card-title grey-text text-darken-4">'+doc.fields.doc_name+'<i class="material-icons right">close</i></span>\
										      <p>\
										      Created By : '+doc.fields.created_by+'<br>\
										      Created On : '+doc.fields.created_on+'<br>\
										      </p>\
												<a class="waves-effect waves-light btn teal col s2" id="opener" href="'+sign+'delete_doc/">Delete this document</a><br>\
												<br>\
												<form id="rename_doc_form'+i.toString()+'" method="get" action="'+sign+'rename_doc/">\
												<label for="rename_id_'+i.toString()+'">New Name of sheet</label>\
												<input id="rename_id_'+i.toString()+'" type="text"  name="new_name" value="'+doc.fields.doc_name+'">\
												</form>\
												<a class="waves-effect waves-light btn teal col s2" id="opener" onclick="$(\'#rename_doc_form'+i.toString()+'\').submit()">Rename this document</a><br>\
										    </div>\
										</div>';
									}
		else{
			win1 = '<i class="material-icons right">more_vert</i></span>\
										      <p><a href="'+sign+'">Click to open sheet</a></p>\
										    </div>\
										    <div class="card-reveal">\
										      <span class="card-title grey-text text-darken-4">'+doc.fields.doc_name+'<i class="material-icons right">close</i></span>\
										      <p>\
										      Created By : '+doc.fields.created_by+'<br>\
										      Created On : '+doc.fields.created_on+'<br>\
										      </p>\
									    </div>\
										</div>';
		}							
		return win1;							
}

function GenerateDocs(docs1,signs,permissions) {
	    //Create a HTML Table element.
	    console.log(JSON.stringify(docs1));
	    var table1 = document.getElementById("doc_table");
	    table1.border = "1";
	    table1.style.padding = "15px";
	    table1.className = "highlight responsive-table";
	    table1.innerHTML = "";

	    var docs=[];
	   	var temp_doc=[];
	    for(var j=0;j<docs1.length;j++){
	    	temp_doc.push(docs1[j]);
	    	if((j+1)%3==0){
	    		docs.push(temp_doc);
	    		temp_doc=[];
	    	}
	    }
	    if(temp_doc!=[]){
	    	docs.push(temp_doc);
	    }
	    //Add the header row.
	    var win = '<div class="card small">\
									    <div class="card-image waves-effect waves-block waves-light">\
									      <img class="activator" src="/static/sheets/css/5.png">\
									    </div>\
									    <div class="card-content">\
									      <span class="card-title activator grey-text text-darken-4">';


		for( var j=0; j<docs.length; j++){
			var row = table1.insertRow(-1);		    
		    for( var i=0; i < docs[j].length; i++){
		    	var cell = row.insertCell(-1);
	            cell.style.border= "1px solid #eeeeee";
	            cell.style.padding ="10px";
	            cell.innerHTML = win+ docs[j][i].fields.doc_name + sheet_name_after_card(docs[j][i],signs[j*docs[j].length+i],i+3*j,permissions[j*docs[j].length+i]);
		    }
		}
	}

function GenerateTable(i) {

    //Build an array containing Customer records.
    var table=cells[i];
    var sheet=sheets[i];
    //Create a HTML Table element.
    var table = document.createElement("TABLE");
    table.border = "1";
    table.className = "";

    //Get the count of columns.
    var columnCount = sheet.fields.total_columns;
    
    //Add the header row.
    var row = table.insertRow(-1);
    for (var j = 0; j < columnCount; j++) {
        var headerCell = document.createElement("TH");
	     headerCell.innerHTML='<div id="r'+(0).toString()+'_c'+j.toString()+'" contenteditable="true">'+''+'</div>'
         headerCell.style.backgroundColor = "#e0e0e0";
         headerCell.style.border= "1px solid #9e9e9e";
        headerCell.background="black";
        row.appendChild(headerCell);
    }

    //Add the data rows.
    for (var i = 1; i < sheet.fields.total_rows; i++) {
        row = table.insertRow(-1);
        for (var j = 0; j < sheet.fields.total_rows; j++) {
            var cell = row.insertCell(-1);
            cell.style.border= "1px solid #eeeeee";
	        cell.innerHTML='<div id="r'+i.toString()+'_c'+j.toString()+'" style="height:100%" contenteditable="true">'+''+'</div>';
        }
    }

    var dvTable = document.getElementById("dvTable");
    dvTable.innerHTML = "";
    dvTable.appendChild(table);
}
