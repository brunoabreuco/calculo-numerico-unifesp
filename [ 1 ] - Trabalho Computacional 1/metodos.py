def bisseccao(f, a, b, eps=1e-8, max_iter=200):
    # Validação de entrada: A bissecção deve levantar ValueError se f(a) · f(b) ≥ 0.
    if f(a) * f(b) >= 0:
        raise ValueError

    # Chute inicial do x_k
    xk_previous = a 

    # Histórico de iterações.
    historic = []

    # Itera até atingir o número máximo de iterações. De 1 até max_iter+1 para melhor visualização do número de iterações.
    for k in range(1, max_iter+1):
        # Cálculo do x_k
        xk = (a+b)/2

        # Cálculo do erro absoluto
        error = abs(xk - xk_previous)

        # Cálculo de f(x_k), para evitar chamar f() desnecessariamente
        fxk = f(xk)

        # Adiciona a iteração atual ao histórico
        historic.append({"k": k, "xk": xk, "error": error})
        
        """
        Os critérios definidos neste Trabalho Computacional são:

        1. O erro absoluto deve ser menor que eps. (|x_k+1 - x_k| < eps)
        2. O valor absoluto de f(x_k+1) deve ser menor que eps. (|f(x_k+1)| < eps)
        3. O número de iterações deve ser menor que max_iter. (k < max_iter)

        No entanto, nos slides, os critérios definidos foram:
        
        1. O valor de f(x) é exatamente 0 (f(x) == 0)
        2. O erro máximo possível não pode ser maior que metade do comprimento do intervalo em que a raiz se encontra ((b-a)/2)

        Entendemos que o critério de parada 1, definido no slide, é um caso que pode não funcionar bem no computador, já que dízimas e arredondamentos podem fazer com que f(x) nunca seja exatamente 0.

        Além disso, o critério de parada 2 definido no slide é igual ao critério de parada 1 definido no trabalho computacional. O módulo de |x_k+1 - x_k| é exatamente a metade do tamanho do intervalo (b-a)/2, pois o ponto x_k é calculado exatamente no meio do intervalo [a, b].

        Assim, seguimos com os critérios do Trabalho Computacional que estão definidos abaixo.
        """
        # Se o erro absoluto for menor que eps OU o valor absoluto de f(x_k+1) for menor que eps, então xk é uma raiz aproximada.
        if error < eps or abs(fxk) < eps: 
            return xk, historic

        # Se f(a) * f(x_k) < 0, então a raiz está no intervalo [a, x_k]. Atualiza-se o intervalo com b = x_k
        elif f(a) * fxk < 0:
            b = xk

        # Se f(a) * f(x_k) >= 0, então a raiz está no intervalo [x_k, b]. Atualiza-se o intervalo com a = x_k
        else:
            a = xk

        xk_previous = xk # Atualiza o chute inicial do x_k

    # Se max_iter for atingido, retorna a raiz aproximada e o histórico de iterações
    return xk, historic