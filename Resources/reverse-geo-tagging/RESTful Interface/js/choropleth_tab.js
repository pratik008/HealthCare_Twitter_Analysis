  // ===============
  // Choropleth code
  // ===============

  $( ".choropleth-input-button" ).on('click', function() {
  
    // hide the display section and clear the map's div
    // ------------------------------------------------
    $( "#choropleth-display-section" ).hide();
    $( "#choropleth-display" ).empty();
  
    // get & display the query term
    // ----------------------------
    var search_term = $( "#choropleth-text" ).val();
    if (search_term === "") {
      search_term = $( "#choropleth-text" ).attr("placeholder");
      search_term = $.trim(search_term);
    }
    header_string = "Frequency of the term " +
                    "<span style='text-decoration: underline;font-style: italic;'>" +
                    search_term +
                    "</span>";
    $("#choropleth-display-header").html(header_string);
    
    // display the progress bar
    $( "#choropleth-progress-bar" ).show();
    
    // start the progress bar
    //   on a set interval, increase the bar's width 
    var intProg   = 0,
        countProg = 1;
    var intVar = setInterval(function() {
      intProg+=0.10;
      if (intProg > 100) {
        countProg+=1;
        if (countProg == 2) {
          intProg = 0;
          // set new colors
          $( "#progressbar" ).css({ 'background': 'LightYellow' });
          $( "#progressbar > div").css({ 'background': 'DarkRed' });
        } else if (countProg == 3) {
            intProg = 0;
            // set new colors
            $( "#progressbar" ).css({ 'background': 'LightYellow' });
            $( "#progressbar > div").css({ 'background': 'Red' });
          } else {
            clearInterval(intVar);
          }
      }
      $( "#progressbar" ).progressbar({
        value: intProg
      });
    }, 10);
  
  // choropleth code: borrowed from D3.js gallery
  // http://bl.ocks.org/mbostock/4060606
  // --------------------------------------------
  var width  = 960,
      height = 600;

  var rateById = d3.map();

  var domain = [],
      quantize;

  var projection = d3.geo.albersUsa()
      .scale(1280)
      .translate([width / 2, height / 2]);

  var path = d3.geo.path()
      .projection(projection);

  var svg = d3.select("div#choropleth-display").append("svg")
      .attr("width", width)
      .attr("height", height);
      
  queue()
      
      .defer(d3.json, "data/us.json") 
      
      // RESTful call to the server
      // --------------------------
      // very convoluted, very difficult; it took me HOURS to figure this out
      // see https://groups.google.com/forum/#!topic/d3-js/3PpbrzI8yLg
       .defer(function(url, callback) {
          d3.json(url, function(error, data) {
            data.forEach(function(d) {
              domain.push(+d.count);           // create the quantize input domain
              rateById.set(d._id, +d.count);   // set the map values
             })
            // To compute the quantiles, the input domain is sorted 
            // and treated as a population of discrete values.
            quantize = d3.scale.quantize()
              .domain(domain)
              .range(["q0-9","q1-9","q2-9","q3-9","q4-9","q5-9","q6-9","q7-9","q8-9"]);
            callback(error, data);
          });
        }, "choropleth/" + search_term)
      
       .await(ready); 
      

  function ready(error, us) {
    svg.append("g")
        .attr("class", "counties")
      .selectAll("path")
        .data(topojson.feature(us, us.objects.counties).features)
      .enter().append("path")
        .attr("class", function(d) { return quantize(rateById.get(d.id)); })
        .attr("d", path);

    svg.append("path")
        .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
        .attr("class", "states")
        .attr("d", path);
        
    // display the section & cancel the progress bar
    $( "#choropleth-display-section" ).show();
    clearInterval(intVar);
  }

  d3.select(self.frameElement).style("height", height + "px");  
  
}); // <=== $( ".choropleth-input-button" ).on('click'