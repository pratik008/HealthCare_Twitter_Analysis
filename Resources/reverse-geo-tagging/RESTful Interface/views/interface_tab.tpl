      <section class="query-input">
        <label for="query-text" style='font-size:200%;'>MongoDB Command-Line Query &nbsp;</label>
        <input type="text" id="query-text" name="query-text" 
               placeholder=" {$text: {$search: '#Sepsis'}}"
               style='width:450px;height:40px;font-size:200%'>
        <br>
        
        <label id="tooltip" for="query-limit" style='font-size:200%;' 
               title="Set this value to zero (0) to return every matching record">Enter the maximum to return &nbsp;&nbsp;&nbsp; </label>
        <input type="number" id="query-limit" name="query-limit" 
               value="5" 
               style='width:150px;height:40px;font-size:200%;text-align: center;margin:5px 0 5px 0;'>
        <br>
        
        <button id="button" class="query-input-button"  style='margin: 15px 0 15px 400px;font-size:200%;border-radius: 15px;'>
                Click to send the query</button><br>
        <button id="button2" class="display-first-button" style='margin: 15px 0 15px 455px;font-size:200%;border-radius: 15px; display: none;'>
                Display the first</button><br>
        <button id="button3" class="display-all-button" style='margin: 15px 0 15px 485px;font-size:200%;border-radius: 15px; display: none;'>
                Display all</button>
      </section>
      
      <hr>
      
      <section id="query-response-section" style='display: none;'>
        <p id="query-str-display" style='font-size:150%;'>The query: <span></span></p>
        <p id="limit-display"     style='font-size:150%;'>Limited to: <span></span></p>
        <p id="numRet-display"    style='font-size:150%;'>Number returned: <span></span></p>
        
        <hr>
        
        <pre id="query-results" style='font-size:150%;'></pre>
      </section>
      