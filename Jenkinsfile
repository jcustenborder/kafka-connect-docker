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
            sh "echo ${it['plugin_resource_url']}"
        }

    }
}