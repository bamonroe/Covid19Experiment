let final_ns = new function() {
	let selector_sets = ["Final Payment", "Task 1", "Task 2", "Task 3", "Task 4"];
	let selected = ["Final Payment"];

	let time_to_pay = function(when) {
		if (when == 0) {
			return(" today");
		} else {
			return(" on " + when);
		}
	}

	let final_view = function() {
		let inhtml = "";

		let bfp = beliefs_dat["beldat"];
		let rfp = risk_dat["final_payment"];
		let tfp = time_dat["final_payment"];
		let cfp = ca_dat["final_payment"];

		inhtml += "Session Date: " +  session_date  + "\n<br>";
		inhtml += "<br>";
		inhtml += "The study is now complete. ";
		inhtml += "Any payments marked as payable today will be verified by research staff and sent within 24 hours. ";
		inhtml += "Once you have looked at your payment information you can close this browser window. ";
		inhtml += "You can always return to view this information by clicking on the custom web link sent in your invitation email. ";

		inhtml += "<br>\n";
		inhtml += "<br>\n";
		inhtml += "For participating in this experiment, you will be paid " + rfp["currency"] +endowment + " today.\n";
		inhtml += "<br>\n";
		inhtml += "<br>\n";
		inhtml += "For Task 1 you will be paid based on the correct answer to the question " + bfp["pay_by"] + ".\n";
		inhtml += "<br>\n";
		inhtml += "For Task 2 you will be paid " + rfp["currency"] + rfp["amounts"][0] + time_to_pay(rfp["when"][0]) + ".\n";
		inhtml += "<br>\n";
		inhtml += "For Task 3 you will be paid " + tfp["currency"] + tfp["amounts"][0] + time_to_pay(tfp["when"][0]) + ".\n";
		inhtml += "<br>\n";
		inhtml += "For Task 4 you will be paid " + 
			cfp["currency"] + cfp["amounts"][0] + time_to_pay(cfp["when"][0]) + " AND " +
			cfp["currency"] + cfp["amounts"][1] + time_to_pay(cfp["when"][1]) + ".\n";
		inhtml += "<br>\n";

		if (risk_dat["final_payment"]["currency"] == "R") {
			inhtml += "<br>\n";
			inhtml += "<br>\n";
			inhtml += "<br>\n";
			inhtml += "<img src='/static/self_care.jpg'/>\n";
		}
		$("#viewer").html(inhtml);
	}

	this.select_view = function(val) {
		select_tab(val);
		final_ns.selected = val;
		if (val == "Final Payment") {
			final_view();
			$("#viewer").css("width", "100%");
		}
		if (val == "Task 1") {
			beliefs_ns.mkview(beliefs_dat, "viewer", results = 1, show_submit = 0);
			$("#viewer").css("width", "100%");
		}
		if (val == "Task 2") {
			$("#viewer").css("width", "60%");
			risk_ns.mkview(risk_dat, "viewer", results = 1, show_submit = 0);
		}
		if (val == "Task 3") {
			time_ns.mkview(time_dat, "viewer", results = 1, show_submit = 0);
			$("#viewer").css("width", "100%");
		}
		if (val == "Task 4") {
			ca_ns.mkview(ca_dat, "viewer", results = 1, show_submit = 0);
			$("#viewer").css("width", "100%");
		}
	}

	let select_tab = function(val) {
		$("[id='" + val + "']").css("background-color", "");
		for (let i = 0 ; i < selector_sets.length ; i++) {
			nval = selector_sets[i];
			if (nval != val) {
				$("[id='" + nval + "']").css("background-color", "#cccccc");
			}
		}
	}

	this.fill_selector = function() {
		let inhtml = "";
		for (let i = 0 ; i < selector_sets.length ; i++) {
			inhtml += "<div class='selector' ";
			inhtml += " id='" + selector_sets[i] + "'";
			inhtml += " onclick='final_ns.select_view(\"" + selector_sets[i] + "\");'";
			inhtml += ">";
			inhtml += selector_sets[i];
			inhtml += "</div>";
		}
		$("#selector").html(inhtml);
	}
}
