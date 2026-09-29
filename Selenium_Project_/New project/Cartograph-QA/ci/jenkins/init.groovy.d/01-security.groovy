#!groovy
import hudson.security.FullControlOnceLoggedInAuthorizationStrategy
import hudson.security.HudsonPrivateSecurityRealm
import jenkins.install.InstallState
import jenkins.model.Jenkins

def instance = Jenkins.get()
if (instance.getSecurityRealm() instanceof HudsonPrivateSecurityRealm && instance.getSecurityRealm().getAllUsers().any { it.id == 'admin' }) {
    return
}

def realm = new HudsonPrivateSecurityRealm(false)
realm.createAccount('admin', 'CartographQA!2026')
instance.setSecurityRealm(realm)

def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
strategy.setAllowAnonymousRead(false)
instance.setAuthorizationStrategy(strategy)
instance.setNumExecutors(2)
instance.setInstallState(InstallState.INITIAL_SETUP_COMPLETED)
instance.save()
println 'Cartograph Jenkins admin user is ready.'
