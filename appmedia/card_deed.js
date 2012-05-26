    var CardsCount = 0;
    
    var a=new Array();
	var b=new Array();

	var single = new Array();
	var j = new Array();
	var y = new Array();
	var s = new Array();
	var h = new Array();
	
	//-----------------------------------------------------------------------------
	// Таблицы транслитерации
	single['a'] = 'а';
	single['b'] = 'б';
	single['v'] = 'в';
	single['g'] = 'г';
	single['d'] = 'д';
	single['e'] = 'е';
	single['z'] = 'з';
	single['i'] = 'и';
	single['k'] = 'к';
	single['l'] = 'л';
	single['m'] = 'м';
	single['n'] = 'н';
	single['o'] = 'о';
	single['p'] = 'п';
	single['r'] = 'р';
	single['s'] = 'с';
	single['t'] = 'т';
	single['u'] = 'у';
	single['f'] = 'ф';
	single['c'] = 'ц';
	//single['y'] = 'ы';
	single['y'] = 'й';
	single['"'] = 'ъ';
	single["'"] = 'ь';

	single['A'] = 'А';
	single['B'] = 'Б';
	single['V'] = 'В';
	single['G'] = 'Г';
	single['D'] = 'Д';
	single['E'] = 'Е';
	single['Z'] = 'З';
	single['I'] = 'И';
	single['K'] = 'К';
	single['L'] = 'Л';
	single['M'] = 'М';
	single['N'] = 'Н';
	single['O'] = 'О';
	single['P'] = 'П';
	single['R'] = 'Р';
	single['S'] = 'С';
	single['T'] = 'Т';
	single['U'] = 'У';
	single['F'] = 'Ф';
	single['C'] = 'Ц';
	single['Y'] = 'Ы';

	j['o'] = 'ё';
	j['j'] = 'й';
	j['u'] = 'ю';
	j['a'] = 'я';
	
	y['e'] = 'є';
	y['o'] = 'ё';
	y['u'] = 'ю';
	y['a'] = 'я';

	j['O'] = 'Ё';
	j['J'] = 'Й';
	j['U'] = 'Ю';
	j['A'] = 'Я';
	
	y['E'] = 'Є';
	y['O'] = 'Ё';
	y['U'] = 'ю';
	y['A'] = 'Я';

	h['z'] = 'ж';
	h['k'] = 'х';
	h['c'] = 'ч';
	h['s'] = 'ш';
	h['sh'] = 'щ';
	h['e'] = 'э';

	h['Z'] = 'Ж';
	h['K'] = 'Х';
	h['C'] = 'Ч';
	h['S'] = 'Ш';
	h['SH'] = 'Щ';
	h['E'] = 'Э';

	s['ch'] = 'щ';
	s['h'] = 'ш';

	/*
	Таблицы ГОСТ-а 16876-71

	Буквы j и h используются в качестве модификаторов, причем j ставится перед основной буквой, а h - после основной буквы.

	 а - a       к - k       х - kh
	 б - b       л - l       ц - c
	 в - v       м - m       ч - ch
	 г - g       н - n       ш - sh
	 д - d       о - o       щ - shh
	 е - e       п - p       ъ - "
	 ё - jo      р - r       ы - y
	 ж - zh      с - s       ь - '
	 з - z       т - t       э - eh
	 и - i       у - u       ю - ju
	 й - jj      ф - f       я - ja
	*/

	//-----------------------------------------------------------------------------
	// 
	function findA(c)
	{
		for (i=0; i < a.length; i++)
			if (a[i] == c) return i;
		return -1;
	}
	
	//-----------------------------------------------------------------------------
	// транслитератор by Щеглов Константин
	function transliterateText(src)
	{

		var res = '';

		for (i=0; i < src.length; i++)
		{
			c = src.charAt(i);
			c1 = src.charAt(i+1);
			if (c == 'y' && y[c1] != null)
			{
				res += y[c1];
				i++;
			}
			else if (c == 'j' && j[c1] != null)
			{
				res += j[c1];
				i++;
			}
			else if (c == 's')
			{
				if (c1=='h')
				{
					res += s['h'];
					i += 1;
				}
				else if (c1=='c' && src.charAt(i+2) == 'h')
				{
					res += s['ch'];
					i += 2;
				}
				else
				{
					res += single[c];
				}
			}
			else if (c1 == 'h')
			{
				if (c == 's' && c1=='h' && src.charAt(i+2) == 'h')
				{
					res += h['sh'];
					i += 2;
				}
				else
				{
					if (h[c] != null)
						res += h[c];
					else
						res +=c;
					i++;
				}
			}
			else if (single[c] != null && single[c] != null)
			{
				res += single[c];
			}
			else
			{
				res += c;
			}       	
		}
		//alert(res);
			
		return res;
	}

	//-----------------------------------------------------------------------------
	//
    function CardNameChanged(id, card_number) {
    	//var reader_enabled = document.getElementById("reader_enabled").checked;
    	
    	var text = document.getElementById(id).value;
    	
    	if (text.charAt(0) == '%') {
    		document.getElementById("card_number" + card_number).value = text.substring(2,18);
    		
    		var s = text.substring(19,45);
		s = s.toLowerCase();
    		
    		var translit_enabled = document.getElementById("translit_enabled").checked;
    		if (translit_enabled) {
    			s = transliterateText(s);
    			}
    		
    		var words = s.split("/");
    		
    		var strOut = '';
    		
    		for (i = 0; i < words.length; i++) {
    			firstChar = words[i].substring(0,1);
       			remainChar = words[i].substring(1);
       			
       			firstChar = firstChar.toUpperCase(); 
       			remainChar = remainChar.toLowerCase();
       			
       			strOut += firstChar + remainChar + ' ';
    			}
    		
    		document.getElementById(id).value = strOut;
    		
    		var checked_enabled = document.getElementById("checked_enabled").checked;
    		if (checked_enabled) {
    		   document.getElementById("have_pin"+card_number).checked = true;
            }
    	}
    }
	
    //-----------------------------------------------------------------------------
	//
    function CreditCardChanged(id) {
    	var text = document.getElementById(id).value;
    	
    	if (text.charAt(0) == '%') {
    		document.getElementById(id).value = text.substring(2,18);
    	}
    }
	
    //-----------------------------------------------------------------------------
	// 
    function AddRowsToTable(count) {
	    var card_records = document.getElementById("card_records");
		
		for (var i = 0; i < count; i++) {
			CardsCount += 1;
			var new_row = card_records.insertRow(CardsCount);
			var a = new_row.insertCell(0);
			var b = new_row.insertCell(1);
			var c = new_row.insertCell(2);
			var d = new_row.insertCell(3);
			var e = new_row.insertCell(4);
            var f = new_row.insertCell(5);
			a.innerHTML = CardsCount;
			b.innerHTML = '<input id="card_name'+ CardsCount +'" name="card_name'+ CardsCount +'" type="text" class="name_field" onchange="CardNameChanged(this.id, '+ CardsCount +')"/>';
			c.innerHTML = '<input id="card_number'+ CardsCount +'" name="card_number'+ CardsCount +'" type="text" class="number" />';
			d.innerHTML = '<input id="card_credit'+ CardsCount +'" name="card_credit'+ CardsCount +'" type="text" class="number" onchange="CreditCardChanged(this.id)"/>';
			e.innerHTML = '<input id="have_pin'+ CardsCount +'" name="have_pin'+ CardsCount +'" type="checkbox" />';
            f.innerHTML = '<input id="card_note'+ CardsCount +'" name="card_note'+ CardsCount +'" type="text" class="number" />';
			}
		
    }
    
    //-----------------------------------------------------------------------------
	// 
    function RemoveRowFromTable() {
    	var card_records = document.getElementById("card_records");
    	
    	if (CardsCount == 0) {
    		return;
    	}
    	
    	card_records.deleteRow(CardsCount);
    	CardsCount -= 1;
    }
    
    //-----------------------------------------------------------------------------
	// 
    function PrintDeed() {
    	var client_name = document.getElementById("client_name").value;
    	var date_doc = document.getElementById("date_doc").value;
    
    
    	var html = '<html>\n<head>\n<title>\n Акт '  + client_name + ' від ' + date_doc +  '\n</title>\n';
    	html += '<META http-equiv="content-type" content="text/html; charset=utf-8">\n</head>\n<body>\n';
    	html += '<p style="margin:8px; font: bold 12pt arial">Акт прийому передачі карток на ' + client_name + ' від ' + date_doc + '</p>\n\n';
    	html += '<table cellspacing="0" cellpadding="2"> \n'
    	html += '<tr style="background:black"><th style="border: 1px solid black; background:white;"> № </th>'
    	     +'<th width="350" style="border: 1px solid black; background:white;"> П.І.Б.	</th>'
    	     +'<th width="250" style="border: 1px solid black; background:white;"> Номер зп. карти </th>'
    	     +'<th width="250" style="border: 1px solid black; background:white;"> Номер кр. карти </th>'
    	     +'<th width="100" style="border: 1px solid black; background:white;"> Зп. картку отримав </th>'
    	     +'<th width="100" style="border: 1px solid black; background:white;"> Кред. картку отримав</th>'
    	     +'</tr>\n';
    	
    	var card_names = document.getElementsByName("card_name");
    	var card_numbers = document.getElementsByName("card_number");
    	var card_credits = document.getElementsByName("card_credit");
    	
    	for (var i = 0; i < card_names.length; i++) {
	    	var card_name = card_names[i].value;
	    	var card_number = card_numbers[i].value;
	    	var card_credit = card_credits[i].value;
	    	
	    	html += '<tr style="background:black">\n<td style="border: 1px solid black; background:white">\n' 
	    		 + (i+1) + ' </td><td style="border: 1px solid black; background:white;">\n' 
	    		 + card_name + '&nbsp; </td><td style="border: 1px solid black; background:white;">\n' 
	    		 + card_number + '&nbsp; </td><td style="border: 1px solid black; background:white;">\n' 
	    		 + card_credit + '&nbsp; </td>\n'
	    		 + '<td style="border: 1px solid black; background:white;">&nbsp;</td>'
	    		 + '<td style="border: 1px solid black; background:white;">&nbsp;</td>'
	    		 +'</tr>';
	    	
    		}
    	
    	html += '</table>\n<p>'; 
    	html += '<p>Картки передав ___________________________ \n'
    	html += '<p>Картки прийняв ___________________________ \n'
    	html += '</body>\n</html>'
    	
    	//alert(html);
    	var myWindow = window.open('','','');
		myWindow.document.write(html);
    }
