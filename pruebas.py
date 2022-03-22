
#def seleccionar(T: Nodo){
#   Si terminal(T) or TieneHijosSinExpandir(T)
#       return T
#   SiNo
#       return Select(Hijo con mayor UCT(nt))
# }

#def expandir(n){
#   Si n no tiene hijos
#       return n
#   SiNo
#       accion <- decisionAleatoria(nt, hijo SE)
#       nuevonodo <- realizarLaAccion(accion)en nt# 
#       eliminar accion vector hijos SE
#       dic[accion]=nuevono
#       return nuevonodo
# }

#def simular()

#def retropropagacion(nt, valor){
#   nt:victoria[valor] +=1 
#   nt:nºvisitas +=1
#   aux <- nt:padre
#   Mientras aux != None
#      aux:nv +=1
#      aux:vict[valor]+=1
#      aux <-aux:padre
#   return nt
# }

#Mientras haya recursos{
#   n <- seleccionar(T)
#   n1 <- expandir(n)
#   valor <- simular(n1)
#   nt <- retropropagacion(nt, valor)
#   ActualizarRecursos
#   }
#con esto conseguimos una estimacion de los hijos de la raiz, para poder elegir según el criterio que yo ponga(el más común: el que más victoria tenga(greedy)pero poner UCT)



#n = nodo
#valor= 0 empate, 1 jugador1 gana, 2 jugador2 gana

