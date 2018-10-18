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

        components.each {
            def plugin_resource_url = new URL(it['plugin_resource_url'])
            def plugin_resource = new JsonSlurperClassic().parse(pluginsUrl)
            def plugin_name = plugin_resource['name']
            def plugin_owner = plugin_resource['owner']['username']
            def plugin_version = plugin_resource['version']

            sh "echo confluent-hub install --no-prompt ${plugin_owner}/${plugin_name}:${plugin_version}"
        }

    }
}
