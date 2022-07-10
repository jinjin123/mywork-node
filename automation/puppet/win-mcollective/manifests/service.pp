class win-mcollective::service {
    service { 'mcollectived':
     ensure  => running,
     enable  => true,
     require => Class['win-mcollective::config'],
    }
}
