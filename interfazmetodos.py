import streamlit as st 
from sympy import symbols, Eq, solve, Matrix

# Función para resolver por sustitución
def metodo_sustitucion(ecuaciones, variables):
    pasos = []
    soluciones = solve(ecuaciones, variables)
    for i, eq in enumerate(ecuaciones):
        pasos.append(f"Paso {i + 1}: Usamos la ecuación {eq} para despejar variables.")
    pasos.append("Finalmente, resolvemos el sistema completo:")
    for var, val in soluciones.items():
        pasos.append(f"{var} = {val}")
    return pasos, soluciones

# Función para resolver por Gauss-Jordan
def metodo_gauss_jordan(coeficientes, independientes):
    pasos = []
    matriz = Matrix([fila + [ind] for fila, ind in zip(coeficientes, independientes)])
    pasos.append(f"Matriz inicial aumentada:\n{matriz}")
    matriz_reducida, pivotes = matriz.rref()
    pasos.append(f"Matriz escalonada reducida:\n{matriz_reducida}")
    soluciones = [matriz_reducida[i, -1] for i in range(matriz_reducida.rows)]
    for i, sol in enumerate(soluciones):
        pasos.append(f"x{i + 1} = {sol}")
    return pasos, soluciones

# Función para resolver por regla de Cramer
def metodo_cramer(coeficientes, independientes):
    pasos = []
    matriz_coeficientes = Matrix(coeficientes)
    matriz_independientes = Matrix(independientes)
    det_coeficientes = matriz_coeficientes.det()

    if det_coeficientes == 0:
        pasos.append("El sistema no tiene solución única porque el determinante de la matriz de coeficientes es 0.")
        return pasos, "El sistema no tiene solución única."

    pasos.append(f"Determinante de la matriz de coeficientes (A): {det_coeficientes}")
    soluciones = []
    for i in range(len(coeficientes)):
        matriz_sustituida = matriz_coeficientes.copy()
        matriz_sustituida[:, i] = matriz_independientes
        det_sustituida = matriz_sustituida.det()
        pasos.append(f"Matriz con columna {i + 1} sustituida:\n{matriz_sustituida}")
        pasos.append(f"Determinante de la matriz modificada: {det_sustituida}")
        soluciones.append(det_sustituida / det_coeficientes)
        pasos.append(f"x{i + 1} = {det_sustituida} / {det_coeficientes} = {soluciones[-1]}")

    return pasos, soluciones

# Interfaz de Streamlit
st.title("Resolución de Sistemas de Ecuaciones")
st.write("Esta aplicación resuelve sistemas de ecuaciones utilizando los métodos de Sustitución, Gauss-Jordan y Regla de Cramer.")

# Entrada: Número de ecuaciones
num_ecuaciones = st.number_input("Número de ecuaciones:", min_value=2, step=1)

if num_ecuaciones:
    # Entrada: Coeficientes y términos independientes
    st.write("Ingrese los coeficientes y términos independientes:")

    coeficientes = []
    terminos_independientes = []

    for i in range(num_ecuaciones):
        st.write(f"Ecuación {i + 1}:")
        fila = [st.number_input(f"Coeficiente de x{j + 1} (Ecuación {i + 1}):", key=f"coef_{i}_{j}") for j in range(num_ecuaciones)]
        coeficientes.append(fila)
        terminos_independientes.append(st.number_input(f"Término independiente (Ecuación {i + 1}):", key=f"indep_{i}"))

    # Selección del método
    metodo = st.selectbox("Seleccione el método para resolver:", ["Sustitución", "Gauss-Jordan", "Regla de Cramer"])

    if st.button("Resolver"):
        variables = symbols(' '.join([f'x{i + 1}' for i in range(num_ecuaciones)]))

        if metodo == "Sustitución":
            ecuaciones = []
            for i in range(num_ecuaciones):
                ecuacion = Eq(sum(coeficientes[i][j] * variables[j] for j in range(num_ecuaciones)), terminos_independientes[i])
                ecuaciones.append(ecuacion)
            pasos, soluciones = metodo_sustitucion(ecuaciones, variables)

        elif metodo == "Gauss-Jordan":
            pasos, soluciones = metodo_gauss_jordan(coeficientes, terminos_independientes)

        elif metodo == "Regla de Cramer":
            pasos, soluciones = metodo_cramer(coeficientes, terminos_independientes)

        # Mostrar los pasos y las soluciones
        st.write("### Pasos del cálculo:")
        for paso in pasos:
            st.write(paso)

        st.write("### Soluciones:")
        if isinstance(soluciones, str):
            st.write(soluciones)
        else:
            for i, solucion in enumerate(soluciones):
                st.write(f"x{i + 1} = {solucion}")
