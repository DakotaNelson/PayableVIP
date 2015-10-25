$(document).ready(function() {
  var margin = {top: 20, right: 60, bottom: 60, left: 60},
      width = 800 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

  var x = d3.scale.ordinal()
            .rangeRoundBands([0, width], .1);

  var y = d3.scale.linear()
            .range([height, 0]);

  var xAxis = d3.svg.axis()
        .scale(x)
        .tickFormat(function(d) { 
            dte = new Date(1970, d-1, 1);
            return dte.toLocaleString('en-us', { month: "short" });
          })
        .orient("bottom");

  var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .tickFormat(function(d) { return "$" + d; })
        .ticks(10);

  var svg = d3.select('.bill-chart')
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  $.get("/api/get-data", {"username": "arjun"}, function(data) {
    data = JSON.parse(data);
    // allBills, myBills, predictedBills

    data = data.myBills;

    cleaned = [];
    months = [];
    _.each(data, function(value, key) {
      sum = value.water + value.electric + value.gas;
      months.push(key);
      cleaned.push({"month":key, "total": sum});
    });

    x.domain(months);
    y.domain([0, d3.max(cleaned, function(d) { return d.total; })]);

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Cost");

    svg.selectAll(".bar")
        .data(cleaned)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.month); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.total); })
        .attr("height", function(d) { return height - y(d.total); });

    $.get("/api/get-monthly-rate", {"username": "arjun"}, function(data) {
      data = JSON.parse(data);

      avgLine = svg.append("g")

      avgLine.append("svg:line")
           .attr("class", "average-line")
           .attr("x1", 0)
           .attr("x2", width)
           .attr("y1", y(data.monthlyRate.cost))
           .attr("y2", y(data.monthlyRate.cost))
           .attr("class","label-line");

      avgLine.append("text")
           .attr("x", function(d) { return width + 3; })
           .attr("y", y(data.monthlyRate.cost) + 4)
           .text('$' + data.monthlyRate.cost.toFixed(2));
    });

  });

});
