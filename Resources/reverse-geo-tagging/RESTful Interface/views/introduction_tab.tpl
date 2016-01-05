        <section class="tabs-1" style='font-size:150%;'>
          <h1>Healthcare Twitter Analysis</h1>
          <p>The objective of the Healthcare Twitter Analysis (HTA) project is to find ways to add  
             value to all sectors of the worldwide medical community by utilizing data science to analyze very 
             large volumes of Twitter messages. Starting with a collection of csv files containing
             health-related tweets from Jan-Jun 2014, the project recruited data-science expertise 
             via crowd-sourcing to help push the analysis forward and at one point had several hundred 
             participants.</p>
          <p>This website and all the technology & data that powers it was created by 
             George Fisher<a href="#footnote">*</a>, one of the participants.</p>
             
          <h1>Technology</h1>
              This website is constructed as a single-page web app which means that after the initial
              download there are no more page loads; all requests to the server for data are done in 
              the background with none of the usual flickering and stuttering of a Web 2.0 website.</p>
          <p>The "stack" for this website is the following:</p>
          <ul>
            <li>Front End
              <ul>
                <li>HTML5 & CSS3</li>
                <li>JavaScript, jQuery & jQuery UI</li>
                <li>D3.js</li>
              </ul>
            </li>
            <li style='margin-top:10px;'>HTTP Server & REST interface
              <ul>
                <li>Bottle</li>
                <li>Pymongo</li>
                <li>Python 2.7</li>
              </ul>
            </li>
            <li style='margin-top:10px;'>Database
              <ul>
                <li>MongoDB</li>
              </ul>
            </li>
          </ul>
          <p>The <a href="https://github.com/grfiv/healthcare_twitter_analysis/blob/master/Status%20Report.pdf?raw=true">
             status report</a> on my <a href="https://github.com/grfiv/healthcare_twitter_analysis">
             repo for this project</a> contains a detailed record of the work that went into creating
             the ~5 million documents in the current database as well as the code that was used
             to create those records; plus all the code for this website.</p>
        </section>
        <footer>
        <a name="footnote">*</a>
        <a href="https://github.com/grfiv">GitHub</a>, 
        <a href="https://www.linkedin.com/in/georgerfisher">Linkedin</a>
        </footer>