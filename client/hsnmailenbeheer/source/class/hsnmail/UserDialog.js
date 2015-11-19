
qx.Class.define(
  "hsnmailenbeheer.UserDialog",
  {
    extend: qx.ui.window.Window,
    events: { "changeUserData": "qx.event.type.Data"},
    construct: function () 
    {
      this.base(arguments, this.tr("User info"));

      // Layout
      var layout = new qx.ui.layout.Basic();
      this.setLayout( layout );
      this.setModal( true );

      this.__form = new qx.ui.form.Form();

      // User id field
      var usrId = new qx.ui.form.TextField();
      this.__form.add( usrId, this.tr( "Username" ), null, "Id" );

      // User password field
      var usrPassword = new qx.ui.form.PasswordField();
      usrPassword.setRequired( true );
      this.__form.add( usrPassword, this.tr( "Password"), null, "Password");

      // Adding form controller and model
      var controller = new qx.data.controller.Form( null, this.__form );
      this.__model = controller.createModel();

      // Save button
      var okbutton = new qx.ui.form.Button( this.tr( "Ok" ) );
      this.__form.addButton( okbutton );
      okbutton.addListener( "execute", function () 
      {
        if (this.__form.validate()) {
          var usrData = qx.util.Serializer.toJson( this.__model );
          this.fireDataEvent( "changeUserData", usrData );
          this.close();
        };
      }, this );

      // Cancel button
      var cancelbutton = new qx.ui.form.Button( this.tr( "Cancel" ) );
      this.__form.addButton( cancelbutton );
      cancelbutton.addListener( "execute", function () {
          this.close();
      }, this );

      var renderer = new qx.ui.form.renderer.Single( this.__form );
      this.add( renderer );
    }
  }
);
