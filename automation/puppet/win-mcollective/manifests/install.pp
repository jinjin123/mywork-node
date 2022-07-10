class win-mcollective::install {
    if $operatingsystem == "windows" {
        $filepath   = "C:/Users/Administrator/Downloads"
        $installdir   = "C:/Program Files"
        Exec{ path => ["${installdir}/Ruby193/bin","C:/Windows/system32","${installdir}/Puppet Labs/Puppet/bin" ] }
        
        #安装ruby
        file { 'ruby':
            path    => "${filepath}/rubyinstaller-1.9.3-p551.exe",
            ensure  => file,
            owner   => 'Administrator',
            mode    => '0755',
            group   => 'Administrators',
            source  => 'puppet:///modules/win-mcollective/rubyinstaller-1.9.3-p551.exe',
        }
        exec { 'ruby':
            command => 'cmd.exe /c Start "puppet-install" /w "C:/Users/Administrator/Downloads/rubyinstaller-1.9.3-p551.exe" /SILENT /DIR="C:/Program Files/Ruby193"',
            provider => 'windows',
            creates     => "${installdir}/Ruby193/bin/ruby.exe",
            require=> File['ruby'],
        }
    
        #安装mcollective
        file { 'mcollective':
            path    => "${filepath}/mcollective_2_3_2_Setup.exe",
            ensure  => file,
            owner   => 'Administrator',
            mode    => '0755',
            group   => 'Administrators',
            source  => 'puppet:///modules/win-mcollective/mcollective_2_3_2_Setup.exe',
        }
        exec { 'mcollective':
            command  => 'cmd.exe /c Start "puppet-install" /w "C:/Users/Administrator/Downloads/mcollective_2_3_2_Setup.exe" /SILENT /DIR="C:/Program Files/mcollective"',
            provider => 'windows',
            creates  => "${installdir}/mcollective/bin/mco.bat",
            require  => File['mcollective'],
        }
        
        # 安装gem包
        exec { 'install_gems':
            command  => 'cmd.exe /c gem install -l -f "C:/Program Files/mcollective/gems/*.gem"',
            provider => 'windows',
            unless   => 'cmd.exe /c gem list --local | findstr win32-dir',
            require  => [Exec['ruby'],Exec['mcollective']],
        }
        # 安装服务
        exec { 'install_service':
            command  => 'cmd.exe /c C:/Progra~1/mcollective/bin/register_service.bat',
            provider => 'windows',
            unless   => 'cmd.exe /c net start | find "The Marionette Collective"',
            require  => Exec['install_gems'],
        }
        #puppet插件和aq连接认证文件
        file { "${installdir}/mcollective/plugins/mcollective":
            ensure  => directory,
            ignore  => '.svn',
            source_permissions => ignore,
            source  => 'puppet:///modules/win-mcollective/mcollective-puppet-agent-1.6.1',
            recurse => true,
            require => Exec['mcollective'],
        }
        file { "${installdir}/mcollective/etc/ssl":
        ensure  => directory,
        ignore  => '.svn',
        source_permissions => ignore,
                source  => 'puppet:///modules/win-mcollective/pem',
                recurse => true,
        require => Exec['mcollective'],
        }
	file{ "${installdir}/mcollective/plugins/mcollective/agent/":
	ensure =>  directory,
	source_permissions => ignore,
		source => 'puppet:///modules/win-mcollective/agent/',
	require => Exec['mcollective'],
	}
	file{ "${installdir}/mcollective/plugins/mcollective/application/":
	ensure =>  directory,
	source_permissions => ignore,
		source => 'puppet:///modules/win-mcollective/server/',
	require => Exec['mcollective'],
	}
    }
}
