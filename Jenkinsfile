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

        def dockerFile = new File("Dockerfile");
        def baseVersion = '5.0.0'
        dockerFile.withWriter('UTF-8') { writer ->
            writer.write("FROM confluentinc/cp-kafka-connect:${baseVersion}\n")
            writer.write('ENV CONNECT_PLUGIN_PATH="/usr/share/java,/usr/share/confluent-hub-components"\n')

            components.each {
                def plugin_resource_url = new URL(it['plugin_resource_url'])
                def plugin_resource = new JsonSlurperClassic().parse(plugin_resource_url)
                def plugin_name = plugin_resource['name']
                def plugin_owner = plugin_resource['owner']['username']
                def plugin_version = plugin_resource['version']
                writer.write(
                        "RUN confluent-hub install --no-prompt ${plugin_owner}/${plugin_name}:${plugin_version}"
                )
            }
        }

        archiveArtifacts 'Dockerfile'
    }
}
