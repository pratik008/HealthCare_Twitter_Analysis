<!DOCTYPE html>
<html lang="en-us">
  <head>
    <meta charset="utf-8">
    <meta name="description" content="RESTful Interface to Healthcare Twitter Analysis MongoDB database">
    <meta name="author"      content="George Fisher">
    <meta name="viewport"    content="width=device-width,initial-scale=1">
 
    <title>RESTful Interface to Healthcare Twitter Analysis MongoDB database</title>

    <link href="css/jquery-ui.css"       rel="stylesheet">
    <link href="css/jQueryUI_inline.css" rel="stylesheet">
    <link href="css/choropleth.css"      rel="stylesheet">
  </head>
  
  <body>
  
  <!-- ========================================================= -->
  <!-- =========================  TABS ========================= -->
  <!-- ========================================================= -->
  <h1 class="demoHeaders" 
      style='font-size:300%;text-align: center;'>
      RESTful Interface to Healthcare Twitter Analysis MongoDB database</h1>
      
  <div id="tabs">
      <ul>
          <li><a href="#tabs-1">Introduction</a></li>
          <li><a href="#tabs-2">Interface</a></li>
          <li><a href="#tabs-3">Choropleth</a></li>
          <li><a href="#tabs-4">Instructions</a></li>
      </ul>
      
      <!-- ====================  INTRODUCTION ==================== -->
      <div id="tabs-1">
% include('introduction_tab.tpl')

      </div> <!-- id="tabs-1"  -->      

      <!-- ====================  INTERFACE ==================== -->
      <div id="tabs-2">
% include('interface_tab.tpl')

      </div> <!-- id="tabs-2"  -->
      
      <!-- ====================  CHOROPLETH ==================== -->
      <div id="tabs-3">
% include('choropleth_tab.tpl')

      </div> <!-- id="tabs-3"  -->
      
      <!-- ====================  INSTRUCTIONS ==================== -->
      <div id="tabs-4" style='font-size:150%;'>
% include('instructions_tab.tpl')

      </div> <!-- id="tabs-4"  -->
      
  </div> <!-- id="tabs"  -->
  
  <script src="js/jquery-2.1.1.min.js"></script>
  <script src="js/jquery-ui.js"></script>
  <script src="js/d3.v3.min.js"></script>
  <script src="js/queue.v1.min.js"></script>
  <script src="js/topojson.v1.min.js"></script>
  <script>
  // ==============
  // jQuery UI code
  // ==============
  $( "#tabs" ).tabs();
  $( "#tooltip" ).tooltip();
  $( "#button" ).button();
  $( "#radioset" ).buttonset();
  
  // =========
  // Utilities
  // =========
  function isNonNegInt(n) {
    // is n a non-negative integer?
    // (+n coerces n to a number) 
    if ($.isNumeric(n) && (+n)%1 == 0 && (+n) >= 0) { return true; }
    return false;
  }
  
  function refreshPage() {
    // reload the page 
    location.reload();
  }
  </script>
  <script src="js/interface_tab.js"></script>
  <script src="js/choropleth_tab.js"></script>
  
  </body>
</html>