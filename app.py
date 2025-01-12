from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return "Bem-vindo ao Simulador Online!"

@app.route('/simulador', methods=['GET', 'POST'])
def simulador():
    if request.method == 'POST':
        # Receber dados do formulário
        valor_inicial = float(request.form['valor_inicial'])
        aporte_mensal = float(request.form['aporte_mensal'])
        taxa_juros = float(request.form['taxa_juros'])
        periodo = int(request.form['periodo'])

        # Cálculos de investimento
        saldo = valor_inicial
        historico = [int(saldo)]  # Arredondado para inteiro

        for mes in range(1, periodo + 1):
            saldo += aporte_mensal
            saldo += saldo * (taxa_juros / 100) / 12
            historico.append(int(saldo))  # Arredondado para inteiro

        # Gerar o gráfico
        img = gerar_grafico(historico)

        # Retornar resultados
        return render_template('resultado.html', saldo_final=int(saldo), historico=historico, grafico=img)
    return render_template('simulador.html')

def gerar_grafico(historico):
    """Gera um gráfico da evolução do saldo e retorna como uma imagem base64."""
    plt.figure(figsize=(8, 5))
    plt.plot(range(len(historico)), historico, marker='o', color='blue', label="Saldo Acumulado")
    plt.title("Evolução do Saldo")
    plt.xlabel("Meses")
    plt.ylabel("Saldo (R$)")
    plt.grid()
    plt.legend()

    # Salvar o gráfico como imagem em memória
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    grafico_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()
    return grafico_base64

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


