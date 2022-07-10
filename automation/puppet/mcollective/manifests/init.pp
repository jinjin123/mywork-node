class mcollective{
    $activemq_server = "puppetmaster.kisspuppet.com"
    $mcollective_password = "mcopwd123"
    
    package { ['mcollective','mcollective-puppet-agent','mcollective-service-agent']:
        ensure => installed,
    }
    service { 'mcollective':
        ensure  => running,
        enable  => true,
        require => Package['mcollective'],
    }
    #通过SVN提交的，需要过滤.svn目录
    file { '/etc/mcollective':
        ensure  => directory,
        source  => 'puppet:///modules/mcollective/pem',
        ignore  => '.svn',
        owner   => root,
        group   => root,
        mode    => '0640',
        recurse => remote,
        notify  => Service['mcollective'],
    }
    file { '/etc/mcollective/server.cfg':
        ensure  => file,
        owner   => root,
        group   => root,
        mode    => 400,
        content => template("mcollective/server.cfg.erb"),
        notify  => Service['mcollective'],
    }
}
