function populateNPosts(dataset) {
    console.log("populateNPosts");
    console.log(dataset);
    var nPostsPlot = $("#n-posts-plot");
    console.log(nPostsPlot);

    var m = [20, 20, 30, 50],
	w = 700 - m[1] - m[3],
	h = 300 - m[0] - m[2],
	barPadding = 1;
    
    var svg = d3.select("#n-posts-plot").append("svg")
        .attr("width", w + m[1] + m[3])
        .attr("height", h + m[0] + m[2])
	.append("g")
        .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

    var minDate = new Date(d3.min(dataset, function(d){
    	return d.date;
    }));

    var maxDate = new Date(d3.max(dataset, function(d){
    	return d.date;
    }));

    console.log(minDate);
    console.log(maxDate);

    var xscale = d3.time.scale().range([0, w]).domain([new Date(minDate - 3600 * 1000), new Date(maxDate.getTime() + (3600 * 1000))]);
    var xaxis = d3.svg.axis();
    xaxis.orient('bottom');
    xaxis.scale(xscale);

    var minY = d3.min(dataset, function(d){ return d.n_posts; });
    var maxY = d3.max(dataset, function(d){ return d.n_posts; });
    console.log(minY);
    console.log(maxY);

    var yscale = d3.scale.linear()
        .range([h, 0])
        .domain([minY - minY * 0.1, maxY + maxY * 0.1]);
    var yaxis = d3.svg.axis();
    yaxis.scale(yscale);
    yaxis.orient('left');

    var line = d3.svg.line()
        .x(function(d){ return xscale(new Date(d.date)); })
        .y(function(d){ return yscale(d.n_posts); })


    svg.append("path")
        .datum(dataset)
        .attr("class", "line")
        .attr("d", line);

    svg.append("g").call(xaxis)
        .attr("transform", "translate(0, " + h + ")")
        .attr("class", "axis");
    svg.append("g").call(yaxis)
        .attr("class", "axis");
}

$(document).ready(function(){
    var today = new Date();
    today.setHours(0,0,0,0)
    console.log(today);
    var lastTenDays = [];
    var lastTenDaysStr = []
    for(i=1; i<60; i++){
	var date = new Date(today);
	date.setDate(today.getDate() - i);
	lastTenDays.push(date);
	lastTenDaysStr.push(date.toString());
    }
    console.log(lastTenDays);

    $.get("api/n_posts", {dates: lastTenDaysStr}, function(response){ populateNPosts(response); });

    $(".controller .btn").click(function(e){
	if($(this).hasClass("active")){
	    console.log("button already active");
	} else {
    	    var controller = $(this).parent();
	    var active_button = controller.find(".btn.active");
	    active_button.removeClass("active");
	    $(this).addClass("active");
	}
    });
});
