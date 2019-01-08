'docker run -d --env ENVT=%s --env PROJ=%s --restart=always --name=%s -p 80:80 %s' % (
    self.environment_name, self.project_name, self.project_name, self.image_url)
