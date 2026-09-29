#!groovy
import com.cloudbees.plugins.credentials.CredentialsScope
import com.cloudbees.plugins.credentials.SystemCredentialsProvider
import com.cloudbees.plugins.credentials.domains.Domain
import com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl
import jenkins.model.Jenkins
import org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition
import org.jenkinsci.plugins.workflow.job.WorkflowJob

def qaRoot = 'C:\\Users\\User\\Downloads\\New project\\Cartograph-QA'
def envFile = new File(qaRoot, '.env')
def email = 'demo@example.com'
def password = 'change-me'
if (envFile.exists()) {
    envFile.readLines().each { line ->
        if (line.startsWith('AE_EMAIL=')) { email = line.substring('AE_EMAIL='.length()).trim() }
        if (line.startsWith('AE_PASSWORD=')) { password = line.substring('AE_PASSWORD='.length()).trim() }
    }
}

def store = SystemCredentialsProvider.instance.store
def domain = Domain.global()
def existing = store.getCredentials(domain).find { it.id == 'automation-exercise-test-user' }
if (existing) {
    store.removeCredentials(domain, existing)
}
store.addCredentials(domain, new UsernamePasswordCredentialsImpl(
    CredentialsScope.GLOBAL,
    'automation-exercise-test-user',
    'Automation Exercise dedicated test account',
    email,
    password
))

def jenkins = Jenkins.get()
def jobName = 'Cartograph-QA'
def jenkinsfile = new File(qaRoot, 'Jenkinsfile').text
def job = jenkins.getItem(jobName)
if (job == null) {
    job = jenkins.createProject(WorkflowJob, jobName)
}
job.setDescription('Live Robot Framework pipeline for the Cartograph QA capstone.')
job.setDefinition(new CpsFlowDefinition(jenkinsfile, true))
job.save()
println "Pipeline job ${jobName} is ready."
