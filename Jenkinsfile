import groovy.json.JsonSlurperClassic

properties([
        buildDiscarder(logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '', numToKeepStr: '10'))
])

//triggers {
//    upstream(upstreamProjects: "jcustenborder/connect-utils/job/master", threshold: hudson.model.Result.SUCCESS)
//}

node {
    stage('checkout') {
        deleteDir()
        checkout scm
    }

    stage('generate') {
        def pluginsUrl = new URL("https://api.hub.confluent.io/api/plugins/jcustenborder")
        def components = new JsonSlurperClassic().parse(pluginsUrl)
        def baseVersion = '5.0.0'

        def dockerFileText = "FROM confluentinc/cp-kafka-connect:${baseVersion}\n" +
                'ENV CONNECT_PLUGIN_PATH="/usr/share/java,/usr/share/confluent-hub-components"\n'

        components.each {
            def plugin_resource_url = new URL(it['plugin_resource_url'])
            def plugin_resource = new JsonSlurperClassic().parse(plugin_resource_url)
            def plugin_name = plugin_resource['name']
            def plugin_owner = plugin_resource['owner']['username']
            def plugin_version = plugin_resource['version']
            dockerFileText += "RUN confluent-hub install --no-prompt ${plugin_owner}/${plugin_name}:${plugin_version}\n"
        }

        writeFile encoding: 'UTF-8', file: 'Dockerfile', text: dockerFileText
        archiveArtifacts 'Dockerfile'
    }

    def image

    stage('build') {
        image = docker.build('jcustenborder/kafka-connect-all')
    }

    stage('publish') {
        image.push "${env.BUILD_NUMBER}"
        image.push "latest"
    }
}
