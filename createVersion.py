from jira import JIRA
import random

# Nombre del proyecto
projectKey = "ELQ"
year = 20
createVersions = False
createComponents = False
deleteComponents = False
createIssues = True

# Generador de Issues
a = ("Mejorar", "Solucionar", "Optimizar", "Crear", "Habilitar", "Eliminar")
b = ("soporte", "formulario", "configuracion", "acceso", "consulta", "edicion", "jobs")
c = ("frontal", "back", "GUI", "trazas", "monitorizacion", "performance", "crontab")
d = ("de Wordpress", "de Redis", "del balanceador", "de la base de datos", "de WebSphere", "de shell-scripts", "de WebLogic", "de Dynatrace")
l = [a, b, c, d]

# Generador de Componentes
componentsList = ["db", "redis", "tutorial", "result", "vote", "worker"]

jira = JIRA("http://localhost:8082", basic_auth=('jcla', 'jcla'))

def gettingComponentes(project):
    componentsAvailables = jira.project_components(project)
    return componentsAvailables

def componentsToCreate(project, components):
    componentsAvailables = gettingComponentes(project)
    for myComps in componentsAvailables:
        if myComps.name in components:
            components.remove(myComps.name)
    return components

# Creacion de versiones
for month in range(12):
    month = month + 1
    days = 30
    if month in [1, 3, 5, 7, 8, 10, 12]:
        days = 31
    if month == 2:
        days = 29
    prefix = ""
    if month < 10:
        prefix = "0"
    monthStr = "{0}{1}".format(prefix, month)
    version = "{0}.{1}".format(year,monthStr)
    endDate = "{0}{1}-{2}-{3}".format("20", year, monthStr, days)
    createVersions and jira.create_version(version, projectKey, releaseDate=endDate)


# Creacion de componentes
for component in componentsToCreate(projectKey, componentsList):
    createComponents and jira.create_component(component, projectKey)
    print("------------>> " + component)

# Eliminacion de componentes
for myComponent in gettingComponentes(projectKey):
    deleteComponents and jira.delete_component(myComponent.id)

# Obtener descripcion aleatoria
def getIssueDescription():
    return " ".join([random.choice(i) for i in l])

# Creacion de issues
for i in range(5):
    fields = {
            "project": {
                "key": "ELQ"
            },
            "summary": getIssueDescription(),
            "description": getIssueDescription(),
            "issuetype": {
                "name": "Nueva función"
            },
            "fixVersions": [{"name": "20.10"}],
            "components": [{"name": "redis"}, {"name": "vote"}],
        }
    print("Creando issue = {0}".format(i))
    createIssues and jira.create_issue(fields=fields)




# print(random.sample(componentsList, random.choice(range(1, 3))))
