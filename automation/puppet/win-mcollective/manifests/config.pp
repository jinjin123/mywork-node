class win-mcollective::config {
    file { 'C:\\Progra~1\\mcollective\\etc\\server.cfg':
         ensure  => present,
         content => template("win-mcollective/server.cfg.erb"),
         notify  => Class['win-mcollective::service'],
         require => Class['win-mcollective::install'],
    }
}
