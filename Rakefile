require 'octokit'


task :generate do
  Octokit.auto_paginate = true
  client = Octokit::Client.new(:access_token => ENV['TOKEN'])

  download_urls=[]
  package_versions = {}
  client.repos('jcustenborder').each do |repository|
    if repository.has_downloads && repository.name =~ /^kafka-connect-/
      project_type = nil

      if repository.name =~ /^kafka-connect-transform-/
        project_type = "transformations"
      else
        project_type = "connectors"
      end


      latest_release = nil
      begin
        latest_release = client.latest_release(repository.full_name)
        latest_release.assets.each do |asset|
          if asset.name  =~ /\.tar\.gz$/
            puts "Adding #{repository.full_name}"
            download_urls << asset.browser_download_url
            package_versions[repository.full_name] = {
                'version' => latest_release.tag_name,
                'project_url' => repository.html_url,
                'docs_url' => "https://jcustenborder.github.io/kafka-connect-documentation/projects/#{repository.name}/#{project_type}.html"
            }
          end
        end
      rescue Octokit::NotFound

      end
    end
  end

  download_urls.sort

  File.open('Dockerfile', 'w') do |f|
    f << "FROM confluentinc/cp-kafka-connect\n"
    f << "ENV CONNECT_PLUGIN_PATH='/usr/share/java,/usr/share/kafka-connect'\n\n"

    download_urls.each do |download_url|
      f << "RUN curl -Ls #{download_url} | tar -xzC /\n"
    end
  end

  File.open('README.md', 'w') do |f|
    f << "| Project | Version | Documentation | Source |\n"
    f << "|---------|---------|---------------|--------|\n"
    package_versions.each do |project, info|
      f << "| #{project} | #{ info['version'] } | [Documentation](#{info['docs_url']}) | [Source](#{info['project_url']}) |\n"
    end
  end

end