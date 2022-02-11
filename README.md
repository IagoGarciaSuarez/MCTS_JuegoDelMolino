# game-p1
Repositorio dedicado a la realización de la práctica de Diseño de Algoritmos 2022.

La práctica consistirá en la implementación de un juego que deberá ser:

- Determinista.
- Totalmente observable.
- De estrategia.
- Multijugador.
- Por turnos.
- De tablero.

## Autores
- Iago García Suárez
- Celia Díaz Fernández
- Carlos Almodóvar Román
- David Illescas Herrera

## Definición y Explicación del juego
Se ha elegido el [**Juego del Molino**](https://es.wikipedia.org/wiki/Juego_del_molino) como objetivo:

- Existen distintas variantes. Para un caso inicial se escogerá la variante de 9 piezas.
- El tablero consta de 24 posiciones distintas.
- 2 jugadores.
- Cada jugador dispone de 9 fichas.
- Inicialmente, el tablero está vacío.
- 1 movimiento por turno.
- Reglas:
    - Al inicio, cada jugador puede situar una ficha por turno en cualquier posición libre del tablero.
    - Sólo cuando estén todas las fichas colocadas en el tablero, se podrán mover de posición. El movimiento se puede realizar a las posiciones adyacentes conectadas. Cuando el jugador que tiene el turno disponga de 3 fichas, podrá mover cualquier ficha a cualquier posición libre.
    - Cada vez que se consiga alinear 3 fichas del mismo color, el jugador correspondiente a esas fichas podrá elegir una ficha del jugador contrario para eliminarla, exceptuando aquellas que estén formando un molino, a menos que no haya ninguna otra disponible.
    - Un jugador pierde cuando disponga de menos de 3 fichas.
