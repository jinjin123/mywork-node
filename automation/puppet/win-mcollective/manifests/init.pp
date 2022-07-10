class win-mcollective{
     $activemq_server = "puppetmaster.kisspuppet.com"
     $mcollective_password = "mcopwd123"
     $mcollective_path 	  = "C:\Program Files\mcollective"
     include win-mcollective::install,win-mcollective::config,win-mcollective::service 
}
