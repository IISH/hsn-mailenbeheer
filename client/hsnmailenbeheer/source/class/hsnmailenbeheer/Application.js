/**
 * Author:      Fons Laan, KNAW IISH - International Institute of Social History
 * Project      HSN Mail
 * Name:        Application.js
 * Version:     1.0.2
 * Goal:        Main js file
 * Notice:      Qooxdoo itself needs Python-2.6+, not Python-3
 *
 * functions:
 * main                  : function()
 * url                   : function( path )
 * getHsnData            : function()
 * getHsnOpData          : function( ev )
 * saveHsnOpData         : function( path, data )
 * createWindows         : function()
 * createWindow0         : function()
 * createWindow1         : function()
 * createWindow1Dialog   : function()
 * createWindow1Missing  : function()
 * createWindow2         : function()
 * createWindow3         : function()
 * createWindow4         : function()
 * createWindow5         : function()
 * createWindow6         : function()
 * isNumeric             : function( n )
 * isValidDate           : function( dateString )
 * location2nr           : function( location_value )
 * getUservalueCombobox  : function( combobox, value, key )
 * closeWindow           : function( window, text )
 * showDialog            : function( text )
 * createLogin           : function()
 * _doAuthenticate       : function( ev )
 * _AuthenticateResponse : function( ev )
 * createLogout          : function( ev )
 * 
 * possible table selection modes: 
 *  model.NO_SELECTION;                        // 1 
 *  model.SINGLE_SELECTION;                    // 2
 *  model.SINGLE_INTERVAL_SELECTION;           // 3
 *  model.MULTIPLE_INTERVAL_SELECTION;         // 4
 *  model.MULTIPLE_INTERVAL_SELECTION_TOGGLE;  // 5
 * 
 * FL-19-Jun-2015: Created
 * FL-26-Jun-2015: New Dialog class
 * FL-03-Jul-2015: Fixed strings from db
 * FL-14-Sep-2016: A few Marja wishes
 */

/**
 * Main application class of "hsnmailenbeheer"
 * 
 * @asset(qx/icon/${qx.icontheme}/32/status/dialog-information.png)
 * @asset(qx/icon/${qx.icontheme}/16/devices/printer.png)
 *
 * @asset(hsnmailenbeheer/*)
 */
qx.Class.define( "hsnmailenbeheer.Application",
{
  extend : qx.application.Standalone,

  members :
  {
    /**
     * This method contains the initial application code and gets called 
     * during startup of the application
     * 
     * @lint ignoreDeprecated(alert)
     */
    
    timestamp_client : "14-Sep-2016 13:33",
    
    // hsnmail.<vars> now from config.json
    wsgi_method : qx.core.Environment.get( "hsnmail.wsgi_method" ),
    wsgi_path   : qx.core.Environment.get( "hsnmail.wsgi_path" ),
    
    test_usr : "",
    test_pwd : "",
    
    //debugIE : false,
    
    _username : null,
    _password : null,
  
    MAIN_WIDTH  : 800,
    MAIN_HEIGHT : 500,
    
    opinfo_valid : false,
    opinfo_str   : "",
    opinfo_html  : "",
	
    HSN : null,
    
    show_layout : false,
    
    color_Khaki  : "#F0E68C",
    color_Yellow : "#FFFF00",
    
    color_LightGreen  : "#90EE90",
    color_LightYellow : "#FFFFE0",
    
    color_BackgroundColor : "#F3F3F3",  // default
    
    // columns of table Hsn_kwyt
    MISSING_nr       :  0,   // screen table row counter: 1,2,3...
    MISSING_id       :  1,   // primary key
    MISSING_idvolgnr :  2,
    MISSING_idnr     :  3,
    MISSING_begin_d  :  4,
    MISSING_begin_m  :  5,
    MISSING_begin_y  :  6,
    MISSING_end_d    :  7,
    MISSING_end_m    :  8,
    MISSING_end_y    :  9,
    MISSING_location : 10,
    MISSING_reason   : 11,
    MISSING_found    : 12,
    
    // columns of screen table Mail
    MAIL_nr          :  0,   // (not in db) screen table row counter: 1,2,3...
    MAIL_id          :  1,   // primary key
    MAIL_idnr        :  2,
    MAIL_briefnr     :  3,
    MAIL_aard        :  4,
    MAIL_datum       :  5,
    MAIL_periode     :  6,
    MAIL_gemnr       :  7,
    MAIL_naamgem     :  8,
    MAIL_status      :  9,
    MAIL_printdatum  : 10,
    MAIL_printen     : 11,
    MAIL_ontvdat     : 12,
    MAIL_opmerk      : 13,
    MAIL_opident     : 14,
    MAIL_oppartner   : 15,
    MAIL_opvader     : 16,
    MAIL_opmoeder    : 17,
    MAIL_type        : 18,
    MAIL_infoouders  : 19,
    MAIL_infopartner : 20,
    MAIL_inforeis    : 21,
    
    input_opnum : null,
    
    
    main : function()
    {
      
      this.base( arguments );		// Call super class
      
      var debug = qx.core.Environment.get( "qx.debug" );
      //console.log( "debug: " + debug );
      if( debug ) // Enable logging in debug variant
      {
        qx.log.appender.Native;   // support native logging capabilities, e.g. Firebug for Firefox
        qx.log.appender.Console;  // support additional cross-browser console. Press F7 to toggle visibility
      }
      
      // actual application code...
      qx.locale.Manager.getInstance().setLocale( "nl" );
      console.debug( "Qooxdoo version: " + qx.core.Environment.get( 'qx.version' ) );
      
      this.js_location = window.location;
      console.debug( this.js_location );
      
      console.debug( "wsgi_method: " + this.wsgi_method );
      console.debug( "wsgi_path: " + this.wsgi_path );
      
      /*
      var csrftoken = qx.bom.Cookie.get( "csrftoken" );
      var sessionid = qx.bom.Cookie.get( "sessionid" )
      
      console.debug( "csrftoken: " + csrftoken );   // OK
      console.debug( "sessionid: " + sessionid );   // null, initially
      */
      
      this.createLogin();
    //this.getHsnData();    // get 'static' data; then create and fill the windows
      
    }, // main



    /**
      * wsgi_url
      *
      * Construct a url
      * @param path {string} 
      */
    wsgi_url : function( path ) 
    {
        var prot = this.js_location.protocol;
        var host = this.js_location.host;
        var port = this.js_location.port;
        var wsgi = this.wsgi_path;
        /*
        console.debug( "prot: " + prot );
        console.debug( "host: " + host );
        console.debug( "port: " + port );
        console.debug( "wsgi: " + wsgi );
        */
        var url = prot + "//" + host + port + wsgi + path;
        console.debug( url );
        
        return url;
    },
    
    
    
    /**
     * getHsnData
     */
    getHsnData : function()
    {    
      console.debug( "getHsnData()" );
      
      var url = this.wsgi_url( "/gethsndata" );
      
      var method = this.wsgi_method;
      if( method === "POST" ) { url += '/'; }
      console.debug( "url: " + url );
      
      var request = new qx.io.request.Xhr( url );
      request.setMethod( method );
      
      if( method === "POST" )
      { request.setRequestHeader( "X-CSRFToken", qx.bom.Cookie.get( "csrftoken" ) ); }
        
      request.addListener
      ( 
        "success", 
        function( ev ) 
        {
          var request = ev.getTarget();
          /*
          var sessionid = request.cookie.get( "sessionid" );
          var csrftoken = request.cookie.get( "csrftoken" );
          console.debug( "sessionid: " + sessionid );
          console.debug( "csrftoken: " + csrftoken );
          */
          var json_data = request.getResponse();
          var content_type = request.getResponseContentType();
        //console.debug( "getHsnData() content_type: " + content_type );
          
          if( content_type !== "application/json" )
          { this.createAlert( "getHsnData() unexpected response:<br>" + content_type + "<br>" + request.getResponseText() ); }
          
          if( json_data.printers.list.length == 0 ) {
            this.have_printer = false;
            this.showDialog( "CUPS - Common Unix Printing System<br><br><b>" + json_data.printers.msg + "</b><br><br>Er zijn geen printers gevonden, printen is niet mogelijk." );
          }
          else { this.have_printer = true; }
          
          this.python_version   = json_data.python_version;
          this.django_version   = json_data.django_version;
          
          this.info( "python_version: " + this.python_version );
          this.info( "django_version: " + this.django_version );
      
        //console.debug( json_data );
          this.HSN = json_data;
          
          // create location array-of-arrays for location ComboTable
          this.location_array = [];
          var locations = this.HSN.locations;
          for( var l = 0; l < locations.length; l++ ) 
          {
          //console.debug( l, "'" + locations[ l ] + "'" );
            var location = locations[ l ];
            var gemname  = location.name;
          //var gemnr    = location.nr;
            
            var loc_arr = [ (l+1).toString(), gemname ];
            this.location_array.push( loc_arr );
          }
          
        //console.debug( "timestamp client: " + timestamp_client );
        //console.debug( "timestamp server: " + this.HSN.timestamp_server );
          
          // now create the windows, and fill some of their data structures
          this.createWindows();
        }, 
        this 
      );
      
      request.addListener
      ( 
        "fail", 
        function( ev ) 
        {
          var request = ev.getTarget();
          var response = request.getResponse();
          console.debug( "getHsnData() fail: " + response );
          this.showDialog( "fail" + "<br><br>" + response );
        }, 
        this 
      );
      
      request.addListener
      ( 
        "statusError", 
        function( ev ) 
        {
          var request = ev.getTarget();
          var response = request.getResponse();
          console.debug( "getHsnData() statusError: " + response );
          this.showDialog( "statusError" + "<br><br>" + response );
        }, 
        this 
      );
      
      request.send();        // Send the request
      
    }, // getHsnData
    
    
    
    /**
     * getHsnOpData
     */
    getHsnOpData : function( ev )
    {
      this.labelOpinfo      .setValue( "" ); // clear previous OP info string
      this.label_opstatus   .setValue( "" ); // clear previous OP status string
      this.textareaMutations.setValue( "" ); // clear previous OP mutation data
      
      
      this.label_opstatus.set({ backgroundColor : this.color_BackgroundColor });
      
      var opnum = this.input_opnum.getValue();
      if( opnum == null ) { opnum = ""; }
      console.debug( "getHsnOpData, opnum: " + opnum );
      
      var url = this.wsgi_url( "/gethsnopdata" );
      
      var method = this.wsgi_method;
      
      var params = ""
      if( method === "GET" )        // only for testing, 
      { params += "?"; }
      else if( method === "POST" )  // use POST for login.
      { url += '/'; }               // required: POST + Django: APPEND_SLASH
      
      params += "op_num=" + opnum;
      
      if( method === "GET" ) { url += params; }
      console.debug( url );
      
      var request = new qx.io.request.Xhr( url );
      
      request.setMethod( method );
      
      if( method === "POST" )           // set parameters in data
      { 
        request.setRequestHeader( "X-CSRFToken", qx.bom.Cookie.get( "csrftoken" ) );
        request.setRequestData( params ); 
      }
          
      request.addListener
      ( 
        "success", 
        function( ev ) 
        {
          var request = ev.getTarget();
          var json_data = request.getResponse();
          var content_type = request.getResponseContentType();
          //console.debug( "content_type: " + content_type );
          if( content_type !== "application/json" )
          { this.createAlert( "unexpected response:<br>" + content_type + "<br>" + request.getResponseText() ); }
          
          //console.debug( json_data );
          this.OP = json_data.OP;
          console.debug( this.OP );
          
          this.opinfo_valid = json_data.op_isvalid;
          if( this.opinfo_valid ) 
          {
            this.buttonWindow1.setEnabled( true );
            this.buttonWindow2.setEnabled( true );
            this.buttonWindow3.setEnabled( true );
            this.buttonWindow5.setEnabled( true );
            this.buttonWindow6.setEnabled( true );
            this.buttonWindow7.setEnabled( true );
            
            var opinfo_num  = this.OP.op_num;
            console.debug( "op_num: " + opinfo_num + ", opinfo_valid: " + this.opinfo_valid );
            console.debug( "op_err_str: " + this.OP.op_err_str );
            
            var statustekst = this.OP.hsnmanage.statustekst;
            this.label_opstatus.setValue( "&nbsp;&nbsp;" + statustekst + "&nbsp;&nbsp;" );
            if( statustekst.length > 0 ) { this.label_opstatus.set({ backgroundColor : this.color_Yellow }); }
            
            var op_info_str = "";
            var op_info_list = this.OP.op_info_list;
            var op_mutation_list = [];  // for printed letter
            var mutation_lines = "";    // for window0 display
            
            for( var i = 0; i < op_info_list.length; i++ ) 
            {
              var op_info_dict = op_info_list[ i ];
              var id_origin = op_info_dict.id_origin;
              var display_str = op_info_dict.display_str;
              console.debug( "id_origin: " + id_origin + ", " + display_str );
              
              if( id_origin == 10 ) { 
                op_info_str = display_str; 
                this.OP.op_info_str = op_info_str;
                this.opinfo_html = "<h3><b>" + op_info_str + "</b></h3>"
                this.labelOpinfo.setValue( this.opinfo_html );
              }
              else {
                op_mutation_list.push( display_str );
                mutation_lines += "mutatie type " + op_info_dict.id_origin;
                mutation_lines += ", per " + op_info_dict.valid_date;
                mutation_lines += ", " + display_str + "\n";
              }
            }
            this.OP.op_mutation_list = op_mutation_list;
            
            console.debug( "mutations: " + mutation_lines );
            this.textareaMutations.setEnabled( true );
            this.textareaMutations.setValue( mutation_lines );
            this.textareaMutations.setEnabled( false );
          }
          else 
          {
            this.buttonWindow1.setEnabled( false );
            this.buttonWindow2.setEnabled( false );
            this.buttonWindow3.setEnabled( false );
            this.buttonWindow5.setEnabled( false );
            this.buttonWindow6.setEnabled( false );
            //this.buttonWindow7.setEnabled( false );   // 'Stoppen' always enabled
            
            op_info_str = this.OP.op_err_str; 
            this.opinfo_html = "<h3><b>" + op_info_str + "</b></h3>"
            this.labelOpinfo.setValue( this.opinfo_html );
          }
        }, 
        this 
      );
      /*
      request.addListener
      ( 
        "load", 
        function( ev ) 
        {
          var request = ev.getTarget();
          var response = request.getResponse();
          console.debug( "load: " + response );
        }, 
        this 
      );
      */
      request.addListener
      ( 
        "fail", 
        function( ev ) 
        {
          var request = ev.getTarget();
          var response = request.getResponse();
          console.debug( "fail: " + response );
          this.showDialog( "fail" + "<br><br>" + response );
        }, 
        this 
      );
      
      request.addListener
      ( 
        "statusError", 
        function( ev ) 
        {
          var request = ev.getTarget();
          var response = request.getResponse();
          console.debug( "statusError: " + response );
          this.showDialog( "statusError" + "<br><br>" + response );
        }, 
        this 
      );
      /*
      request.addListener
      ( 
        "readyStateChange", 
        function( ev ) 
        {
          var request = ev.getTarget();
          var phase = request.getPhase();
          console.debug( "readyStateChange, phase: " + phase );
        }, 
        this 
      );
      */
      request.send();        // Send the request
    }, // getHsnOpData
    
    
    
    /**
     * saveHsnOpData
     */
    saveHsnOpData : function( path, data )
    {    
      console.debug( "saveHsnOpData() path: " + path );
      console.debug( data );
      
      var url = this.wsgi_url( path );
      
      var method = this.wsgi_method;
      
      if( method === "GET" )        // only for testing, 
      { url += "?"; }
      else if( method === "POST" )  // use POST for login.
      { url += '/'; }               // required: POST + Django: APPEND_SLASH
      
      if( method === "GET" ) { url += data; }
      
      console.debug( "url: " + url );
      var request = new qx.io.request.Xhr( url );
      request.setMethod( method );
      
      if( method === "POST" )           // set parameters in data
      { 
        request.setRequestHeader( "X-CSRFToken", qx.bom.Cookie.get( "csrftoken" ) );
        request.setRequestData( data ); 
      }
      
      request.addListener
      ( 
        "success", 
        function( ev ) 
        {
          var request = ev.getTarget();
          var response = request.getResponse();
          console.debug( "saveHsnOpData() success: " + response.status );
          
          this.getHsnOpData();  // whatever has been saved, update the OP data in this client
        }, 
        this 
      );
      
      request.addListener
      ( 
        "fail", 
        function( ev ) 
        {
          var request = ev.getTarget();
          var response = request.getResponse();
          console.debug( "saveHsnOpData() fail: " + response.status );
          
          this.getHsnOpData();  // whatever happened, update the OP data in this client
        }, 
        this 
      );
      
      request.addListener
      ( 
        "statusError", 
        function( ev ) 
        {
          var request = ev.getTarget();
          var response = request.getResponse();
          console.debug( "saveHsnOpData() statusError: " + response.status );
          
          this.getHsnOpData();  // whatever happened, update the OP data in this client
        }, 
        this 
      );
      
      request.send();        // Send the request
    }, // saveHsnOpData
    
    
    
    /**
     * createWindows
     */
    createWindows : function()
    {    
      console.debug( "createWindows()" );

      this.window0 = this.createWindow0();
      this.window1 = this.createWindow1();
      this.window2 = this.createWindow2();
      this.window3 = this.createWindow3();
      this.window4 = this.createWindow4();
      this.window5 = this.createWindow5();
      this.window6 = this.createWindow6();
      
      this.window1missing = this.createWindow1Missing();
      
      var root = this.getRoot();
      
      root.add( this.window0 );
      root.add( this.window1 );
      root.add( this.window2 );
      root.add( this.window3 );
      root.add( this.window4 );
      root.add( this.window5 );
      root.add( this.window6 );
      
      root.add( this.window1missing );  // subwindow of window1
      
      root.addListener
      (
        "resize", 
        function( e ) 
        {
        //console.debug( "resize" );
          var vp_width  = qx.bom.Viewport.getWidth();
          var vp_height = qx.bom.Viewport.getHeight();
          
          this.window0.setWidth(  vp_width );
          this.window0.setHeight( vp_height );
          
          this.window1.setWidth(  vp_width );
          this.window1.setHeight( vp_height );
          
          this.window2.setWidth(  vp_width );
          this.window2.setHeight( vp_height );
          
          this.window3.setWidth(  vp_width );
          this.window3.setHeight( vp_height );
          
          this.window4.setWidth(  vp_width );
          this.window4.setHeight( vp_height );
          
          this.window5.setWidth(  vp_width );
          this.window5.setHeight( vp_height );
          
          this.window6.setWidth(  vp_width );
          this.window6.setHeight( vp_height );
          
          this.window1missing.setWidth(  vp_width );
          this.window1missing.setHeight( vp_height );
        }, 
        this
      );
      
    this.window0.open();  // start screen
      
    }, // createWindows
    
    
    
    /**
     * createWindow0
     * HSN - Mail
     */
    createWindow0 : function()
    {    
      console.debug( "createWindow0()" );
      
      var wd_width  = this.MAIN_WIDTH;
      var wd_height = this.MAIN_HEIGHT;
      
      var ct_width = wd_width - 32;  // 22 = estimated margin
      
      var window = new qx.ui.window.Window( "HSN - Mail en Beheer" );
      window.set({
        width         : wd_width,
        height        : wd_height,
        allowGrowX    : true,
        allowGrowY    : true,
        allowShrinkX  : true,
        allowShrinkY  : true,
        allowStretchX : true,
        allowStretchY : true
      });
      window.addListener( "resize", window.center );
      
      //window.setAllowMaximize( false );
      
      // main layout
      var layout_window = new qx.ui.layout.VBox( 5 );
      window.setLayout( layout_window );
      
      var layoutSelop = new qx.ui.layout.VBox();
      var containerSelop = new qx.ui.container.Composite( layoutSelop ).set({
        decorator     : "main",  // shows border
        padding       : 5,
        width         : ct_width,
        height        : 150,
        allowGrowX    : true,
        allowGrowY    : true,
        allowShrinkX  : true,
        allowShrinkY  : true,
        allowStretchX : true,
        allowStretchY : true
      });
      window.add( containerSelop, { flex : 1 } );
      
      // Selecteer OP row 0
      var layoutOpnum = new qx.ui.layout.HBox( 10 ).set({ alignY : "middle" });    // spacing = 10
      var containerOpnum = new qx.ui.container.Composite( layoutOpnum ).set({
        allowGrowY: false
      });
      containerSelop.add( new qx.ui.core.Spacer( 10 ) );
      containerSelop.add( containerOpnum );
      
      var opnum_html = "OP-nummer:";
    //var opnum_html = "<span vertical-align: middle>OP-nummer:</span>";
      var labelOpnum = new qx.ui.basic.Label().set({ value : opnum_html });
      containerOpnum.add( new qx.ui.core.Spacer( 50 ) );
      containerOpnum.add( labelOpnum );
      
      var inputOpnum = new qx.ui.form.TextField().set({ maxLength: 15 });
      this.input_opnum = inputOpnum; // accessed by getHsnOpData
      inputOpnum.addListener( "keypress", function( ev ) {
        if( ev.getKeyIdentifier() === "Enter" )
        { this.getHsnOpData( ev ); }
      }, this ); 
      containerOpnum.add( inputOpnum );
      
      var buttonOpnum = new qx.ui.form.Button( "Zoek" );
      buttonOpnum.addListener
      ( 
        "execute", 
        function( ev ) { this.getHsnOpData( ev ) },
        this
      );
      containerOpnum.add( buttonOpnum );
      
      var label_opstatus = new qx.ui.basic.Label().set({ 
        rich       : true, 
        allowGrowX : true
      });
      this.label_opstatus = label_opstatus; // accessed by getHsnOpData
    //label_opstatus.set({ backgroundColor : this.color_Yellow });
      
      containerOpnum.add( new qx.ui.core.Spacer( 10 ), { flex : 1 } );
      containerOpnum.add( label_opstatus, { flex : 100 } );
      
      // set the focus in the appear event (before the window is shown)
      containerOpnum.addListener( "appear", function() { inputOpnum.focus(); }, containerOpnum );
      
      // Selecteer OP row 1
      var layoutOpinfo = new qx.ui.layout.HBox( 10 );    // spacing = 10
      var containerOpinfo = new qx.ui.container.Composite( layoutOpinfo ).set({ allowGrowY: false });
      containerSelop.add( containerOpinfo );
      
      this.labelOpinfo = new qx.ui.basic.Label().set({ rich : true });
      
      containerOpinfo.add( new qx.ui.core.Spacer( 50 ) );
      containerOpinfo.add( this.labelOpinfo );
      
      // is mutation lines
      
      var layout_mutations = new qx.ui.layout.VBox().set({ alignY : "top" });
      var container_mutations = new qx.ui.container.Composite( layout_mutations ).set({
      //decorator     : "main",
        padding       : 5,
        marginLeft    : 50,
        width         : 200,
        height        : 30,
        allowGrowX    : true,
        allowGrowY    : true,
        allowShrinkX  : true,
        allowShrinkY  : true,
        allowStretchX : true,
        allowStretchY : true
      });
      containerSelop.add( container_mutations, { flex : 1 } );
      
      container_mutations.add( new qx.ui.core.Spacer( 50 ) );
      var textareaMutations = this.textareaMutations = new qx.ui.form.TextArea().set({ 
        width         : 200, 
        height        : 30,
        wrap          : false,
        allowGrowX    : true,
        allowGrowY    : true,
        allowShrinkX  : true,
        allowShrinkY  : true,
        allowStretchX : true,
        allowStretchY : true
      });
      container_mutations.add( textareaMutations, { flex : 1 } );
      
      
      // Menu buttons   
      var col2_width = 300;
      var extra = 10;
      var col13_width = (ct_width - (col2_width + extra ))/2;
      var layout_outer = new qx.ui.layout.Grid( 5, 5 );
      layout_outer.setColumnWidth( 0, col13_width );
      layout_outer.setColumnWidth( 1, col2_width );
      layout_outer.setColumnWidth( 2, col2_width );
      
      var container_outer = new qx.ui.container.Composite( layout_outer ).set({
        decorator  : "main",  // shows border
        padding    : 5,
        width      : ct_width,
        height     : 250,
        allowGrowY : false
      });
    //window.add( container_outer, { row : 1, column : 0, colSpan : 3 } );
      window.add( container_outer );
      
      var layout_btns = new qx.ui.layout.VBox();
      layout_btns.setSpacing( 5 );
      var container_btns = new qx.ui.container.Composite( layout_btns ).set({
        width      : col2_width,
        height     : 250,
        allowGrowY : false
      });
    //window.add( container_btns, { row : 1, column : 1 } );
      container_outer.add( container_btns, { row : 1, column : 1 } );
      
      if( this.show_layout ) {
        containerSelop.setbackgroundColor( this.color_Khaki );
        containerOpnum.setBackgroundColor( this.color_Yellow );
        container_btns. setBackgroundColor( this.color_LightGreen );
      }
      
      var button1 = new qx.ui.form.Button( "1) Bijwerken tabel HSN-beheer" );
      var button2 = new qx.ui.form.Button( "2) Aanmaken mail bevolkingsregister" );
      var button3 = new qx.ui.form.Button( "3) Aanmaken mail huwelijksakten" );
      var button4 = new qx.ui.form.Button( "4) Printen mail-aanvragen" );
      var button5 = new qx.ui.form.Button( "5) Verwerken binnengekomen mail" );
      var button6 = new qx.ui.form.Button( "6) Vastleggen identiteitsverandering" );
      var button7 = new qx.ui.form.Button( "7) Stoppen met dit programma" );
      
      // several buttons need a valid OP before being enabled
      button1.set({ center : false, enabled : false });
      button2.set({ center : false, enabled : false });
      button3.set({ center : false, enabled : false });
      button4.set({ center : false });
      button5.set({ center : false, enabled : false });
      button6.set({ center : false, enabled : false });
      button7.set({ center : false });
      
      // and we need to toggle them from elsewhere
      this.buttonWindow1 = button1;
      this.buttonWindow2 = button2;
      this.buttonWindow3 = button3;
      this.buttonWindow5 = button5;
      this.buttonWindow6 = button6;
      this.buttonWindow7 = button7;
      
      container_btns.add( button1, { flex : 0 } );
      container_btns.add( button2, { flex : 0 } );
      container_btns.add( button3, { flex : 0 } );
      container_btns.add( button4, { flex : 0 } );
      container_btns.add( button5, { flex : 0 } );
      container_btns.add( button6, { flex : 0 } );
      container_btns.add( new qx.ui.core.Spacer( 20 ) );
      container_btns.add( button7, { flex : 0 } );
      
      button1.addListener( "execute", function( ev ) 
      {
        console.debug( "button1 Bijwerken tabel HSN-beheer" );
        if( this.opinfo_valid == true ) {
          this.labelOpinfo1a.setValue( this.opinfo_html );
          this.labelOpinfo1b.setValue( "<b>" + this.OP.hsnmanage.statustekst + "</b>");
          this.window1.open();
        }
        else { console.debug ( "No valid OP" ); }
      }, this );
      
      button2.addListener( "execute", function( ev ) 
      {
        console.debug( "button2 Aanmaken mail bevolkingsregister" );
        if( this.opinfo_valid == true ) {
          this.labelOpinfo2.setValue( this.opinfo_html );
          this.window2.open();
        }
        else { console.debug ( "No valid OP" ); }
      }, this );
      
      button3.addListener( "execute", function( ev ) 
      {
        console.debug( "button3 Aanmaken mail huwelijksakten" );
        if( this.opinfo_valid == true ) {
          this.labelOpinfo3.setValue( this.opinfo_html );
          this.window3.open();
        }
        else { console.debug ( "No valid OP" ); }
      }, this );
      
      button4.addListener( "execute", function( ev ) 
      {
        console.debug( "button4 Printen mail-aanvragen" );
        this.window4.open();
      }, this );
      
      button5.addListener( "execute", function( ev ) 
      {
        console.debug( "button5 Verwerken binnengekomen mail" );
        if( this.opinfo_valid == true ) {
          this.labelOpinfo5.setValue( this.opinfo_html );
          this.window5.open();
        }
        else { console.debug ( "No valid OP" ); }
      }, this );
      
      button6.addListener( "execute", function( ev ) 
      {
        console.debug( "button6 Vastleggen identiteitsverandering" );
        if( this.opinfo_valid == true ) {
          this.labelOpinfo6.setValue( this.opinfo_html );
          this.window6.open();
        }
        else { console.debug ( "No valid OP" ); }
      }, this );
      
      button7.addListener( "execute", function( ev ) 
      {
        console.debug( "button7 Stoppen met dit programma" );
        this.window0.close();
        this.createLogout( ev );
      }, this );              
      
      return window;
    }, // createWindow0
    
    
    
    /**
     * createWindow1
     * Bijwerken tabel HSN-beheer
     */
    createWindow1 : function()
    {
      console.debug( "createWindow1()" );
      
      var wd_width  = this.MAIN_WIDTH;
      var wd_height = this.MAIN_HEIGHT;
      
      var ct_width  = wd_width - 22;  // 22 = estimated margin
      
      var window = new qx.ui.window.Window( "Bijwerken tabel HSN-beheer" );
      window.set({
        width  : wd_width,
      //height : wd_height,
        modal  : true
      });
      window.addListener( "resize", window.center );
      window.setLayout( new qx.ui.layout.VBox( 5 ) );
      
       window.addListener
      ( 
        "appear", 
        function( ev ) 
        {
          window.setWidth(  qx.bom.Viewport.getWidth() );
          window.setHeight( qx.bom.Viewport.getHeight() );
          
          // clear data from previous OP
          textareaMarriages.setValue( "" );
          
          textfieldDeathDay  .setValue( "" );
          textfieldDeathMonth.setValue( "" );
          textfieldDeathYear .setValue( "" );
          
          comboboxDeathLocation.setValue( null );
          
          comboboxPhaseA.setValue( null );
          comboboxPhaseB.setValue( null );
          comboboxPhaseC.setValue( null );
          
          var marriages = this.OP.marriages;
          var lines = "";
          for( var i = 0; i < marriages.length; i++ ) 
          { lines += marriages[ i ]; lines += "\n"; }
          textareaMarriages.setValue( lines );   // OP 20507  has 4 marriages
          
          // death info may come from 3 different tables: 
          // Ovlknd: not editable, Pkknd: not editable, Hsnbeheer: editable
          var editable = true;
          var day   = "";
          var month = "";
          var year  = "";
          
          var death_list = this.OP.deaths;
          console.debug( "death entries: " + death_list.length );
          for( i = 0; i < death_list.length; i++ ) 
          {
            var death = death_list[ i ];
            console.debug( death );
            
            day   = death.death_day  .toString();
            month = death.death_month.toString();
            year  = death.death_year .toString();
            
            if( death.edit == false ) {
              editable = false;
              break;  // don't care if an Hsnbeheer editable follows
            }
          }
          
          if( editable ) 
          {
            textfieldDeathDay    .setEnabled( true );
            textfieldDeathMonth  .setEnabled( true );
            textfieldDeathYear   .setEnabled( true );
            comboboxDeathLocation.setEnabled( true );
            
            textfieldDeathDay.addListener( "input", function( ev ) {
              var day = textfieldDeathDay.get( "value" );
              if( isNaN( day ) ) { textfieldDeathDay.setValue( "" ); }            // ignore NaNs
              else if( day.length > 2 ) { textfieldDeathDay.setValue( "" ); }     // too long
              else if( day.length == 2 ){ textfieldDeathMonth.focus(); }          // OK, next field
            });
            
            textfieldDeathMonth.addListener( "input", function( ev ) {
              var month = textfieldDeathMonth.get( "value" );
              if( isNaN( month ) ) { textfieldDeathMonth.setValue( "" ); }        // ignore NaNs
              else if( month.length > 2 ) { textfieldDeathMonth.setValue( "" ); } // too long
              else if( month.length == 2 ){ textfieldDeathYear.focus(); }         // OK, next field
            });
            
            textfieldDeathYear.addListener( "input", function( ev ) {
              var year = textfieldDeathYear.get( "value" );
              if( isNaN( year ) ) { textfieldDeathYear.setValue( "" ); }          // ignore NaNs
              else if( year.length > 4 ) { textfieldDeathYear.setValue( "" ); }   // too long
              else if( year.length == 4 ){ comboboxDeathLocation.focus(); }       // OK, next field
            });
            
            if( death_list.length == 0 || ( day == 0 && month == 0 && year == 0 )) 
            { labelDeathLegend.setValue( "" ); }
            else { labelDeathLegend.setValue( "Overlijdensdatum is bekend" ); }
          }
          else { 
            textfieldDeathDay    .setEnabled( false );
            textfieldDeathMonth  .setEnabled( false );
            textfieldDeathYear   .setEnabled( false );
            comboboxDeathLocation.setEnabled( false );
            
            labelDeathLegend.setValue( "Overlijdensakte is ingevoerd" );
          }
          
          console.debug( "ovldag: " + day + ", ovlmnd: " + month + ", ovljaar: " + year );
          //datefield.setValue( new Date( year, month-1, day ) );   // month starts at 0, not 1
          if( ! ( day == 0 && month == 0 && year == 0) ) { // ignore meaningless date
            textfieldDeathDay  .setValue( day );
            textfieldDeathMonth.setValue( month );
            textfieldDeathYear .setValue( year );
          }
          
          
          var hsnmanage = this.OP.hsnmanage;
          
          var location = hsnmanage.ovlplaats;
          var location_num = hsnmanage.ovlplaats_gemnr
          console.debug( "ovlplaats: " + location + ", gemnr: " + location_num );
          comboboxDeathLocation.setValue( location );
          
          var phase_a_id = hsnmanage.phase_a;
          var phase_b_id = hsnmanage.phase_b;
          var phase_c_id = hsnmanage.phase_c;
          console.debug( "phase A: " + phase_a_id + ", phase B: " + phase_b_id + ", phase C: " + phase_c_id );
          
          var phase_a_str  = hsnmanage.phase_a_str;
          var phase_b_str  = hsnmanage.phase_b_str;
          var phase_c_str  = hsnmanage.phase_c_str;
          console.debug( "phase A str: " + phase_a_str );
          console.debug( "phase B str: " + phase_b_str );
          console.debug( "phase C str: " + phase_c_str );
          
          console.debug( "set comboboxPhaseA, available: " + comboboxPhaseA.getChildren().length );
          if( phase_a_str === "" ) { comboboxPhaseA.setValue( null ); }
          else { comboboxPhaseA.setValue( phase_a_str ); }
          
          console.debug( "set comboboxPhaseB, available: " + comboboxPhaseB.getChildren().length );
          if( phase_b_str === "" ) { comboboxPhaseB.setValue( null ); }
          else { comboboxPhaseB.setValue( phase_b_str ); }
          
          console.debug( "set comboboxPhaseC, available: " + comboboxPhaseC.getChildren().length );
          if( phase_c_str === "" ) { comboboxPhaseC.setValue( null ); }
          else { comboboxPhaseC.setValue( phase_c_str ); }
          
          if( phase_b_id == 2 || phase_b_id == 3 || phase_b_id == 7 || phase_b_id == 8 || phase_b_id == 9 ) 
          { buttonMissing.setEnabled( true ); }
          else { buttonMissing.setEnabled( false ); }
        },
        this
      );
      
      
      // VBox row 0 : OP-info
      var layoutOpinfo = new qx.ui.layout.VBox();
      var containerOpinfo = new qx.ui.container.Composite( layoutOpinfo ).set({
        decorator   : "main",
        paddingLeft : 20,
        width       : ct_width,
        height      : 70,
        allowGrowY  : false
      });
      window.add( containerOpinfo );
      
      this.labelOpinfo1a = new qx.ui.basic.Label().set({ rich : true });
      containerOpinfo.add( this.labelOpinfo1a );
      
      this.labelOpinfo1b = new qx.ui.basic.Label().set({ rich : true });
      containerOpinfo.add( this.labelOpinfo1b );
      
      containerOpinfo.add( new qx.ui.core.Spacer( 10 ) );  // do not not see it?
      
      
      // VBox row 1 : marriages
      var layout_marriage = new qx.ui.layout.VBox().set({ alignY : "top" });
      var container_marriage = new qx.ui.container.Composite( layout_marriage ).set({
        decorator  : "main",
        padding    : 5,
        width      : ct_width,
        height     : 100,
        allowGrowY : false
      });
      window.add( container_marriage );
      
      var textareaMarriages = new qx.ui.form.TextArea();
      textareaMarriages.set({ 
        width   : 200, 
        height  : 100,
        enabled : false,   // read-only
        wrap    : false
      })
      container_marriage.add( textareaMarriages );
      
      
      // VBox row 2 : edit
      var layoutEdit = new qx.ui.layout.Grid( 5, 5 );
      layoutEdit.setColumnFlex( 1, 1 ); // make column 1 flexible
      
      var containerEdit = new qx.ui.container.Composite( layoutEdit ).set({
        decorator  : "main",
        padding    : 10,
        width      : ct_width,
        height     : 100,
        allowGrowY : false
      });
      window.add( containerEdit );
      
      var labelDate = new qx.ui.basic.Label().set({ value : "Overlijdensdatum" });
      containerEdit.add( labelDate, { row : 0, column : 0 } );
      
      /* // KM & MJ do not want mousy date widgets but keyboard inputs
      var datefield = new qx.ui.form.DateField();
      containerEdit.add( datefield, { row : 0, column : 1 } );
      var format = new qx.util.format.DateFormat( "d MMM yyyy" );
      datefield.setDateFormat( format );
      */
      var layoutDeathDate = new qx.ui.layout.HBox( 5 ).set({ AlignY : "middle" });
      var containerDeathDate = new qx.ui.container.Composite( layoutDeathDate );
      var irow = 0;
      containerEdit.add( containerDeathDate, { row : irow, column : 1 } );
      
      var textfieldDeathDay   = new qx.ui.form.TextField().set({ width : 30, placeholder : "DD", textAlign : "center" });
      var textfieldDeathMonth = new qx.ui.form.TextField().set({ width : 30, placeholder : "MM", textAlign : "center" });
      var textfieldDeathYear  = new qx.ui.form.TextField().set({ width : 40, placeholder :"JJJJ",textAlign : "center" });
      
      containerDeathDate.add( textfieldDeathDay );
      containerDeathDate.add( textfieldDeathMonth );
      containerDeathDate.add( textfieldDeathYear );
      
      var labelDeathLegend = new qx.ui.basic.Label();
      containerDeathDate.add( labelDeathLegend );
      
      irow += 1;
      var labelDeathLocation = new qx.ui.basic.Label().set({ value : "Plaats van overlijden" });
      containerEdit.add( labelDeathLocation, { row : irow, column : 0 } );
      
      // ComboTable is a combination of a ComboBox and a Table for autocompletion
      var combotable_model = new combotable.SearchableModel();
      combotable_model.setColumns( ['Id','Data'], ['id','data'] );
      combotable_model.setData( this.location_array );
      
      var comboboxDeathLocation = new combotable.ComboTable( combotable_model ).set({
          width       : 200,
          placeholder : 'Plaats van overlijden'
      });
      
      containerEdit.add( comboboxDeathLocation, { row : irow, column : 1 } );
      
      
      console.debug( "phase A" );
      irow += 1;
      var label_phaseA = new qx.ui.basic.Label().set({ value : "Stadium fase A" });
      containerEdit.add( label_phaseA, { row : irow, column : 0 } );
      
      var comboboxPhaseA = new qx.ui.form.ComboBox().set({ width : 300 });
      containerEdit.add( comboboxPhaseA, { row : irow, column : 1 } );
      
      // only select, do not type
      comboboxPhaseA.getChildControl( "textfield" ).setReadOnly( true );
      
      var strings = this.HSN.strings.TekstFaseA;
      for( var s = 0; s < strings.length; s++ ) 
      {
        var id = strings[ s ].id;
        var string = id + " - " + strings[ s ].text;
        //console.debug( string ); 
        var listItem = new qx.ui.form.ListItem( string );
        // these '2' values must be removed first from the db before disabling them here
        //if( string === "2 - Zoeken in regio compleet" ) { listItem.setEnabled( false ); }
        
        listItem.setUserData( "id", id );
        comboboxPhaseA.add( listItem );
      }
      
      console.debug( "phase B" );
      irow += 1;
      var label_phaseB = new qx.ui.basic.Label().set({ value : "Stadium fase B" });
      containerEdit.add( label_phaseB, { row : irow, column : 0 } );
      
      var comboboxPhaseB = new qx.ui.form.ComboBox().set({ 
        width         : 300, 
        maxListHeight : 300   // default = 200
      });
      containerEdit.add( comboboxPhaseB, { row : irow, column : 1 } );
      
      // only select, do not type
      comboboxPhaseB.getChildControl( "textfield" ).setReadOnly( true );
      
      strings = this.HSN.strings.TekstFaseB;
      for( var s = 0; s < strings.length; s++ ) 
      {
        var id = strings[ s ].id;
        var string = strings[ s ].id + " - " + strings[ s ].text;
        //console.debug( string );
        var listItem = new qx.ui.form.ListItem( string );
        if( string === "4 - Code is vervallen" || string === "6 - Code is vervallen" ) 
        { listItem.setEnabled( false ); }
        
        listItem.setUserData( "id", id );
        comboboxPhaseB.add( listItem );
      }
      
      comboboxPhaseB.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
          var phase_b_value = comboboxPhaseB.getValue();  // the whole string, not only the number
          var phase_b = this.getUservalueCombobox( comboboxPhaseB, phase_b_value, "id" );
          var phase_b_id = phase_b.user_value;
          console.debug( "phase_b_id: " + phase_b_id + ", phase_b_value: " + phase_b_value );
          
          // There should be no missing periods with "dossier compleet". 
          // We retrieve the missing count from the global OP structure, because the 
          // "Ontbrekende perioden" table might not yet be filled
          var missing_data = this.OP.missing_data;
          var numrows = missing_data.length;
          console.debug( numrows + " missing period records" );
            
          if( phase_b_id == 1 || phase_b_id == 5 )
          {
            var msg = "";
            if( numrows > 0 ) 
            {
              if( numrows == 1 ) { 
                msg = "Voor deze OP is er nog " + numrows + " ontbrekende periode.<br>"; 
                msg += "Deze periode zal worden verwijderd.<br>Wilt u doorgaan?";
              }
              else { 
                msg = "Voor deze OP zijn er nog " + numrows + " ontbrekende perioden.<br>"; 
                msg += "Alle perioden zullen worden verwijderd.<br>Wilt u doorgaan?";
              }
              
              this.createWindow1Dialog( numrows, msg );
            }
          }
          
          else if( phase_b_id == 2 ) { buttonMissing.setEnabled( true ); }
          
          else if( phase_b_id == 3 || phase_b_id == 7 || phase_b_id == 8 || phase_b_id == 9 ) 
          { 
            buttonMissing.setEnabled( true ); 
            if( numrows == 0 ) {
              console.debug( "Fase B is " + phase_b_id + ", maar er zijn geen ontbrekende perioden." );
              this.showDialog( "Fase B is " + phase_b_id + ", <br>maar er zijn geen ontbrekende perioden." );
            }
          }
          
          else { buttonMissing.setEnabled( false ); }
        }, 
        this
      );
      
      
      var buttonMissing = new qx.ui.form.Button( "Ontbrekende periodes" );
      buttonMissing.addListener
      ( 
        "execute", 
        function( ev ) { this.window1missing.open( ev ) }, 
        this
      );
      containerEdit.add( buttonMissing, { row : irow, column : 2 } );
      
      
      console.debug( "phase C/D" );
      irow += 1;
      var label_phaseCD = new qx.ui.basic.Label().set({ value : "Stadium fase C/D" });
      containerEdit.add( label_phaseCD, { row : irow, column : 0 } );
      
      var comboboxPhaseC = new qx.ui.form.ComboBox().set({ width : 300 });
      containerEdit.add( comboboxPhaseC, { row : irow, column : 1 } );
      
      // only select, do not type
      comboboxPhaseC.getChildControl( "textfield" ).setReadOnly( true );
      // phase C/D set by db manager
      comboboxPhaseC.setEnabled( false );
      // comboboxPhaseC is disabled, so we do not need listeners
      
      strings = this.HSN.strings.TekstFaseCD;
      for( var s = 0; s < strings.length; s++ ) 
      {
        var id = strings[ s ].id;
        var id = strings[ s ].id;
        var string = strings[ s ].id + " - " + strings[ s ].text;
        //console.debug( string );
        listItem = new qx.ui.form.ListItem( string );
        listItem.setUserData( "id", id );
        comboboxPhaseC.add( listItem );
      }
      
      
      // VBox row 3 : Save, Cancel
      var layoutSaveCancel = new qx.ui.layout.HBox( 5 ).set({ AlignX : "right" });
      var containerSaveCancel = new qx.ui.container.Composite( layoutSaveCancel );
      window.add( containerSaveCancel );
      
      var buttonCancel = new qx.ui.form.Button( "Annuleren" );
      containerSaveCancel.add( buttonCancel );
      
      buttonCancel.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Annuleren" );
          var legend = "Eventuele wijzigingen zullen <b>niet</b> worden opgeslagen.<br>Akkoord?";
          this.closeWindow( window, "Annuleren", legend );
          //window.close();
        },
        this
      );
      
      var buttonSave = new qx.ui.form.Button( "Opslaan" );
      containerSaveCancel.add( buttonSave );
      
      buttonSave.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Opslaan" );
          var death_day   = textfieldDeathDay  .getValue();
          var death_month = textfieldDeathMonth.getValue();
          var death_year  = textfieldDeathYear .getValue();
          var death_date  = death_day + "/" + death_month + "/" + death_year;
          
          var death_location = comboboxDeathLocation.getValue();
          console.debug( "death_location: " + death_location );
          
          var phase_a_value = comboboxPhaseA.getValue();
          var phase_b_value = comboboxPhaseB.getValue();
          var phase_c_value = comboboxPhaseC.getValue();
          
          var phase_a = this.getUservalueCombobox( comboboxPhaseA, phase_a_value, "id" );
          var phase_b = this.getUservalueCombobox( comboboxPhaseB, phase_b_value, "id" );
          var phase_c = this.getUservalueCombobox( comboboxPhaseC, phase_c_value, "id" );
          
          var phase_a_id = phase_a.user_value;
          var phase_b_id = phase_b.user_value;
          var phase_c_id = phase_c.user_value;
          
          console.debug( "phase A: " + phase_a_value + ", phase B: " + phase_b_value + ", phase C: " + phase_c_value );
          console.debug( "phase_a_id: " + phase_a_id + ", phase_b_id: " + phase_b_id + ", phase_c_id: " + phase_c_id );
          
          console.debug( "Overlijdensdatum: " + death_date );
          console.debug( "Plaats van overlijden: " + death_location );
          
          // Save death & phase data. 
          // The marriage data need not be saved, because they are read-only in this window. 
          var data = new Object();
          data.op_num         = this.OP.op_num;
          data.death_day      = death_day;
          data.death_month    = death_month;
          data.death_year     = death_year;
          data.death_location = death_location;
          data.phase_a        = phase_a_id;
          data.phase_b        = phase_b_id;
          data.phase_cd       = phase_c_id;
          
        //this.showDialog( "NOT saving hsnmanage data" );
          this.saveHsnOpData( "/puthsnmanage", data );
          window.close();
        },
        this
      );
      
      return window;
    }, // createWindow1
    
    
    
    /**
     * createWindow1Dialog
     */
    createWindow1Dialog : function( numrows, text )
    {    
      console.debug( "createWindow1Dialog()" );
      
      if( ! this.__window1Dialog )
      {
        var width = 350;
        var dialog = this.__window1Dialog = new qx.ui.window.Window( "Ontbrekende perioden" )
        .set({
          modal          : true,
          showMinimize   : false,
          showMaximize   : false,
          width          : width,
          contentPadding : [ 10, 10, 10, 10 ]
        });
        dialog.addListener( "resize", dialog.center );
        
        var layout = new qx.ui.layout.Grid( 15, 15 );
        layout.setRowFlex( 0, 1 );
        layout.setColumnFlex( 1, 1 );
        dialog.setLayout( layout );
        
        dialog.add
        (
          new qx.ui.basic.Image( "icon/32/status/dialog-information.png" ),
          { row : 0, column : 0 }
        );
        
        dialog.add
        ( 
          new qx.ui.basic.Label().set({
            rich       : true,
            allowGrowY : true
          }), 
          { row : 0, column : 1, colSpan : 2 }
        );
        
        var layoutButtons = new qx.ui.layout.HBox( 5 ).set({ AlignX : "center" });
        var containerButtons = new qx.ui.container.Composite( layoutButtons );
        dialog.add( containerButtons, { row : 1, column : 1 } );
        
        var buttonOK = new qx.ui.form.Button( "Ja" ).set({
          alignX     : "center",
          allowGrowX : false,
          padding    : [ 2, 10 ]
        });
        
        buttonOK.addListener
        (
          "execute", 
          function( ev ) 
          { 
            dialog.close(); 
            console.debug( "createWindow1Dialog() OK" );
          //console.debug( "deleting " + numrows + " periods" );
            
            var json = new Object();
            json.idnr = this.OP.op_num;
            json.nrows = 0;
            json.rdata = [];
            var json_str = qx.lang.Json.stringify( json );
            var data = new Object();
            data.missing = json_str;
          //console.debug( data );
            
            // we send empty missing data, 
            // so the existing missing data records for this OP will be deleted
            this.saveHsnOpData( "/puthsnmanagemissing", data );
          }, 
          this
        );
        
        
        var buttonCancel = new qx.ui.form.Button( "Nee" ).set({
          alignX     : "center",
          allowGrowX : false,
          padding    : [ 2, 10 ]
        });
        
        buttonCancel.addListener
        (
          "execute", 
          function( ev ) 
          { 
            console.debug( "createWindow1Dialog() Cancel" );
            dialog.close();
          }, 
          this
        );
        
        containerButtons.add( buttonCancel );
        containerButtons.add( new qx.ui.core.Spacer( 10 ) );
        containerButtons.add( buttonOK );
      }
      
      this.__window1Dialog.getChildren()[ 1 ].setValue( text );
      this.__window1Dialog.open();
    //this.__window1Dialog.getChildren()[ 2 ].focus();
    }, // createWindow1Dialog
    
    
    
    /**
     * createWindow1Missing
     * Ontbrekende perioden
     */
    createWindow1Missing : function()
    {    
      console.debug( "createWindow1Missing()" );
      
      var wd_width  = this.MAIN_WIDTH;
      var wd_height = this.MAIN_HEIGHT;
      
      var ct_width  = wd_width - 22;  // 22 = estimated margin
      
      var window = new qx.ui.window.Window( "Ontbrekende perioden" );
      window.set({
        width  : wd_width,
        height : wd_height,
        modal  : true
      });
      window.addListener( "resize", window.center );
      window.setLayout( new qx.ui.layout.VBox( 5 ) );
      
       window.addListener
      ( 
        "appear", 
        function( ev ) 
        {
          window.setWidth(  qx.bom.Viewport.getWidth() );
          window.setHeight( qx.bom.Viewport.getHeight() );
          
          // clear data from previous OP
          var numrows = tableModel.getRowCount();
          tableModel.removeRows( 0, numrows );
          
          tbuttonEdit.setValue( false );
          tbuttonEdit.setLabel( "Bewerken is uit" );
          buttonSave.setEnabled( false );
          
          // fill the table with known missing records
          var missing_data = this.OP.missing_data;
          var rows = [];
          var nmiss = 0
          
          for( var i = 0; i < missing_data.length; i++ ) 
          {
            nmiss++;
            var missing = missing_data[ i ];
          //console.debug( "i: " + i + " " + missing );
            
            /*
            // if we also put the text in the column, we have to extract the reason
            // numbers on Save, because only the numbers must be saved in the table. 
            var text = "";
            var reason_num = missing.reason;
            var reasons = this.HSN.strings.TekstReden;
            for( var t = 0; t < reasons.length; t++ ) {
              var reason = reasons[ t ];
              //console.debug( reason );
              if( reason.id == reason_num ) { text = reason.text; }
            }
            var reason_line = reason_num + " - " + text;
            //console.debug( "text: " + text );
            */
            
            var row = [
              nmiss,
              missing.id.toString(),      // "primairy key"
              missing.idvolgnr,           // 1
              missing.idnr.toString(),    // "10397"
              missing.begin_d,            // 9
              missing.begin_m,            // 8
              missing.begin_y.toString(), // "1926"
              missing.end_d,              // 14
              missing.end_m,              // 11
              missing.end_y.toString(),   // "1930"
              missing.location,           // "Batavia"
              missing.reason,             // 4
              missing.found               // "j"
            ];
            rows.push( row );
          }
          tableModel.addRows( rows, 0, true );
        },
        this
      );
      
      
      // VBox row 0 : input new period
      var layoutInput = new qx.ui.layout.Grid( 5, 5 );
      var containerInput = new qx.ui.container.Composite( layoutInput ).set({
        decorator : "main",
        padding : 5,
        width : ct_width,
        height : 50,
        allowGrowY: false
      });
      window.add( containerInput );
      
      var labelBegin    = new qx.ui.basic.Label( "Begin periode:" );
      var labelEnd      = new qx.ui.basic.Label( "Einde periode:" );
      var labelLocation = new qx.ui.basic.Label( "Locatie:" );
      var labelReason   = new qx.ui.basic.Label( "Reden:" );
      
      containerInput.add( labelBegin,    { row : 0, column : 0 } );
      containerInput.add( labelEnd,      { row : 1, column : 0 } );
      containerInput.add( labelLocation, { row : 2, column : 0 } );
      containerInput.add( labelReason,   { row : 3, column : 0 } );
      
      /* // KM & MJ do not want mousy date widgets but keyboard inputs
      var datefieldBegin = new qx.ui.form.DateField();
      var datefieldEnd   = new qx.ui.form.DateField();
      
      containerInput.add( datefieldBegin, { row : 0, column : 1 } );
      containerInput.add( datefieldEnd,   { row : 1, column : 1 } );
      */
      var layoutDateBegin = new qx.ui.layout.HBox( 5 );
      var containerDateBegin = new qx.ui.container.Composite( layoutDateBegin );
      containerInput.add( containerDateBegin, { row : 0, column : 1 } );
      
      var layoutDateEnd = new qx.ui.layout.HBox( 5 );
      var containerDateEnd = new qx.ui.container.Composite( layoutDateEnd );
      containerInput.add( containerDateEnd, { row : 1, column : 1 } );
      
      var textfieldBeginDay   = new qx.ui.form.TextField().set({ width : 30, placeholder : "DD", textAlign : "center" });
      var textfieldBeginMonth = new qx.ui.form.TextField().set({ width : 30, placeholder : "MM", textAlign : "center" });
      var textfieldBeginYear  = new qx.ui.form.TextField().set({ width : 40, placeholder :"JJJJ",textAlign : "center" });
      
      containerDateBegin.add( textfieldBeginDay );
      containerDateBegin.add( textfieldBeginMonth );
      containerDateBegin.add( textfieldBeginYear );
      
      textfieldBeginDay.addListener( "input", function( ev ) {
        var day = textfieldBeginDay.get( "value" );
        if( isNaN( day ) ) { textfieldBeginDay.setValue( "" ); }            // ignore NaNs
        else if( day.length > 2 ) { textfieldBeginDay.setValue( "" ); }     // too long
        else if( day.length == 2 ){ textfieldBeginMonth.focus(); }          // OK, next field
      });
      
      textfieldBeginMonth.addListener( "input", function( ev ) {
        var month = textfieldBeginMonth.get( "value" );
        if( isNaN( month ) ) { textfieldBeginMonth.setValue( "" ); }        // ignore NaNs
        else if( month.length > 2 ) { textfieldBeginMonth.setValue( "" ); } // too long
        else if( month.length == 2 ){ textfieldBeginYear.focus(); }         // OK, next field
      });
      
      textfieldBeginYear.addListener( "input", function( ev ) {
        var year = textfieldBeginYear.get( "value" );
        if( isNaN( year ) ) { textfieldBeginYear.setValue( "" ); }          // ignore NaNs
        else if( year.length > 4 ) { textfieldBeginYear.setValue( "" ); }   // too long
        else if( year.length == 4 ){ textfieldEndDay.focus(); }             // OK, next field
      });
      
      var textfieldEndDay   = new qx.ui.form.TextField().set({ width : 30, placeholder : "DD", textAlign : "center" });
      var textfieldEndMonth = new qx.ui.form.TextField().set({ width : 30, placeholder : "MM", textAlign : "center" });
      var textfieldEndYear  = new qx.ui.form.TextField().set({ width : 40, placeholder :"JJJJ",textAlign : "center" });
      
      containerDateEnd.add( textfieldEndDay );
      containerDateEnd.add( textfieldEndMonth );
      containerDateEnd.add( textfieldEndYear );
      
      textfieldEndDay.addListener( "input", function( ev ) {
        var day = textfieldEndDay.get( "value" );
        if( isNaN( day ) ) { textfieldEndDay.setValue( "" ); }            // ignore NaNs
        else if( day.length > 2 ) { textfieldEndDay.setValue( "" ); }     // too long
        else if( day.length == 2 ){ textfieldEndMonth.focus(); }          // OK, next field
      });
      
      textfieldEndMonth.addListener( "input", function( ev ) {
        var month = textfieldEndMonth.get( "value" );
        if( isNaN( month ) ) { textfieldEndMonth.setValue( "" ); }        // ignore NaNs
        else if( month.length > 2 ) { textfieldEndMonth.setValue( "" ); } // too long
        else if( month.length == 2 ){ textfieldEndYear.focus(); }         // OK, next field
      });
      
      textfieldEndYear.addListener( "input", function( ev ) {
        var year = textfieldEndYear.get( "value" );
        if( isNaN( year ) ) { textfieldEndYear.setValue( "" ); }          // ignore NaNs
        else if( year.length > 4 ) { textfieldEndYear.setValue( "" ); }   // too long
        else if( year.length == 4 ){ comboboxMissingLocation.focus(); }   // OK, next field
      });
      
      var width_column1 = 300;
      // ComboTable is a combination of a ComboBox and a Table for autocompletion
      var combotable_model = new combotable.SearchableModel();
      combotable_model.setColumns( ['Id','Data'], ['id','data'] );
      combotable_model.setData( this.location_array );
      var comboboxMissingLocation = new combotable.ComboTable( combotable_model ).set({
          width       : width_column1,
          placeholder : 'Locatie'
      });
      containerInput.add( comboboxMissingLocation, { row : 2, column : 1 } );
      
      
      var selectboxReason = new qx.ui.form.SelectBox().set({ width : width_column1 });
      containerInput.add( selectboxReason, { row : 3, column : 1 } );
      
      selectboxReason.setMaxListHeight( 300 );   // default = 200
      
      var strings = this.HSN.strings.TekstReden;
      for( var s = 0; s < strings.length; s++ ) {
        var string = strings[ s ].id + " - " + strings[ s ].text;
        var listItem = new qx.ui.form.ListItem( string );
        if( string === "2 - Code niet in gebruik" ) { listItem.setEnabled( false ); }
        selectboxReason.add( listItem );
      }
      
      
      var labelPeriod = new qx.ui.basic.Label( "Nog verdere levensloop na<br>deze ontbrekende periode?" ).set({ rich : true });
      containerInput.add( labelPeriod, { row : 4, column : 0 }  );
      
      var layoutPeriod = new qx.ui.layout.HBox();
      var containerPeriod = new qx.ui.container.Composite( layoutPeriod );
      containerInput.add( containerPeriod, { row : 4, column : 1, colSpan : 2 } );
      
      var radiobuttonNo  = new qx.ui.form.RadioButton( "Nee" );
      var radiobuttonYes = new qx.ui.form.RadioButton( "Ja" );
      
      var managerPeriod = new qx.ui.form.RadioGroup( radiobuttonNo, radiobuttonYes );
      radiobuttonYes.setValue( true );
      
      containerPeriod.add( radiobuttonNo );
      containerPeriod.add( radiobuttonYes );
      
      
      var layoutAdd = new qx.ui.layout.HBox();
      var containerAdd = new qx.ui.container.Composite( layoutAdd );
      
      var buttonAdd = new qx.ui.form.Button( "Toevoegen" );
      buttonAdd.set({ allowGrowY: false });
      containerAdd.add( buttonAdd );
      containerInput.add( containerAdd, { row : 5, column : 0 } );
      
      buttonAdd.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          buttonSave.setEnabled( true );
          
          var beginDay   = Number( textfieldBeginDay  .getValue() );
          var beginMonth = Number( textfieldBeginMonth.getValue() );
          var beginYear  = Number( textfieldBeginYear .getValue() );
          
          textfieldBeginDay  .setValue( "" );
          textfieldBeginMonth.setValue( "" );
          textfieldBeginYear .setValue( "" );
          
          if( beginDay   == 0 ) { beginDay   = -1; }  // not known
          if( beginMonth == 0 ) { beginMonth = -1; }  // not known
          if( beginYear  == 0 ) { beginYear  = -1; }  // not known
          
          var endDay   = Number( textfieldEndDay  .getValue() );
          var endMonth = Number( textfieldEndMonth.getValue() );
          var endYear  = Number( textfieldEndYear .getValue() );
          
          textfieldEndDay  .setValue( "" );
          textfieldEndMonth.setValue( "" );
          textfieldEndYear .setValue( "" );
          
          if( endDay   == 0 ) { endDay   = -1; }  // not known
          if( endMonth == 0 ) { endMonth = -1; }  // not known
          if( endYear  == 0 ) { endYear  = -1; }  // not known
          
          var missing_location = comboboxMissingLocation.getValue();
          comboboxMissingLocation.setValue( null );
          if( missing_location == null ) { missing_location = ""; }
          console.debug( "missing_location: " + missing_location  );
          
          //var reason_str = selectboxReason.getValue();
          //selectboxReason.setValue( null );
          var reason_str = "";
          var isSelectionEmpty = selectboxReason.isSelectionEmpty();
          console.debug( "isSelectionEmpty: " + isSelectionEmpty );
          if( ! isSelectionEmpty ) {
            var reason_arr = selectboxReason.getSelection();
            //console.debug( "num reasons: " + reason_arr.length );
            var listItem = reason_arr[ 0 ];
            reason_str = listItem.getLabel();
            selectboxReason.resetSelection();
          }
          
          var reason = 0;
          if( reason_str != null && reason_str.length > 0 ) 
          { reason = Number( reason_str.substring( 0, 1 ) ); }
          
          if( radiobuttonNo.getValue() == true ) { var isFinal = "n"; }
          else { var isFinal = "j"; }
          radiobuttonNo.setValue( true );
          
          var msg = "Toevoegen:";
          msg = msg + " begin:" + beginDay + "/" + beginMonth + "/" + beginYear;
          msg = msg + " einde:" + endDay   + "/" + endMonth   + "/" + endYear;
          msg = msg + " reden:" + reason;
          msg = msg + " locatie:" + location;
          msg = msg + " finaal:" + isFinal;
          
          console.debug( msg );
          
          // convert to row data, and append to table
          var idvolgnr = 1 + tableModel.getRowCount();
          var op_num = this.OP.op_num;
          
          var nr = "";  // the "#" column, only filled when filling the whole table
          var id = "";  // (new) primairy key determined by db
          var row = [ 
            nr,                   // #
            id,                   // id
            idvolgnr,             // idvolgnr
            op_num,               // idnr
            beginDay,             // begin_d
            beginMonth,           // begin_m
            beginYear.toString(), // begin_y    we do not want: 2,015
            endDay,               // end_d
            endMonth,             // end_m
            endYear.toString(),   // end_y      we do not want: 2,015
            missing_location,     // location
            reason,               // reason
            isFinal               // found
          ];
          console.debug( row );
          
          var rows = [];
          rows.push( row );
          tableModel.addRows( rows, idvolgnr );
        },
        this
      );
      
      
      // VBox row 1 : table with missing periods
      var layoutMissing = new qx.ui.layout.VBox( 5 );
      var containerMissing = new qx.ui.container.Composite( layoutMissing ).set({
        decorator  : "main",
        padding    : 5,
        width      : ct_width,
        height     : 100,
        allowGrowY : false
      });
      window.add( containerMissing, { flex : 1 } );
      
      var tableModel = new qx.ui.table.model.Simple();
      var column_names = [ "#", "ID", "ID volgnr", "ID nr", "SD", "SM", "SJ", 
        "ED", "EM", "EJ", "Locatie", "Reden", "Latere periode bekend?" ];
      tableModel.setColumns( column_names );
     
      // Customize the table column model. We want one that automatically resizes columns.
      var custom = { tableColumnModel : function( obj ) { return new qx.ui.table.columnmodel.Resize( obj ); } };
      
      var table = this.__tableMissing = new qx.ui.table.Table( tableModel, custom );
      table.set({
        decorator        : "main",
        statusBarVisible : false,       // statusbar at bottom
        width            : ct_width,
        height           : 220,
        allowShrinkX     : true,
        allowStretchX    : true,
        allowShrinkY     : true,
        allowStretchY    : true
      });
      containerMissing.add( table );
      
      // after deselection of selected rows, the last deselected row remained lightblue (i.e. focusline).
      table.highlightFocusedRow( false );
      
      var selModel = qx.ui.table.selection.Model;
      var tsm = table.getSelectionModel();
      tsm.setSelectionMode( selModel.NO_SELECTION );
      console.debug( "table getSelectionMode: " + tsm.getSelectionMode() );
      
      tsm.addListener
      (
        "changeSelection", 
        function( ev ) 
        {
          console.debug( "Listener tsm changeSelection" );
          var selection = [];
          table.getSelectionModel().iterateSelection( function( idx ) {
            selection.push( idx );
          });
          console.debug( "selection: " + selection + ", length: " + selection.length  );
          
          if( selection.length > 0 ) { buttonDelete.setEnabled( true ); }
          else { buttonDelete.setEnabled( false ); }
        }, 
        this
      );
      
      
      var tcm = table.getTableColumnModel();
      var resizeBehavior = tcm.getBehavior();
      
      //preferred column widths
      resizeBehavior.set( this.MISSING_nr,       { width  :"1*", minWidth :  20, maxWidth :  20 } );  //  0 "#" screen table row counter: 1,2,3...
      resizeBehavior.set( this.MISSING_id,       { width  :"1*", minWidth :  60, maxWidth :  60 } );  //  1 "ID" primairy key
      resizeBehavior.set( this.MISSING_idvolgnr, { width  :"1*", minWidth :  60, maxWidth :  60 } );  //  2 "ID volgnr"
      resizeBehavior.set( this.MISSING_idnr,     { width  :"1*", minWidth :  60, maxWidth :  60 } );  //  3 "IDnr"
      resizeBehavior.set( this.MISSING_begin_d,  { width  :"1*", minWidth :  35, maxWidth :  30 } );  //  4 "SD"
      resizeBehavior.set( this.MISSING_begin_m,  { width  :"1*", minWidth :  35, maxWidth :  30 } );  //  5 "SM"
      resizeBehavior.set( this.MISSING_begin_y,  { width  :"1*", minWidth :  45, maxWidth :  40 } );  //  6 "SJ"
      resizeBehavior.set( this.MISSING_end_d,    { width  :"1*", minWidth :  35, maxWidth :  30 } );  //  7 "ED"
      resizeBehavior.set( this.MISSING_end_m,    { width  :"1*", minWidth :  35, maxWidth :  30 } );  //  8 "EM"
      resizeBehavior.set( this.MISSING_end_y,    { width  :"1*", minWidth :  45, maxWidth :  40 } );  //  9 "EJ"
      resizeBehavior.set( this.MISSING_location, { width  :"1*", minWidth : 100                 } );  // 12 "Locatie"
      resizeBehavior.set( this.MISSING_reason,   { width  :"1*", minWidth :  50, maxWidth :  50 } );  // 11 "Reden"
    //resizeBehavior.set( this.MISSING_reason,   { width  :"1*", minWidth : 200, maxWidth : 200 } );  // 11 "Reden" num + text
      resizeBehavior.set( this.MISSING_found,    { width  :"1*", minWidth :  50, maxWidth : 130 } );  // 10 "Latere periode bekend?"
      
      tcm.setColumnVisible( this.MISSING_id, false );
      
      // Buttons container: Bekijk meer/minder, Bewerken is aan/uit, Verwijder regel(s), Opslaan
      var layoutButtons = new qx.ui.layout.HBox( 5 ).set({ AlignX : "right" });
      var containerButtons = new qx.ui.container.Composite( layoutButtons );
      containerMissing.add( containerButtons );
      
      // button bekijk meer/minder ?
      
      var tbuttonEdit = new qx.ui.form.ToggleButton( "Bewerken is uit" ).set({ value : false });
      containerButtons.add( tbuttonEdit );
      
      tbuttonEdit.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
          console.debug( "Listener tbuttonEdit changeValue" );
          var value = tbuttonEdit.getValue();
          console.debug( "value: " + value );
          
          var selModel = qx.ui.table.selection.Model;
          var tsm = table.getSelectionModel();
          
          if( value == true ) 
          { 
            console.debug( "Bewerken uit -> aan" );
            tbuttonEdit.setLabel( "Bewerken is aan" );
            buttonSave.setEnabled( true );
            
            var numcols = tableModel.getColumnCount();
            for( var i = 0; i < numcols; i++ ) 
            { tableModel.setColumnEditable( i, true ); }
            
            tsm.setSelectionMode( selModel.MULTIPLE_INTERVAL_SELECTION_TOGGLE );
            
            table.resetCellFocus();
            table.setShowCellFocusIndicator( true );
          }
          else if( value == false ) 
          { 
            console.debug( "Bewerken aan -> uit" );
            tbuttonEdit.setLabel( "Bewerken is uit" );
            buttonSave.setEnabled( false );
            
            tableModel.setEditable( false );
            
            tsm.setSelectionMode( selModel.NO_SELECTION );
            
            table.resetCellFocus();
            table.setShowCellFocusIndicator( false );
          }
          console.debug( "table getSelectionMode: " + tsm.getSelectionMode() );
        }, 
        this 
      );
      
      
      var buttonDelete = new qx.ui.form.Button( "Verwijder regel(s)" ).set({ enabled : false });
      containerButtons.add( buttonDelete );
      
      buttonDelete.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Listener buttonDelete execute" );
          var remove = [];
          // unshift (i.e. push to begin) instead of push (to end)
          table.getSelectionModel().iterateSelection( function( idx ) { remove.unshift( idx );});
          
          // reset the selection before deleting the rows!, otherwise 'undefined' in Qooxdoo Model.js
          var tsm = table.getSelectionModel();
          tsm.resetSelection();
          
          var tableModel = table.getTableModel();
          
          // remove rows from bottom to top (see unshift above) !
          for( var r = 0; r < remove.length; r++ ) {
            var row = remove[ r ];
            tableModel.removeRows( row, 1 );
            console.debug( "Deleted row " + row );
          }
          
          console.debug( "Deleted " + remove.length + " rows: " + remove );
        },
        this
      );
      
      
      // VBox row 2 : Save, Cancel
      var layoutSaveCancel = new qx.ui.layout.HBox( 5 ).set({ AlignX : "right" });
      var containerSaveCancel = new qx.ui.container.Composite( layoutSaveCancel );
      window.add( containerSaveCancel );
      
      var buttonCancel = new qx.ui.form.Button( "Annuleren" );
      containerSaveCancel.add( buttonCancel );
      
      buttonCancel.addListener
      ( 
        "execute", function( ev ) 
        {
          console.debug( "Annuleren" );
          var legend = "Eventuele wijzigingen zullen <b>niet</b> worden opgeslagen.<br>Akkoord?";
          this.closeWindow( window, "Annuleren", legend );
          //window.close();
        },
        this
      );
      
      var buttonSave = new qx.ui.form.Button( "Opslaan" ).set({ enabled : false });
      containerSaveCancel.add( buttonSave );
      
      buttonSave.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Listener buttonSave execute" );
          tbuttonEdit.setValue( false );
          tbuttonEdit.setLabel( "Bewerken is uit" );
          
          // Save all rows of table missing periods
          var table_data = tableModel.getData();
          var nrows = table_data.length;
          console.debug( "table data rows: " + table_data.length );
          var rows = [];
          
          for( var r = 0; r < nrows; r++ ) 
          {
            var row_data = table_data[ r ];
            console.debug( row_data );
            
            var row = new Object();
            // row_data[ this.MISSING_nr ] is the local # counter (not in db)
            row.id       = row_data[ this.MISSING_id ];
            row.idvolgnr = row_data[ this.MISSING_idvolgnr ];
            row.idnr     = row_data[ this.MISSING_idnr ];
            row.begin_d  = row_data[ this.MISSING_begin_d ];
            row.begin_m  = row_data[ this.MISSING_begin_m ];
            row.begin_y  = row_data[ this.MISSING_begin_y ];
            row.end_d    = row_data[ this.MISSING_end_d ];
            row.end_m    = row_data[ this.MISSING_end_m ];
            row.end_y    = row_data[ this.MISSING_end_y ];
            row.location = row_data[ this.MISSING_location ];
            row.reason   = row_data[ this.MISSING_reason ];
            row.found    = row_data[ this.MISSING_found ];
            
            rows.push( row );
            console.debug( row );
          }
          
          // We send the op_num separately; in case we are sending an empty table, 
          // we then still know for which OP to delete the missing period records. 
          var json = new Object();
          json.idnr = this.OP.op_num;
          json.nrows = nrows;
          json.rdata = rows;
          
          var json_str = qx.lang.Json.stringify( json );
          
          var data = new Object();
          data.missing = json_str;
          
        //this.showDialog( "NOT saving table rows<br>(update, create, delete)" );
          this.saveHsnOpData( "/puthsnmanagemissing", data );
          window.close();
        },
        this
      );
      
      return window;
    }, // createWindow1Missing
    
    
    
    /**
     * createWindow2
     * Aanmaken mail bevolkingsregister
     */
    createWindow2 : function()
    {
      console.debug( "createWindow2()" );
      
      //var wd_width  = this.MAIN_WIDTH;
      //var wd_height = this.MAIN_HEIGHT;
      
      var wd_width  = qx.bom.Viewport.getWidth();   // use whole viewport width
      var wd_height = qx.bom.Viewport.getHeight();  // use whole viewport height
      
      var ct_width  = wd_width - 22;  // 22 = estimated margin
      
      var window = new qx.ui.window.Window( "Aanmaken mail bevolkingsregister" );
      window.set({
        width  : wd_width,
        height : wd_height,
        modal  : true
      });
      window.addListener( "resize", window.center );
      window.setLayout( new qx.ui.layout.VBox( 5 ) );
      
      //var opvader_list = [];
      //var opmoeder_list = [];
      var oppartner_list = [];
      
      window.addListener
      ( 
        "appear", 
        function( ev ) 
        {
          console.debug( "Window2 appear" );
          window.setWidth(  qx.bom.Viewport.getWidth() );
          window.setHeight( qx.bom.Viewport.getHeight() );
          
          // clear data from previous OP
          pk_changed = [];  // empty array of pk's of rows that have been updated
          pk_deleted = [];  // empty array of pk's that have been deleted
          
          var numrows = tableModel.getRowCount();
          tableModel.removeRows( 0, numrows );
          
          var op_info = null;
          for( var i = 0; i < this.OP.op_info_list.length; i++ )
          {
            var op_info = this.OP.op_info_list[ i ];
            if( op_info.id_origin == 10 )   // birth op_info
            {
              var father_firstname = op_info.fa_firstname;
              var father_prefix    = op_info.fa_prefix;
              var father_lastname  = op_info.fa_family;
              
              var mother_firstname = op_info.mo_firstname;
              var mother_prefix    = op_info.mo_prefix;
              var mother_lastname  = op_info.mo_family;
              
              var father_name = "";
              if( father_lastname != "" ) {
                father_name = father_lastname;
                if( father_prefix != "" ) { father_name += ", " + father_prefix; }
                father_name += ", " + father_firstname; 
              }
              
              var mother_name = "";
              if( mother_lastname != "" ) { 
                mother_name = mother_lastname;
                if( mother_prefix != "" ) { mother_name += ", " + mother_prefix; }
                mother_name += ", " + mother_firstname; 
              }
              
              textfield1Father.setValue( father_name );
              textfield1Mother.setValue( mother_name );
              
              textfield2Father.setValue( father_name );
              textfield2Mother.setValue( mother_name );
            }
          }
          
          textareaRemarks.setValue( "" );
          
          comboboxLocation   .setValue( "" );
          textfieldLocationNr.setValue( "" );
          
          radiobuttonParents.setValue( true );
          radiobuttonDepart .setValue( true );
          
          textfieldDepart.setValue( "" );
          textfieldArrive.setValue( "" );
          textfieldPeriod.setValue( "" );
          
          tbuttonEdit.setValue( false );
          tbuttonEdit.setLabel( "Bewerken is uit" );
          buttonSave.setEnabled( false );
          
          table.resetCellFocus();
          table.setShowCellFocusIndicator( false );
          tableModel.setEditable( false );
          tsm.setSelectionMode( selModel.NO_SELECTION );
          // ... set default visible columns?
          
          // fill the table with "bevolkingsregister" mails
          var mails = this.OP.mails.bev;
          var rows = [];
          var nbev = 0;
          
          oppartner_list = [];
          
          for( var i = 0; i < mails.length; i++ ) 
          {
            var mail = mails[ i ];
          //console.debug( "i: " + i + " " + mail );
            
            var oppartner = mail.oppartner;
            if( oppartner!= "" && oppartner_list.indexOf( oppartner ) == -1) 
            { oppartner_list.push( oppartner ); }
            
            nbev++;
            var row = [ 
              nbev,                           //  0
              mail.id.toString(),             //  1
              mail.idnr.toString(),           //  2
              mail.briefnr.toString(),        //  3
              mail.aard,                      //  4
              mail.datum,                     //  5
              mail.periode,                   //  6
              mail.gemnr.toString(),          //  7
              mail.naamgem,                   //  8
              mail.status,                    //  9
              mail.printdatum,                // 10
              mail.printen,                   // 11
              mail.ontvdat,                   // 12
              mail.opmerk,                    // 13
              mail.opident,                   // 14
              mail.oppartner,                 // 15
              mail.opvader,                   // 16
              mail.opmoeder,                  // 17
              mail.type,                      // 18
              mail.infoouders,                // 19
              mail.infopartner,               // 20
              mail.inforeis                   // 21
            ];
            rows.push( row );
          }
          
          var clearSorting = true;
          tableModel.addRows( rows, 0, clearSorting );
          
          combobox1Partner.removeAll();
          combobox2Partner.removeAll();
          
          var partners = this.OP.partners;
          for( var i = 0; i < partners.length; i++ ) 
          { 
            var partner = partners[ i ];
            var listItem1 = new qx.ui.form.ListItem( partner );
            var listItem2 = new qx.ui.form.ListItem( partner );
            combobox1Partner.add( listItem1 );
            combobox2Partner.add( listItem2 );
          }
          
          if( partners.length > 0 ) 
          { 
            var partner = partners[ 0 ];
            combobox1Partner.setValue( partner ); 
            combobox2Partner.setValue( partner ); 
          }
        },
        this
      );
      
      // VBox row 0 : OP-info
      //console.debug( "VBox row 0: OP-info" );
      var layoutOpinfo = new qx.ui.layout.HBox( 10 );    // spacing = 10
      var containerOpinfo = new qx.ui.container.Composite( layoutOpinfo ).set({
        decorator   : "main",
        paddingLeft : 20,
        width       : ct_width,
        allowGrowX  : true,
        allowGrowY  : false
      });
      window.add( containerOpinfo );
      
      this.labelOpinfo2 = new qx.ui.basic.Label().set({ rich : true });
      containerOpinfo.add( this.labelOpinfo2 );
      
      
      // VBox row 1 : make mail
      //console.debug( "VBox row 1: make mail" );
      var layoutMailadd = new qx.ui.layout.Grid( 5, 5 );
      // make column 4 flexible to extent the TextArea to the right border
      layoutMailadd.setColumnFlex( 4, 1 );
      
      var containerMailadd = new qx.ui.container.Composite( layoutMailadd ).set({
        decorator  : "main",
        padding    : 5,
        width      : ct_width,
        height     : 100,
        allowGrowY : false
      });
      window.add( containerMailadd );
      
      var labelTravel = new qx.ui.basic.Label( "Deze persoon migreerde:" );
      containerMailadd.add( labelTravel, { row : 0, column : 0 } );
      
      
      var radiobuttonParents = new qx.ui.form.RadioButton( "met ouders" );
      var radiobuttonPartner = new qx.ui.form.RadioButton( "met echtgeno(o)t(e)" );
      var radiobuttonAlone   = new qx.ui.form.RadioButton( "alleen" );
      
      var managerPerson = new qx.ui.form.RadioGroup( radiobuttonParents, radiobuttonPartner, radiobuttonAlone );
      radiobuttonParents.setValue( true );
      
      containerMailadd.add( radiobuttonParents, { row : 1, column : 0 } );
      containerMailadd.add( radiobuttonPartner, { row : 2, column : 0 } );
      containerMailadd.add( radiobuttonAlone ,  { row : 3, column : 0 });
      
      radiobuttonParents.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
          var value = radiobuttonParents.getValue();
          //console.debug( "Parents: " + value );
          if( value == true ) {
            textfield1Father.setVisibility( "visible" );
            textfield1Mother.setVisibility( "visible" );
            
            textfield1Father.setEnabled( true );
            textfield1Mother.setEnabled( true );
          }
          else {
            textfield1Father.setVisibility( "hidden" );
            textfield1Mother.setVisibility( "hidden" );
            
            textfield1Father.setEnabled( false );
            textfield1Mother.setEnabled( false );
          }
        },
        this
      );
      
      radiobuttonPartner.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
          var value = radiobuttonPartner.getValue();
          //console.debug( "Partner: " + value );
          if( value == true ) { 
            combobox1Partner.setVisibility( "visible" );
            combobox1Partner.setEnabled( true );
          }
          else { 
            combobox1Partner.setVisibility( "hidden" );
            combobox1Partner.setEnabled( false );
          }
        },
        this
      );
      
      radiobuttonAlone.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
          var value = radiobuttonAlone.getValue();
          //console.debug( "Alone: " + value );
          if( value == true ) { 
            checkboxParents.setVisibility( "visible" );
            checkboxPartner.setVisibility( "visible" );
            
            //checkboxParents.setValue( true );   // NOT checked by default
            //checkboxPartner.setValue( true );   // NOT checked by default
            
            checkboxParents.setEnabled( true ); 
            checkboxPartner.setEnabled( true );
          }
          else { 
            checkboxParents.setVisibility( "hidden" );
            checkboxPartner.setVisibility( "hidden" );
            
            checkboxParents.setValue( false );    // uncheck when not alone
            checkboxPartner.setValue( false );    // uncheck when not alone
            
            checkboxParents.setEnabled( false );
            checkboxPartner.setEnabled( false );
          }
        },
        this
      );
      
      
      var textfield1Father = new qx.ui.form.TextField().set({ 
        width       : 200, 
        placeholder : "Vader", 
        visibility  : "visible",
        enabled     : true
      });
      containerMailadd.add( textfield1Father, { row : 1, column : 1 } );
      
      var textfield1Mother = new qx.ui.form.TextField().set({ 
        width       : 200, 
        placeholder : "Moeder", 
        visibility  : "visible",
        enabled     : true 
      });
      containerMailadd.add( textfield1Mother, { row : 1, column : 2 } );
      
      var combobox1Partner = new qx.ui.form.ComboBox().set({ 
        width       : 200, 
        placeholder : "Partner", 
        visibility  : "hidden",
        enabled     : false 
      });
      containerMailadd.add( combobox1Partner, { row : 2, column : 1 } );
      
      
      var checkboxParents = new qx.ui.form.CheckBox( "Extra info ouders" ).set({ 
        visibility : "hidden",
        enabled    : false 
      });
      containerMailadd.add( checkboxParents, { row : 3, column : 1 } );
      
      checkboxParents.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
          var value = checkboxParents.getValue();
          if( value == true ) {
            textfield2Father.setVisibility( "visible" );
            textfield2Mother.setVisibility( "visible" );
            
            textfield2Father .setEnabled( true );
            textfield2Mother .setEnabled( true );
          }
          else {
            textfield2Father.setVisibility( "hidden" );
            textfield2Mother.setVisibility( "hidden" );
            
            textfield2Father .setEnabled( false );
            textfield2Mother .setEnabled( false );
          }
        },
        this
      );
      
      var textfield2Father = new qx.ui.form.TextField().set({ 
        width       : 206, 
        placeholder : "Vader", 
        visibility  : "hidden",
        enabled     : false 
      });
      containerMailadd.add( textfield2Father, { row : 3, column : 2 } );
      
      var textfield2Mother = new qx.ui.form.TextField() .set({ 
        width       : 206, 
        placeholder : "Moeder", 
        visibility  : "hidden",
        enabled     : false 
      });
      containerMailadd.add( textfield2Mother, { row : 3, column : 3 } );
      
      var combobox2Partner = new qx.ui.form.ComboBox().set({ 
        width       : 206, 
        placeholder : "Partner", 
        visibility  : "hidden",
        enabled     : false 
      });
      containerMailadd.add( combobox2Partner, { row : 4, column : 2 } );
      
      
      var checkboxPartner = new qx.ui.form.CheckBox( "Extra info Echtgeno(o)t(e)" ).set({ 
        visibility : "hidden",
        enabled : false 
      });
      containerMailadd.add( checkboxPartner, { row : 4, column : 1 } );
      
      checkboxPartner.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
          var value = checkboxPartner.getValue();
          if( value == true ) { 
            combobox2Partner.setVisibility( "visible" );
            combobox2Partner.setEnabled( true ); 
          }
          else { 
            combobox2Partner.setVisibility( "hidden" );
            combobox2Partner.setEnabled( false ); 
          }
        },
        this
      );
      
      
      var labelDatums = new qx.ui.basic.Label( "Datums:" );
      containerMailadd.add( labelDatums, { row : 5, column : 0 } );
      
      var layoutDates = new qx.ui.layout.Grid( 5, 5 );
      var containerDates = new qx.ui.container.Composite( layoutDates ).set({
        decorator  : "main",
        padding    : 5,
        width      : ct_width,
        height     : 50,
        allowGrowY : false
      });
      containerMailadd.add( containerDates, { row : 5, column : 1, colSpan : 3 } );
      
      var radiobuttonDepart = new qx.ui.form.RadioButton( "Vertrek naar" );
      var radiobuttonArrive = new qx.ui.form.RadioButton( "Vertrokken uit (herkomst)" );
      var radiobuttonPeriod = new qx.ui.form.RadioButton( "Periode van aanwezigheid" );
      
      var managerDates = new qx.ui.form.RadioGroup( radiobuttonDepart, radiobuttonArrive, radiobuttonPeriod );
      radiobuttonDepart.setValue( true );
      
      containerDates.add( radiobuttonDepart, { row : 0, column : 0 } );
      containerDates.add( radiobuttonArrive, { row : 0, column : 1 } );
      containerDates.add( radiobuttonPeriod, { row : 0, column : 2 } );
      
      radiobuttonDepart.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
          var value = radiobuttonDepart.getValue();
          console.debug( "Depart: " + value );
          if( value == true ) { textfieldDepart.setEnabled( true ); }
          else { textfieldDepart.set({ value : "", enabled : false }); }
        },
        this
      );
      
      radiobuttonArrive.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
          var value = radiobuttonArrive.getValue();
          console.debug( "Arrive: " + value );
          if( value == true ) { textfieldArrive.setEnabled( true ); }
          else { textfieldArrive.set({ value : "", enabled : false }); }
        },
        this
      );
      
      radiobuttonPeriod.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
          var value = radiobuttonPeriod.getValue();
          console.debug( "Period: " + value );
          if( value == true ) { textfieldPeriod.setEnabled( true ); }
          else { textfieldPeriod.set({ value : "", enabled : false }); }
        },
        this
      );
      
      
      var textfieldDepart = new qx.ui.form.TextField().set({ width : 200, placeholder : "DD/MM/JJJJ", textAlign : "left", enabled : true });
      var textfieldArrive = new qx.ui.form.TextField().set({ width : 200, placeholder : "DD/MM/JJJJ", textAlign : "left", enabled : false });
      var textfieldPeriod = new qx.ui.form.TextField().set({ width : 200, placeholder : "JJJJ-JJJJ",  textAlign : "left", enabled : false });
      
      containerDates.add( textfieldDepart, { row : 1, column : 0 } );
      containerDates.add( textfieldArrive, { row : 1, column : 1 } );
      containerDates.add( textfieldPeriod, { row : 1, column : 2 } );
      
      
      var labelLocation = new qx.ui.basic.Label( "Gemeente:" );
      containerMailadd.add( labelLocation, { row : 6, column : 0 } );
      
      var layoutLocation = new qx.ui.layout.HBox( 5 ).set({ alignY : "middle" });
      var containerLocation = new qx.ui.container.Composite( layoutLocation );
      
      // ComboTable is a combination of a ComboBox and a Table for autocompletion
      var combotable_model = new combotable.SearchableModel();
      combotable_model.setColumns( ['Id','Data'], ['id','data'] );
      combotable_model.setData( this.location_array );
      
      var comboboxLocation = new combotable.ComboTable( combotable_model ).set({
          width       : 206,
          placeholder : 'Gemeente'
      });
      containerLocation.add( comboboxLocation );
      
      comboboxLocation.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
          var location_value = comboboxLocation.getValue();
          //console.debug( "location_value: " + location_value )
          var location_nr = this.location2nr( location_value );
          
          console.debug( "location_value: " + location_value + ", location_nr: " + location_nr );
          textfieldLocationNr.setValue( location_nr.toString() );   // use proper upper-/lowercase string
        },
        this
      );
      
      
      containerLocation.add( new qx.ui.core.Spacer( 73 ) );
      
      // gemnr not needed in GUI (-> invisible), but needed server-side
      var labelLocationNr = new qx.ui.basic.Label( "Gemeente Nr:" ).set({ visibility: false });
      containerLocation.add( labelLocationNr );
      var textfieldLocationNr = new qx.ui.form.TextField()
      .set({
        width      : 50,
        enabled    : false,
        visibility : false
      });
      containerLocation.add( textfieldLocationNr );
      
      containerMailadd.add( containerLocation, { row : 6, column : 1, colSpan : 3 } );
      
      
      var labelRemarks = new qx.ui.basic.Label( "Opmerkingen:" );
      containerMailadd.add( labelRemarks, { row : 7, column : 0 } );
      
      var textareaRemarks = this.__textareaRemarks = new qx.ui.form.TextArea().
      set({ 
        width        : 622,
        height       : 120,
        allowGrowX   : false,
        allowGrowY   : true,
        allowShrinkX : true,
        allowShrinkY : true
      });
      containerMailadd.add( textareaRemarks, { row : 7, column : 1, colSpan : 4 } );
      
      
      var layoutBtnAdd = new qx.ui.layout.HBox().set({ AlignX : "right" });
      var containerBtnAdd = new qx.ui.container.Composite( layoutBtnAdd );
      
      var buttonAdd = new qx.ui.form.Button( "Mail toevoegen" );
      containerBtnAdd.add( buttonAdd );
      
      containerMailadd.add( containerBtnAdd, { row : 8, column : 4 } );
      
      buttonAdd.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Window 2: Mail toevoegen" );
          buttonSave.setEnabled( true );
          
          var info_journey = null;
          if( radiobuttonParents.getValue() )      { info_journey = 3; }
          else if( radiobuttonPartner.getValue() ) { info_journey = 2; }
          else if( radiobuttonAlone.getValue() )   { info_journey = 1; }
          console.debug( "info_journey: " + info_journey );
          
          var info_parents = checkboxParents.getValue();
          var info_partner = checkboxPartner.getValue();
          
          var op_father  = "";
          var op_mother  = "";
          var op_partner = "";
          
          if( textfield1Father.isEnabled() ) { op_father = textfield1Father.getValue(); }
          else if( textfield2Father.isEnabled() ) { op_father = textfield2Father.getValue(); }
          else { op_father = ""; }
          
          if( textfield1Mother.isEnabled() ) { op_mother = textfield1Mother.getValue(); }
          else if( textfield2Mother.isEnabled() ) { op_mother = textfield2Mother.getValue(); }
          else { op_mother = ""; }
          
          if( combobox1Partner.isEnabled() ) { op_partner = combobox1Partner.getValue(); }
          else if( combobox2Partner.isEnabled() ) { op_partner = combobox2Partner.getValue(); }
          else { op_partner = ""; } 
          
          if( op_father  == null ) { op_father  = ""; }
          if( op_mother  == null ) { op_mother  = ""; }
          if( op_partner == null ) { op_partner = ""; }
          
          console.debug( "father: " + op_father + ", mother: " + op_mother + ", partner: " + op_partner );
          
          var kind   = "";
          var date   = "";
          var period = "";
          
          if( textfieldDepart.isEnabled() ) { kind = "V"; date   = textfieldDepart.getValue(); }
          if( textfieldArrive.isEnabled() ) { kind = "H"; date   = textfieldArrive.getValue(); }
          if( textfieldPeriod.isEnabled() ) { kind = "B"; period = textfieldPeriod.getValue(); }
          
          if( kind   == null ) { kind   = ""; }
          if( date   == null ) { date   = ""; }
          if( period == null ) { period = ""; }
          
          console.debug( "kind: " + kind + ", date: " + date + ", period: " + period );
          
          var location    = comboboxLocation   .getValue();
          var location_nr = textfieldLocationNr.getValue();
          
          var remarks = textareaRemarks.getValue();
          
          console.debug( "location: " + location + ", remarks: " + remarks );
          
          var numrows = tableModel.getRowCount();
          var status  = 0;    // initially
          
          var op_ident = "";
          for( var i = 0; i < this.OP.op_info_list.length; i++ )
          {
            var op_info = this.OP.op_info_list[ i ];
            if( op_info.id_origin == 10 )   // birth op_info
            {
              op_ident = op_info.rp_family;
              if( op_info.rp_prefix != "" ) { op_ident += ", " + op_info.rp_prefix; }
              op_ident += ", " + op_info.rp_firstname;
              op_ident += " [" + op_info.rp_b_sex + "]";
              op_ident += ", geboren";
              op_ident += " " + op_info.rp_b_date;
              op_ident += " te";
              op_ident += " " + op_info.rp_b_place;
            }
          }
          
          var type = "BEV";
          
          if( info_parents == true ) { var print_parents = 1; }
          else { var print_parents = 0; }
          
          if( info_partner == true ) { var print_partner = 1; }
          else { var print_partner = 0; }
          
          if( info_journey == true ) { var print_journey = 1; }
          else { var print_journey = 0; }
          
          var row = [ 
            numrows + 1,            //  0 #
            "",                     //  1 id
            this.OP.op_num,         //  2 idnr
            "",                     //  3 briefnr
            kind,                   //  4 aard
            date,                   //  5 datum
            period,                 //  6 periode
            location_nr,            //  7 gemnr
            location,               //  8 naamgem
            status,                 //  9 status
            "",                     // 10 printdatum
            "",                     // 11 printen
            "",                     // 12 ontvdat
            remarks,                // 13 opmerk
            op_ident,               // 14 opident
            op_partner,             // 15 ppartner
            op_father,              // 16 opvader
            op_mother,              // 17 opmoeder
            type,                   // 18 type
            info_parents,           // 19 
            info_partner,           // 20 
            info_journey            // 21 
          ];
          
          var rows = [];
          rows.push( row );
          var clearSorting = false;
          tableModel.addRows( rows, numrows, clearSorting );
          
          // clear some input fields for possible next mail
          radiobuttonParents.setValue( true );
          radiobuttonDepart .setValue( true );
          
          textfieldDepart.setValue( "" );
          textfieldArrive.setValue( "" );
          textfieldPeriod.setValue( "" );
          
          comboboxLocation   .setValue( "" );
          textfieldLocationNr.setValue( "" );
          
          textareaRemarks.setValue( "" );
        },
        this
      );
      
      
      // VBox row 2 : overview requests
      //console.debug( "VBox row 2: overview requests" );
      var layoutRequests = new qx.ui.layout.VBox( 5 );
      var containerRequests = new qx.ui.container.Composite( layoutRequests ).set({
        decorator  : "main",
        padding    : 5,
        width      : ct_width,
        height     : 100,
        allowGrowX : true,
        allowGrowY : true
      });
      window.add( containerRequests, { flex : 1 } );
      
      var tableModel = this._tableModel = new qx.ui.table.model.Simple();
      var column_names = [
          "#",
          "Id",
          "Id Nr",
          "Brief Nr",
          "Aard",
          "Datum",
          "Periode",
          "Gemeente Nr",
          "Gemeente",
          "Status",
          "Print Datum",
          "Printen",
          "Ontvang Datum",
          "Opmerkingen",
          "OP Ident",
          "OP Partner",
          "OP Vader",
          "OP Moeder",
          "Type",
          "Info Ouders",
          "Info Partner",
          "Info Reis"
      ];
      tableModel.setColumns( column_names );
     
      // Customize the table column model. We want one that automatically resizes columns.
      var custom = { tableColumnModel : function( obj ) { return new qx.ui.table.columnmodel.Resize( obj ); } };
      
      var table = new qx.ui.table.Table( tableModel, custom );
      table.set({
        decorator        : "main",
        statusBarVisible : false,       // statusbar at bottom
        width            : ct_width,
        height           : 100,
        allowGrowX       : true,
        allowGrowY       : true
      });
      containerRequests.add( table, { flex : 1 } );
      
      var pk_changed = [];  // list of pk's (i.e. id) of rows to be updated
      
      
      table.addListener
      ( 
        "dataEdited", 
        function( ev ) 
        {
          console.debug( "dataEdited: " );
          var data = ev.getData();
          var row_data = tableModel.getRowData( data.row );
          var id = row_data[ this.MAIL_id ];
          console.debug( "row idx: " + data.row + ", col idx: " + data.col + ", oldValue: " + 
            data.oldValue + ", value: " + data.value + ", id: " + id );
          pk_changed.push( id );
          
          table.resetCellFocus();
          table.setShowCellFocusIndicator( false );
          tableModel.setEditable( false );
          tsm.setSelectionMode( selModel.NO_SELECTION );
        },
        this
      );
      
      
      table.addListener
      (
        "cellTap", 
        function( ev ) 
        {
          var row_idx    = ev.getRow();
          var column_idx = ev.getColumn();
          console.debug( "cellTap type: " + ev.getType() + ", row: " + row_idx + ", columnn: " + column_idx );
          
          var row_data = tableModel.getRowData( row_idx );
          var status = row_data[ this.MAIL_status ];
          
          if( status != 0 && column_idx == this.MAIL_opmerk )
          {
            // copy old remarks
            var cell_data = row_data[ column_idx ];
            console.debug( cell_data );
            var row_num = row_idx + 1;
            this.createWindow2Remarks( row_num, cell_data );
          }
          else  // edit cell ?
          {
            if( tbuttonEdit.getValue() == true && status == 0 )   // row is editable
            {
              
              // but only some columns are editable
              if
              ( column_idx === this.MAIL_datum       ||
                column_idx === this.MAIL_periode     ||
                column_idx === this.MAIL_naamgem     ||
                column_idx === this.MAIL_opmerk      ||
                column_idx === this.MAIL_oppartner   ||
                column_idx === this.MAIL_opvader     ||
                column_idx === this.MAIL_opmoeder    ||
                column_idx === this.MAIL_infoouders  ||
                column_idx === this.MAIL_infopartner ||
                column_idx === this.MAIL_inforeis
              )
              {
                console.debug( "status: " + status + ", cell editable" );
                
                table.resetCellFocus();
                table.setShowCellFocusIndicator( true );
                
                tableModel.setColumnEditable( column_idx, true );
                tsm.setSelectionMode( selModel.SINGLE_SELECTION );
              }
              else { 
                console.debug( "status: " + status + ", cell NOT editable" );
                table.resetCellFocus();
                table.setShowCellFocusIndicator( false );
                tableModel.setEditable( false );
                tsm.setSelectionMode( selModel.NO_SELECTION );
              }
            }
            else { 
              console.debug( "status: " + status + ", row NOT editable" );
              table.resetCellFocus();
              table.setShowCellFocusIndicator( false );
              tableModel.setEditable( false );
              tsm.setSelectionMode( selModel.NO_SELECTION );
            }
          }
        },
        this
      );
      
      
      table.addListener
      (
        "cellDbltap", 
        function( ev ) 
        {
          var row_idx    = ev.getRow();
          var column_idx = ev.getColumn();
          console.debug( "cellDbltap type: " + ev.getType() + ", row: " + row_idx + ", columnn: " + column_idx );
        },
        this
      );
      
      
      // after deselection of selected rows, the last deselected row remained lightblue (i.e. focusline).
      table.highlightFocusedRow( false );
      
      tableModel.setEditable( false );  // editable via button "Bewerken is aan"
      
      var selModel = qx.ui.table.selection.Model;
      var tsm = table.getSelectionModel();
      tsm.setSelectionMode( selModel.NO_SELECTION );
      console.debug( "table getSelectionMode: " + tsm.getSelectionMode() );
      
      tsm.addListener
      (
        "changeSelection", 
        function( ev ) 
        {
        //console.debug( "Listener tsm changeSelection" );
          var selection = [];
          table.getSelectionModel().iterateSelection( function( idx ) {
            selection.push( idx );
          });
          console.debug( "selection: " + selection + ", length: " + selection.length  );
          
          if( selection.length > 0 ) { buttonDelete.setEnabled( true ); }
          else { buttonDelete.setEnabled( false ); }
        }, 
        this
      );
      
      
      var tcm = table.getTableColumnModel();
      var resizeBehavior = tcm.getBehavior();
      
      //preferred column widths
      resizeBehavior.set( this.MAIL_nr,          { width  :"1*", minWidth :  20, maxWidth :  20 } );  //  0 Nr
      resizeBehavior.set( this.MAIL_id,          { width  :"1*", minWidth :  60, maxWidth :  60 } );  //  1 Id
      resizeBehavior.set( this.MAIL_idnr,        { width  :"1*", minWidth :  50, maxWidth :  50 } );  //  2
      resizeBehavior.set( this.MAIL_briefnr,     { width  :"1*", minWidth :  30, maxWidth :  30 } );  //  3
      resizeBehavior.set( this.MAIL_aard,        { width  :"1*", minWidth :  40, maxWidth :  40 } );  //  4 Aard
      resizeBehavior.set( this.MAIL_datum,       { width  :"1*", minWidth :  70, maxWidth :  70 } );  //  5 Datum
      resizeBehavior.set( this.MAIL_periode,     { width  :"1*", minWidth :  80, maxWidth :  80 } );  //  6 Periode
      resizeBehavior.set( this.MAIL_gemnr,       { width  :"1*", minWidth :  40, maxWidth :  40 } );  //  7 GemeenteNr
      resizeBehavior.set( this.MAIL_naamgem,     { width  :"1*", minWidth : 100                 } );  //  8 Gemeente
      resizeBehavior.set( this.MAIL_status,      { width  :"1*", minWidth :  50, maxWidth :  50 } );  //  9 Status
      resizeBehavior.set( this.MAIL_printdatum,  { width  :"1*", minWidth :  70, maxWidth :  70 } );  // 10 PrintDatum
      resizeBehavior.set( this.MAIL_printen,     { width  :"1*", minWidth :  30, maxWidth :  30 } );  // 11
      resizeBehavior.set( this.MAIL_ontvdat,     { width  :"1*", minWidth :  70, maxWidth :  70 } );  // 12 
      resizeBehavior.set( this.MAIL_opmerk,      { width  :"1*", minWidth : 100 } );                  // 13 Opmerkingen
      resizeBehavior.set( this.MAIL_opident,     { width  :"1*", minWidth : 100 } );                  // 14 
      resizeBehavior.set( this.MAIL_oppartner,   { width  :"1*", minWidth : 100 } );                  // 15
      resizeBehavior.set( this.MAIL_opvader,     { width  :"1*", minWidth : 100 } );                  // 16
      resizeBehavior.set( this.MAIL_opmoeder,    { width  :"1*", minWidth : 100 } );                  // 17
      resizeBehavior.set( this.MAIL_type,        { width  :"1*", minWidth :  40, maxWidth :  40 } );  // 18 Type
      resizeBehavior.set( this.MAIL_infoouders,  { width  :"1*", minWidth :  30, maxWidth :  30 } );  // 19 
      resizeBehavior.set( this.MAIL_infopartner, { width  :"1*", minWidth :  30, maxWidth :  30 } );  // 20
      resizeBehavior.set( this.MAIL_inforeis,    { width  :"1*", minWidth :  30, maxWidth :  30 } );  // 21
      
      // default visibility
    //tcm.setColumnVisible( this.MAIL_nr,          false );  //  0,
    //tcm.setColumnVisible( this.MAIL_id,          false );  //  1,
    //tcm.setColumnVisible( this.MAIL_idnr,        false );  //  2,
      tcm.setColumnVisible( this.MAIL_briefnr,     false );  //  3,
    //tcm.setColumnVisible( this.MAIL_aard,        false );  //  4,
    //tcm.setColumnVisible( this.MAIL_datum,       false );  //  5,
    //tcm.setColumnVisible( this.MAIL_periode,     false );  //  6,
      tcm.setColumnVisible( this.MAIL_gemnr,       false );  //  7,
    //tcm.setColumnVisible( this.MAIL_naamgem,     false );  //  8,
    //tcm.setColumnVisible( this.MAIL_status,      false );  //  9,
    //tcm.setColumnVisible( this.MAIL_printdatum,  false );  // 10,
      tcm.setColumnVisible( this.MAIL_printen,     false );  // 11,
      tcm.setColumnVisible( this.MAIL_ontvdat,     false );  // 12,
    //tcm.setColumnVisible( this.MAIL_opmerk,      false );  // 13,
    //tcm.setColumnVisible( this.MAIL_opident,     false );  // 14,
    //tcm.setColumnVisible( this.MAIL_oppartner,   false );  // 15,
    //tcm.setColumnVisible( this.MAIL_opvader,     false );  // 16,
    //tcm.setColumnVisible( this.MAIL_opmoeder,    false );  // 17,
    //tcm.setColumnVisible( this.MAIL_type,        false );  // 18,
    //tcm.setColumnVisible( this.MAIL_infoouders,  false );  // 19,
    //tcm.setColumnVisible( this.MAIL_infopartner, false );  // 20,
    //tcm.setColumnVisible( this.MAIL_inforeis,    false );  // 21,
      
      // Buttons container: Bekijk meer/minder, Bewerken is aan/uit, Verwijder regel(s), Opslaan
      var layoutButtons = new qx.ui.layout.HBox( 5 ).set({ AlignX : "right" });
      var containerButtons = new qx.ui.container.Composite( layoutButtons );
      containerRequests.add( containerButtons );
      
      
      var tbuttonView = new qx.ui.form.ToggleButton( "Bekijk meer" );
      containerButtons.add( tbuttonView );
      
      tbuttonView.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
          var value = tbuttonView.getValue();
          if( value == true ) 
          {
            tbuttonView.setLabel( "Bekijk minder" );
            
            // more visibility
            tcm.setColumnVisible( this.MAIL_nr,          true );  //  0,
            tcm.setColumnVisible( this.MAIL_id,          true );  //  1,
            tcm.setColumnVisible( this.MAIL_idnr,        true );  //  2,
            tcm.setColumnVisible( this.MAIL_briefnr,     true );  //  3,
            tcm.setColumnVisible( this.MAIL_aard,        true );  //  4,
            tcm.setColumnVisible( this.MAIL_datum,       true );  //  5,
            tcm.setColumnVisible( this.MAIL_periode,     true );  //  6,
            tcm.setColumnVisible( this.MAIL_gemnr,       true );  //  7,
            tcm.setColumnVisible( this.MAIL_naamgem,     true );  //  8,
            tcm.setColumnVisible( this.MAIL_status,      true );  //  9,
            tcm.setColumnVisible( this.MAIL_printdatum,  true );  // 10,
            tcm.setColumnVisible( this.MAIL_printen,     true );  // 11,
            tcm.setColumnVisible( this.MAIL_ontvdat,     true );  // 12,
            tcm.setColumnVisible( this.MAIL_opmerk,      true );  // 13,
            tcm.setColumnVisible( this.MAIL_opident,     true );  // 14,
            tcm.setColumnVisible( this.MAIL_oppartner,   true );  // 15,
            tcm.setColumnVisible( this.MAIL_opvader,     true );  // 16,
            tcm.setColumnVisible( this.MAIL_opmoeder,    true );  // 17,
            tcm.setColumnVisible( this.MAIL_type,        true );  // 18,
            tcm.setColumnVisible( this.MAIL_infoouders,  true );  // 19,
            tcm.setColumnVisible( this.MAIL_infopartner, true );  // 20,
            tcm.setColumnVisible( this.MAIL_inforeis,    true );  // 21,
          }
          else 
          {
            tbuttonView.setLabel( "Bekijk meer" );
            
            // less visibility
            tcm.setColumnVisible( this.MAIL_nr,          true  );  //  0,
            tcm.setColumnVisible( this.MAIL_id,          true  );  //  1,
            tcm.setColumnVisible( this.MAIL_idnr,        true  );  //  2,
            tcm.setColumnVisible( this.MAIL_briefnr,     false );  //  3,
            tcm.setColumnVisible( this.MAIL_aard,        true  );  //  4,
            tcm.setColumnVisible( this.MAIL_datum,       true  );  //  5,
            tcm.setColumnVisible( this.MAIL_periode,     true  );  //  6,
            tcm.setColumnVisible( this.MAIL_gemnr,       false );  //  7,
            tcm.setColumnVisible( this.MAIL_naamgem,     true  );  //  8,
            tcm.setColumnVisible( this.MAIL_status,      true  );  //  9,
            tcm.setColumnVisible( this.MAIL_printdatum,  true  );  // 10,
            tcm.setColumnVisible( this.MAIL_printen,     false );  // 11,
            tcm.setColumnVisible( this.MAIL_ontvdat,     false );  // 12,
            tcm.setColumnVisible( this.MAIL_opmerk,      true  );  // 13,
            tcm.setColumnVisible( this.MAIL_opident,     true  );  // 14,
            tcm.setColumnVisible( this.MAIL_oppartner,   true  );  // 15,
            tcm.setColumnVisible( this.MAIL_opvader,     true  );  // 16,
            tcm.setColumnVisible( this.MAIL_opmoeder,    true  );  // 17,
            tcm.setColumnVisible( this.MAIL_type,        true  );  // 18,
            tcm.setColumnVisible( this.MAIL_infoouders,  true  );  // 19,
            tcm.setColumnVisible( this.MAIL_infopartner, true  );  // 20,
            tcm.setColumnVisible( this.MAIL_inforeis,    true  );  // 21,
          }
        },
        this
      );
      
      
      var tbuttonEdit = new qx.ui.form.ToggleButton( "Bewerken is uit" );
      containerButtons.add( tbuttonEdit );
      
      tbuttonEdit.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
        //console.debug( "Listener tbuttonEdit changeValue" );
          var value = tbuttonEdit.getValue();
          console.debug( "value: " + value );
          
          var selModel = qx.ui.table.selection.Model;
          var tsm = table.getSelectionModel();
          
          if( value == true ) 
          { 
            console.debug( "Bewerken uit -> aan" );
            tbuttonEdit.setLabel( "Bewerken is aan" );
            buttonSave.setEnabled( true );
            
            // make only those columns editable, that are settable by this window
            /*
            tableModel.setColumnEditable( this.MAIL_datum,     true );
            tableModel.setColumnEditable( this.MAIL_periode,   true );
            tableModel.setColumnEditable( this.MAIL_opmerk,    true );
            tableModel.setColumnEditable( this.MAIL_oppartner, true );
            tableModel.setColumnEditable( this.MAIL_opvader,   true );
            tableModel.setColumnEditable( this.MAIL_opmoeder,  true );
            */
            tsm.setSelectionMode( selModel.MULTIPLE_INTERVAL_SELECTION_TOGGLE );
            
            table.resetCellFocus();
            table.setShowCellFocusIndicator( true );
          }
          else if( value == false ) 
          { 
            console.debug( "Bewerken aan -> uit" );
            tbuttonEdit.setLabel( "Bewerken is uit" );
            buttonSave.setEnabled( false );
            
            tableModel.setEditable( false );
            
            tsm.setSelectionMode( selModel.NO_SELECTION );
            
            table.resetCellFocus();
            table.setShowCellFocusIndicator( false );
          }
          console.debug( "table getSelectionMode: " + tsm.getSelectionMode() );
        }, 
        this 
      );
      
      var pk_deleted = [];  // list of pk's (i.e. id) to be deleted
      
      var buttonDelete = new qx.ui.form.Button( "Verwijder regel(s)" ).set({ enabled : false });
      containerButtons.add( buttonDelete );
      
      buttonDelete.addListener
      ( 
        "execute", 
        function( ev ) 
        {
        //console.debug( "Listener buttonDelete execute" );
          
          var remove = [];
          // unshift (i.e. push to begin) instead of push (to end)
          table.getSelectionModel().iterateSelection( function( idx ) { remove.unshift( idx );});
          
          // reset the selection before deleting the rows!, otherwise 'undefined' in Qooxdoo Model.js
          var tsm = table.getSelectionModel();
          tsm.resetSelection();
          
          var tableModel = table.getTableModel();
          var ndeleted = 0;
          
          // remove rows from bottom to top (see unshift above) !
          for( var r = 0; r < remove.length; r++ ) 
          {
            var row_idx = remove[ r ].valueOf();
            var row_num = row_idx + 1;
            var row_data = tableModel.getRowData( row_idx );
          //console.debug( "idx: " + row_idx + " (#: " + row_num + ")" );
          //console.debug( row_data );
            var status = row_data[ this.MAIL_status ];
            
            if( status == 0 ) {
              var id = row_data[ this.MAIL_id ];
              pk_deleted.push( id );
              ndeleted++;
              tableModel.removeRows( row_idx, 1 );
              console.debug( "Deleted idx: " + row_idx + " (#: " + row_num + ")" + ", id: " + id );
            } 
            else {
              console.debug( "NOT Deleting  idx: " + row_idx + " (#: " + row_num + ")" + ", id: " + id );
              var msg = "Regel # " + row_num + " zal NIET worden verwijderd<br>Status = " + status;
              this.showDialog( msg );
            }
          }
          
          console.debug( "Deleted " + ndeleted + " rows, pk_deleted: " + pk_deleted );
        },
        this
      );
      
      
      // VBox row 3 : Save, Cancel
      //console.debug( "VBox row 3: Save, Cancel" );
      var layoutSaveCancel = new qx.ui.layout.HBox( 5 ).set({ AlignX : "right" });
      var containerSaveCancel = new qx.ui.container.Composite( layoutSaveCancel );
      window.add( containerSaveCancel );
      
      var buttonCancel = new qx.ui.form.Button( "Annuleren" );
      containerSaveCancel.add( buttonCancel );
      
      buttonCancel.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Annuleren" );
          var legend = "Eventuele wijzigingen zullen <b>niet</b> worden opgeslagen.<br>Akkoord?";
          this.closeWindow( window, "Annuleren", legend );
          //window.close();
        },
        this
      );
      
      var buttonSave = new qx.ui.form.Button( "Opslaan" ).set({ enabled : false });
      containerSaveCancel.add( buttonSave );
    
      buttonSave.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Opslaan" );
          
          tbuttonEdit.setValue( false );
          tbuttonEdit.setLabel( "Bewerken is uit" );
          
          console.debug( "pk_deleted: " + pk_deleted );
          
          // Save the rows of table mail bev that are new (no pk) or have changed
          var table_data = tableModel.getData();
          var nrows = table_data.length;
          console.debug( "table data rows: " + table_data.length );
          var rows = [];
          
          for( var r = 0; r < nrows; r++ ) 
          {
            var row_data = table_data[ r ];
            console.debug( row_data );
            var id = row_data[ this.MAIL_id ];
            
            if( id === "" || pk_changed.indexOf( id ) != -1 ) 
            {
              var row = new Object();
              // only save the columns that are filled (or fillable) by "Mail toevoegen", 
              // but plus pk id for updates and deletes
              row.id           = row_data[ this.MAIL_id ];
              row.idnr         = row_data[ this.MAIL_idnr ];
              row.kind         = row_data[ this.MAIL_aard ];
              row.date         = row_data[ this.MAIL_datum ];
              row.period       = row_data[ this.MAIL_periode ];
              row.location_nr  = row_data[ this.MAIL_gemnr ];
              row.location     = row_data[ this.MAIL_naamgem ];
              row.status       = row_data[ this.MAIL_status ];
              row.remarks      = row_data[ this.MAIL_opmerk ];
              row.op_ident     = row_data[ this.MAIL_opident ];
              row.op_partner   = row_data[ this.MAIL_oppartner ];
              row.op_father    = row_data[ this.MAIL_opvader ];
              row.op_mother    = row_data[ this.MAIL_opmoeder ];
              row.type         = row_data[ this.MAIL_type ];
              row.info_parents = row_data[ this.MAIL_infoouders ];
              row.info_partner = row_data[ this.MAIL_infopartner ];
              row.info_journey = row_data[ this.MAIL_inforeis ];
              
              rows.push( row );
              console.debug( row );
            }
          }
          
          // We send the op_num separately; in case we are sending an empty table, 
          // we then still know for which OP to delete the deleted mail records. 
          var json = new Object();
          json.idnr = this.OP.op_num;
          json.nrows = nrows;
          json.rdata = rows;
          json.pkdeleted = pk_deleted;
          console.debug( json );
          
          var json_str = qx.lang.Json.stringify( json );
          
          var data = new Object();
          data.mailbev = json_str;
          
          pk_changed = [];  // empty array of pk's of rows that have been updated
          pk_deleted = [];  // empty array of pk's that have been deleted
          
          //this.showDialog( "NOT saving table rows<br>(update, create, delete)" );
          this.saveHsnOpData( "/putmailbev", data );
          window.close();
        },
        this
      );
      
      return window;
    }, // createWindow2
    
    
    
    /**
     * createWindow2Remarks
     */
    createWindow2Remarks : function( row_num, text )
    {    
      console.debug( "createWindow2Remarks()" );
      
      if( ! this.__window2Dialog )
      {
        var width = 350;
        var dialog = this.__window2Dialog = new qx.ui.window.Window( "Kopieer opmerking van regel # " + row_num + " ?" )
        .set({
          modal          : true,
          showMinimize   : false,
          showMaximize   : false,
          width          : width,
          contentPadding : [ 10, 10, 10, 10 ]
        });
        dialog.addListener( "resize", dialog.center );
        
        var layout = new qx.ui.layout.Grid( 15, 15 );
        layout.setRowFlex( 0, 1 );
        layout.setColumnFlex( 1, 1 );
        dialog.setLayout( layout );
        
        dialog.add
        (
          new qx.ui.basic.Image( "icon/32/status/dialog-information.png" ),
          { row : 0, column : 0 }
        );
        
        dialog.add
        ( 
          new qx.ui.basic.Label().set({
            rich       : true,
            allowGrowY : true
          }), 
          { row : 0, column : 1, colSpan : 2 }
        );
        
        var layoutButtons = new qx.ui.layout.HBox( 5 ).set({ AlignX : "center" });
        var containerButtons = new qx.ui.container.Composite( layoutButtons );
        dialog.add( containerButtons, { row : 1, column : 1 } );
        
        var buttonOK = new qx.ui.form.Button( "Ja" ).set({
          alignX     : "center",
          allowGrowX : false,
          padding    : [ 2, 10 ]
        });
        
        buttonOK.addListener
        (
          "execute", 
          function( ev ) 
          { 
            dialog.close(); 
            console.debug( "createWindow2Remarks() OK" );
            
            this.__textareaRemarks.setValue( text );
          }, 
          this
        );
        
        
        var buttonCancel = new qx.ui.form.Button( "Nee" ).set({
          alignX     : "center",
          allowGrowX : false,
          padding    : [ 2, 10 ]
        });
        
        buttonCancel.addListener
        (
          "execute", 
          function( ev ) { 
            dialog.close(); 
            console.debug( "createWindow2Remarks() Cancel" );
          }, 
          this
        );
        
        containerButtons.add( buttonCancel );
        containerButtons.add( new qx.ui.core.Spacer( 10 ) );
        containerButtons.add( buttonOK );
      }
      
      this.__window2Dialog.getChildren()[ 1 ].setValue( text );
      this.__window2Dialog.open();
    //this.__window2Dialog.getChildren()[ 2 ].focus();
    }, // createWindow2Remarks
    
    
    
    /**
     * createWindow3
     * Aanmaken mail huwelijksakten
     */
    createWindow3 : function()
    {
      console.debug( "createWindow3()" );
      
      //var wd_width  = this.MAIN_WIDTH;
      //var wd_height = this.MAIN_HEIGHT;
      
      var wd_width  = qx.bom.Viewport.getWidth();   // use whole viewport width
      var wd_height = qx.bom.Viewport.getHeight();  // use whole viewport height
      
      var ct_width  = wd_width - 22;  // 22 = estimated margin
      
      var window = new qx.ui.window.Window( "Aanmaken mail huwelijksakten" );
      window.set({
        width  : wd_width,
        height : wd_height,
        modal  : true
      });
      window.addListener( "resize", window.center );
      window.setLayout( new qx.ui.layout.VBox( 5 ) );
      
      window.addListener
      ( 
        "appear", 
        function( ev ) 
        {
          window.setWidth(  qx.bom.Viewport.getWidth() );
          window.setHeight( qx.bom.Viewport.getHeight() );
          
          // clear data from previous OP
          pk_changed = [];  // empty array of pk's of rows that have been updated
          pk_deleted = [];  // empty array of pk's that have been deleted
          
          var numrows = tableModel.getRowCount();
          tableModel.removeRows( 0, numrows );
          
          textfieldPartnerlastname  .setValue( "" );
          textfieldPartnerfirstnames.setValue( "" );
          
          textfieldMarriage.setValue( "" );
          textfieldPeriod  .setValue( "" );
          
          comboboxLocation   .setValue( "" );
          textfieldLocationNr.setValue( "" );
          
          table.resetCellFocus();
          table.setShowCellFocusIndicator( false );
          tableModel.setEditable( false );
          tsm.setSelectionMode( selModel.NO_SELECTION );
          // ... set default visible columns?
          
          
          // fill the table with "huwelijksakten" mails
          var mails = this.OP.mails.huw;
          var rows = [];
          var nhuw = 0
          
          for( var i = 0; i < mails.length; i++ ) 
          {
            var mail = mails[ i ];
          //console.debug( "i: " + i + " " + mail );
            
            if( mail.type === "HUW" )     // HUWelijksakten
            {
              nhuw++;
              var row = [ 
                nhuw,                           //  0
                mail.id.toString(),             //  1
                mail.idnr.toString(),           //  2
                mail.briefnr.toString(),        //  3
                mail.aard,                      //  4
                mail.datum,                     //  5
                mail.periode,                   //  6
                mail.gemnr.toString(),          //  7
                mail.naamgem,                   //  8
                mail.status,                    //  9
                mail.printdatum,                // 10
                mail.printen,                   // 11
                mail.ontvdat,                   // 12
                mail.opmerk,                    // 13
                mail.opident,                   // 14
                mail.oppartner,                 // 15
                mail.opvader,                   // 16
                mail.opmoeder,                  // 17
                mail.type,                      // 18
                mail.infoouders,                // 19
                mail.infopartner,               // 20
                mail.inforeis                   // 21
              ];
              rows.push( row );
            }
          }
          tableModel.addRows( rows, 0, true );
        },
        this
      );
      
      // VBox row 0 : OP-info
      var layoutOpinfo = new qx.ui.layout.HBox( 10 );    // spacing = 10
      var containerOpinfo = new qx.ui.container.Composite( layoutOpinfo ).set({
        decorator   : "main",
        paddingLeft : 20,
        width       : ct_width,
        allowGrowY  : false
      });
      
      this.labelOpinfo3 = new qx.ui.basic.Label().set({ rich : true });
      containerOpinfo.add( this.labelOpinfo3 );
    //window.add( containerOpinfo, { row : 0, column : 0 } );
      window.add( containerOpinfo );
      
      
      // VBox row 1 : add mail
      var layoutMailadd = new qx.ui.layout.Grid( 5, 5 );
      // make column 3 flexible to get button "Mail toevoegen" at the right border
      layoutMailadd.setColumnFlex( 3, 1 );
      
      var containerMailadd = new qx.ui.container.Composite( layoutMailadd ).set({
        decorator  : "main",
        padding    : 5,
        width      : ct_width,
        height     : 100,
        allowGrowY : false
      });
      window.add( containerMailadd );
      
      
      var labelTry = new qx.ui.basic.Label( "Huwelijksgegevens zo goed mogelijk invullen" );
    //labelTry.setMaxWidth( 400 );
      containerMailadd.add( labelTry, { row : 0, column : 0, colSpan : 2 } );
      
      
      var labelPartnerlastname = new qx.ui.basic.Label( "Achternaam partner:" );
      containerMailadd.add( labelPartnerlastname, { row : 1, column : 0 } );
      
      var textfieldPartnerlastname = new qx.ui.form.TextField().set({ width : 200 });
      containerMailadd.add( textfieldPartnerlastname, { row : 1, column : 1 } );
      
      
      var labelPartnerfirstnames = new qx.ui.basic.Label( "Voornamen partner:" );
      containerMailadd.add( labelPartnerfirstnames, { row : 2, column : 0 } );
      
      var textfieldPartnerfirstnames = new qx.ui.form.TextField().set({ width : 200 });
      containerMailadd.add( textfieldPartnerfirstnames, { row : 2, column : 1 } );
      
      
      var labelMarriagestartdate = new qx.ui.basic.Label( "Datum huwelijk:" );
      containerMailadd.add( labelMarriagestartdate, { row : 3, column : 0 } );
      
      var layoutDates = new qx.ui.layout.HBox( 5 ).set({ alignY : "middle" });
      var containerDates = new qx.ui.container.Composite( layoutDates );
      
      var textfieldMarriage = new qx.ui.form.TextField().set({ width : 200, placeholder : "DD/MM/JJJJ", textAlign : "left", enabled : true });
      containerDates.add( textfieldMarriage );
      
      containerDates.add( new qx.ui.core.Spacer( 25 ) );
      
      var labelMarriageenddate = new qx.ui.basic.Label( "of periode huwelijk:" );
      containerDates.add( labelMarriageenddate );
      
    //var datefieldMarriageend = new qx.ui.form.DateField();
    //containerDates.add( datefieldMarriageend );
      
      var textfieldPeriod = new qx.ui.form.TextField().set({ width : 200, placeholder : "JJJJ-JJJJ",  textAlign : "left", enabled : true });
      containerDates.add( textfieldPeriod );

      containerMailadd.add( containerDates, { row : 3, column : 1, colSpan : 3 } );
      
      var labelLocation = new qx.ui.basic.Label( "Gemeente:" );
      containerMailadd.add( labelLocation, { row : 4, column : 0 } );
      
      var layoutLocation = new qx.ui.layout.HBox( 5 ).set({ alignY : "middle" });
      var containerLocation = new qx.ui.container.Composite( layoutLocation );
      
      // ComboTable is a combination of a ComboBox and a Table for autocompletion
      var combotable_model = new combotable.SearchableModel();
      combotable_model.setColumns( ['Id','Data'], ['id','data'] );
      combotable_model.setData( this.location_array );
      
      var comboboxLocation = new combotable.ComboTable( combotable_model ).set({
          width       : 200,
          placeholder : 'Gemeente'
      });
      containerLocation.add( comboboxLocation );
      
      comboboxLocation.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
          var location_value = comboboxLocation.getValue();
          var location_nr = this.location2nr( location_value );
          
          console.debug( "location_value: " + location_value + ", location_nr: " + location_nr );
          textfieldLocationNr.setValue( location_nr.toString() );   // use proper upper-/lowercase string
        },
        this
      );
      
      
      containerLocation.add( new qx.ui.core.Spacer( 23 ) );
      
      // gemnr not needed in GUI (-> invisible), but needed server-side
      var labelLocationNr = new qx.ui.basic.Label( "Gemeente Nr:" ).set({ visibility: false });
      containerLocation.add( labelLocationNr );
      
      containerLocation.add( new qx.ui.core.Spacer( 25 ) );
      
      var textfieldLocationNr = new qx.ui.form.TextField()
      .set({
        width     : 50,
        enabled   : false,
        visibility: false
      });
      containerLocation.add( textfieldLocationNr );
      
      containerMailadd.add( containerLocation, { row : 4, column : 1, colSpan : 3 } );
      
      
      var layoutBtnAdd = new qx.ui.layout.HBox().set({ AlignX : "right" });
      var containerBtnAdd = new qx.ui.container.Composite( layoutBtnAdd );
      
      var buttonAdd = new qx.ui.form.Button( "Mail toevoegen" );
      containerBtnAdd.add( buttonAdd );
      
      containerMailadd.add( containerBtnAdd, { row : 5, column : 3 } );
      
      buttonAdd.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Window 3: Mail toevoegen" );
          buttonSave.setEnabled( true );
          
          var op_partnerlastname   = textfieldPartnerlastname  .getValue();
          var op_partnerfirstnames = textfieldPartnerfirstnames.getValue();
          
          var date   = textfieldMarriage.getValue();
          var period = textfieldPeriod  .getValue();
          
          var location    = comboboxLocation   .getValue();
          var location_nr = textfieldLocationNr.getValue();
          
          var numrows = tableModel.getRowCount();
          var status  = 0;    // initially
          
          var op_ident = "";
          for( var i = 0; i < this.OP.op_info_list.length; i++ )
          {
            var op_info = this.OP.op_info_list[ i ];
            if( op_info.id_origin == 10 )   // birth op_info
            {
              op_ident = op_info.rp_family;
              if( op_info.rp_prefix != "" ) { op_ident += ", " + op_info.rp_prefix; }
              op_ident += ", " + op_info.rp_firstname;
              op_ident += " [" + op_info.rp_b_sex + "]";
              op_ident += ", geboren";
              op_ident += " " + op_info.rp_b_date;
              op_ident += " te";
              op_ident += " " + op_info.rp_b_place;
            }
          }
          
          var op_partner = op_partnerlastname + ", " + op_partnerfirstnames;
          
          var kind = "B"    // B, F, W ?
          var type = "HUW";
          
          var row = [ 
            numrows + 1,            //  0 #
            "",                     //  1 id
            this.OP.op_num,         //  2 idnr
            "",                     //  3 briefnr
            kind,                   //  4 aard
            date,                   //  5 datum
            period,                 //  6 periode
            location_nr,            //  7 gemnr
            location,               //  8 naamgem
            status,                 //  9 status
            "",                     // 10 printdatum
            "",                     // 11 printen
            "",                     // 12 ontvdat
            "",                     // 13 opmerk
            op_ident,               // 14 opident
            op_partner,             // 15 ppartner
            "",                     // 16 opvader
            "",                     // 17 opmoeder
            type,                   // 18 type
            "",                     // 19 infoouders
            "",                     // 20 infopartner
            ""                      // 21 inforeis
          ];
          
          var rows = [];
          rows.push( row );
          var clearSorting = false;
          tableModel.addRows( rows, numrows, clearSorting );
          
          // clear fields for possible next mail
          textfieldPartnerlastname  .setValue( "" );
          textfieldPartnerfirstnames.setValue( "" );
          textfieldMarriage         .setValue( "" );
          textfieldPeriod           .setValue( "" );
          textfieldLocationNr       .setValue( "" );
          comboboxLocation          .setValue( "" );
        },
        this
      );

      
      // VBox row 2 : marriages
      var layoutMarriages = new qx.ui.layout.VBox( 5 );
      var containerMarriages = new qx.ui.container.Composite( layoutMarriages ).set({
        decorator  : "main",
        padding    : 5,
        width      : ct_width,
        height     : 100,
        allowGrowX : true,
        allowGrowY : true
      });
      window.add( containerMarriages, { flex : 1 } );
      
      var tableModel = this._tableModel = new qx.ui.table.model.Simple();
      var column_names = [
          "#",
          "Id",
          "Id Nr",
          "Brief Nr",
          "Aard",
          "Datum",
          "Periode",
          "Gemeente Nr",
          "Gemeente",
          "Status",
          "Print Datum",
          "Printen",
          "Ontvang Datum",
          "Opmerkingen",
          "OP Ident",
          "OP Partner",
          "OP Vader",
          "OP Moeder",
          "Type",
          "Info Ouders",
          "Info Partner",
          "Info Reis"
      ];
      tableModel.setColumns( column_names );
      
      // Customize the table column model. We want one that automatically resizes columns.
      var custom = { tableColumnModel : function( obj ) { return new qx.ui.table.columnmodel.Resize( obj ); } };
      
      var table = new qx.ui.table.Table( tableModel, custom );
      table.set({
        decorator        : "main",
        statusBarVisible : false,       // statusbar at bottom
        width            : ct_width,
        height           : 100,
        allowGrowX       : true,
        allowGrowY       : true
      });
      containerMarriages.add( table, { flex : 1 } );
      
      var pk_changed = [];  // list of pk's (i.e. id) of rows to be updated
      
      table.addListener
      ( 
        "dataEdited", 
        function( ev ) 
        {
          console.debug( "dataEdited: " );
          var data = ev.getData();
          var row_data = tableModel.getRowData( data.row );
          var id = row_data[ this.MAIL_id ];
          console.debug( "row idx: " + data.row + ", col idx: " + data.col + ", oldValue: " + 
            data.oldValue + ", value: " + data.value + ", id: " + id );
          pk_changed.push( id );
          
          table.resetCellFocus();
          table.setShowCellFocusIndicator( false );
          tableModel.setEditable( false );
          tsm.setSelectionMode( selModel.NO_SELECTION );
        },
        this
      );
      
      
      table.addListener
      (
        "cellTap", 
        function( ev ) 
        {
          var row_idx    = ev.getRow();
          var column_idx = ev.getColumn();
          console.debug( "cellTap type: " + ev.getType() + ", row: " + row_idx + ", columnn: " + column_idx );
          
          var row_data = tableModel.getRowData( row_idx );
          
          if( column_idx == this.MAIL_opmerk ) {
            
            var cell_data = row_data[ column_idx ];
            console.debug( cell_data );
            var row_num = row_idx + 1;
            this.createWindow2Remarks( row_num, cell_data );
          }
          else  // edit cell ?
          {
            var status = row_data[ this.MAIL_status ];
            if( tbuttonEdit.getValue() == true && status == 0 )   // row is editable
            {
              
              // but only some columns are editable
              if( column_idx === this.MAIL_datum   ||
                column_idx === this.MAIL_periode   ||
                column_idx === this.MAIL_naamgem   ||
                column_idx === this.MAIL_oppartner )
              {
                console.debug( "status: " + status + ", column editable" );
                
                table.resetCellFocus();
                table.setShowCellFocusIndicator( true );
                
                tableModel.setColumnEditable( column_idx, true );
                tsm.setSelectionMode( selModel.SINGLE_SELECTION );
              }
              else { 
                console.debug( "status: " + status + ", column NOT editable" );
                table.resetCellFocus();
                table.setShowCellFocusIndicator( false );
                tableModel.setEditable( false );
                tsm.setSelectionMode( selModel.NO_SELECTION );
              }
            }
            else { 
              console.debug( "status: " + status + ", row NOT editable" );
              table.resetCellFocus();
              table.setShowCellFocusIndicator( false );
              tableModel.setEditable( false );
              tsm.setSelectionMode( selModel.NO_SELECTION );
            }
          }
        },
        this
      );
      
      
      table.addListener
      (
        "cellDbltap", 
        function( ev ) 
        {
          var row_idx    = ev.getRow();
          var column_idx = ev.getColumn();
          console.debug( "cellDbltap type: " + ev.getType() + ", row: " + row_idx + ", columnn: " + column_idx );
        },
        this
      );
      
      
      // after deselection of selected rows, the last deselected row remained lightblue (i.e. focusline).
      table.highlightFocusedRow( false );
      
      var selModel = qx.ui.table.selection.Model;
      var tsm = table.getSelectionModel();
      tsm.setSelectionMode( selModel.NO_SELECTION );
      console.debug( "table getSelectionMode: " + tsm.getSelectionMode() );
      
      tsm.addListener
      (
        "changeSelection", 
        function( ev ) 
        {
        //console.debug( "Listener tsm changeSelection" );
          var selection = [];
          table.getSelectionModel().iterateSelection( function( idx ) {
            selection.push( idx );
          });
          console.debug( "selection: " + selection + ", length: " + selection.length  );
          
          if( selection.length > 0 ) { buttonDelete.setEnabled( true ); }
          else { buttonDelete.setEnabled( false ); }
        }, 
        this
      );
      
      
      var tcm = table.getTableColumnModel();      
      var resizeBehavior = tcm.getBehavior();
      
      //preferred column widths
      resizeBehavior.set( this.MAIL_nr,          { width  :"1*", minWidth :  20, maxWidth :  20 } );  //  0 Nr
      resizeBehavior.set( this.MAIL_id,          { width  :"1*", minWidth :  60, maxWidth :  60 } );  //  1 Id
      resizeBehavior.set( this.MAIL_idnr,        { width  :"1*", minWidth :  50, maxWidth :  50 } );  //  2
      resizeBehavior.set( this.MAIL_briefnr,     { width  :"1*", minWidth :  30, maxWidth :  30 } );  //  3
      resizeBehavior.set( this.MAIL_aard,        { width  :"1*", minWidth :  40, maxWidth :  40 } );  //  4 Aard
      resizeBehavior.set( this.MAIL_datum,       { width  :"1*", minWidth :  70, maxWidth :  70 } );  //  5 Datum
      resizeBehavior.set( this.MAIL_periode,     { width  :"1*", minWidth :  80, maxWidth :  80 } );  //  6 Periode
      resizeBehavior.set( this.MAIL_gemnr,       { width  :"1*", minWidth :  40, maxWidth :  40 } );  //  7 GemeenteNr
      resizeBehavior.set( this.MAIL_naamgem,     { width  :"1*", minWidth : 100                 } );  //  8 Gemeente
      resizeBehavior.set( this.MAIL_status,      { width  :"1*", minWidth :  50, maxWidth :  50 } );  //  9 Status
      resizeBehavior.set( this.MAIL_printdatum,  { width  :"1*", minWidth :  70, maxWidth :  70 } );  // 10 PrintDatum
      resizeBehavior.set( this.MAIL_printen,     { width  :"1*", minWidth :  30, maxWidth :  30 } );  // 11
      resizeBehavior.set( this.MAIL_ontvdat,     { width  :"1*", minWidth :  70, maxWidth :  70 } );  // 12 
      resizeBehavior.set( this.MAIL_opmerk,      { width  :"1*", minWidth : 100 } );                  // 13 Opmerkingen
      resizeBehavior.set( this.MAIL_opident,     { width  :"1*", minWidth : 100 } );                  // 14 
      resizeBehavior.set( this.MAIL_oppartner,   { width  :"1*", minWidth : 100 } );                  // 15
      resizeBehavior.set( this.MAIL_opvader,     { width  :"1*", minWidth : 100 } );                  // 16
      resizeBehavior.set( this.MAIL_opmoeder,    { width  :"1*", minWidth : 100 } );                  // 17
      resizeBehavior.set( this.MAIL_type,        { width  :"1*", minWidth :  40, maxWidth :  40 } );  // 18 Type
      resizeBehavior.set( this.MAIL_infoouders,  { width  :"1*", minWidth :  30, maxWidth :  30 } );  // 19 
      resizeBehavior.set( this.MAIL_infopartner, { width  :"1*", minWidth :  30, maxWidth :  30 } );  // 20
      resizeBehavior.set( this.MAIL_inforeis,    { width  :"1*", minWidth :  30, maxWidth :  30 } );  // 21
      
      // default visibility
    //tcm.setColumnVisible( this.MAIL_nr,          false );  //  0,
    //tcm.setColumnVisible( this.MAIL_id,          false );  //  1,
    //tcm.setColumnVisible( this.MAIL_idnr,        false );  //  2,
      tcm.setColumnVisible( this.MAIL_briefnr,     false );  //  3,
    //tcm.setColumnVisible( this.MAIL_aard,        false );  //  4,
    //tcm.setColumnVisible( this.MAIL_datum,       false );  //  5,
    //tcm.setColumnVisible( this.MAIL_periode,     false );  //  6,
      tcm.setColumnVisible( this.MAIL_gemnr,       false );  //  7,
    //tcm.setColumnVisible( this.MAIL_naamgem,     false );  //  8,
    //tcm.setColumnVisible( this.MAIL_status,      false );  //  9,
    //tcm.setColumnVisible( this.MAIL_printdatum,  false );  // 10,
      tcm.setColumnVisible( this.MAIL_printen,     false );  // 11,
      tcm.setColumnVisible( this.MAIL_ontvdat,     false );  // 12,
      tcm.setColumnVisible( this.MAIL_opmerk,      false );  // 13,
    //tcm.setColumnVisible( this.MAIL_opident,     false );  // 14,
    //tcm.setColumnVisible( this.MAIL_oppartner,   false );  // 15,
      tcm.setColumnVisible( this.MAIL_opvader,     false );  // 16,
      tcm.setColumnVisible( this.MAIL_opmoeder,    false );  // 17,
    //tcm.setColumnVisible( this.MAIL_type,        false );  // 19,
      tcm.setColumnVisible( this.MAIL_infoouders,  false );  // 20,
      tcm.setColumnVisible( this.MAIL_infopartner, false );  // 21,
      tcm.setColumnVisible( this.MAIL_inforeis,    false );  // 22
      
      
      // Buttons container: Bekijk meer/minder, Bewerken is aan/uit, Verwijder regel(s), Opslaan
      var layoutButtons = new qx.ui.layout.HBox( 5 ).set({ AlignX : "right" });
      var containerButtons = new qx.ui.container.Composite( layoutButtons );
      containerMarriages.add( containerButtons );
      
      
      var tbuttonView = new qx.ui.form.ToggleButton( "Bekijk meer" );
      containerButtons.add( tbuttonView );
      
      tbuttonView.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
          var value = tbuttonView.getValue();
          if( value == true ) 
          {
            tbuttonView.setLabel( "Bekijk minder" );
            
            // more visibility
            tcm.setColumnVisible( this.MAIL_nr,                   true );  //  0,
            tcm.setColumnVisible( this.MAIL_id,                   true );  //  1,
            tcm.setColumnVisible( this.MAIL_idnr,                 true );  //  2,
            tcm.setColumnVisible( this.MAIL_briefnr,              true );  //  3,
            tcm.setColumnVisible( this.MAIL_aard,        true );  //  4,
            tcm.setColumnVisible( this.MAIL_datum,       true );  //  5,
            tcm.setColumnVisible( this.MAIL_periode,     true );  //  6,
            tcm.setColumnVisible( this.MAIL_gemnr,       true );  //  7,
            tcm.setColumnVisible( this.MAIL_naamgem,     true );  //  8,
            tcm.setColumnVisible( this.MAIL_status,      true );  //  9,
            tcm.setColumnVisible( this.MAIL_printdatum,  true );  // 10,
            tcm.setColumnVisible( this.MAIL_printen,     true );  // 11,
            tcm.setColumnVisible( this.MAIL_ontvdat,     true );  // 12,
            tcm.setColumnVisible( this.MAIL_opmerk,      true );  // 13,
            tcm.setColumnVisible( this.MAIL_opident,     true );  // 14,
            tcm.setColumnVisible( this.MAIL_oppartner,   true );  // 15,
            tcm.setColumnVisible( this.MAIL_opvader,     true );  // 16,
            tcm.setColumnVisible( this.MAIL_opmoeder,    true );  // 17,
            tcm.setColumnVisible( this.MAIL_type,        true );  // 18,
            tcm.setColumnVisible( this.MAIL_infoouders,  true );  // 19,
            tcm.setColumnVisible( this.MAIL_infopartner, true );  // 20,
            tcm.setColumnVisible( this.MAIL_inforeis,    true );  // 21
          }
          else 
          {
            tbuttonView.setLabel( "Bekijk meer" );
            
            // less visibility
            tcm.setColumnVisible( this.MAIL_nr,          true  );  //  0,
            tcm.setColumnVisible( this.MAIL_id,          true  );  //  1,
            tcm.setColumnVisible( this.MAIL_idnr,        true  );  //  2,
            tcm.setColumnVisible( this.MAIL_briefnr,     false );  //  3,
            tcm.setColumnVisible( this.MAIL_aard,        true  );  //  4,
            tcm.setColumnVisible( this.MAIL_datum,       true  );  //  5,
            tcm.setColumnVisible( this.MAIL_periode,     true  );  //  6,
            tcm.setColumnVisible( this.MAIL_gemnr,       false );  //  7,
            tcm.setColumnVisible( this.MAIL_naamgem,     true  );  //  8,
            tcm.setColumnVisible( this.MAIL_status,      true  );  //  9,
            tcm.setColumnVisible( this.MAIL_printdatum,  true  );  // 10,
            tcm.setColumnVisible( this.MAIL_printen,     false );  // 11,
            tcm.setColumnVisible( this.MAIL_ontvdat,     false );  // 12,
            tcm.setColumnVisible( this.MAIL_opmerk,      false );  // 13,
            tcm.setColumnVisible( this.MAIL_opident,     true  );  // 14,
            tcm.setColumnVisible( this.MAIL_oppartner,   true  );  // 15,
            tcm.setColumnVisible( this.MAIL_opvader,     false );  // 16,
            tcm.setColumnVisible( this.MAIL_opmoeder,    false );  // 17,
            tcm.setColumnVisible( this.MAIL_type,        true  );  // 18,
            tcm.setColumnVisible( this.MAIL_infoouders,  false );  // 19,
            tcm.setColumnVisible( this.MAIL_infopartner, false );  // 20,
            tcm.setColumnVisible( this.MAIL_inforeis,    false );  // 21,
          }
        },
        this
      );
      
      
      var tbuttonEdit = new qx.ui.form.ToggleButton( "Bewerken is uit" ).set({ value : false });
      containerButtons.add( tbuttonEdit );
      
      tbuttonEdit.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
        //console.debug( "Listener tbuttonEdit changeValue" );
          var value = tbuttonEdit.getValue();
          console.debug( "value: " + value );
          
          var model = qx.ui.table.selection.Model;
          var tsm = table.getSelectionModel();
          
          if( value == true ) 
          { 
            console.debug( "Bewerken uit -> aan" );
            tbuttonEdit.setLabel( "Bewerken is aan" );
            buttonSave.setEnabled( true );
            
            // make only those columns editable, that are settable by this window
            tableModel.setColumnEditable( this.MAIL_datum,     true );
            tableModel.setColumnEditable( this.MAIL_periode,   true );
          //tableModel.setColumnEditable( this.MAIL_opmerk,    true );
            tableModel.setColumnEditable( this.MAIL_oppartner, true );
          //tableModel.setColumnEditable( this.MAIL_opvader,   true );
          //tableModel.setColumnEditable( this.MAIL_opmoeder,  true );
            
            tsm.setSelectionMode( model.MULTIPLE_INTERVAL_SELECTION_TOGGLE );
            
            table.resetCellFocus();
            table.setShowCellFocusIndicator( true );
          }
          else if( value == false ) 
          { 
            console.debug( "Bewerken aan -> uit" );
            tbuttonEdit.setLabel( "Bewerken is uit" );
            buttonSave.setEnabled( false );
            
            tableModel.setEditable( false );
            
            tsm.setSelectionMode( model.NO_SELECTION );
            
            table.resetCellFocus();
            table.setShowCellFocusIndicator( false );
          }
          console.debug( "table getSelectionMode: " + tsm.getSelectionMode() );
        }, 
        this 
      );
      
      var pk_deleted = [];  // list of pk's (i.e. id) to be deleted
      
      var buttonDelete = new qx.ui.form.Button( "Verwijder regel(s)" ).set({ enabled : false });
      containerButtons.add( buttonDelete );
      
      buttonDelete.addListener
      ( 
        "execute", 
        function( ev ) 
        {
        //console.debug( "Listener buttonDelete execute" );
          
          var remove = [];
          // unshift (i.e. push to begin) instead of push (to end)
          table.getSelectionModel().iterateSelection( function( idx ) { remove.unshift( idx );});
          
          // reset the selection before deleting the rows!, otherwise 'undefined' in Qooxdoo Model.js
          var tsm = table.getSelectionModel();
          tsm.resetSelection();
          
          var tableModel = table.getTableModel();
          var ndeleted = 0;
          
          // remove rows from bottom to top (see unshift above) !
          for( var r = 0; r < remove.length; r++ ) 
          {
            var row_idx = remove[ r ].valueOf();
            var row_num = row_idx + 1;
            var row_data = tableModel.getRowData( row_idx );
          //console.debug( "idx: " + row_idx + " (#: " + row_num + ")" );
          //console.debug( row_data );
            var status = row_data[ this.MAIL_status ];
            
            if( status == 0 ) {
              var id = row_data[ this.MAIL_id ];
              pk_deleted.push( id );
              ndeleted++;
              tableModel.removeRows( row_idx, 1 );
              console.debug( "Deleted idx: " + row_idx + " (#: " + row_num + ")" + ", id: " + id );
            }
            else {
              console.debug( "NOT Deleting  idx: " + row_idx + " (#: " + row_num + ")" + ", id: " + id );
              var msg = "Regel # " + row_num + " zal NIET worden verwijderd<br>Status = " + status;
              this.showDialog( msg );
            }
          }
          
          console.debug( "Deleted " + ndeleted + " rows, pk_deleted: " + pk_deleted );
        },
        this
      );
      
      
      // VBox row 3 : Save, Cancel
      var layoutSaveCancel = new qx.ui.layout.HBox( 5 ).set({ AlignX : "right" });
      var containerSaveCancel = new qx.ui.container.Composite( layoutSaveCancel );
      window.add( containerSaveCancel );
      
      var buttonCancel = new qx.ui.form.Button( "Annuleren" );
      containerSaveCancel.add( buttonCancel );
      
      buttonCancel.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Annuleren" );
          var legend = "Eventuele wijzigingen zullen <b>niet</b> worden opgeslagen.<br>Akkoord?";
          this.closeWindow( window, "Annuleren", legend );
          //window.close();
        },
        this
      );
      
      var buttonSave = new qx.ui.form.Button( "Opslaan" ).set({ enabled : false });
      containerSaveCancel.add( buttonSave );
      
      buttonSave.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Opslaan" );
          
          tbuttonEdit.setValue( false );
          tbuttonEdit.setLabel( "Bewerken is uit" );
          
          console.debug( "pk_deleted: " + pk_deleted );
          
          // Save the rows of table mail bev that are new (no pk) or have changed
          var table_data = tableModel.getData();
          var nrows = table_data.length;
          console.debug( "table data rows: " + table_data.length );
          var rows = [];
          
          for( var r = 0; r < nrows; r++ ) 
          {
            var row_data = table_data[ r ];
            console.debug( row_data );
            var id = row_data[ this.MAIL_id ];
            
            if( id === "" || pk_changed.indexOf( id ) != -1 ) 
            {
              var row = new Object();
              // only save the columns that are filled (or fillable) by "Mail toevoegen", 
              // but plus pk id for updates and deletes
              row.id          = row_data[ this.MAIL_id ];
              row.idnr        = row_data[ this.MAIL_idnr ];
              row.kind        = row_data[ this.MAIL_aard ];
              row.date        = row_data[ this.MAIL_datum ];
              row.period      = row_data[ this.MAIL_periode ];
              row.location_nr = row_data[ this.MAIL_gemnr ];
              row.location    = row_data[ this.MAIL_naamgem ];
              row.status      = row_data[ this.MAIL_status ];
            //row.remarks     = row_data[ this.MAIL_opmerk ];
              row.op_ident    = row_data[ this.MAIL_opident ];
              row.op_partner  = row_data[ this.MAIL_oppartner ];
            //row.op_father   = row_data[ this.MAIL_opvader ];
            //row.op_mother   = row_data[ this.MAIL_opmoeder ];
              row.type        = row_data[ this.MAIL_type ];
              
              rows.push( row );
              console.debug( row );
            }
          }
          
          // We send the op_num separately; in case we are sending an empty table, 
          // we then still know for which OP to delete the deleted mail records. 
          var json = new Object();
          json.idnr = this.OP.op_num;
          json.nrows = nrows;
          json.rdata = rows;
          json.pkdeleted = pk_deleted;
          console.debug( json );
          
          var json_str = qx.lang.Json.stringify( json );
          
          var data = new Object();
          data.mailhuw = json_str;
          
          pk_changed = [];  // empty array of pk's of rows that have been updated
          pk_deleted = [];  // empty array of pk's that have been deleted
          
        //this.showDialog( "NOT saving table rows<br>(update, create, delete)" );
          this.saveHsnOpData( "/putmailhuw", data );
          window.close();
        },
        this
      );
      
      return window;
    }, // createWindow3
    
    
    
    /**
     * createWindow4
     * Printen mail-aanvragen
     */
    createWindow4 : function()
    {
      console.debug( "createWindow4()" );
      
    //var wd_width  = this.MAIN_WIDTH;
    //var wd_height = this.MAIN_HEIGHT;
      
    //var ct_width  = wd_width - 22;  // 22 = estimated margin
      
      var window = new qx.ui.window.Window( "Printen BEV mail-aanvragen" );
      window.set({
        modal          : true,
        contentPadding : [ 10, 10, 10, 10 ],
        showMinimize   : false,
        showMaximize   : false,
        width          : 350,
        height         : 250
      });
      window.addListener( "resize", window.center );
      window.setLayout( new qx.ui.layout.VBox( 5 ) );
      
      window.addListener
      ( 
        "appear", 
        function( ev ) 
        {
        //window.setWidth(  qx.bom.Viewport.getWidth() );
        //window.setHeight( qx.bom.Viewport.getHeight() );
          
          var nmails_bev = this.HSN.mails_print.bev.length;
          console.debug( "nmails_bev: " + nmails_bev );
          textfieldCount.setValue( nmails_bev.toString() );
          
          if( this.have_printer == true && nmails_bev > 0 ) 
          {
            buttonPrint .setEnabled( true );
          //checkboxShow.setEnabled( true );
          }
          else
          { 
            buttonPrint .setEnabled( false ); 
          //checkboxShow.setEnabled( false );
          }
        },
        this
      );
      
      var layoutPrint = new qx.ui.layout.VBox( 5 );
      var containerPrint = new qx.ui.container.Composite( layoutPrint ).set({
        decorator  : "main",
        padding : [ 50, 5, 5, 5 ]   // additional top margin
      });
      window.add( containerPrint, { flex : 1 } );
      
      /*
      // VBox row 0 : tab widget
      var tabview = new qx.ui.tabview.TabView();
      window.add( tabview, { flex : 1 } );
      
      var page_bev = new qx.ui.tabview.Page( "Bevolkingsregister", "icon/16/devices/printer.png" );
      tabview.add( page_bev );
      */
      
      // VBox row 0 : Letter count
      var layoutType = new qx.ui.layout.HBox().set({ AlignX : "center" });
      var containerType = new qx.ui.container.Composite( layoutType );
      containerPrint.add( containerType );
      
      /*
      var labelType = new qx.ui.basic.Label( "Type mailing:" );
      containerType.add( labelType );
      
      containerType.add( new qx.ui.core.Spacer( 25 ) );
      
      var radioGroup = new qx.ui.form.RadioButtonGroup();
      
      var radiobuttonNew    = new qx.ui.form.RadioButton( "Nieuwe mail" );
      var radiobuttonRemind = new qx.ui.form.RadioButton( "Herinnering" );
      
      radiobuttonRemind.setEnabled( false );
      var manager = new qx.ui.form.RadioGroup( radiobuttonNew, radiobuttonRemind );
      
      containerType.add( radiobuttonNew );
      containerType.add( radiobuttonRemind );
      */
      
      var layoutCount = new qx.ui.layout.HBox().set({ AlignX : "center" });
      var containerCount = new qx.ui.container.Composite( layoutCount );
      containerPrint.add( containerCount );
      
      var labelCount = new qx.ui.basic.Label( "Aantal brieven:" );
      containerCount.add( labelCount );
      
      containerCount.add( new qx.ui.core.Spacer( 25 ) );
      
      var textfieldCount = new qx.ui.form.TextField().set({ 
        width       : 100, 
        placeholder : "12345", 
        textAlign   : "center",
        enabled     : false
      });
      containerCount.add( textfieldCount );
      
      /*
      var layoutShow = new qx.ui.layout.HBox().set({ AlignX : "center" });
      var containerShow = new qx.ui.container.Composite( layoutShow );
      window.add( containerShow );
      
      var checkboxShow = new qx.ui.form.CheckBox( "Toon Word tijdens printen" );
      containerShow.add( checkboxShow );
      */
      
      //var layoutPrint1 = new qx.ui.layout.HBox().set({ AlignX : "center" });
      //var containerPrint1 = new qx.ui.container.Composite( layoutPrint1 );
      //window.add( containerPrint1 );
      
      /*
      var page_huw = new qx.ui.tabview.Page( "Huwelijksakten", "icon/16/devices/printer.png" );
      tabview.add( page_huw );
      
    //page_huw.setLayout( new qx.ui.layout.VBox( 5 ) );
      page_huw.setEnabled( false );
      */
      
      // VBox row 1 : PrintCancel
      var layoutPrintCancel = new qx.ui.layout.HBox( 5 ).set({ AlignX : "right" });
      var containerPrintCancel = new qx.ui.container.Composite( layoutPrintCancel );
      window.add( containerPrintCancel );
      
      var buttonCancel = new qx.ui.form.Button( "Annuleren" );
      containerPrintCancel.add( buttonCancel );
      
      buttonCancel.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Annuleren" );
          window.close();
        },
        this
      );
      
      var buttonPrint = new qx.ui.form.Button( "Printen" );
      containerPrintCancel.add( buttonPrint );
      
      buttonPrint.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Printen" );
          
        //var newm  = radiobuttonNew.getValue();
          var count = textfieldCount.getValue();
        //var show  = checkboxShow.getValue();
          
        //console.debug( "newm: " + newm );
          console.debug( "count: " + count );
        //console.debug( "show: " +  show );
          
          var data = "";
          
        //this.showDialog( "Volgende keer gaan we printen" );
          this.saveHsnOpData( "/printmailbev", data );
          
          window.close();
        },
        this
      );
      
      return window;
    }, // createWindow4
    
    
    
    /**
     * createWindow5
     * Verwerken binnengekomen mail
     */
    createWindow5 : function()
    {
      console.debug( "createWindow5()" );
      
      var wd_width  = this.MAIN_WIDTH;
      var wd_height = this.MAIN_HEIGHT;
      
      var ct_width  = wd_width - 22;  // 22 = estimated margin
      
      var window = new qx.ui.window.Window( "Verwerken binnengekomen mail" );
      window.set({
        width  : wd_width,
        height : wd_height,
        modal  : true
      });
      window.addListener( "resize", window.center );
      window.setLayout( new qx.ui.layout.VBox( 5 ) );
      
      window.addListener
      ( 
        "appear", 
        function( ev ) 
        {
          window.setWidth(  qx.bom.Viewport.getWidth() );
          window.setHeight( qx.bom.Viewport.getHeight() );
          
          // clear data from previous OP
          console.debug( "clearing id list to update" );
          ids_update = [];
          
          var numrows = tableModel.getRowCount();
          tableModel.removeRows( 0, numrows );
          
          textfieldId.setValue( "" );
          
          // fill the table with "bevolkingsregister" mails
          var mails = this.OP.mails.bev;
          var rows = [];
          var nbev = 0;
          
          for( var i = 0; i < mails.length; i++ ) 
          {
            var mail = mails[ i ];
          //console.debug( "i: " + i + " " + mail );
            
            nbev++;
            var row = [ 
              nbev,                           //  0
              mail.id.toString(),             //  1
              mail.idnr.toString(),           //  2
              mail.briefnr.toString(),        //  3
              mail.aard,                      //  4
              mail.datum,                     //  5
              mail.periode,                   //  6
              mail.gemnr.toString(),          //  7
              mail.naamgem,                   //  8
              mail.status,                    //  9
              mail.printdatum,                // 10
              mail.printen,                   // 11
              mail.ontvdat,                   // 12
              mail.opmerk,                    // 13
              mail.opident,                   // 14
              mail.oppartner,                 // 15
              mail.opvader,                   // 16
              mail.opmoeder,                  // 17
              mail.type,                      // 18
              mail.infoouders,                // 19
              mail.infopartner,                // 20
              mail.inforeis                   // 21
            ];
            rows.push( row );
          }
          
          var clearSorting = true;
          tableModel.addRows( rows, 0, clearSorting );
        },
        this
      );
      
      // VBox row 0 : OP-info
      var layoutOpinfo = new qx.ui.layout.HBox( 10 );    // spacing = 10
      var containerOpinfo = new qx.ui.container.Composite( layoutOpinfo ).set({
        decorator   : "main",
        paddingLeft : 20,
        width       : ct_width,
        allowGrowY  : false
      });
      
      this.labelOpinfo5 = new qx.ui.basic.Label().set({ rich : true });
      containerOpinfo.add( this.labelOpinfo5 );
      window.add( containerOpinfo );
      
      
      // VBox row 1 : process mailing
      var layoutProcess = new qx.ui.layout.VBox( 5 );
      var containerProcess = new qx.ui.container.Composite( layoutProcess ).set({
        decorator  : "main",
        padding    : 5,
        width      : ct_width,
        allowGrowY : false
      });
      window.add( containerProcess );
      
      
      var tableModel = this._tableModel = new qx.ui.table.model.Simple();
    //tableModel.setColumns([ "Id", "Type", "Gemeente", "Datum", "Periode", "Print Datum", "Status", "Ontvangst Datum" ]);
      var column_names = [
        "#",
        "Id",
        "Id Nr",
        "Brief Nr",
        "Aard",
        "Datum",
        "Periode",
        "Gemeente Nr",
        "Gemeente",
        "Status",
        "Print Datum",
        "Printen",
        "Ontvangst Datum",
        "Opmerkingen",
        "OP Ident",
        "OP Partner",
        "OP Vader",
        "OP Moeder",
        "Type",
        "Info Ouders",
        "Info Partner",
        "Info Reis"
      ];
      tableModel.setColumns( column_names );
      
      // Customize the table column model. We want one that automatically resizes columns.
      var custom = { tableColumnModel : function( obj ) { return new qx.ui.table.columnmodel.Resize( obj ); } };
      
      var table = new qx.ui.table.Table( tableModel, custom );
      table.set({
        decorator        : "main",
        statusBarVisible : false,
        width            : ct_width,
        height           : 200,
        allowGrowX       : true,
        allowGrowY       : true
      });
      containerProcess.add( table, { flex : 1 } );
      
      table.addListener
      (
        "cellTap", 
        function( ev ) 
        {
          var row_idx    = ev.getRow();
          var column_idx = ev.getColumn();
          console.debug( "cellTap type: " + ev.getType() + ", row: " + row_idx + ", columnn: " + column_idx );
          
          var row_data = tableModel.getRowData( row_idx );
          var status = row_data[ this.MAIL_status ];
            
          if( status == 1 )   // row is selectable
            {
            console.debug( "status: " + status + ", row selectable" );
          //table.resetCellFocus();
            table.setShowCellFocusIndicator( true );
            tsm.setSelectionMode( selModel.SINGLE_SELECTION );
            tsm.setSelectionInterval( row_idx, row_idx );
            var id = row_data[ this.MAIL_id ];
            textfieldId.setValue( id );
          }
          else 
          { 
            console.debug( "status: " + status + ", row NOT selectable" );
            table.resetCellFocus();
            table.setShowCellFocusIndicator( false );
            tsm.setSelectionMode( selModel.NO_SELECTION );
            textfieldId.setValue( "" );
          }
        },
        this
      );
      
      // after deselection of selected rows, the last deselected row remained lightblue (i.e. focusline).
      table.highlightFocusedRow( false );
      
      var selModel = qx.ui.table.selection.Model;
      var tsm = table.getSelectionModel();
      tsm.setSelectionMode( selModel.NO_SELECTION );
      console.debug( "table getSelectionMode: " + tsm.getSelectionMode() );
      
      
      // after deselection of selected rows, the last deselected row remained lightblue (i.e. focusline).
      table.highlightFocusedRow( false );
      
      var tcm = table.getTableColumnModel();
      var resizeBehavior = tcm.getBehavior();
      
      //preferred column widths
      resizeBehavior.set( this.MAIL_nr,          { width  :"1*", minWidth :  20, maxWidth :  20 } );  //  0 Nr
      resizeBehavior.set( this.MAIL_id,          { width  :"1*", minWidth :  60, maxWidth :  60 } );  //  1 Id
      resizeBehavior.set( this.MAIL_idnr,        { width  :"1*", minWidth :  50, maxWidth :  50 } );  //  2
      resizeBehavior.set( this.MAIL_briefnr,     { width  :"1*", minWidth :  30, maxWidth :  30 } );  //  3
      resizeBehavior.set( this.MAIL_aard,        { width  :"1*", minWidth :  40, maxWidth :  40 } );  //  4 Aard
      resizeBehavior.set( this.MAIL_datum,       { width  :"1*", minWidth :  70, maxWidth :  70 } );  //  5 Datum
      resizeBehavior.set( this.MAIL_periode,     { width  :"1*", minWidth :  80, maxWidth :  80 } );  //  6 Periode
      resizeBehavior.set( this.MAIL_gemnr,       { width  :"1*", minWidth :  40, maxWidth :  40 } );  //  7 GemeenteNr
      resizeBehavior.set( this.MAIL_naamgem,     { width  :"1*", minWidth : 100                 } );  //  8 Gemeente
      resizeBehavior.set( this.MAIL_status,      { width  :"1*", minWidth :  50, maxWidth :  50 } );  //  9 Status
      resizeBehavior.set( this.MAIL_printdatum,  { width  :"1*", minWidth :  70, maxWidth :  70 } );  // 10 PrintDatum
      resizeBehavior.set( this.MAIL_printen,     { width  :"1*", minWidth :  30, maxWidth :  30 } );  // 11
      resizeBehavior.set( this.MAIL_ontvdat,     { width  :"1*", minWidth : 100, maxWidth : 100 } );  // 12 
      resizeBehavior.set( this.MAIL_opmerk,      { width  :"1*", minWidth : 100 } );                  // 13 Opmerkingen
      resizeBehavior.set( this.MAIL_opident,     { width  :"1*", minWidth : 100 } );                  // 14 
      resizeBehavior.set( this.MAIL_oppartner,   { width  :"1*", minWidth : 100 } );                  // 15
      resizeBehavior.set( this.MAIL_opvader,     { width  :"1*", minWidth : 100 } );                  // 15
      resizeBehavior.set( this.MAIL_opmoeder,    { width  :"1*", minWidth : 100 } );                  // 17
      resizeBehavior.set( this.MAIL_type,        { width  :"1*", minWidth :  40, maxWidth :  40 } );  // 18 Type
      resizeBehavior.set( this.MAIL_infoouders,  { width  :"1*", minWidth :  30, maxWidth :  30 } );  // 19 
      resizeBehavior.set( this.MAIL_infopartner, { width  :"1*", minWidth :  30, maxWidth :  30 } );  // 20
      resizeBehavior.set( this.MAIL_inforeis,    { width  :"1*", minWidth :  30, maxWidth :  30 } );  // 21
      
      // default visibility
    //tcm.setColumnVisible( this.MAIL_nr,          false );  //  0,
    //tcm.setColumnVisible( this.MAIL_id,          false );  //  1,
      tcm.setColumnVisible( this.MAIL_idnr,        false );  //  2,
      tcm.setColumnVisible( this.MAIL_briefnr,     false );  //  3,
    //tcm.setColumnVisible( this.MAIL_aard,        false );  //  4,
    //tcm.setColumnVisible( this.MAIL_datum,       false );  //  5,
    //tcm.setColumnVisible( this.MAIL_periode,     false );  //  6,
      tcm.setColumnVisible( this.MAIL_gemnr,       false );  //  7,
    //tcm.setColumnVisible( this.MAIL_naamgem,     false );  //  8,
    //tcm.setColumnVisible( this.MAIL_status,      false );  //  9,
    //tcm.setColumnVisible( this.MAIL_printdatum,  false );  // 10,
    //tcm.setColumnVisible( this.MAIL_printen,     false );  // 11,
    //tcm.setColumnVisible( this.MAIL_ontvdat,     false );  // 12,
      tcm.setColumnVisible( this.MAIL_opmerk,      false );  // 13,
      tcm.setColumnVisible( this.MAIL_opident,     false );  // 14,
      tcm.setColumnVisible( this.MAIL_oppartner,   false );  // 15,
      tcm.setColumnVisible( this.MAIL_opvader,     false );  // 16,
      tcm.setColumnVisible( this.MAIL_opmoeder,    false );  // 17,
    //tcm.setColumnVisible( this.MAIL_type,        false );  // 18,
      tcm.setColumnVisible( this.MAIL_infoouders,  false );  // 19,
      tcm.setColumnVisible( this.MAIL_infopartner, false );  // 20,
      tcm.setColumnVisible( this.MAIL_inforeis,    false );  // 21,
      
      var layoutBooking = new qx.ui.layout.HBox( 5 );
      var containerBooking = new qx.ui.container.Composite( layoutBooking );
      containerProcess.add( containerBooking );
      
      var labelId = new qx.ui.basic.Label( "Id:" );
      containerBooking.add( labelId );
      
      var textfieldId = new qx.ui.form.TextField().set({ enabled : false });
      containerBooking.add( textfieldId );
      
      textfieldId.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
          if( textfieldId.getValue() === "" ) { buttonUpdate.setEnabled( false ); }
          else { buttonUpdate.setEnabled( true ); }
        },
        this
      );
      
      containerBooking.add( new qx.ui.core.Spacer( 25 ) );
      
      var labelBooking = new qx.ui.basic.Label( "Datum inboeken:" );
      containerBooking.add( labelBooking );
      
      var datefieldBooking = new qx.ui.form.DateField().set({ width : 150 });
      containerBooking.add( datefieldBooking );
      datefieldBooking.setValue( new Date() );  // default is current date
      
      var dateformat = new qx.util.format.DateFormat( "d MMMM y" ); // e.g.: "18 september 2015"
      datefieldBooking.setDateFormat( dateformat );
      
      
      containerBooking.add( new qx.ui.core.Spacer( 25 ) );
      
      var tbuttonView = new qx.ui.form.ToggleButton( "Bekijk meer" );
      containerBooking.add( tbuttonView );
      
      tbuttonView.addListener
      ( 
        "changeValue", 
        function( ev ) 
        {
          var value = tbuttonView.getValue();
          if( value == true ) 
          {
            tbuttonView.setLabel( "Bekijk minder" );
            
            // more visibility
            tcm.setColumnVisible( this.MAIL_nr,          true );  //  0,
            tcm.setColumnVisible( this.MAIL_id,          true );  //  1,
            tcm.setColumnVisible( this.MAIL_idnr,        true );  //  2,
            tcm.setColumnVisible( this.MAIL_briefnr,     true );  //  3,
            tcm.setColumnVisible( this.MAIL_aard,        true );  //  4,
            tcm.setColumnVisible( this.MAIL_datum,       true );  //  5,
            tcm.setColumnVisible( this.MAIL_periode,     true );  //  6,
            tcm.setColumnVisible( this.MAIL_gemnr,       true );  //  7,
            tcm.setColumnVisible( this.MAIL_naamgem,     true );  //  8,
            tcm.setColumnVisible( this.MAIL_status,      true );  //  9,
            tcm.setColumnVisible( this.MAIL_printdatum,  true );  // 10,
            tcm.setColumnVisible( this.MAIL_printen,     true );  // 11,
            tcm.setColumnVisible( this.MAIL_ontvdat,     true );  // 12,
            tcm.setColumnVisible( this.MAIL_opmerk,      true );  // 13,
            tcm.setColumnVisible( this.MAIL_opident,     true );  // 14,
            tcm.setColumnVisible( this.MAIL_oppartner,   true );  // 15,
            tcm.setColumnVisible( this.MAIL_opvader,     true );  // 16,
            tcm.setColumnVisible( this.MAIL_opmoeder,    true );  // 17,
            tcm.setColumnVisible( this.MAIL_type,        true );  // 18,
            tcm.setColumnVisible( this.MAIL_infoouders,  true );  // 19,
            tcm.setColumnVisible( this.MAIL_infopartner, true );  // 20,
            tcm.setColumnVisible( this.MAIL_inforeis,    true );  // 21,
          }
          else 
          {
            tbuttonView.setLabel( "Bekijk meer" );
            
            // less visibility
            tcm.setColumnVisible( this.MAIL_nr,          true  );  //  0,
            tcm.setColumnVisible( this.MAIL_id,          true  );  //  1,
            tcm.setColumnVisible( this.MAIL_idnr,        true  );  //  2,
            tcm.setColumnVisible( this.MAIL_briefnr,     false );  //  3,
            tcm.setColumnVisible( this.MAIL_aard,        true  );  //  4,
            tcm.setColumnVisible( this.MAIL_datum,       true  );  //  5,
            tcm.setColumnVisible( this.MAIL_periode,     true  );  //  6,
            tcm.setColumnVisible( this.MAIL_gemnr,       false );  //  7,
            tcm.setColumnVisible( this.MAIL_naamgem,     true  );  //  8,
            tcm.setColumnVisible( this.MAIL_status,      true  );  //  9,
            tcm.setColumnVisible( this.MAIL_printdatum,  true  );  // 10,
            tcm.setColumnVisible( this.MAIL_printen,     true  );  // 11,
            tcm.setColumnVisible( this.MAIL_ontvdat,     true  );  // 12,
            tcm.setColumnVisible( this.MAIL_opmerk,      false );  // 13,
            tcm.setColumnVisible( this.MAIL_opident,     false );  // 14,
            tcm.setColumnVisible( this.MAIL_oppartner,   false );  // 15,
            tcm.setColumnVisible( this.MAIL_opvader,     false );  // 16,
            tcm.setColumnVisible( this.MAIL_opmoeder,    false );  // 17,
            tcm.setColumnVisible( this.MAIL_type,        true  );  // 18,
            tcm.setColumnVisible( this.MAIL_infoouders,  false );  // 19,
            tcm.setColumnVisible( this.MAIL_infopartner, false );  // 20,
            tcm.setColumnVisible( this.MAIL_inforeis,    false );  // 21,
          }
        },
        this
      );
      
      var ids_update = [];
      
      var buttonUpdate = new qx.ui.form.Button( "Inboeken" ).set({ enabled : false });
      containerBooking.add( buttonUpdate );
      
      buttonUpdate.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "buttonUpdate" );
          
          var date = datefieldBooking.getValue();
          var dateformat = new qx.util.format.DateFormat( "dd-MM-yyyy" );
          var fdate = dateformat.format( date );
          console.debug( "booking date: " + fdate );
          
          table.getSelectionModel().iterateSelection
          ( 
            function( row_idx ) 
            {
              console.debug( "row idx: " + row_idx );
              var row_data = tableModel.getRowData( row_idx );
              //console.debug( row_data );
              
              var status = tableModel.getValue( this.MAIL_status,  row_idx );
              if( status == 1 ) 
              {
                var id = tableModel.getValue( this.MAIL_id,  row_idx );
                ids_update.push( id );
                
                // update status and date
                tableModel.setValue( this.MAIL_status,  row_idx, 9 );
                tableModel.setValue( this.MAIL_ontvdat, row_idx, fdate );
              
                //var row_data = tableModel.getRowData( row_idx );
                //console.debug( row_data );
              }
            }, 
            this
          );
        },
        this
      );
      
      
      // VBox row 2 : Save, Cancel
      var layoutSaveCancel = new qx.ui.layout.HBox( 5 ).set({ AlignX : "right" });
      var containerSaveCancel = new qx.ui.container.Composite( layoutSaveCancel );
      window.add( containerSaveCancel );
      
      var buttonCancel = new qx.ui.form.Button( "Annuleren" );
      containerSaveCancel.add( buttonCancel );
      
      buttonCancel.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Window 5: Annuleren" );
          var legend = "Eventuele wijzigingen zullen <b>niet</b> worden opgeslagen.<br>Akkoord?";
          this.closeWindow( window, "Annuleren", legend );
          //window.close();
        },
        this
      );
      
      var buttonSave = new qx.ui.form.Button( "Opslaan" );
      containerSaveCancel.add( buttonSave );
      
      buttonSave.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Window 5: Opslaan" );
          
          var date = datefieldBooking.getValue();
          var dateformat = new qx.util.format.DateFormat( "dd-MM-yyyy" );
          var fdate = dateformat.format( date );
          console.debug( "date: " + date + ", fdate: " + fdate );
          console.debug( "ids: " + ids_update );
          
          var json   = new Object();
          json.idnr  = this.OP.op_num;
          json.ids   = ids_update;
          json.fdate = fdate;
          console.debug( json );
          
          var json_str = qx.lang.Json.stringify( json );
          
          var data = new Object();
          data.mailbevreceived = json_str;
          
          console.debug( "clearing id list to update" );
          ids_update = [];
          
        //this.showDialog( "NOT saving table rows<br>(update, create, delete)" );
          this.saveHsnOpData( "/putmailbevreceived", data );
          window.close();
        },
        this
      );
      
      return window;
    }, // createWindow5
    
    
    
    /**
     * createWindow6
     * Vastleggen geconstateerde identiteitsverandering
     */
    createWindow6 : function()
    {
      console.debug( "createWindow6()" );
      
      var wd_width  = this.MAIN_WIDTH;
      var wd_height = this.MAIN_HEIGHT;
      
      var ct_width  = wd_width - 22;  // 22 = estimated margin
      
      var window = new qx.ui.window.Window( "Vastleggen geconstateerde identiteitsverandering" );
      window.set({
        width  : wd_width,
        height : wd_height,
        modal  : true
      });
      window.addListener( "resize", window.center );
      window.setLayout( new qx.ui.layout.VBox( 5 ) );
      
      window.addListener
      ( 
        "appear", 
        function( ev ) 
        {
          window.setWidth(  qx.bom.Viewport.getWidth() );
          window.setHeight( qx.bom.Viewport.getHeight() );
          
          // clear previous values
          textfieldSource  .setValue( "" );
          textareaMutations.setValue( "" ); // clear previous OP mutation data
          
          textfieldMutationDay  .setValue( "" ); 
          textfieldMutationMonth.setValue( "" );
          textfieldMutationYear .setValue( "" );
          textfieldRemark       .setValue( "" );
          
          checkboxLastname  .setValue( false );
          checkboxPrefix    .setValue( false );
          checkboxFirstname .setValue( false );
          checkboxBirthdate .setValue( false );
          checkboxBirthplace.setValue( false );
          checkboxGender    .setValue( false );
      
          buttonAdd .setEnabled( true );
          buttonSave.setEnabled( false );
          
          // set new OP values
          var op_info_str = "";
          var op_info_list = this.OP.op_info_list;
          var op_mutation_list = [];  // for printed letter
          var mutation_lines = "";    // for window0 display
          
          for( var i = 0; i < op_info_list.length; i++ ) 
          {
            var op_info = op_info_list[ i ];
            var id_origin = op_info.id_origin;
            var display_str = op_info.display_str;
            console.debug( "id_origin: " + id_origin + ", " + display_str );
            
            if( id_origin == 10 ) { 
              op_info_str = display_str; 
              this.OP.op_info_str = op_info_str;
              this.opinfo_html = "<h3><b>" + op_info_str + "</b></h3>"
              this.labelOpinfo.setValue( this.opinfo_html );
              
              textfieldLastname .setValue( op_info.rp_family );
              textfieldPrefix   .setValue( op_info.rp_prefix );
              textfieldFirstname.setValue( op_info.rp_firstname );
              
              // months numbers start from 0 in JavaScript, not from 1.
              //var birthdate = new Date( op_info.rp_b_year, -1 + op_info.rp_b_month, op_info.rp_b_day );
              //datefieldBirthdate.setValue( birthdate );
              
              textfieldBirthDay  .setValue( op_info.rp_b_day  .toString() ); 
              textfieldBirthMonth.setValue( op_info.rp_b_month.toString() );
              textfieldBirthYear .setValue( op_info.rp_b_year .toString() );
              
              comboboxBirthplace.setValue( op_info.rp_b_place );
              textfieldGender   .setValue( op_info.rp_b_sex );
            }
            else 
            {
              op_mutation_list.push( display_str );
              mutation_lines += "mutatie type " + op_info.id_origin;
              mutation_lines += ", per " + op_info.valid_date;
              mutation_lines += ", " + display_str + "\n";
            }
          }
          this.OP.op_mutation_list = op_mutation_list;
          
          console.debug( "mutations: " + mutation_lines );
          textareaMutations.setValue( mutation_lines );   // OP 5267  has 4 mutations
        },
        this
      );
      
      
      // VBox row 0 : OP-info
      var layoutOpinfo = new qx.ui.layout.HBox( 10 );    // spacing = 10
      var containerOpinfo = new qx.ui.container.Composite( layoutOpinfo ).set({
        decorator   : "main",
        paddingLeft : 20,
        width       : ct_width,
        allowGrowY  : false
      });
      
      this.labelOpinfo6 = new qx.ui.basic.Label().set({ rich : true });
      containerOpinfo.add( this.labelOpinfo6 );
      window.add( containerOpinfo );
      
      
      // VBox row 1 : list identity changes
      var layoutMutations = new qx.ui.layout.VBox( 5 );
      var containerMutations = new qx.ui.container.Composite( layoutMutations ).set({
        decorator  : "main",
        padding    : 5,
        width      : ct_width,
        height     : 100,
        allowGrowY : false
      });
      window.add( containerMutations );
      
      var textareaMutations = new qx.ui.form.TextArea().set({ 
        width   : ct_width, 
        height  : 100,
        enabled : false,    // read-only
        wrap    : false
      });
      containerMutations.add( textareaMutations );
      
      
      // VBox row 2 : add identity changes
      var layoutMutationAdd = new qx.ui.layout.Grid( 5, 5 );
      layoutMutationAdd.setColumnWidth( 1, 200 );
      layoutMutationAdd.setColumnFlex( 2, 1 );     // make column 2 flexible
      var containerMutationAdd = new qx.ui.container.Composite( layoutMutationAdd ).set({
        decorator  : "main",
        padding    : 10,
        width      : ct_width,
        height     : 100,
        allowGrowY : false
      });
      window.add( containerMutationAdd );
      
      var labelSource = new qx.ui.basic.Label( "Bron" );
      var labelDate   = new qx.ui.basic.Label( "Datum Identiteitsverandering" );
      var labelRemark = new qx.ui.basic.Label( "Opmerking" );
      
      containerMutationAdd.add( labelSource, { row : 0, column : 0 } );
      containerMutationAdd.add( labelDate,   { row : 1, column : 0 } );
      containerMutationAdd.add( labelRemark, { row : 2, column : 0 } );
      
      var textfieldSource = new qx.ui.form.TextField();
      containerMutationAdd.add( textfieldSource,  { row : 0, column : 1 } );
      
      var layoutMutationDate = new qx.ui.layout.HBox( 5 );
      var containerMutationDate = new qx.ui.container.Composite( layoutMutationDate );
      containerMutationAdd.add( containerMutationDate, { row : 1, column : 1 }  );
      
      var textfieldMutationDay   = new qx.ui.form.TextField().set({ width : 30, placeholder : "DD", textAlign : "center" });
      var textfieldMutationMonth = new qx.ui.form.TextField().set({ width : 30, placeholder : "MM", textAlign : "center" });
      var textfieldMutationYear  = new qx.ui.form.TextField().set({ width : 40, placeholder :"JJJJ",textAlign : "center" });
      
      containerMutationDate.add( textfieldMutationDay );
      containerMutationDate.add( textfieldMutationMonth );
      containerMutationDate.add( textfieldMutationYear );
      
      textfieldMutationDay.addListener( "input", function( ev ) {
        var day = textfieldMutationDay.get( "value" );
        if( isNaN( day ) ) { textfieldMutationDay.setValue( "" ); }             // ignore NaNs
        else if( day.length > 2 ) { textfieldMutationDay.setValue( "" ); }      // too long
        else if( day.length == 2 ){ textfieldMutationMonth.focus(); }           // OK, next field
      });
      
      textfieldMutationMonth.addListener( "input", function( ev ) {
        var month = textfieldMutationMonth.get( "value" );
        if( isNaN( month ) ) { textfieldMutationMonth.setValue( "" ); }         // ignore NaNs
        else if( month.length > 2 ) { textfieldMutationMonth.setValue( "" ); }  // too long
        else if( month.length == 2 ){ textfieldMutationYear.focus(); }          // OK, next field
      });
      
      textfieldMutationYear.addListener( "input", function( ev ) {
        var year = textfieldMutationYear.get( "value" );
        if( isNaN( year ) ) { textfieldMutationYear.setValue( "" ); }           // ignore NaNs
        else if( year.length > 4 ) { textfieldMutationYear.setValue( "" ); }    // too long
        else if( year.length == 4 ){ textfieldRemark.focus(); }                 // OK, next field
      });
      
      var textfieldRemark = new qx.ui.form.TextField();
      containerMutationAdd.add( textfieldRemark, { row : 2, column : 1, colSpan : 2 } );
      
      var checkboxLastname   = new qx.ui.form.CheckBox( "Achternaam" );
      var checkboxPrefix     = new qx.ui.form.CheckBox( "Prefix" );
      var checkboxFirstname  = new qx.ui.form.CheckBox( "Voornamen" );
      var checkboxBirthdate  = new qx.ui.form.CheckBox( "Geboortedatum" );
      var checkboxBirthplace = new qx.ui.form.CheckBox( "Geboorteplaats" );
      var checkboxGender     = new qx.ui.form.CheckBox( "Geslacht" );
      
      containerMutationAdd.add( checkboxLastname,   { row : 3, column : 0 } );
      containerMutationAdd.add( checkboxPrefix,     { row : 4, column : 0 } );
      containerMutationAdd.add( checkboxFirstname,  { row : 5, column : 0 } );
      containerMutationAdd.add( checkboxBirthdate,  { row : 6, column : 0 } );
      containerMutationAdd.add( checkboxBirthplace, { row : 7, column : 0 } );
      containerMutationAdd.add( checkboxGender,     { row : 8, column : 0 } );
      
      checkboxLastname.addListener( "execute", function( ev ) {
          if( checkboxLastname.get( "value" ) == true ) { textfieldLastname.setEnabled( true ); }
          else { textfieldLastname.setEnabled( false ); }
      });
      
      checkboxPrefix.addListener( "execute", function( ev ) {
          if( checkboxPrefix.get( "value" ) == true ) { textfieldPrefix.setEnabled( true ); }
          else { textfieldPrefix.setEnabled( false ); }
      });
      
      checkboxFirstname.addListener( "execute", function( ev ) {
          if( checkboxFirstname.get( "value" ) == true ) { textfieldFirstname.setEnabled( true ); }
          else { textfieldFirstname.setEnabled( false ); }
      });
      
      checkboxBirthdate.addListener( "execute", function( ev ) {
          if( checkboxBirthdate.get( "value" ) == true ) {
            textfieldBirthDay  .setEnabled( true );
            textfieldBirthMonth.setEnabled( true );
            textfieldBirthYear .setEnabled( true );
          }
          else {
            textfieldBirthDay  .setEnabled( false );
            textfieldBirthMonth.setEnabled( false );
            textfieldBirthYear .setEnabled( false );
          }
      });
      
      checkboxBirthplace.addListener( "execute", function( ev ) {
          if( checkboxBirthplace.get( "value" ) == true ) { comboboxBirthplace.setEnabled( true ); }
          else { comboboxBirthplace.setEnabled( false ); }
      });
      
      checkboxGender.addListener( "execute", function( ev ) {
          if( checkboxGender.get( "value" ) == true ) { textfieldGender.setEnabled( true ); }
          else { textfieldGender.setEnabled( false ); }
      });
      
      var textfieldLastname = new qx.ui.form.TextField().set({ enabled : false });
      containerMutationAdd.add( textfieldLastname, { row : 3, column : 1 } );
      
      var textfieldPrefix = new qx.ui.form.TextField().set({ enabled : false });
      containerMutationAdd.add( textfieldPrefix, { row : 4, column : 1 } );
      
      var textfieldFirstname = new qx.ui.form.TextField().set({ enabled : false });
      containerMutationAdd.add( textfieldFirstname, { row : 5, column : 1 } );
      
      
      var layoutBirthDate = new qx.ui.layout.HBox( 5 );
      var containerBirthDate = new qx.ui.container.Composite( layoutBirthDate );
      containerMutationAdd.add( containerBirthDate, { row : 6, column : 1 }  );
      
      var textfieldBirthDay   = new qx.ui.form.TextField().set({ width : 30, placeholder : "DD", textAlign : "center", enabled : false });
      var textfieldBirthMonth = new qx.ui.form.TextField().set({ width : 30, placeholder : "MM", textAlign : "center", enabled : false });
      var textfieldBirthYear  = new qx.ui.form.TextField().set({ width : 40, placeholder :"JJJJ",textAlign : "center", enabled : false });
      
      containerBirthDate.add( textfieldBirthDay );
      containerBirthDate.add( textfieldBirthMonth );
      containerBirthDate.add( textfieldBirthYear );
      
      
    //var comboboxBirthplace = new qx.ui.form.ComboBox().set({ enabled : false, width : 200 });
      // ComboTable is a combination of a ComboBox and a Table for autocompletion
      var combotable_model = new combotable.SearchableModel();
      combotable_model.setColumns( ['Id','Data'], ['id','data'] );
      combotable_model.setData( this.location_array );
      
      var comboboxBirthplace = new combotable.ComboTable( combotable_model ).set({
          enabled     : false,
          width       : 200,
          placeholder : 'Geboorteplaats'
      });
      containerMutationAdd.add( comboboxBirthplace, { row : 7, column : 1 } );
      
      
      var textfieldGender = new qx.ui.form.TextField().set({ enabled : false });
      containerMutationAdd.add( textfieldGender, { row : 8, column : 1 } );
      
      var layoutBtnAdd = new qx.ui.layout.HBox();
      var containerBtnAdd = new qx.ui.container.Composite( layoutBtnAdd );
      
      var id_origin = 19;   // used in buttonAdd.addListener & buttonSave.addListener
      
      var buttonAdd = new qx.ui.form.Button( "Toevoegen" );
      containerBtnAdd.add( buttonAdd );
      containerMutationAdd.add( containerBtnAdd, { row : 9, column : 0 } );
      
      buttonAdd.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Toevoegen" );
          
          buttonSave.setEnabled( true );
          
          var valid_day   = textfieldMutationDay  .getValue();
          var valid_month = textfieldMutationMonth.getValue();
          var valid_year  = textfieldMutationYear .getValue();
          
          console.debug( "valid_day: " + valid_day + ", valid_month: " + valid_month + ", valid_year: " + valid_year );
          var valid_date_str = valid_day + "/" + valid_month + "/" + valid_year;
          console.debug( "valid_date_str: " + valid_date_str );
          
          /*
          // No date validation, because wrong input from outside must be copied as such
          if( ! ( this.isNumeric( valid_day ) && this.isNumeric( valid_month  ) && this.isNumeric( valid_year ) ) ) {
            this.showDialog( "Identiteitsverandering<br><br><b>De datum van de identiteitsverandering is niet goed</b>" );
            return;
          }
          
          // they may use -1 for missing components
          if( ! ( this.isValidDate( valid_date_str  ) ) ) {
            this.showDialog( "Identiteitsverandering<br><br><b>De datum van de identiteitsverandering is niet goed</b>" );
            return;
          }
          */
          
          var birth_day   = textfieldBirthDay  .getValue();
          var birth_month = textfieldBirthMonth.getValue();
          var birth_year  = textfieldBirthYear .getValue();
          
          console.debug( "birth_day: " + birth_day + ", birth_month: " + birth_month + ", birth_year: " + birth_year );
          var birth_date_str = birth_day + "/" + birth_month + "/" + birth_year;
          console.debug( "birth_date_str: " +  birth_date_str );
          
          /*
          // No date validation, because wrong input from outside must be copied as such
          if( ! ( this.isNumeric( birth_day ) && this.isNumeric( birth_month  ) && this.isNumeric( birth_year ) ) ) {
            this.showDialog( "Identiteitsverandering<br><br><b>De geboortedatum is niet goed</b>" );
            return;
          }
           
          // they may use -1 for missing components
          if( ! ( this.isValidDate( birth_date_str  ) ) ) {
            this.showDialog( "Identiteitsverandering<br><br><b>De geboortedatum is niet goed</b>" );
            return;
          }
          */
          
          var lastname   = textfieldLastname .getValue();
          var prefix     = textfieldPrefix   .getValue();
          var firstname  = textfieldFirstname.getValue();
          var birthplace = comboboxBirthplace.getValue();
          var gender     = textfieldGender   .getValue();
          
          console.debug( "lastname: " + lastname + ", prefix: " + prefix + ", firstname: " + firstname + ", birthplace: " + birthplace + ", gender: " + gender );
          
          var mutation_str = "mutatie type " + id_origin + ", per " + valid_date_str;
          mutation_str += ", " + lastname + ", " + firstname + " [" + gender + "]";
          mutation_str += " * " + birth_date_str + " " + birthplace + "\n";
          
          console.debug( mutation_str );
          
          var mutation_lines = textareaMutations.getValue();
          mutation_lines += mutation_str;
          textareaMutations.setValue( mutation_lines );
          
          buttonAdd.setEnabled( false );
        },
        this
      );
      
      // VBox row 3 : Save, Cancel
      var layoutSaveCancel = new qx.ui.layout.HBox( 5 ).set({ AlignX : "right" });
      var containerSaveCancel = new qx.ui.container.Composite( layoutSaveCancel );
      window.add( containerSaveCancel );
      
      var buttonCancel = new qx.ui.form.Button( "Annuleren" );
      containerSaveCancel.add( buttonCancel );
      
      buttonCancel.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Window 6: Annuleren" );
          var legend = "Eventuele wijzigingen zullen <b>niet</b> worden opgeslagen.<br>Akkoord?";
          this.closeWindow( window, "Annuleren", legend );
          //window.close();
        },
        this
      );
      
      var buttonSave = new qx.ui.form.Button( "Opslaan" ).set({ enabled : false });
      containerSaveCancel.add( buttonSave );
      
      buttonSave.addListener
      ( 
        "execute", 
        function( ev ) 
        {
          console.debug( "Window 6: Opslaan" );
          
          var json = new Object();
          
          json.idnr = this.OP.op_num;
          json.id_origin = id_origin;
          
          json.source      = textfieldSource       .getValue();
          json.valid_day   = textfieldMutationDay  .getValue();
          json.valid_month = textfieldMutationMonth.getValue();
          json.valid_year  = textfieldMutationYear .getValue();
          json.remarks     = textfieldRemark       .getValue();
          json.lastname    = textfieldLastname     .getValue();
          json.prefix      = textfieldPrefix       .getValue();
          json.firstname   = textfieldFirstname    .getValue();
          json.birth_day   = textfieldBirthDay     .getValue();
          json.birth_month = textfieldBirthMonth   .getValue();
          json.birth_year  = textfieldBirthYear    .getValue();
          json.birthplace  = comboboxBirthplace    .getValue();
          json.gender      = textfieldGender       .getValue();
          
          console.debug( json );
          
          var json_str = qx.lang.Json.stringify( json );
          
          var data = new Object();
          data.opmutation = json_str;
          
        //this.showDialog( "NOT yet saving new mutation" );
          this.saveHsnOpData( "/putopmutation", data );
          window.close();
        },
        this
      );
      
      return window;
      
    }, // createWindow6
    
    
    
    isNumeric : function( n ) 
    {
      return ! isNaN( parseFloat( n ) ) && isFinite( n );
    }, // isNumeric
    
    
    
    isValidDate : function( dateString )
    {
      // Validates that the input string is a valid date formatted as "dd/mm/yyyy"
      // First check for the pattern
      if( !/^\d{1,2}\/\d{1,2}\/\d{4}$/.test( dateString ) ) { 
        console.debug( "regexp failed" );
        return false; 
      }
      
      // Parse the date parts to integers
      var parts = dateString.split( "/" );
      var day   = parseInt( parts[ 0 ], 10 );
      var month = parseInt( parts[ 1 ], 10 );
      var year  = parseInt( parts[ 2 ], 10 );
      
      // Check the ranges of month and year
      if( year < 1000 || year > 3000 || month == 0 || month > 12 ) { 
        console.debug( "ranges of month and year failed" );
        return false;
      }
      
      var monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];
      
      // Adjust for leap years
      if( year % 400 == 0 || ( year % 100 != 0 && year % 4 == 0 ) )
      { monthLength[ 1 ] = 29; }
      
      // Check the range of the day
      return day > 0 && day <= monthLength[ month - 1 ];
    }, // isValidDate
    
    
    
    location2nr : function( location_value )
    {
      // with the _underscore library we would do: 
      // _.some(myArray, function(elem) {return elem.key == 'key1';});
      
      var location_nr =  "";
      var locations = this.HSN.locations;
      
      for( var l = 0; l < locations.length; l++ ) 
      {
        var location = locations[ l ];
        if( location.name === location_value ) { 
          location_nr = location.nr 
          break;
        }
      }
      return location_nr;
    }, // location2nr
    
    
    
    getUservalueCombobox : function( combobox, value, key )
    {
      var list = combobox.getChildControl( "list" );
      var item = null;
      var label = null;
      var user_value = "";
      if( value ) { item = list.findItem( value ); }  // findItem is case-insensitive
      if( item ) { 
        user_value = item.getUserData( key ); 
        label = item.getLabel();
      }
      var data = new Object();
      data.user_value = user_value;
      data.label = label;
      return data;
    }, // getUservalueCombobox
    
    
    
    /**
     * closeWindow
     */
    closeWindow : function( window_to_close, title, legend )
    {    
      console.debug( "closeWindow()" );
      
    //if( ! this.__windowClose )
    //{
        var width = 350;
        var dialog = this.__windowClose = new qx.ui.window.Window( title )
        .set({
          modal          : true,
          showMinimize   : false,
          showMaximize   : false,
          width          : width,
          contentPadding : [ 10, 10, 10, 10 ]
        });
        dialog.addListener( "resize", dialog.center );
        
        var layout = new qx.ui.layout.Grid( 15, 15 );
        layout.setRowFlex( 0, 1 );
        layout.setColumnFlex( 1, 1 );
        dialog.setLayout( layout );
        
        dialog.add
        (
          new qx.ui.basic.Image( "icon/32/status/dialog-information.png" ),
          { row : 0, column : 0 }
        );
        
        dialog.add
        ( 
          new qx.ui.basic.Label().set({
            rich       : true,
            allowGrowY : true,
            value      : legend
          }), 
          { row : 0, column : 1, colSpan : 2 }
        );
        
        var layoutButtons = new qx.ui.layout.HBox( 5 ).set({ AlignX : "center" });
        var containerButtons = new qx.ui.container.Composite( layoutButtons );
        dialog.add( containerButtons, { row : 1, column : 1 } );
        
        var buttonOK = new qx.ui.form.Button( "Ja" ).set({
          alignX     : "center",
          allowGrowX : false,
          padding    : [ 2, 10 ]
        });
        
        buttonOK.addListener
        (
          "execute", 
          function( ev ) { 
            console.debug( "closeWindow() OK" );
            window_to_close.close();
            dialog.close(); 
          }, 
          this
        );
        
        
        var buttonCancel = new qx.ui.form.Button( "Nee" ).set({
          alignX     : "center",
          allowGrowX : false,
          padding    : [ 2, 10 ]
        });
        
        buttonCancel.addListener
        (
          "execute", 
          function( ev ) { 
            console.debug( "closeWindow() Cancel" );
            dialog.close(); 
          }, 
          this
        );
        
        containerButtons.add( buttonCancel );
        containerButtons.add( new qx.ui.core.Spacer( 10 ) );
        containerButtons.add( buttonOK );
    //}
      
      this.__windowClose.getChildren()[ 1 ].setValue( legend );
      this.__windowClose.open();
    //this.__windowClose.getChildren()[ 2 ].focus();
    }, // closeWindow
    
    
    
    showDialog : function( text, title )
    {
      console.debug( "showDialog()" );
      console.debug( text );
      
    //if( ! this.__dialog )
    //{
        var dialog = this.__dialog = new qx.ui.window.Window( title ).set({
          modal          : true,
          showMinimize   : false,
          showMaximize   : false,
          width          : 400,
          contentPadding : [ 10, 10, 10, 10 ]
        });
        dialog.moveTo( 315, 100 );
        
        dialog.addListener( "appear", dialog.center );
        
        var layout = new qx.ui.layout.Grid( 15, 15 );
        layout.setRowFlex( 0, 1 );
        layout.setColumnFlex( 1, 1 );
        dialog.setLayout( layout );
        
        dialog.add
        (
          new qx.ui.basic.Image( "icon/32/status/dialog-information.png" ),
          { row : 0, column : 0 }
        );
        
        dialog.add
        ( 
          new qx.ui.basic.Label().set({
            rich       : true,
            allowGrowY : true
          }), 
          { row: 0, column: 1 }
        );
        
        var button = new qx.ui.form.Button( "OK" ).set({
          alignX     : "center",
          allowGrowX : false,
          padding: [ 2, 10 ]
        });
        
        button.addListener
        (
          "execute", 
          function( ev ) { dialog.close(); }, 
          this
        );
        
        dialog.add( button, { row : 1, column : 0, colSpan : 2 } );
    //}
      
      this.__dialog.getChildren()[ 1 ].setValue( text );
      this.__dialog.open();
      this.__dialog.getChildren()[ 2 ].focus();
    }, // showDialog
    
    
    
    // login related
    __windowLogin : null,
    __buttonLogin : null,
    
    createLogin : function()
    {
      console.debug( "createLogin()" );
      console.debug( "createLogin() this.timestamp_client: " + this.timestamp_client );
      
      // login windowLogin
      var layout = new qx.ui.layout.Grid( 9, 5 );
      layout.setColumnAlign( 0, "right", "top" );
      layout.setColumnAlign( 2, "right", "top" );
      
      var window = this.__windowLogin = new qx.ui.window.Window( "HSN - Mail en Beheer -- LDAP/Jira Login" ).
      set({
        modal          : true,
        width          : 255,
        contentPadding : [ 20, 20, 20, 20 ],
        showMinimize   : false,
        showMaximize   : false,
        showClose      : false,
        allowGrowX     : false,
        allowGrowY     : false,
        allowShrinkX   : false,
        allowShrinkY   : false,
        allowStretchX  : false,
        allowStretchY  : false
      });
      
      window.center();
      window.setLayout( layout );
      this.getRoot().add( window );
      window.open();
      
      window.addListener
      ( 
        "appear", function()
        {
          window.center();
          fieldUsername.setValue( this.test_usr );
          fieldPassword.setValue( this.test_pwd );
          
          fieldUsername.focus();           // so that user can start typing his/her name right away
        }, 
        this
      );
      
      // Labels
    //var labels = [ this.tr("Username") + ":", this.tr("Password") + ":" ];
      var labels = [ "Gebruikersnaam:", "Wachtwoord:" ];
      for( var i = 0; i < labels.length; i++ )
      {
        window.add( new qx.ui.basic.Label( labels[ i ] ).set({
          allowShrinkX : false,
          paddingTop   : 3
        }), { row : i, column : 0 });
      }
      
      // Text fields
      var fieldUsername = this._fieldUsername = new qx.ui.form.TextField()    .set({ width : 150 });
      var fieldPassword = this._fieldPassword = new qx.ui.form.PasswordField().set({ width : 150 });
      
      window.add( fieldUsername.set({
        allowShrinkX : false,
        paddingTop   : 3
      }), { row : 0, column : 1 });
      
      window.add( fieldPassword.set({
        allowShrinkX : false,
        paddingTop   : 3
      }), { row : 1, column : 1 });
      
      // PasswordField has no "execute" event
      fieldPassword.addListener
      (
        "keypress", 
        function( ev )
        {
          if( ev.getKeyIdentifier() === "Enter" ) { 
            window.close();
            this._doAuthenticate( ev ); 
          }
        }, 
        this
      );
      
      var layoutButtons = new qx.ui.layout.HBox( 5 ).set({ AlignX : "center" });
      var containerButtons = new qx.ui.container.Composite( layoutButtons );
      window.add( containerButtons, { row : 3, column : 1 } );
      
      // Cancel button
      var buttonCancel = this.__buttonCancel =  new qx.ui.form.Button( "Annuleren" );
      buttonCancel.setAllowStretchX( false );
      
      buttonCancel.addListener
      ( 
        "execute", 
        function( ev ) { window.close(); },
        this 
      );
      
      // Login button
      var buttonLogin = this.__buttonLogin =  new qx.ui.form.Button( "Aanmelden" );
      buttonLogin.setAllowStretchX( false );
      
      buttonLogin.addListener
      ( 
        "execute", 
        function( ev ) 
        { 
          window.close();
          this._doAuthenticate( ev ); 
        },
        this 
      );
      
      containerButtons.add( buttonCancel );
      containerButtons.add( new qx.ui.core.Spacer( 10 ) );
      containerButtons.add( buttonLogin );
      
    }, // createLogin
    
    
    
    _doAuthenticate : function( ev )
    {
      console.debug( "_doAuthenticate()" );
      console.debug( "_doAuthenticate() this.timestamp_client: " + this.timestamp_client );
      
      this._username = this._fieldUsername.getValue();
      this._password = this._fieldPassword.getValue();
      
      console.debug( "username :", this._username );
    //console.debug( "password :", this._password );
      
      if( this._username === null || this._password === null )
      { 
        this.__windowLogin.show();
        return;
      }
      
      var url = this.wsgi_url( "/login" );
      
      var method = this.wsgi_method;
      var params = "";
      
      if( method === "GET" )        // only for testing, 
      { params += "?"; }
      else if( method === "POST" )  // use POST for login.
      { url += '/'; }               // required: POST + Django: APPEND_SLASH
      
      //if( this.debugIE ) { params += "qxenv:qx.debug.io:true"; }
      
      if( method === "GET" )
      {
        params += "&usr=" + encodeURIComponent( this._username );
        params += "&pwd=" + encodeURIComponent( this._password );
      }
      else
      {
        params += "usr="  + encodeURIComponent( this._username );   // POST: without leading '?'
        params += "&pwd=" + encodeURIComponent( this._password );
      }
      
      if( method === "GET" ) { url += params; }
      console.debug( url );
      
      var request = new qx.io.request.Xhr( url );
      request.setMethod( method );
      
      if( method === "POST" )           // set parameters in data
      {
        request.setRequestHeader( "X-CSRFToken", qx.bom.Cookie.get( "csrftoken" ) );
        request.setRequestData( params ); 
      }
      
      request.addListener
      (
        "success",
        function( ev ) { this._AuthenticateResponse( ev ); },
        this
      );
      
      request.addListener
      (
        "fail",
        function( ev )
        {
          var request = ev.getTarget();
          
          var msg = "Authentication info:<br>failed, using:<br>host: " + this.prototocol + "://" + this.host + ", @ port: " + this.port;
          this.showDialog( msg );
          
          var response = request.getResponse();
          this.showDialog( response );
        },
        this
      );
      
      request.addListener
      ( 
        "statusError", 
        function( ev ) 
        {
          var request = ev.getTarget();
          
          var msg = "Authentication info:<br>statusError, using:<br>host: " + this.prototocol + "://" + this.host + ", @ port: " + this.port;
          this.showDialog( msg );
          
          var response = request.getResponse();
          this.showDialog( response );
        }, 
        this 
      );
      
      request.send();             // Send the request
      
    }, // _doAuthenticate
    
    
    
    _AuthenticateResponse : function( ev )
    {
      console.debug( "_AuthenticateResponse()" );
      console.debug( "_AuthenticateResponse() this.timestamp_client: " + this.timestamp_client );
      
      this.io_login = this.IO_SUCCESS;
      var request = ev.getTarget();
      
      // Response parsed according to the server's response content type, e.g. JSON
      var json_data = request.getResponse();
      console.debug( json_data );
      
      console.debug( "csrftoken: " + qx.bom.Cookie.get( "csrftoken" ) );
      console.debug( "sessionid: " + qx.bom.Cookie.get( "sessionid" ) );
      
      var content_type = request.getResponseContentType();
      console.debug( "content_type: " + content_type );
      if( content_type !== "application/json" )
      { 
        var msg = "unexpected response:<br>" + request.getResponseText();
        this.showDialog( msg );
      //this.createAlert( msg ); // unparsed
      }   
      
      var resp_status = json_data.status;
      console.log( "resp_status: " + resp_status );
      this.timestamp_server = json_data.timestamp;
      this.info( "timestamp_server: " + this.timestamp_server );
      
      if( resp_status === "ok" )
      {
      //this.showDialog( this.tr( "Welcome" ) + " " + this._username );
        this.getHsnData();    // get 'static' data; then create and fill the windows
      }
      else
      {
        var server_msg = json_data.msg;
        var msg = "Authentication";
        msg += "<br><br>Server response: " + resp_status;
        msg += "<br>Message: " + server_msg;
      //msg += "<br><br>You can retry to login by reloading the page.";
        var title = "HSN - Mail en Beheer";
        this.showDialog( msg, title );
        
        this.__windowLogin.show();
      }
      
      if( this.timestamp_client !== this.timestamp_server )
      { 
        var msg = "client/server timestamp mismatch<br>version " + this.timestamp_client + " client<br>version " + this.timestamp_server + " server<br><br> This can be an innocent oversight, or it could imply a potential problem. Start with flushing your browser cache, and restarting the browser.";
        this.showDialog( msg );
      }
      
    }, // _AuthenticateResponse
    
    
    
    createLogout : function( ev )
    {
      console.debug( "createLogout()" );
    //var msg = "Afmelden van <b>" + this._username + "</b> ...";
    //this.showDialog( msg );
    //this.__windowLogout.show();
      
      // logout windowLogout
      var layout = new qx.ui.layout.Grid( 1, 1 );
      layout.setColumnAlign( 0, "center", "center" );
      
      var window = this.__windowLogout = new qx.ui.window.Window( "HSN - Mail en Beheer -- Logout" ).
      set({
        modal          : true,
        width          : 255,
        contentPadding : [ 20, 20, 20, 20 ],
        showMinimize   : false,
        showMaximize   : false,
        allowGrowX     : false,
        allowGrowY     : false,
        allowShrinkX   : false,
        allowShrinkY   : false,
        allowStretchX  : false,
        allowStretchY  : false
      });
      
      window.center();
      window.setLayout( layout );
      this.getRoot().add( window );
      window.open();
      
      var msg = "Afmelden van <b>" + this._username + "</b> ...";
      var label = new qx.ui.basic.Label( msg ).set({
          allowShrinkX : false,
          paddingTop   : 3,
          rich         : true
        });
      window.add( label, { row : 0, column : 0 });
      
      var url = this.wsgi_url( "/logout" );
      
      var method = this.wsgi_method;
      var params = "";
      
      if( method === "GET" )        // only for testing, 
      { params += "?"; }
      else if( method === "POST" )  // use POST for login.
      { url += '/'; }               // required: POST + Django: APPEND_SLASH
      
      //if( this.debugIE ) { params += "qxenv:qx.debug.io:true"; }
      
      if( method === "GET" )
      {
        params += "&usr=" + encodeURIComponent( this._username );
      //params += "&pwd=" + encodeURIComponent( this._password );
      }
      else
      {
        params += "usr="  + encodeURIComponent( this._username );   // POST: without leading '?'
      //params += "&pwd=" + encodeURIComponent( this._password );
      }
      
      if( method === "GET" ) { url += params; }
      console.debug( url );
      
      var request = new qx.io.request.Xhr( url );
      request.setMethod( method );
      
      if( method === "POST" )           // set parameters in data
      { 
        request.setRequestHeader( "X-CSRFToken", qx.bom.Cookie.get( "csrftoken" ) );
        request.setRequestData( params ); 
      }
      
      request.addListener
      (
        "success",
        function( ev ) {
          console.debug( "Logout: success" );
          this.__windowLogout.close();
          this.__windowLogin.open();
        },
        this
      );
      
      request.addListener
      (
        "fail",
        function( ev )
        {
          console.debug( "Logout: fail" );
          this.__windowLogout.close();
          
          var request = ev.getTarget();
          var msg = "Logout info:<br>failed, using:<br>host: " + this.prototocol + "://" + this.host + ", @ port: " + this.port;
          this.showDialog( msg );
          
          var response = request.getResponse();
          this.showDialog( response );
        },
        this
      );
      
      request.addListener
      ( 
        "statusError", 
        function( ev ) 
        {
          console.debug( "Logout: fail" );
          this.__windowLogout.close();
          
          var request = ev.getTarget();
          var msg = "Logout info:<br>statusError, using:<br>host: " + this.prototocol + "://" + this.host + ", @ port: " + this.port;
          this.showDialog( msg );
          
          var response = request.getResponse();
          this.showDialog( response );
        }, 
        this 
      );
      
      request.send();             // Send the request
      
    } // createLogout
      
  } // members
});

