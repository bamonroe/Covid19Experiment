let ca_ns = new function() {

// Some globals
let days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
let month_abbvr   = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

let T_clicks  = 0
let B_clicks  = 0

let T_choice = -1
let B_choice = -1

let start_time = "";

// Set the Main table for choices
let set_main_table = function() {
	let options = [ca_ns.pairdat["option_A"], ca_ns.pairdat["option_B"]]
	if (ca_ns.pairdat["top_opt"] == "B") {
		options = [ca_ns.pairdat["option_B"], ca_ns.pairdat["option_A"]]
	}
	console.log(options);
	for (let i = 0; i < 2; i++) {
		let tb = (i == 0 ? "t" : "b")
		$(".p0").html(ca_ns.pairdat["p0_caption"])
		$(".p1").html(ca_ns.pairdat["p1_caption"])
		$(".SS_delay").html(ca_ns.pairdat["SS_delay"] + " days")
		$(".LL_delay").html(ca_ns.pairdat["LL_delay"] + " days")
		$("#" + tb + "S0").html(ca_ns.cur + options[i]["S0"] + " in ")
		$("#" + tb + "L0").html(ca_ns.cur + options[i]["L0"] + " in ")
		$("#" + tb + "S1").html(ca_ns.cur + options[i]["S1"] + " in ")
		$("#" + tb + "L1").html(ca_ns.cur + options[i]["L1"] + " in ")
	}
	//disable submit button upon initial painting of lotteries
	$("#submit_button").prop('disabled', true);
}

// Function to change colors and fill out choices
this.click_check = function(val) {
	log_event(val)
	if (val == "t") {
		T_clicks += 1
		if (B_choice == 1) {
			T_choice = 1
			B_choice = 0
		} else if (T_choice == 1) {
			T_choice = -1
			B_choice = -1
		} else {
			T_choice = 1
			B_choice = 0
		}
	} else if (val == "b") {
		B_clicks += 1
		if (T_choice == 1) {
			T_choice = 0
			B_choice = 1
		} else if (B_choice == 1) {
			T_choice = -1
			B_choice = -1
		} else {
			T_choice = 0
			B_choice = 1
		}
	}

	// Set the selected and unselected option colors
	select_option();
}

let select_option = function() {
	// Set the selected and unselected option colors
	$("#option_t").css("border",           (T_choice <= 0 ? "1px solid black" : "2px solid red"))
	$("#option_t").css("background-color", (T_choice <= 0 ? ""                : "#ADD8E6"))
	$("#option_t").css("fontWeight",       (T_choice <= 0 ? ""                : "bold"))

	$("#option_b").css("border",           (B_choice <= 0 ? "1px solid black" : "2px solid red"))
	$("#option_b").css("background-color", (B_choice <= 0 ? ""                : "#ADD8E6"))
	$("#option_b").css("fontWeight",       (B_choice <= 0 ? ""                : "bold"))
	// Enable submit button if a choice is selected
	$("#submit_button").prop('disabled', (T_choice == 1 | B_choice == 1 ? false : true));
}

// Check that necessary conditions are completed so subject can proceed
let done_check = function() {
	return(T_choice >=0 & B_choice >= 0);
}

// Fill out the form inputs
let fill_form = function() {
	$("#choice").val((T_choice == 1 ? "0" : "1"))

}

this.submit_click = function() {
	let msg = "You need to select one of the two options to proceed"
	if (done_check()) {
		log_event("submit")
		fill_form();
		$("#submit_message").html("");
		$("#submit_button").prop("type", "");
	} else {
		$("#submit_message").html(msg);
	}
}

let max2 = function(val1, val2) {
	if (val1 > val2) {
		return(val1)
	} else {
		return(val2)
	}
}

let get_delay_date = function(today_date, today_month, delay) {
	let num_months = 0;
	let num_days   = today_date + delay;
	let ref_month  = days_in_month[today_month];
	while (num_days > ref_month) {
		num_months+=1;
		lookup_month = today_month + num_months;
		// Loop back to January if we're past december
		if (lookup_month > 11) {
			lookup_month -= 12;
		}
		num_days -= ref_month;
		ref_month  = days_in_month[lookup_month];
		console.log("Num days");
		console.log(num_days);
		console.log("ref month");
		console.log(ref_month);
	}
	return([num_months, num_days])
}

let get_delays = function() {
	return {"ss": ca_ns.pairdat["SS_delay"], "ll": ca_ns.pairdat["LL_delay"]}
}

let set_calendar = function() {
	// Get the delays from the timesheet
	let delays = get_delays()

	// Get today's things
	let today = new Date(
		ca_ns.start_time[0],
		ca_ns.start_time[1],
		ca_ns.start_time[2],
		ca_ns.start_time[3],
		ca_ns.start_time[4],
	);

	let today_year  = today.getFullYear();
	let today_month = today.getMonth();
	let today_date  = today.getDate();
	let today_day   = today.getDay();

	let ss_delay_md = get_delay_date(today_date, today_month, delays["ss"])
	let ll_delay_md = get_delay_date(today_date, today_month, delays["ll"])

	let ss_month = today_month + ss_delay_md[0]
	let ss_date  = ss_delay_md[1]
	let ll_month = today_month + ll_delay_md[0]
	let ll_date  = ll_delay_md[1]

	let ss_year = today_year;
	let ll_year = today_year;

	console.log(ss_month);
	console.log(ll_month);

	// Adjust future dates for delays running into the next year
	if (ss_month > 11) {
		ss_month -= 12;
		ss_year += 1;
	}
	if (ll_month > 11) {
		ll_month -= 12;
		ll_year += 1;
	}

	let ss_header = ss_date + " " + month_abbvr[ss_month] + " " + ss_year;
	let ll_header = ll_date + " " + month_abbvr[ll_month] + " " + ll_year;

	if (delays["ss"] == 0) {
		ss_header += "\n(Today)"
	} else {
		ss_header += "\n(" + delays["ss"] + " days from today)"
	}

	if (delays["ll"] == 0) {
		ll_header += "\n(Today)"
	} else {
		ll_header += "\n(" + delays["ll"] + " days from today)"
	}

	$("#ss_header").html(ss_header);
	$("#ll_header").html(ss_header);

	// Get the staring day
	let first_of_month = new Date(today_year, today_month, 1, 0, 0, 0, 1)
	let first_dow      = first_of_month.getDay();

	// The calandar for this month
	let cal = make_calendar(first_dow, today_month, 0,
		today_month, today_date, ss_month, ss_date, ll_month, ll_date)

	let out_html = "<div>" + cal[1] + "</div>";

	// Number of monthly calenars to display
	let num_cals_to_display = max2(ll_delay_md[0] + 1, 5)

	for (let i = 1; i < num_cals_to_display; i ++ ) {
		// The Table style for any particular element
		let this_month = (today_month + i) % 12;
		cal = make_calendar(cal[0] + 2, this_month, i,
			today_month, today_date, ss_month, ss_date, ll_month, ll_date)

		out_html += "<div>" + cal[1] + "</div>";
	}


	$("#calendar").html(out_html);
	$("#today_date").css("border", "2px solid black");
	$("#today_date").css("padding", "0px");

	$("#ss_date").css("background-color", ca_ns.hex_colors[0]);
	$("#ll_date").css("background-color", ca_ns.hex_colors[1]);

}

let make_calendar = function(start_dow, month_num, cal_id,
	today_month, today_date, ss_month, ss_date, ll_month, ll_date) {

	let start_table = "<table class='cal_month' id=cal'" + cal_id +"'>\n"
	let month_head = "<tr><td colspan=7>" + month_abbvr[month_num] + "</td></tr>"
	let dow_head = "<tr><th>Su</th> <th>Mo</th> <th>Tu</th> <th>We</th> <th>Th</th> <th>Fr</th> <th>Sa</th> </tr>\n"
	let end_table = "</table>\n"

	// Construct the calendar
	let in_html = ""
	let end_val = days_in_month[month_num] + start_dow
	let da = 0
	let di = ""
	let dotw = 0

	let td_tag = "<td>"

	for (let d = 0; d < end_val ; d++) {

		if (d >= start_dow) {
			da += 1
			di = da
		}

		td_tag = "<td>"

		if (month_num == today_month) {
			if (da == today_date) {
				td_tag = "<td id=\"today_date\">"
			}
		}
		if (month_num == ss_month) {
			if (da == ss_date) {
				td_tag = "<td id=\"ss_date\">"
			}
		}
		if (month_num == ll_month) {
			if (da == ll_date) {
				td_tag = "<td id=\"ll_date\">"
			}
		}


		if (d == 0) {
			in_html += "<tr>" + td_tag + di + "</td>"
		} else if ((d + 1) == end_val) {
			if (d % 7 == 0) {
				in_html += "</tr><tr>" + td_tag + di + "</td></tr>"
			} else {
				in_html += td_tag + di + "</td></tr>"
			}
		} else if (d % 7 == 0) {
			dotw = 0
			in_html += "</tr><tr>\n" + td_tag + di + "</td>"
		} else {
			dotw += 1
			in_html += td_tag + di + "</td>"
		}
	}

	let out_html = start_table + month_head + dow_head + in_html + end_table;
	return([ dotw, out_html])
}

let make_charts = function() {
	let p0 = ca_ns.pairdat["p0"];
	let p1 = ca_ns.pairdat["p1"];
	let p0_label = ca_ns.pairdat["p0_label"];
	let p1_label = ca_ns.pairdat["p1_label"];
	let p0_caption = ca_ns.pairdat["p0_caption"];
	let p1_caption = ca_ns.pairdat["p1_caption"];

	let pie_data = {
		labels: [p0_label, p1_label],
		datasets: [{
			data: [p0, p1],
			labels2: [p0_label, p1_label],
			backgroundColor: ["#ffffff", "#ffffff"],
			borderColor: ["#000000", "#000000"]
		}],
	}
	let pie_options = {
		rotation: (-.5 - p0 ) * Math.PI,
		legend : {
			display: false,
		},
		tooltips: {
			callbacks: {
				label: function(tooltipItem, data) {
					var label = data.datasets[tooltipItem.datasetIndex].labels2[tooltipItem.index] || '';
					return(label);
				}
			}
		},
		pieceLabel: [
			{
				render: function(args) {
					return args.dataset.labels2[args.index];
				},
				textMargin: 15,
				position: "outside",
				precision: 2,
				fontSize: 18,
				fontColor: "#000",
				fontStype: "bold"
			}
		]
	}

	for (let i = 0; i < 2; i++ ) {
		var myChart = new Chart($("#pie_" + (i == 0 ? "t" : "b")), {
			type: "pie",
			data: pie_data,
			options: pie_options
		}); 
	}
}

let fill_full_div = function(full_div, results = 0, show_submit = 1) {

	let do_onclick = "";
	let fp = ca_ns.ca_dat["final_payment"];

	inhtml = "";
	if (results == 1) {
		inhtml += "<div id=\"results_text\">\n";
		inhtml += "<span id='screen_for_payment'>Decision screen <span id=\"pair_for_pay\"></span> was chosen for payment.</span><br>\n";
		inhtml += "You selected the <span id=\"choice_for_pay\"></span> option.<br>\n";
		inhtml += "The number " + ca_ns.ca_dat["rand_num_for_payment"] + " was chosen out of " + ca_ns.pairdat["num_events"] + ".<br>\n";
		inhtml += "You will be paid ";

		in_on       = (fp["is_date"] ? " on " : " in ");;
		days_nodays = (fp["is_date"] ? "" : " days");

		inhtml += fp["currency"] + fp["amounts"][0] + in_on + fp["when"][0] + days_nodays;
		inhtml += " AND ";
		inhtml += fp["currency"] + fp["amounts"][1] + in_on + fp["when"][1] + days_nodays;
		inhtml += ".<br>\n";

		if (show_submit == 1) {
			inhtml += "<br>\n";
			inhtml += "Click the Next button below to continue.<br>\n";
			inhtml += "<button class=\"btn btn-primary btn-large\" type=\"\" id=\"submit_button\">Next</button>\n";
		}

		inhtml += "</div>\n";
		inhtml += "<br>\n";
	}
	inhtml += "<div id=\"calendar\" class=\"cal_wrapper\"></div>\n";

	inhtml += "<!-- The Table containing the choices -->\n";

	inhtml += "<div id='main_table_wrapper'>\n";
	inhtml += "<table class=\"main_table\">\n";
	for (let i = 0 ; i < ca_ns.ca_dat["top_bot"].length ; i++) {
		opt = ca_ns.ca_dat["top_bot"][i];

		do_onclick = (results == 0 ? "onclick='ca_ns.click_check(\"" + opt + "\")'" : "");

		inhtml += "<tr id=\"option_" + opt + "\" class=\"choice_row\" " + do_onclick + ">\n";
			inhtml += "<td class=\"circle_cell\">\n";
				inhtml += "<canvas class=\"pie_chart\" id=\"pie_" + opt + "\"></canvas>\n";
			inhtml += "</td>\n";
			inhtml += "<td class=\"text_cell\">\n";
				inhtml += "<table class=\"choice_text\">\n";
					inhtml += "<tr id='top_row'>\n";
						inhtml += "<td class=\"ctd p0\">60% chance of</td>\n";
						inhtml += "<td class = \"ctd ss_val\">\n";
							inhtml += "<span id=\"" + opt + "S0\">R450</span>\n";
							inhtml += "<span class=\"SS_delay\">in 7 days</span>\n";
						inhtml += "</td>\n";
						inhtml += "<td class=\"ctd\">AND</td>\n";
						inhtml += "<td class = \"ctd ll_val\">\n";
							inhtml += "<span id=\"" + opt + "L0\">R450</span>\n";
							inhtml += "<span class=\"LL_delay\">in 21 days</span>\n";
						inhtml += "</td>\n";
					inhtml += "</tr>\n";
					inhtml += "<tr id='bottom_row'>\n";
						inhtml += "<td class=\"ctd\ p1\">40% chance of</td>\n";
						inhtml += "<td class = \"ctd ss_val\">\n";
							inhtml += "<span id=\"" + opt + "S1\">R20</span>\n";
							inhtml += "<span class=\"SS_delay\">in 7 days</span>\n";
						inhtml += "</td>\n";
						inhtml += "<td class=\"ctd\">AND</td>\n";
						inhtml += "<td class = \"ctd ll_val\">\n";
							inhtml += "<span id=\"" + opt + "L1\">R20</span>\n";
							inhtml += "<span class=\"LL_delay\">in 21 days</span>\n";
						inhtml += "</td>\n";
					inhtml += "</tr>\n";
				inhtml += "</table>\n";
			inhtml += "</td>\n";
		inhtml += "</tr>\n";
	}
	inhtml += "</table>\n";
	inhtml += "</div>\n";

	inhtml += "<!-- The div containing the form data -->\n";
	inhtml += "<div id=\"form_values\">\n";
		inhtml += "<input type=\"hidden\" name=\"choice\"   id=\"choice\"   value=-1 required id=\"choice\"   class=\"form-control\" />\n";
		inhtml += "<input type=\"hidden\" name=\"timeStamps\" id=\"timeStamps\" value=-1 class=\"form-control\" />\n";

	inhtml += "</div>\n";

	// We don't show the submit button on the final payment page
	if (show_submit == 1 & results == 0) {
		inhtml += "<p>\n";
		inhtml += "<center>\n";
		do_onclick = (results == 0 ? "onclick=\"ca_ns.submit_click();\"" : "");
		type = (results == 0 ? "button" : "");
		inhtml += "<button class=\"btn btn-primary btn-large\" type=\"" + type + "\" id=\"submit_button\" " + do_onclick + ">Submit</button>\n";
		inhtml += "<br><br><div id=\"submit_message\"></div>\n";
		inhtml += "</center>\n";
		inhtml += "</p>\n";
	}

	$("#" + full_div).html(inhtml);
}

this.mkview = function(ca_dat, full_div, results = 0, show_submit = 1) {
	ca_ns.ca_dat     = ca_dat;
	ca_ns.pairdat    = ca_dat["pairdat"];
	ca_ns.hex_colors = ca_dat["hex_colors"];
	ca_ns.start_time = ca_dat["start_time"];

	$("#number_of_rounds").html(ca_dat["number_of_rounds"]);
	$("#round_number").html(ca_dat["round_number"]);
	$("#round_number").css("color", "red");
	$("#round_number").css("font-weight", "bold");

	ca_ns.SS_delay=ca_ns.pairdat["ss_delay"]
	ca_ns.LL_delay=ca_ns.pairdat["ll_delay"]
	ca_ns.cur=ca_ns.pairdat["currency"]

	// Add in the interior elements
	fill_full_div(full_div = full_div, results = results, show_submit);
	
	// Set some colors immediatly
	$('.ss_val').css('color', ca_ns.hex_colors[0]);
	$('.ll_val').css('color', ca_ns.hex_colors[1]);

	// Call the functions needed to setup the page
	set_main_table()
	set_calendar()

	// Implement Chart.js pir charts. Not so hard, and they look nice
	$(document).ready(make_charts)
	$(window).resize(make_charts)

	if (results == 1) {
		$("#pair_for_pay").html(ca_dat["pair_for_pay"] + 1);
		$("#choice_for_pay").html((ca_dat["choice_for_pay"] == 0 ? "Top" : "Bottom"));

		if (ca_dat["choice_for_pay"] == 0) {
			T_choice = 1
			B_choice = 0
		} else {
			T_choice = 0
			B_choice = 1
		}
		select_option();
	}
	log_event("Start")
}

// End of namespace
}
