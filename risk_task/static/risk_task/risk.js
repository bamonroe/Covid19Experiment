let risk_ns = new function() {

	// initialized globals for this namespace
	let chosen = {"A" : -1, "B" : -1}

let fill_lot_text = function (lotdat, risk_dat) {
	let outcomes   = risk_dat["num_ops"];
	let hex_colors = risk_dat["hex_colors"];
	// Set the text part of the choices
	for (let j = 0; j <= 1; j++) {
		let lot      = (j == 0 ? "A" : "B");
		let thislot  = lotdat["lot" + lot]
		let currency = lotdat["currency"];
		let probs    = thislot["probabilities"]
		let outs     = thislot["outcomes"]
		let captions = thislot["caption"]

		for (let i = 0; i <= outcomes; i++) {
			if (probs[i] > 0) {
				$("#" + lot + "_out" + i).html("Win " + currency + outs[i] + " if " + captions[i]);
				$("#" + lot + "_out" + i).css("color", hex_colors[i]);
				$("#" + lot + "_out" + i).css("fontWeight", "");
			} else {
				$("#" + lot + "_out" + i).html("&nbsp;");
			}
		}
	}
	$("#lhcA").html(lotdat["lotA"]["top_header"]);
	$("#lhcB").html(lotdat["lotB"]["top_header"]);
}

this.select_lot = function (lid) {
	// Capture time stamp as soon as lottery is selected
	log_event(lid)
	// Set the chosen lottery
	let olid = (lid == "A" ? "B" : "A");
	chosen[lid]  = (chosen[lid] == 1 ? 0 : 1);
	chosen[olid] = (chosen[lid] == 1 ? 0 : chosen[olid]);

	// Set the background color for the lotteries
	set_selected_bgcolor(chosen);
	// Enable submit button if a lottery is chosen
	$("#submit_button").prop('disabled', (chosen[lid] == 1 | chosen[olid] == 1 ? false : true));
}

let set_selected_bgcolor = function (chosen) {
	// The color for a selected lottery
	let selected_color = "#ADD8E6";
	// Set background color of selected lottery
	$("#lotA_cell").css("background-color", (chosen["A"] == 1 ? selected_color : ""))
	$("#lotB_cell").css("background-color", (chosen["B"] == 1 ? selected_color : ""))
}

this.submit_click = function () {
	if ((chosen["A"] == 1) | (chosen["B"] == 1)) {
		// Capture time stamp as soon as submit button is clicked
		log_event("submit")
		// Fill the form fields
		$("#choice").val((chosen["A"] == 1 ? 0 : 1));
		// Clear any submit message
		$("#submit_message").html("&nbsp;");
		// Remove the button type to submit
		$("#submit_button").prop("type", "");
	} else {
		$("#submit_message").html("You need to select a lottery before you can submit.");
	}
}

let make_pies = function (lotdat, risk_dat) {

	let hex_colors = risk_dat["hex_colors"];
	let currency   = risk_dat["currency"];

	for (let i = 0; i <= 1 ; i++) {
		let lot = (i == 0 ? "A" : "B")
		let thislot = lotdat["lot" + lot]
		let currency = lotdat["currency"];

		let outcome_labels = []
		for (let i = 0 ; i < thislot["outcomes"].length ; i++) {
			outcome_labels[i] = currency + thislot["outcomes"][i]
		}

		var myChart = new Chart($("#Lottery" + lot), {
			type: 'pie',
			data: {
				labels: outcome_labels,
				datasets: [{
					data : thislot["probabilities"],
					labels2: thislot["prob_labels"],
					backgroundColor: hex_colors,
				}],
			},
			options: {
				layout: {
					padding: {
						left: 20,
						right: 20,
						top: 20,
						bottom: 20
					}
				},
				tooltips : {
					enabled : false,
				},
				legend: {
					display : false
				},
				pieceLabel: [
					{ 
						render: "label",
						position: "outside",
						fontSize: 18,
						fontColor: "#000",
						fontStype: "bold"
					},
					{ 
						render: function(args) {
							return args.dataset.labels2[args.index];
						},
						precision: 2,
						fontSize: 18,
						fontColor: "#000",
						fontStype: "bold"
					}
				],
				events: []
			}
		});
	}
	//disable submit button upon initial painting of lotteries
	$("#submit_button").prop('disabled', true);
}

let fill_stuff = function(full_div, risk_dat, results = 0, show_submit = 1) {
	let options = risk_dat["options"];
	let num_ops = risk_dat["num_ops"];

	inhtml = "";
	inhtml += "<div id=\"results_text\">";
	inhtml += "<div id=\"task_chosen\"></div>\n";
	inhtml += "<div id=\"you_chose\"></div>\n";
	inhtml += "</div>\n";

	for (let i = 0 ; i < options.length ; i++) {
		opt = options[i];
		let onclick = (results == 0 ? "onclick=\"risk_ns.select_lot('" + opt + "');\"" : "");
		inhtml += "<div class=\"lot_div\" id=\"lot" + opt + "_cell\"" + onclick + " >\n";
		// inhtml += "<div class=\"lot_header\">Lottery " + opt + "</div>\n";
		let lotLabel = (opt==="A" ? "Left" : "Right");
		inhtml += "<div class=\"lot_header\">" + lotLabel + "</div>\n";
		inhtml += "<div id=\"lhc" + opt + "\" class=\"lot_header_caption\">&nbsp;</div>\n";
		inhtml += "<canvas id=\"Lottery" + opt + "\" width=\"400\" height=\"400\"></canvas>\n";
		for (let i = 0 ; i <= num_ops ; i++) {
			inhtml += "<div class=\"option_text\" id=\"" + opt + "_out" + i + "\">" + opt + " " + i + "</div>\n";
		}
		inhtml += "</div>\n";
	}
	inhtml += "<br>\n";

	// We don't show the submit button on the final page
	if (show_submit == 1 & results == 0) {
		inhtml += "<div class=\"submit\">\n";
		let onclick = (results == 0 ? "onclick=\"risk_ns.submit_click();\"" : "");
		let type    = (results == 0 ? "button" : "");
		inhtml += "<br>\n";
		inhtml += "<button class=\"btn btn-primary btn-large\" type=\"" + type + "\" id=\"submit_button\" " + onclick + ">Submit</button>\n";
		inhtml += "<div id=\"submit_message\"></div>\n";
		inhtml += "</div>\n";

		inhtml += "<input type=\"hidden\" name=\"choice\"     id=\"choice\"     value=-1 class=\"form-control\" required />\n";
		inhtml += "<input type=\"hidden\" name=\"timeStamps\" id=\"timeStamps\" value=-1 class=\"form-control\" />\n";
	}

	$("#" + full_div).html(inhtml);

}

this.mkview = function(risk_dat, full_div, results = 0, show_submit = 1) {
	let outcomes   = risk_dat["num_ops"];
	let lotdat     = risk_dat["lotdat"];
	let chosen     = {"A" : -1, "B" : -1}
	let hex_colors = risk_dat["hex_colors"];

	let local_chosen = chosen;
	// Some non-interface stuff
	$("#round_number").html(risk_dat["round_number"]);
	$("#number_of_rounds").html(risk_dat["number_of_rounds"]);

	fill_stuff(full_div, risk_dat, results, show_submit);
	// Set the text part of the choices
	fill_lot_text(lotdat, risk_dat);
	// Make the lottery pies
	make_pies(lotdat, risk_dat);
	// Some stuff just if we're showing results
	if (results == 1) {
		local_chosen["A"] = (risk_dat["choice_for_payment"] == 0 ? 1 : 0);
		local_chosen["B"] = (risk_dat["choice_for_payment"] == 0 ? 0 : 1);
		chosen = local_chosen;
		$("#task_chosen").html("Decision screen " + risk_dat["pair_for_payment"] + " was randomly selected for payment.");
		set_selected_bgcolor(chosen);

		// let inhtml = "You chose Lottery " + (chosen["A"] == 1 ? "A" : "B") + ".<br\ >\n";
		let lotLabel = (chosen["A"] == 1 ? "Left" : "Right");
		let inhtml = "Your choice is displayed below.<br>\n";
		inhtml += "You chose " + lotLabel + ".<br\ >\n";
		inhtml += "The random number chosen out of " + lotdat["num_events"] + " is " + risk_dat["random_number_for_pay"] + ".<br\ >\n";
			console.log(risk_dat["is_don"])
			console.log(risk_dat["random_number_for_don"])

		let is_don = 0;
		if (risk_dat["is_don"]) {
			is_don = 1;
			
			inhtml += "This outcome involves Double or Nothing.<br\>\n";

			if (risk_dat["random_number_for_don"] == 1) {
				inhtml += "The virtual coin toss landed on Heads.<br\>\n";
				inhtml += "As the virtual coin toss landed on Heads, you receive double earnings for this task.<br\>\n";
			} else {
				inhtml += "The virtual coin toss landed on Tails.<br \>\n";
				inhtml += "As the virtual coin toss landed on Tails, you receive no earnings for this task.<br\>\n";
			}
		}

		let fp = risk_dat["final_payment"]
		inhtml += "Based on your choice and the random number drawn, your earnings for this task are: " + fp["currency"] + fp["amounts"][0] + "<br>\n";
		inhtml += "<br>";
		if (show_submit == 1) {
			inhtml += "<br>";
			inhtml += "Click the Next button below to continue.\n";
			inhtml += "<br>";
			inhtml += "<button class=\"btn btn-primary btn-large\" type=\"\" id=\"submit_button\">Next</button>\n";
		}

		$("#you_chose").html(inhtml);
		// Enable submit button if a lottery is chosen
		$("#submit_button").prop('disabled', false);
		// disable hover highlighting when reviewing prior choice
		$(".lot_div").css('pointer-events', 'none');
	}
	// Capture the time the page was loaded in ms
	log_event("Start")
}
}
