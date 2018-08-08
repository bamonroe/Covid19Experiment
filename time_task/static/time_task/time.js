// Make a namespace for time functions
let time_ns = new function() {

let days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
let month_abbvr   = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
let SS_choices = [];
let LL_choices = [];
let start_time = "";

// Set the Main table for choices
let set_main_table = function(pairdat, time_dat, onclick = true) {

	let td_style = "style='padding-top:6px;padding-bottom:6px;'";
	let in_html  = "<tr id='main_table_header'><th id='ss_header'>Smaller Sooner</th><th></th><th id='ll_header'>Larger Later</th></tr>\n";
	let num_per_page = time_dat["num_per_page"];

	for (let i = 0; i < num_per_page; i++) {
		let pair_val = pairdat[i]
		// Start this row
		let row = "<tr >"
		// Smaller Sooner
		let SS_beg = "<td class='SS_td' " + td_style + " id=\"SS" + i + "\""
		// Larger Later
		let LL_beg = "<td class='LL_td' " + td_style + " id=\"LL" + i + "\""

		if (onclick) {
			SS_beg += " onclick='time_ns.click_check(\"SS\"," + i + ")'"
			LL_beg += " onclick='time_ns.click_check(\"LL\"," + i + ")'"
		}

		SS_beg += ">"
		LL_beg += ">"

		let suffix = ""
		if (pair_val["SS_delay"] == 0) {
			suffix = " today"
		} else {
			suffix = " in " + pair_val["SS_delay"] + " days"
		}
		row += SS_beg + pair_val["currency"] + pair_val["SS_amount"] + suffix + "</td>"
		row += "<td> OR </td>"
		// Larger Later Amount
		row += LL_beg + pair_val["currency"] + pair_val["LL_amount"] + " in " + pair_val["LL_delay"] + " days</td>"
		row += "</tr>\n"
		in_html += row
	}
	$("#main_table").html(in_html);
}

// Function to change colors and fill out choices
this.click_check = function(side, val) {
	log_event(val + "_" + side)
	if (side == "SS") {
		if (LL_choices[val] == 1) {
			LL_choices[val] = 0
			SS_choices[val] = 1
		} else if (SS_choices[val] == 1) {
			SS_choices[val] = -1
			LL_choices[val] = -1
		} else {
			SS_choices[val] = 1
			LL_choices[val] = 0
		}
	} else if (side == "LL") {
		if (SS_choices[val] == 1) {
			SS_choices[val] = 0
			LL_choices[val] = 1
		} else if (LL_choices[val] == 1) {
			SS_choices[val] = -1
			LL_choices[val] = -1
		} else {
			SS_choices[val] = 0
			LL_choices[val] = 1
		}
	}

	$("#SS" + val).css("background-color", (SS_choices[val] <=0 ? "" : "#ADD8E6"));
	$("#SS" + val).css("fontWeight",       (SS_choices[val] <=0 ? "" : "bold"));
	$("#LL" + val).css("background-color", (LL_choices[val] <=0 ? "" : "#ADD8E6"));
	$("#LL" + val).css("fontWeight",       (LL_choices[val] <=0 ? "" : "bold"));

	fill_form()
	submit_enabler()
}

let submit_enabler = function() {
	if (done_check()){
		$("#submit_button").prop('disabled', false);
		$("#submit_message").html("&nbsp;");
	} else{
		$("#submit_button").prop('disabled', true);
		$("#submit_message").html("You must make a choice on each of the rows above.");
	}
}

// Check that necessary conditions are completed so subject can proceed
let done_check = function() {
	let num_per_page = time_ns.time_dat["num_per_page"];
	// Check that num_per_page options have been chosen
	let length_check   = SS_choices.length == num_per_page;
	// Check that no options are empty
	let empty_check    = ! SS_choices.includes(undefined);
	// Check that every option has a choice assigned with it
	let one_zero_check = SS_choices.every(v => v == 0 | v == 1);
	return(length_check & empty_check & one_zero_check);
}

// Fill out the form inputs
let fill_form = function() {
	let num_per_page = time_ns.time_dat["num_per_page"];

	let inputs_vals = ["choice"]
	for (let i = 0; i < num_per_page; i++) {
		let j = i + 1
		let fval = "choice_" + j
		if (SS_choices[i] == 0) {
			$("#" + fval).val(1);
		} else if (SS_choices[i] == 1) {
			$("#" + fval).val(0);
		} else {
			$("#" + fval).val(-1);
		}
	}
}

this.submit_click = function() {
	log_event("submit")
	fill_form(time_ns.time_dat);
	$("#submit_message").html("&nbsp;");
	document.getElementById("submit_button").type = "";
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

let set_calendar = function(pairdat) {
	let hex_colors = time_ns.time_dat["hex_colors"];
	// Get the delays from the timesheet
	let pair_val = pairdat[0]
	let SS_delay = pair_val["SS_delay"]
	let LL_delay = pair_val["LL_delay"]

	// Get today's things
	let today = new Date(
		time_ns.start_time[0],
		time_ns.start_time[1],
		time_ns.start_time[2],
		time_ns.start_time[3],
		time_ns.start_time[4],
	);

	let today_year  = today.getFullYear();
	let today_month = today.getMonth();
	let today_date  = today.getDate();

	let ss_delay_md = get_delay_date(today_date, today_month, SS_delay)
	let ll_delay_md = get_delay_date(today_date, today_month, LL_delay)

	let ss_month = today_month + ss_delay_md[0]
	let ss_date  = ss_delay_md[1]
	let ll_month = today_month + ll_delay_md[0]
	let ll_date  = ll_delay_md[1]

	let ss_year = today_year;
	let ll_year = today_year;

	// Adjust future dates for delays running into the next year
	if (ss_month > 11) {
		ss_month -= 12;
		ss_year += 1;
	}
	if (ll_month > 11) {
		ll_month -= 12;
		ll_year += 1;
	}

	let ss_header = ss_date + " " + month_abbvr[ss_month] + " " + ss_year
	let ll_header = ll_date + " " + month_abbvr[ll_month] + " " + ll_year

	if (SS_delay == 0) {
		ss_header += "\n(Today)"
	} else {
		ss_header += "\n(" + SS_delay + " days from today)"
	}

	if (LL_delay == 0) {
		ll_header += "\n(Today)"
	} else {
		ll_header += "\n(" + LL_delay + " days from today)"
	}

	$("#ss_header").html(ss_header);
	$("#ll_header").html(ll_header);

	// Get the staring day
	let first_of_month = new Date(today_year, today_month, 1, 0, 0, 0, 1)
	let first_dow      = first_of_month.getDay();

	// The calendar for this month
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

	$("#ss_date").css("background-color", hex_colors[0]);
	$("#ll_date").css("background-color", hex_colors[1]);

	if (SS_delay == 0) {
		$("#ss_date").css("border", "2px solid black");
	}

	// Disable submit button upon initial page paint
	// Perhaps a better location to put this?
	submit_enabler()
}

let make_calendar = function(start_dow, month_num, cal_id, today_month, today_date, ss_month, ss_date, ll_month, ll_date) {

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

let select_payment_pair = function(pair_id) {
	let num_per_page = time_ns.time_dat["num_per_page"];

	for (let i = 0 ; i < num_per_page ; i++) {
		SS_choices[i] = (time_ns.choices[i] == 0 ? 1 : 0);
		LL_choices[i] = (time_ns.choices[i] == 1 ? 1 : 0);

		$("#SS" + i).css("background-color", (SS_choices[i] <=0 ? "" : "#ADD8E6"));
		$("#SS" + i).css("fontWeight",       (SS_choices[i] <=0 ? "" : "bold"));
		$("#LL" + i).css("background-color", (LL_choices[i] <=0 ? "" : "#ADD8E6"));
		$("#LL" + i).css("fontWeight",       (LL_choices[i] <=0 ? "" : "bold"));
	}

	let option = (time_ns.choices[pair_id] == 0 ? "SS" : "LL");

	$("#" + option + pair_id).css("border", "3px solid red");
}

let fill_full_div = function(full_div, results = 0, show_submit = 1) {
	inhtml = ""
	if (results == 1) {
		let pay_pair = time_ns.time_dat["pay_pair"];
		let topay =  time_ns.time_dat["choices"];
		topay = topay[time_ns.time_dat["pay_pair_num"]];
		topay = (topay == 0 ? "SS" : "LL")

		let pay_day    = pay_pair[topay + "_delay"];
		let pay_amount = pay_pair[topay + "_amount"];

		if (pay_day == 0) {
			pay_day = "today."
		} else {
			pay_day = "in " + pay_day + " days."
		}

		inhtml += "<div id=\"results_text\">";
		inhtml += "<span id='decision_text'>Decision screen <span id=\"pay_block_num\"></span> and row <span id=\"pay_pair_num\"></span> were randomly selected for payment.</span><br\>\n";
		inhtml += "Your choice is displayed below<br>\n";
		inhtml += "You chose the " + (topay == "SS" ? "Left" : "Right") + " option.<br>\n";
		inhtml += "Based on the random row drawn and your choice, your earnings are " + pay_pair["currency"] + pay_amount + " " + pay_day + "<br>\n";

		if (show_submit == 1) {
			inhtml += "<br>\n";
			inhtml += "Click the Next button below to continue.\n<br>";
			inhtml += "<button class=\"btn btn-primary btn-large\" type=\"\">Next</button>";
		}

		inhtml += "</div>";
		inhtml += "<br>";
	}

	inhtml += "<div id=\"calendar\" class=\"cal_wrapper\"></div>\n";
	inhtml += "<!-- The Table containing the choices -->\n";
	inhtml += "<table id=\"main_table\" > </table>\n";

	if (results == 0) {
		inhtml += "<!-- The div containing the form data -->\n";
		inhtml += "<div id=\"form_values\">\n";
		for (let i = 1 ; i <= time_ns.time_dat["num_per_page"] ; i++) {
			inhtml += "<input type=\"hidden\" name=\"choice_" + i + "\" id=\"choice_" + i + "\" value=-1 required class=\"form-control\" />\n";
		}
		inhtml += "<input type=\"hidden\" name=\"timeStamps\" id=\"timeStamps\" value=-1 class=\"form-control\" />\n";
		inhtml += "</div>\n";

		inhtml += "<p>\n";
		inhtml += "<center>\n";
		inhtml += "<button class=\"btn btn-primary btn-large\" type=\"button\" id=\"submit_button\" onclick=\"time_ns.submit_click();\">Submit</button>\n";
		inhtml += "<!-- The div containing possible error messages -->\n";
		inhtml += "<br><br><div id=\"submit_message\"></div>\n";
		inhtml += "</center>\n";
	} else {
		// We don't show the submit button on the final payment page
	}
	inhtml += "</p>\n";

	$("#" + full_div).html(inhtml);
}

this.mkview = function(time_dat, full_div, results = 0, show_submit = 1) {

	// Fill the full_div
	time_ns.time_dat = time_dat;

	fill_full_div(full_div, results, show_submit);

	if (results == 1) {
		let pay_block_num = time_dat["pay_block_num"];
		time_ns.choices = time_dat["choices"];
	}

	let pairdat      = time_dat["pairdat"];
	let num_per_page = time_dat["num_per_page"];
	let hex_colors   = time_dat["hex_colors"];
	time_ns.start_time = time_dat["start_time"];

	$("#ss_header").css("background-color", hex_colors[0]);
	$("#ll_header").css("background-color", hex_colors[1]);
	$("#task_number").html(time_dat["task_number"]);
	$("#round_number").html(time_dat["round_number"]);
	$("#number_of_rounds").html(time_dat["number_of_rounds"]);

	// Call the functions needed to setup the page
	set_main_table(pairdat, time_dat, (results == 0 ? true : false));
	set_calendar(pairdat, time_dat);
	if (results == 1) {
		select_payment_pair(time_dat["pay_pair_num"]);
		$("#pay_pair_num").html(time_dat["pay_pair_num"] + 1);
		$("#pay_block_num").html(time_dat["pay_block_num"] + 1);
	}
	// Capture the time the page was loaded in ms
	log_event("Start")
}

// End of time_ns
}
