#! /usr/bin/env python
import poplib, re, getpass,os

#constantes
POP_SERVER = 'pop.gmail.com'
POP_USER = 'louis.poirel'
PATH = '/media/LOUIS_16GO/mailsd/junk'

# On se place dans le dossier
chemin = raw_input('Dans quel dossier doit-on enregistrer les mails ?\n(' + PATH + ') ')
if not reponse : chemin = PATH
print ' -> ' + chemin
os.chdir(chemin)

# On cherche le plus haut numero deja present dans le dossier, et sinon on met 0
compteur=max([int(x) for x in ['0'] + os.listdir(chemin) if x[0] in str(range(10))])

# On cree la connexion avec le serveur
pop = poplib.POP3_SSL(POP_SERVER)
print 'Connecte a ' + POP_SERVER
print pop.user(POP_USER)
print pop.pass_(getpass.getpass())

# On telecharge la liste des mails
lis = pop.list()
nmail = len(lis[1]);
print lis[0], '\n' + '\n'.join(lis[1])
messages = [[i, lis[1][i].split()[1], '---', '---', [], str(compteur + 1 + i)] for i in range(nmail)]

# On choisit l'action à accomplir sur chaque mail
while 1:
    for m in messages: 
        print '\n', m[0:4], '\n'
        reponse = raw_input('top (t), telecharge (d), supprime (s), passe (p) ?')
        if reponse in 'tT' :
            m[2] = ['top']
            m[4] = pop.top(m[0]+1,10)[1]         
            for ligne in m[4] : print ligne
            f = open(m[5],'w')
            for l in m[4] : f.write(l+'\n')
            f.close()
            print m[0:4],'\n'
            reponse = raw_input('telecharge (d), supprime (s), passe (p) ?')
        if reponse in 'dD':
            m[2] = ['tel']
            texte = pop.retr(m[0]+1)[1]
            m[4] = texte[1:10]
            for ligne in m[4] : print ligne
            f = open(m[5],'w')
            for l in texte : f.write(l+'\n')
            f.close()
        if reponse in 'sS':
            m[3] = 'sup'
            pop.dele(m[0] + 1)
        print m[0:4], '\n'
    print '\n' * 3
    for m2 in messages: 
        print m2[0:4]
    reponse = raw_input('quitte (q) reste (r) annule les suppressions (a) ?')
    if reponse in 'qQ':
        break
    if reponse in 'aA':
        pop.rset()
        for m2 in messages:m2[3] = '---'
pop.quit()
