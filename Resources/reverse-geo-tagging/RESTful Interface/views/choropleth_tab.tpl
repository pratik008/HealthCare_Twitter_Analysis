        <section class="choropleth-input-section">
          <label for="choropleth-text" style='font-size:200%;'>Enter a term to search for &nbsp;</label>
          <input type="text" id="choropleth-text" name="choropleth-text" 
                 placeholder=" cancer"
                 style='width:450px;height:40px;font-size:200%'>
          <br>
          
          <button id="choropleth-button" class="choropleth-input-button"  style='margin: 15px 0 15px 400px;font-size:200%;border-radius: 15px;'>
                  Click to send the query</button><br>
                  
          <!-- Progressbar -->
          <div id="choropleth-progress-bar" style='display: none;'>
            <h2 class="demoHeaders">Progressbar</h2>
            <div id="progressbar"></div>
          </div>
          
        </section>
        
        <hr>
        
        <section id="choropleth-display-section" style='display: none;'>
          <h1 id="choropleth-display-header"></h1>
          <div id="choropleth-display"></div>
          <div id="choropleth-gradient"><img src="img/choropleth-gradient.jpg" alt="choropleth gradient" />
        </section>