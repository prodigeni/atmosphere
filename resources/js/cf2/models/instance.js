Atmo.Models.Instance = Atmo.Models.Base.extend(
  {
    defaults: { 'model_name': 'instance' },
    initialize: function() {
      this.set('name_or_id', this.get('name') || this.get('id'));
      this.set('launch_relative', Atmo.Utils.relative_time(this.get('launch_time')));
    },
    parse: function(response) {
      //console.log(response);
      var attributes = response;
      attributes.description = response.name;
      attributes.id = response.alias;
      attributes.name = response.name;
      attributes.image_id = response.machine_alias;
      attributes.image_name = response.machine_name;
      attributes.image_hash = response.alias_hash;
      attributes.image_url = Atmo.profile.get_icon(response.machine_alias_hash);
      attributes.type = response.size_alias;
      attributes.launch_time = new Date(response.start_date);
      //attributes.launch_relative = Atmo.Utils.relative_time(response.start_date); 
      attributes.state = response.status;
      attributes.state_is_active = (   response.status == 'active'
                            || response.status == 'running' );
      attributes.state_is_build = (    response.status == 'building'
	  						|| response.status == 'building - spawning'
							|| response.status == 'building - networking' 
							|| response.status == 'pending' );
      attributes.state_is_delete = (    response.status == 'delete'
	  						|| response.status == 'active - deleting'
							|| response.status == 'deleted'
						    || response.status == 'shutting-down'
						    || response.status == 'terminated' );
      attributes.private_dns_name = response.ip_address;
      attributes.public_dns_name = response.ip_address;
      return attributes;
    },
    confirm_terminate: function(options) {
      
      var header = "Are you sure you want to terminate this instance?";
      var body = '<p class="alert alert-error"><i class="icon-warning-sign"></i> <b>WARNING</b> Unmount volumes within your instance before terminating or risk corrupting your data and the volume.</p>';
      body += "<p>Your instance <strong>" + this.get('name') + " #" + this.get('id') + "</strong> will be shut down and all data will be permanently lost!</p>";
      body += "<p><u>Note:</u> Your resource usage charts will not reflect changes until the instance is completely terminated and has disappeared from your list of instances.</p>";
      var self = this;
      
      Atmo.Utils.confirm(header, body, {
	on_confirm : function() {
	  self.destroy({
	    wait: true, 
	    success: options.success,
	    error: options.error
	  });
	},
        ok_button: 'Yes, terminate this instance'
      });
  
    },
    select: function() {
        this.collection.select_instance(this);
    }
  });

_.extend(Atmo.Models.Instance.defaults, Atmo.Models.Base.defaults);
