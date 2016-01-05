/*
The JavaScript to run the original interface page
that allows raw MongoDB queries against the Healthcare
Twitter Analysis database.
*/

// holds the list of _id's returned
var id_list;

// ====================================================
// when the 'Click to send the query' button is clicked
// ====================================================
$( ".query-input-button" ).on('click', function() {

  // get the query and limit
  // -----------------------
  var query_str = $( "#query-text" ).val();
  if (query_str === "") {
    query_str = $( "#query-text" ).attr("placeholder");
  }
  
  var limit = $( "#query-limit" ).val();
  if (!isNonNegInt(limit)) { 
    limit = "5"; 
    $( "#query-limit" ).val(limit)
    }
    
  // check for abusive queries
  // -------------------------
  if (/{[ ]*?}/im.test(query_str)) {
    if (limit == 0 || limit > 10) {
      alert("Don't be like that");
      return
    }
  }
  
  // convert the query string to object form (eval)
  // and then JSON stringify it for transmission to server
  // -----------------------------------------------------
  query_str = JSON.stringify(eval('(' + query_str + ')'));
  
  // display the query and limit on the page
  // ---------------------------------------
  $("#query-response-section").show();
  $("#query-str-display").find("span").text(query_str);
  $("#limit-display").find("span").text(limit);
  
  // send the query to the server
  // ----------------------------
  var request = $.ajax({
    url:         "http://localhost:8082/query/" + limit,
    type:        "POST",
    data:        query_str, 
    dataType:    "json",
    contentType: "application/json"
  });
  
  // if the request is successful
  // ----------------------------
  request.done(function( response ) {
      console.log( response );
      
      // save the list of '_id's returned
      id_list = response['id_list'];
      
      // display the response
      var jsonPretty = JSON.stringify(response, null, '\t');
      $( "pre" ).text(jsonPretty);
      
      // display the number of matches returned
      $( "#numRet-display" ).find("span").text(response['num']);
      
      // show or hide the 'Display the first' and 'Display all' buttons
      if (response['num'] > 0) {
        $( ".display-first-button" ).show();
        $( ".display-all-button" ).show();
      } else {
        $( ".display-first-button" ).hide();
        $( ".display-all-button" ).hide();
      }
  });
  
  // if the request fails
  // --------------------
  request.fail(function( jqXHR, textStatus ) {
    alert( "Request failed: " + textStatus );
  });

}); // <=== $( ".query-input-button" ).on('click'

// ==============================================
// when the 'Display the first' button is clicked
// ==============================================
$( ".display-first-button" ).on('click', function() {

  // pull the ObjectId string of the first '_id' returned
  var first_id = id_list[0]['_id']['$oid'];
  
  // send the query to the server
  // ----------------------------
  var request = $.getJSON( "http://localhost:8082/findone/" + first_id );
  
  // if the request is successful
  // ----------------------------
  request.done(function( response ) {
      console.log( response );
      
      var first_tweet = response['first_tweet'];
      // display the response
      var jsonPretty = JSON.stringify(first_tweet, null, '\t');
      $( "pre" ).text(jsonPretty);
  });
  
  // if the request fails
  // --------------------
  request.fail(function( jqXHR, textStatus ) {
    alert( "Request failed: " + textStatus );
  });

});  // <=== $( ".display-first-button" ).on('click'

// ========================================
// when the 'Display all' button is clicked
// ========================================
$( ".display-all-button" ).on('click', function() {

  // pull the ObjectId strings
  var list_ids = [];
  id_list.forEach(function(entry) {
    list_ids.push(entry['_id']['$oid']);
  });
  
  // send the query to the server
  // ----------------------------
  var request = $.getJSON( "http://localhost:8082/find/" + list_ids );
  
  // if the request is successful
  // ----------------------------
  request.done(function( response ) {
      console.log( response );
      
      // display the response
      var jsonPretty = JSON.stringify(response, null, '\t');
      $( "pre" ).text(jsonPretty);
  });
  
  // if the request fails
  // --------------------
  request.fail(function( jqXHR, textStatus ) {
    alert( "Request failed: " + textStatus );
  });
  
});  // <=== $( ".display-all-button" ).on('click'