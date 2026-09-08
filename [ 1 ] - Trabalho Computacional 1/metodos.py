def bisseccao(f, a, b, eps=1e-8, max_iter=200):
    # Validação de entrada: A bissecção deve levantar ValueError se f(a) · f(b) ≥ 0.
    if f(a) * f(b) >= 0:
        raise ValueError

    # Chute inicial do x_k.
    xk = a 

    # Histórico de iterações.
    historic = []

    # Itera até atingir o número máximo de iterações. De 1 até max_iter+1 para melhor visualização do número de iterações. 
    # IMPORTANTE: Entenda xk como x_k e xk_next como x_{k+1}.
    for k in range(1, max_iter+1):
        # Cálculo do x_{k+1}
        xk_next = (a+b)/2

        # Cálculo do erro absoluto
        error = abs(xk_next - xk)

        # Cálculo de f(x_{k+1}), para evitar chamar f() desnecessariamente.
        fxk_next = f(xk_next)

        # Adiciona a iteração atual ao histórico
        historic.append({"k": k, "x": xk_next, "fx": fxk_next, "erro": error})
        
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
        # Se o erro absoluto for menor que eps OU o valor absoluto de f(x_k+1) for menor que eps, então x_{k+1} é uma raiz aproximada.
        if error < eps or abs(fxk_next) < eps: 
            return xk_next, historic

        # Se f(a) * f(x_{k+1}) < 0, então a raiz está no intervalo [a, x_{k+1}]. Atualiza-se o intervalo com b = x_{k+1}.
        elif f(a) * fxk_next < 0:
            b = xk_next

        # Se f(a) * f(x_{k+1}) >= 0, então a raiz está no intervalo [x_{k+1}, b]. Atualiza-se o intervalo com a = x_{k+1}.
        else:
            a = xk_next

        # Atualiza o chute inicial do x_k.
        xk = xk_next 

    # Se max_iter for atingido, retorna a raiz aproximada e o histórico de iterações
    return xk, historic

def newton(f, df, x0, eps=1e-8, max_iter=200):
    # Chute inicial do x_k.
    xk = x0
    
    # Histórico de iterações.
    historic = []

    # Itera até atingir o número máximo de iterações. De 1 até max_iter+1 para melhor visualização do número de iterações.
    # IMPORTANTE: Entenda xk como x_k e xk_next como x_{k+1}.
    for k in range(1, max_iter+1):
        # Cálculo de f'(x_k), para evitar chamar f() desnecessariamente.
        dfxk = df(xk)

        # Validação de entrada: O método de Newton deve tratar f'(x_k) = 0.
        if dfxk == 0:
            raise ValueError
        
        # Cálculo do x_k+1
        xk_next = xk - f(xk)/dfxk

        # Cálculo do erro absoluto
        error = abs(xk_next - xk)

        # Cálculo de f(xk_next)
        fxk_next = f(xk_next)

        # Adiciona a iteração atual ao histórico
        historic.append({"k": k, "x": xk_next, "fx": fxk_next, "erro": error})

        # Se o erro absoluto for menor que eps OU o valor absoluto de f(x_k+1) for menor que eps, então xk é uma raiz aproximada.
        if error < eps or abs(fxk_next) < eps: 
            return xk_next, historic
        
        # Atualiza o chute inicial do x_k.
        xk = xk_next

    # Se max_iter for atingido, retorna a raiz aproximada e o histórico de iterações
    return xk, historic

def secante(f, x0, x1, eps=1e-8, max_iter=200):
    # Chutes iniciais para x_k e x_{k-1}.
    xk_previous = x0
    xk = x1
    
    # Histórico de iterações.
    historic = []

    # Itera até atingir o número máximo de iterações. De 1 até max_iter+1 para melhor visualização do número de iterações.
    # IMPORTANTE: Entenda xk como x_k e xk_previous como x_{k-1} e xk_next como x_{k+1}.
    for k in range(1, max_iter+1):
        # Cálculo do denominador para evitar chamar f() desnecessariamente.
        denominator = f(xk) - f(xk_previous)

        # Validação de entrada: A secante deve tratar denominador nulo.
        if denominator == 0:
            raise ValueError
        
        # Cálculo do x_k+1
        xk_next = xk - (f(xk) * (xk - xk_previous)) / denominator

        # Cálculo do erro absoluto
        error = abs(xk_next - xk)

        # Cálculo de f(xk_next)
        fxk_next = f(xk_next)

        # Adiciona a iteração atual ao histórico
        historic.append({"k": k, "x": xk_next, "fx": fxk_next, "erro": error})

        # Se o erro absoluto for menor que eps OU o valor absoluto de f(x_k+1) for menor que eps, então xk é uma raiz aproximada.
        if error < eps or abs(fxk_next) < eps: 
            return xk_next, historic
        
        # Atualiza os chutes iniciais para x_k e x_{k-1}.
        xk_previous = xk
        xk = xk_next

    # Se max_iter for atingido, retorna a raiz aproximada e o histórico de iterações
    return xk, historic


# =====================================================================================================
# Funções Auxiliares

# Função auxiliar de sinal: verifica se houve mudança de sinal entre dois pontos consecutivos.
def sinal(atual, anterior):
    # Se o produto for menor ou igual a zero, há travessia de eixo ou raiz exata.
    if(atual*anterior<=0):
        return True # Retorna verdadeiro indicando que achou uma raiz (ou raiz exata) no subintervalo
        
    else:
        return False # Retorna falso indicando que não há travessia garantida ali


# Função de varredura: divide o intervalo [a, b] em 'n' pontos para encontrar subintervalos com raízes.
def tabelar_sinais(f_alvo, a, b, n):
    tamanhoPasso = abs(b - a) / (n - 1) # Calcula a distância uniforme entre os pontos da malha
    
    # Avalia a função no limite inferior do intervalo global
    anterior = f_alvo(a)

    # Guarda a coordenada x do limite inferior
    cordXanterior = a 

    # Calcula a coordenada x do próximo ponto da malha
    cordXatual = tamanhoPasso + a
    
     # Inicializa a lista vazia que vai armazenar as tuplas (a, b) dos subintervalos com raiz
    lista = []
    
    # Percorre todos os subintervalos (total de n-1 passos)
    for i in range(n - 1): 
         # Avalia a função no extremo direito do subintervalo atual
        atual = f_alvo(cordXatual)
        
        # Usa a função auxiliar para checar mudança de sinal (f(a)*f(b) <= 0)
        if sinal(atual, anterior): 
            # Se mudou o sinal, salva esse subintervalo na lista de retorno
            lista.append((cordXanterior, cordXatual)) 

        # Atualiza o 'f(a)' do próximo passo para ser o 'f(b)' do passo atual (evita recálculos)    
        anterior = atual
        
        # Avança a coordenada direita da malha
        cordXatual += tamanhoPasso 

        # Avança a coordenada esquerda da malha
        cordXanterior += tamanhoPasso 

    # Retorna a lista completa com todos os subintervalos que contêm raízes    
    return lista


# Método de Newton modificado para raízes múltiplas
def newton_modificado(f, df, x0, m, eps=1e-8, max_iter=200):
    # Define o chute inicial
    xk = x0 
    
    # Inicializa o histórico vazio para rastrear a convergência
    historic = [] 
    
    # Roda o limite de iterações para evitar laços infinitos
    for k in range(1, max_iter+1): 
        # Avalia a derivada no ponto atual
        dfxk = df(xk) 
        
        # Proteção contra divisão por zero (reta tangente horizontal)
        if dfxk == 0: 
            raise ValueError
            
        # Fórmula do Newton Modificado: multiplicando o passo tradicional pela multiplicidade 'm' da raiz
        xk_next = xk - m * f(xk)/dfxk 
        
        # Calcula o erro de passo (distância absoluta entre xk e x_k+1)
        error = abs(xk_next - xk) 
        
        # Cálculo de f(xk_next)
        fxk_next = f(xk_next)
        
        # Salva os dados desta iteração
        historic.append({"k": k, "x": xk_next, "fx": fxk_next, "erro": error}) 
        
        # Critério de parada: se erro de passo ou resíduo for menor que a tolerância, o método convergiu
        if error < eps or abs(fxk_next) < eps: 
            # Retorna a raiz encontrada e toda a jornada do histórico
            return xk_next, historic 
            
        # Prepara xk para a próxima iteração, caso não tenha convergido
        xk = xk_next 
        
    # Retorna a última tentativa mesmo se estourar o limite de iterações
    return xk, historic

# Modificação da função de bissecção para remover o critério do resíduo (|f(x)| < eps)
# Garantindo que ela só vai parar quando o tamanho do passo (|x_k+1 - x_k| < eps) for atingido
def bisseccao_apenas_passo(f, a, b, eps=1e-8, max_iter=200):
    if f(a) * f(b) >= 0:
        raise ValueError
        
    xk = a 
    historic = []
    
    for k in range(1, max_iter+1):
        # Ponto médio do intervalo
        xk_next = (a+b)/2 
        
        # Tamanho do passo (metade do intervalo atual)
        error = abs(xk_next - xk) 
        
        fxk_next = f(xk_next)
        historic.append({"k": k, "x": xk_next, "fx": fxk_next, "erro": error})
        
        # Critério de parada ÚNICO: apenas erro no eixo x (tamanho do intervalo)
        if error < eps: 
            return xk_next, historic
            
        # Atualização normal dos limites [a, b] da bissecção
        elif f(a) * fxk_next < 0:
            b = xk_next
        else:
            a = xk_next
            
        xk = xk_next 
        
    return xk, historic

# Decorator para contar o número de chamadas de uma função
def contador(f):
    def wrapper(x):
        wrapper.n += 1
        return f(x)
    wrapper.n = 0
    return wrapper
